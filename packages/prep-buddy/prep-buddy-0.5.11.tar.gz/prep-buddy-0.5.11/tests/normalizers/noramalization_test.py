from utils.python_test_case import PySparkTestCase
from pyprepbuddy.normalizers.normalizers import MinMaxNormalizer, ZScoreNormalizer, DecimalScalingNormalizer
from pyprepbuddy.rdds.transformable_rdd import TransformableRDD


class NormalizationTest(PySparkTestCase):
    def test_should_normalize_by_Min_Max_normalization(self):
        initial_dataset = self.sc.parallelize([
            "07434677419,07371326239,Incoming,211,Wed Sep 15 19:17:44 +0100 2010",
            "07641036117,01666472054,Outgoing,0,Mon Feb 11 07:18:23 +0000 1980",
            "07641036117,07371326239,Incoming,45,Mon Feb 11 07:45:42 +0000 1980",
            "07641036117,07371326239,Incoming,45,Mon Feb 11 07:45:42 +0000 1980",
            "07641036117,07681546436,Missed,12,Mon Feb 11 08:04:42 +0000 1980"])
        transformable_rdd = TransformableRDD(initial_dataset, 'csv')
        final_rdd = transformable_rdd.normalize(3, MinMaxNormalizer(0, 1))
        normalized_durations = final_rdd.select(3).collect()
        expected1 = "1.0"
        expected2 = "0.0"
        expected3 = "0.2132701421800948"
        expected4 = "0.2132701421800948"
        expected5 = "0.05687203791469194"

        self.assertTrue(normalized_durations.__contains__(expected1))
        self.assertTrue(normalized_durations.__contains__(expected2))
        self.assertTrue(normalized_durations.__contains__(expected3))
        self.assertTrue(normalized_durations.__contains__(expected4))
        self.assertTrue(normalized_durations.__contains__(expected5))

    def test_should_normalize_by_Z_Score_normalization(self):
        initial_dataset = self.sc.parallelize([
            "07434677419,07371326239,Incoming,211,Wed Sep 15 19:17:44 +0100 2010",
            "07641036117,01666472054,Outgoing,0,Mon Feb 11 07:18:23 +0000 1980",
            "07641036117,07371326239,Incoming,45,Mon Feb 11 07:45:42 +0000 1980",
            "07641036117,07371326239,Incoming,45,Mon Feb 11 07:45:42 +0000 1980",
            "07641036117,07681546436,Missed,12,Mon Feb 11 08:04:42 +0000 1980"])
        transformable_rdd = TransformableRDD(initial_dataset, 'csv')
        final_rdd = transformable_rdd.normalize(3, ZScoreNormalizer())
        normalized_durations = final_rdd.select(3).collect()
        expected1 = "1.944528306701421"
        expected2 = "-0.8202659838241843"
        expected3 = "-0.2306179123850742"
        expected4 = "-0.2306179123850742"
        expected5 = "-0.6630264981070882"

        self.assertTrue(normalized_durations.__contains__(expected1))
        self.assertTrue(normalized_durations.__contains__(expected2))
        self.assertTrue(normalized_durations.__contains__(expected3))
        self.assertTrue(normalized_durations.__contains__(expected4))
        self.assertTrue(normalized_durations.__contains__(expected5))

    def test_should_normalize_by_Decimal_Scale(self):
        initial_dataset = self.sc.parallelize([
            "07434677419,07371326239,Incoming,211,Wed Sep 15 19:17:44 +0100 2010",
            "07641036117,01666472054,Outgoing,0,Mon Feb 11 07:18:23 +0000 1980",
            "07641036117,07371326239,Incoming,45,Mon Feb 11 07:45:42 +0000 1980",
            "07641036117,07371326239,Incoming,45,Mon Feb 11 07:45:42 +0000 1980",
            "07641036117,07681546436,Missed,12,Mon Feb 11 08:04:42 +0000 1980"])
        transformable_rdd = TransformableRDD(initial_dataset, 'csv')
        final_rdd = transformable_rdd.normalize(3, DecimalScalingNormalizer())
        normalized_durations = final_rdd.select(3).collect()
        expected1 = "2.11"
        expected2 = "0.0"
        expected3 = "0.45"
        expected4 = "0.45"
        expected5 = "0.12"

        self.assertTrue(normalized_durations.__contains__(expected1))
        self.assertTrue(normalized_durations.__contains__(expected2))
        self.assertTrue(normalized_durations.__contains__(expected3))
        self.assertTrue(normalized_durations.__contains__(expected4))
        self.assertTrue(normalized_durations.__contains__(expected5))
