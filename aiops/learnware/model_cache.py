import pickle

module_cache = {}


def save_file_model(clf, model_name):
    model_file_path = './' + model_name + '.pickle'
    with open(model_file_path, 'wb') as f:
        pickle.dump(clf, f)
    module_cache[model_file_path] = clf
    return model_file_path


def load_file_model(model_file_path):
    if model_file_path in module_cache:
        return module_cache[model_file_path]
    # TODO: 如果文件没有发现，是否需要重新训练，还是报错。
    with open(model_file_path, 'rb') as f:
        clf = pickle.load(f)
        module_cache[model_file_path] = clf
        return clf
