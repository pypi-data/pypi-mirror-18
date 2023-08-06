from py4j.java_gateway import java_import

from pyprepbuddy.class_names import ClassNames


class SimpleMovingAverage(object):
    """
    A smoothing method which smooths data based on Simple Moving Average which is the unweighted mean of
    the previous n data. This method ensure that variations in the mean are aligned
    with the variations in the data rather than being shifted in time.
    """
    def __init__(self, window_size):
        self.__window_size = window_size

    def _get_smoothing_method(self, spark_context):
        java_import(spark_context._jvm, ClassNames.SIMPLE_MOVING_AVERAGE)
        return spark_context._jvm.SimpleMovingAverageMethod(self.__window_size)


class WeightedMovingAverage(object):
    """
    A smoothing method which smooths data based on Weighted Moving Average method that is any
    average that has multiplying factors to give different weights to data at
    different positions in the sampleColumnValues window.
    """
    def __init__(self, window_size, weights):
        self.__window_size = window_size
        self.__python_weights = weights

    def _get_smoothing_method(self, spark_context):
        java_import(spark_context._jvm, ClassNames.WEIGHTS)
        java_import(spark_context._jvm, ClassNames.WEIGHTED_MOVING_AVERAGE)
        java_weights = spark_context._jvm.Weights(self.__python_weights.limit())
        for index in range(self.__window_size):
            java_weights.add(self.__python_weights.get(index))

        return spark_context._jvm.WeightedMovingAverageMethod(self.__window_size, java_weights)


class Weights(object):
    """
    Contains weights in sequence for the weighted sliding window.
    """
    def __init__(self, limit):
        self.__weights = []
        self.__limit = limit

    def add(self, weight):
        self.__weights.append(weight)

    def get(self, index):
        return self.__weights[index]

    def limit(self):
        return self.__limit
