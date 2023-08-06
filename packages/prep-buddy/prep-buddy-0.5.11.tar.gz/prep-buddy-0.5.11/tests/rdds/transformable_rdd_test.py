from utils.python_test_case import PySparkTestCase
from pyprepbuddy.cleansers.imputation import *
from pyprepbuddy.rdds.transformable_rdd import TransformableRDD


class UnitTestsForTransformableRDD(PySparkTestCase):
    def test_transformableRDD_gives_a_count_of_element(self):
        rdd = self.sc.parallelize(["2", "3", "4", "5", "6", "7", "7", "7"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        self.assertEquals(8, transformable_rdd.count())

    def test_transformableRDD_can_collect_all_the_elements(self):
        rdd = self.sc.parallelize(["2", "3", "4", "5", "6", "7", "7", "7"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        self.assertEquals(["2", "3", "4", "5", "6", "7", "7", "7"], transformable_rdd.collect())

    def test_transformableRDD_can_deduplicate_the_given_list(self):
        rdd = self.sc.parallelize(["2", "3", "4", "5", "6", "7", "7", "7"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        deduplicate_rdd = transformable_rdd.deduplicate()
        self.assertEquals(6, deduplicate_rdd.count())

    def test_transformableRDD_can_deduplicate_by_given_column_index(self):
        rdd = self.sc.parallelize(["2", "3", "4", "5", "6", "7", "7", "7"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        deduplicate_rdd = transformable_rdd.deduplicate([0])
        self.assertEquals(6, deduplicate_rdd.count())

    def test_transformableRDD_can_impute_the_missing_values_by_ModeSubstitution(self):
        rdd = self.sc.parallelize(["Ram,23", "Joe,45", "Jill,45", "Soa,"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        imputed_rdd = transformable_rdd.impute(1, ModeSubstitution())
        self.assertTrue(imputed_rdd.collect().__contains__("Soa,45"))

    def test_transformableRDD_can_impute_the_missing_values_by_MeanSubstitution(self):
        rdd = self.sc.parallelize(["Ram,9", "Joe,45", "Jill,45", "Soa,"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        imputed_rdd = transformable_rdd.impute(1, MeanSubstitution())
        self.assertTrue(imputed_rdd.collect().__contains__("Soa,33.0"))

    def test_transformableRDD_can_impute_the_missing_values_by_ApproxMeanSubstitution(self):
        rdd = self.sc.parallelize(["Ram,9", "Joe,45", "Jill,45", "Soa,"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        imputed_rdd = transformable_rdd.impute(1, ApproxMeanSubstitution())
        self.assertTrue(imputed_rdd.collect().__contains__("Soa,33.0"))

    def test_transformableRDD_can_impute_the_missing_values_by_UnivariateLinearRegressionSubstitution(self):
        rdd = self.sc.parallelize(["60,3.1", "61,3.6", "62,3.8", "63,4", "65,4.1", "64,"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        imputed_rdd = transformable_rdd.impute(1, UnivariateLinearRegressionSubstitution(0))
        self.assertTrue(imputed_rdd.collect().__contains__("64,4.06"))

    def test_transformableRDD_can_impute_the_missing_values_by_NaiveBayesSubstitution(self):
        rdd = self.sc.parallelize(["Drew,No,Blue,Short,Male",
                                   "Claudia,Yes,Brown,Long,Female",
                                   "Drew,No,Blue,Long,Female",
                                   "Drew,No,Blue,Long,Female",
                                   "Alberto,Yes,Brown,Short,Male",
                                   "Karin,No,Blue,Long,Female",
                                   "Nina,Yes,Brown,Short,Female",
                                   "Sergio,Yes,Blue,Long,Male",
                                   "Drew,Yes,Blue,Long,"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        imputed_rdd = transformable_rdd.impute(4, NaiveBayesSubstitution(0, 1, 2, 3))
        self.assertTrue(imputed_rdd.collect().__contains__("Drew,Yes,Blue,Long,Female"))

    def test_get_duplicates_should_give_duplicates_of_rdd(self):
        rdd = self.sc.parallelize(["Ram,23", "Ram,23", "Jill,45", "Soa,"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        duplicates = transformable_rdd.get_duplicates()
        self.assertEqual("Ram,23", duplicates.first())

    def test_get_duplicates_should_give_duplicates_of_given_column_indexes(self):
        rdd = self.sc.parallelize(["Ram,23", "Ram,23", "Jill,45", "Soa,"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        duplicates = transformable_rdd.get_duplicates([0])
        self.assertEqual("Ram,23", duplicates.first())

    def test_drop_column_should_drop_the_given_column(self):
        rdd = self.sc.parallelize(["Ram,23,Male", "Ram,23,Male", "Jill,45,Female", "Soa,,Female,"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        dropped = transformable_rdd.drop_column(1)
        self.assertEqual("Ram,Male", dropped.first())

    def test_multiply_column_should_multiply_two_given_column(self):
        initial_dataset = self.sc.parallelize(["1,1", "1,2", "1,3"])
        transformable_rdd = TransformableRDD(initial_dataset)
        multiplied_rdd = transformable_rdd.multiply_columns(0, 1)
        collected = multiplied_rdd.collect()
        self.assertTrue(collected.__contains__(1.0))
        self.assertTrue(collected.__contains__(2.0))
        self.assertTrue(collected.__contains__(3.0))

    def test_to_double_rdd_should_change_string_to_double_rdd(self):
        initial_dataset = self.sc.parallelize(["1,1", "5,2", "8,3"])
        transformable_rdd = TransformableRDD(initial_dataset)
        rdd = transformable_rdd.to_double_rdd(0)
        collected = rdd.collect()
        self.assertTrue(collected.__contains__(1.0))
        self.assertTrue(collected.__contains__(5.0))
        self.assertTrue(collected.__contains__(8.0))

    def test_add_columns_from_should_merge_all_columns_of_other_transformable_rdd(self):
        initial_spelled_numbers = self.sc.parallelize([
            "One,Two,Three",
            "Four,Five,Six",
            "Seven,Eight,Nine",
            "Ten,Eleven,Twelve"
        ])
        spelled_numbers = TransformableRDD(initial_spelled_numbers, "csv")
        initial_numeric_data = self.sc.parallelize([
            "1\t2\t3",
            "4\t5\t6",
            "7\t8\t9",
            "10\t11\t12"
        ])
        numeric_data = TransformableRDD(initial_numeric_data, "tsv")

        result = spelled_numbers.add_columns_from(numeric_data).collect()

        self.assertTrue(result.__contains__("One,Two,Three,1,2,3"))
        self.assertTrue(result.__contains__("Four,Five,Six,4,5,6"))
        self.assertTrue(result.__contains__("Seven,Eight,Nine,7,8,9"))
        self.assertTrue(result.__contains__("Ten,Eleven,Twelve,10,11,12"))

    def test_pivot_table_by_count_should_give_pivoted_table(self):
        initial_dataSet = self.sc.parallelize([
            "known,new,long,home,skips",
            "unknown,new,short,work,reads",
            "unknown,follow Up,long,work,skips",
            "known,follow Up,long,home,skips",
            "known,new,short,home,reads",
            "known,follow Up,long,work,skips",
            "unknown,follow Up,short,work,skips",
            "unknown,new,short,work,reads",
            "known,follow Up,long,home,skips",
            "known,new,long,work,skips",
            "unknown,follow Up,short,home,skips",
            "known,new,long,work,skips",
            "known,follow Up,short,home,reads",
            "known,new,short,work,reads",
            "known,new,short,home,reads",
            "known,follow Up,short,work,reads",
            "known,new,short,home,reads",
            "unknown,new,short,work,reads"
        ])
        initial_rdd = TransformableRDD(initial_dataSet, "csv")
        table = initial_rdd.pivot_by_count(4, [0, 1, 2, 3])
        entry = table.value_at("skips", "known")
        self.assertEqual(6, entry)
        self.assertEqual(3, table.value_at("skips", "unknown"))

    def test_map_should_give_Transformable_rdd(self):
        initial_dataset = self.sc.parallelize(["1,2", "1,2", "1,3"])
        transformable_rdd = TransformableRDD(initial_dataset, "csv")
        rdd_map = transformable_rdd.map(lambda line: line + "yes")
        deduplicate = rdd_map.deduplicate()
        collected = deduplicate.collect()
        self.assertEqual(2, collected.__len__())
        expected = "1,2yes"
        self.assertTrue(collected.__contains__(expected))

    def test_filter_should_give_Transformable_rdd(self):
        initial_dataset = self.sc.parallelize(["1,2", "1,2", "1,3"])
        transformable_rdd = TransformableRDD(initial_dataset, "csv")
        rdd_filter = transformable_rdd.filter(lambda line: line.split(",")[1] != "2")
        collected = rdd_filter.collect()
        self.assertEqual(1, collected.__len__())

