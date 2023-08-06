from py4j.java_gateway import java_import

from pyprepbuddy.class_names import ClassNames


class SimpleFingerprint(object):
    """
    This algorithm generates a key using Simple Fingerprint Algorithm for
    every cardinal value (facet) in column and add them to the Cluster.
    """

    def _get_algorithm(self, spark_context):
        java_import(spark_context._jvm, ClassNames.SIMPLE_FINGERPRINT)
        return spark_context._jvm.SimpleFingerprintAlgorithm()


class NGramFingerprintAlgorithm(object):
    """
    This algorithm generates a key using N Gram Fingerprint Algorithm for
    every cardinal value (facet) in column and add them to the Cluster.
    """
    def __init__(self, n_gram):
        self.__n_gram = n_gram

    def _get_algorithm(self, spark_context):
        java_import(spark_context._jvm, ClassNames.N_GRAM_FINGERPRINT)
        return spark_context._jvm.NGramFingerprintAlgorithm(self.__n_gram)
