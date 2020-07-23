import abc

class LearnwareBase(metaclass=abc.ABCMeta):

    # @abc.abstractmethod
    # def load_raw_data(self):
    #     pass
    #
    # @abc.abstractmethod
    # def data_clean(self):
    #     pass
    #
    # @abc.abstractmethod
    # def feature_project(self):
    #     pass
    #
    # @abc.abstractmethod
    # def train_model(self):
    #     pass
    #
    # @abc.abstractmethod
    # def optimization_learnware(self):
    #     pass
    #
    # @abc.abstractmethod
    # def evaluation(self):
    #     pass

    @abc.abstractmethod
    def call(self, indices, data):
        pass