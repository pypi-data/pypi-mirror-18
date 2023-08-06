from py4j.java_gateway import java_import

from pyprepbuddy import py2java_int_array
from pyprepbuddy.class_names import ClassNames


class ModeSubstitution(object):
    """
    ModeSubstitution is a simplest imputation strategy used for filling missing values
    in a data set.It imputes the missing values by most occurring values in data set.
    """

    def _get_strategy(self, sc):
        java_import(sc._jvm, ClassNames.MODE_SUBSTITUTION)
        return sc._jvm.ModeSubstitution()


class MeanSubstitution(object):
    """
    An imputation strategy that imputes the missing values by mean of the values in a data set.
    It imputes the missing values by mean of the values in data set.
    This implementation is only for imputing numeric columns.
    """

    def _get_strategy(self, sc):
        java_import(sc._jvm, ClassNames.MEAN_SUBSTITUTION)
        return sc._jvm.MeanSubstitution()


class ApproxMeanSubstitution(object):
    """
    An imputation strategy that imputes the missing values by an approx mean of the values in data set.
    This implementation is only for imputing numeric columns.
    Recommended when imputing on large data set.
    """

    def _get_strategy(self, sc):
        java_import(sc._jvm, ClassNames.APPROX_MEAN_SUBSTITUTION)
        return sc._jvm.ApproxMeanSubstitution()


class UnivariateLinearRegressionSubstitution(object):
    """
    An imputation strategy that is based on Linear Regression which is an approach
    for modeling the relationship between a scalar dependent variable y and an explanatory
    variable x.
    This strategy imputes the value of y by : slope * x + intercept
    This implementation is only for imputing numeric columns.
    """
    def __init__(self, column_index):
        self._column_index = column_index

    def _get_strategy(self, sc):
        java_import(sc._jvm, ClassNames.UNIVARIATE_SUBSTITUTION)
        return sc._jvm.UnivariateLinearRegressionSubstitution(self._column_index)


class NaiveBayesSubstitution(object):
    """
    An imputation strategy that is based on Naive Bayes Algorithm which is the probabilistic classifier.
    This implementation is only for imputing the categorical values.
    """
    def __init__(self, *column_index):
        self._column_index = column_index

    def _get_strategy(self, sc):
        java_import(sc._jvm, ClassNames.NAIVE_BAYES_SUBSTITUTION)
        independent_column_indexes = py2java_int_array(sc, self._column_index)
        return sc._jvm.NaiveBayesSubstitution(independent_column_indexes)
