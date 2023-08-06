from py4j.java_gateway import java_import

from pyprepbuddy.class_names import ClassNames


class MinMaxNormalizer(object):
    """
    A normalizer which scales the data within the specified range.
    Default range is (0,1)
    A' = (A - min(A)) / (max(A) - min(A)) * (D-C) + C
    where (C,D) is the range and A is the value.
    """
    def __init__(self, min_range=0, max_range=1):
        self.min_range = min_range
        self.max_range = max_range

    def _get_normalizer(self, spark_context):
        java_import(spark_context._jvm, ClassNames.MIN_MAX_NORMALIZER)
        return spark_context._jvm.MinMaxNormalizer(self.min_range, self.max_range)


class ZScoreNormalizer(object):
    """
    A normalizer technique which normalizes data by their standard score.
    Formula for Z Score Normalization : (X - Mean) / Standard Deviation.
    """

    def _get_normalizer(self, spark_context):
        java_import(spark_context._jvm, ClassNames.Z_SCORE_NORMALIZER)
        return spark_context._jvm.ZScoreNormalizer()


class DecimalScalingNormalizer(object):
    """
    A normalizer strategy which normalizes the data by multiplying it to pow(10,i-1)
    where i is the length of the number.
    """

    def _get_normalizer(self, spark_context):
        java_import(spark_context._jvm, ClassNames.DECIMAL_SCALING_NORMALIZER)
        return spark_context._jvm.DecimalScalingNormalizer()
