import pymysql
import pandas as pd

import math
from aiops.database.database import SessionLocal
from sqlalchemy.orm import Session
from aiops.database import repository
from aiops.database.models import LearnwareModel, Learnware
from sklearn.ensemble import IsolationForest
from aiops.learnware.model_cache import load_file_model, save_file_model


class MachineLearnware():

    def call(self, index_name, resource_name, data):

        try:
            db = SessionLocal()
            # 通过指标名称来确定具体的学件，TODO：需要增加对学件的选择判断
            learnware = self._get_learnware(db, "MachineLearnware")
            # 通过指标和资源名称查找对应的模型，一个学件可能对应很多模型
            # 获取模型，其中如果发现模型不存在，需要通过train_model的方法进行自动训练
            learnware_model_defining = self._get_learnware_model(db, learnware, index_name, resource_name)
            clf = self._load_learnware_model(db, learnware, learnware_model_defining)
            result = clf.predict(data)
            return result
        finally:
            db.close()

    def train_model(self, db: Session, learnware, index_name, resource_name):

        df = self._load_raw_data(db, learnware, index_name, resource_name)
        df = self._clean_data(df)
        featured_df = self._feature_project(df, index_name, resource_name)
        clf = self._train_model(featured_df)

        # 验证是否有复用模型
        reuse_model = self._try_reuse_model(db, df, clf, learnware, index_name, resource_name)

        estimate_result = self._estimate_model(featured_df, clf)
        print("Train the model", learnware.name, index_name, resource_name)
        return {'clf': clf, 'model': reuse_model}

    def _get_learnware(self, db: Session, learnware_name):
        learnware = repository.get_learnware_by_name(db, learnware_name)
        if learnware is None:
            raise Exception("Learnware Not Found")
        print("Find the learware", learnware.name)
        return learnware

    def _get_learnware_model(self, db: Session, learnware, index_name, resource_name):
        model_name = index_name + "_" + resource_name
        #TODO: 目前支持相当于一个资源的一个指标一个模型，需要提供多种策略支持
        models = repository.get_learnware_model(db, learnware.id, model_name)
        if models is None or len(models) == 0:
            # 训练一个新的模型
            res = self.train_model(db, learnware, index_name, resource_name)
            clf = res["clf"]
            reuse_model = res["model"]

            # 讲模型存入所在学件的模型组里
            model = self._save_model(clf, db, learnware, index_name, resource_name, None, reuse_model)
        elif len(models) > 1:
            # TODO: select the best model
            raise Exception("Too many Learnware's models")
        else:
            # TODO：需要判断更新策略，模型是会过期的，过期了需要重新更新
            model = models[0]
            # 如下为强制更新模型策略
            res = self.train_model(db, learnware, index_name, resource_name)
            clf = res["clf"]
            reuse_model = res["model"]

            self._save_model(clf, db, learnware, index_name, resource_name, model, reuse_model)
        #print("Find the learware's model", model.name)

        return model

    def _load_raw_data(self, db: Session, learnware: Learnware, index_name, resource_name):
        datasource = repository.get_datasource_by_id(db, learnware.datasource_id)
        print("datasource:", datasource.name)
        # TODO: 目前写主要只支持mysql的训练数据源，需要增加clickhouse的数据源支持
        if datasource.driver == 'mysql':
            connection = pymysql.connect(host=datasource.host, user=datasource.username,
                                         password=datasource.password, database=datasource.database)
        else:
            raise Exception("database driver not support " + datasource.driver)

        # TODO: 需要增加返回数据数量的限制train_data_max_size
        # TODO: 时间区间的限制
        sql = learnware.train_data_fetch_sql
        sql = sql.replace("${index_name}", index_name)
        sql = sql.replace("${resource_name}", resource_name)
        print("use sql fetch data:", sql)
        df = pd.read_sql(sql, connection)
        print("Load the data:", df.info())
        return df

    def _load_learnware_model(self, db: Session, learnware, learnware_model_defining: LearnwareModel):
        clf = load_file_model(learnware_model_defining.file_path)

        print("Load the model file:", learnware_model_defining.file_path)
        return clf

    def _clean_data(self, df):
        return df.dropna()

    def _feature_project(self, df, index_name, resource_name):
        df = df.sort_values('event_time')
        df = df.set_index('event_time')

        featured_df = pd.DataFrame(df[index_name].resample("T").mean().ffill())
        featured_df['value'] = featured_df[index_name]
        featured_df['diff'] = featured_df[index_name].diff().fillna(0)
        print("Feature Project", featured_df)
        return featured_df

    def _train_model(self, df):
        X_train = df[['value', 'diff']].values
        # TODO: 超参优化需要完成
        # 污染率需要通过3sigema的方式形成预估值，这里的预估就是要根据业务重新设定，如cpu使用率，值比较低，波动也不大，从3sigema就容易出现问题
        # 为了降低污染率，用更严格的6sigema
        values_mean = df['value'].mean()
        values_std = df['value'].std()
        pollution_rate = df[(df['value'] >= (values_mean + 6 * values_std)) | (df['value'] <= (values_mean - 6 * values_std))]['value'].count() / df['value'].count()
        print("Estimate Pollution_rate", pollution_rate)

        if pollution_rate < 0.001:
            clf = IsolationForest(max_samples=100 * 2, contamination=0.001)
        elif pollution_rate < 0.01:
            clf = IsolationForest(max_samples=100 * 2, contamination=0.005)
        else:
            clf = IsolationForest(max_samples=100 * 2, contamination=0.01)

        clf.fit(X_train)
        print("Train the isloation Forest", clf)
        return clf

    def _model_predict(self, values, clf):
        df = pd.DataFrame({'value': values})
        df['diff'] = df['value'].diff().fillna(0)
        X_test = df[['value', 'diff']].values
        X_test_predict = clf.predict(X_test)
        print("Predict Result:", X_test_predict)
        return X_test_predict

    def _estimate_model(self, df, clf):
        values = df['value'].values
        predict = self._model_predict(values, clf)
        anomaly_rate = len(predict[predict == -1]) / len(predict)
        print("Anoamly_rate: ", anomaly_rate)
        return {'anomaly_rate': anomaly_rate}

    def _save_model(self, clf, db: Session, learnware, index_name, resource_name, model: LearnwareModel = None, reuse_model_path = None):
        model_name = index_name + "_" + resource_name

        if model is None and reuse_model_path is None:
            model_file_path = save_file_model(clf, model_name)
            model = LearnwareModel(name=model_name, learnware_id=learnware.id, resource_name=resource_name, index_name=index_name,
                                   file_path=model_file_path)
            repository.insert_learnware_model(db, model)
        elif model is None and reuse_model_path is not None:
            model = LearnwareModel(name=model_name, learnware_id=learnware.id, resource_name=resource_name,
                                  index_name=index_name,
                                  file_path=reuse_model_path.file_path)
            repository.insert_learnware_model(db, model)
        elif model is not None and reuse_model_path is None:
            model.file_path = save_file_model(clf, model_name)
            repository.update_learnware_model(db, model)
        else:
            model.file_path = reuse_model_path.file_path
            repository.update_learnware_model(db, model)
        return model

    def _try_reuse_model(self, db: Session, df, clf, learnware, index_name, resource_name):
        models = repository.find_learnware_model_by_index_name(db, learnware.id, index_name)

        X_train_predict = self._model_predict(df[index_name].values, clf)
        for model in models:
            if model.name == index_name + "_" +resource_name:
                continue
            clf = self._load_learnware_model(db, learnware, model)
            if clf is None:
                # TODO: 如果需要抛出异常，并处理该异常
                pass
            X_predict = self._model_predict(df[index_name].values, clf)
            # 通过欧氏距离来计算两次预测的结果的相似程度，这里定的是5
            # TODO: 相似度存入learnware的参数
            print("*"*10, math.sqrt(((X_predict - X_train_predict) ** 2).sum()))
            if math.sqrt(((X_predict - X_train_predict) ** 2).sum()) < 5:
                return model
        return None


    def preprocess_data(self, values):
        df = pd.DataFrame(values)
        df.columns = ["event_time", "value"]
        df['event_time'] = pd.to_datetime(df['event_time'])
        df = df.sort_values('event_time')
        df = df.set_index('event_time')
        # 重采样保障数据对齐
        df = pd.DataFrame(df['value'].resample("T").mean().bfill())
        # 计算差分
        df['diff'] = df['value'].diff().fillna(0)
        # 返回所有的值
        return df.values

