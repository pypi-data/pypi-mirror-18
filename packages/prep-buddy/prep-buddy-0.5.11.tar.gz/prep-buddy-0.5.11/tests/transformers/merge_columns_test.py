from utils.python_test_case import PySparkTestCase
from pyprepbuddy.rdds.transformable_rdd import TransformableRDD


class MergeColumnsTest(PySparkTestCase):
    def test_should_merge_given_column_indexes(self):
        initial_data_set = self.sc.parallelize(["FirstName,LastName,732,MiddleName"])
        initial_rdd = TransformableRDD(initial_data_set, "csv")

        joined_column_rdd = initial_rdd.merge_columns([3, 1, 0], "_", False)
        self.assertEquals("732,MiddleName_LastName_FirstName", joined_column_rdd.first())

        with_originals = initial_rdd.merge_columns([3, 1, 0], "_", True)
        self.assertEquals("FirstName,LastName,732,MiddleName,MiddleName_LastName_FirstName", with_originals.first())

        joined_column_with_defaults = initial_rdd.merge_columns([3, 1, 0])
        self.assertEquals("732,MiddleName LastName FirstName", joined_column_with_defaults.first())
