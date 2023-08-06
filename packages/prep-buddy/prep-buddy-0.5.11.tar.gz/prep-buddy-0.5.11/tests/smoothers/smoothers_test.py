from utils.python_test_case import PySparkTestCase
from pyprepbuddy.rdds.transformable_rdd import TransformableRDD
from pyprepbuddy.smoothers.smoothing_algorithms import SimpleMovingAverage, Weights, WeightedMovingAverage


class SmoothersTest(PySparkTestCase):
    def test_should_smooth_data_by_Simple_Moving_Average(self):
        initial_dataset = self.sc.parallelize(
                ["52,3,53", "23,4,64", "23,5,64", "23,6,64", "23,7,64", "23,8,64", "23,9,64"], 3)
        transformable_rdd = TransformableRDD(initial_dataset, "csv")
        transformed = transformable_rdd.smooth(1, SimpleMovingAverage(3))
        excepted = 4.0
        self.assertEquals(excepted, transformed.first())

    def test_should_smooth_data_by_Weighted_Moving_Average(self):
        initial_dataset = self.sc.parallelize(["10", "12", "16", "13", "17", "19", "15", "20", "22", "19", "21", "19"],
                                              3)
        transformable_rdd = TransformableRDD(initial_dataset, "csv")

        weights = Weights(3)
        weights.add(0.166)
        weights.add(0.333)
        weights.add(0.5)

        moving_average = WeightedMovingAverage(3, weights)
        rdd = transformable_rdd.smooth(0, moving_average)

        expected = 13.656
        actual = rdd.first()
        self.assertEquals(expected, actual)
