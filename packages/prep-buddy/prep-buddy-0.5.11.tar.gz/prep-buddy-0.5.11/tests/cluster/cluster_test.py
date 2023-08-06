from utils.python_test_case import PySparkTestCase
from pyprepbuddy.cluster.clustering_algorithm import SimpleFingerprint, NGramFingerprintAlgorithm
from pyprepbuddy.exceptions.application_exception import ApplicationException
from pyprepbuddy.rdds.transformable_rdd import TransformableRDD


class ClusterTest(PySparkTestCase):
    def test_should_give_highest_of_facets(self):
        initial_dataset = self.sc.parallelize(["X,Y", "A,B", "X,Z", "A,Q", "A,E"])
        transformable_rdd = TransformableRDD(initial_dataset)
        text_facets = transformable_rdd.list_facets_of(0)
        highest = text_facets.highest()
        self.assertEqual("A", highest[0]._1())

    def test_clusters_should_give_clusters_of_given_column_index(self):
        rdd = self.sc.parallelize(["CLUSTER Of Finger print", "finger print of cluster", "finger print for cluster"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        clusters = transformable_rdd.clusters(0, SimpleFingerprint())
        list_of_clusters = clusters.get_all_clusters()
        one_cluster = list_of_clusters[0]
        self.assertTrue(one_cluster.__contains__("CLUSTER Of Finger print"))
        self.assertFalse(one_cluster.__contains__("finger print for cluster"))

    def test_clusters_should_give_clusters_By_n_gram_fingerprint(self):
        rdd = self.sc.parallelize(["CLUSTER Of Finger print", "finger print of cluster", "finger print for cluster"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        clusters = transformable_rdd.clusters(0, NGramFingerprintAlgorithm(1))
        list_of_clusters = clusters.get_all_clusters()
        one_cluster = list_of_clusters[0]
        self.assertTrue(one_cluster.__contains__("CLUSTER Of Finger print"))
        self.assertTrue(one_cluster.__contains__("finger print for cluster"))

    def test_list_facets_should_give_facets(self):
        initial_dataset = self.sc.parallelize(["X,Y", "A,B", "X,Z", "A,Q", "A,E"])
        transformable_rdd = TransformableRDD(initial_dataset)
        text_facets = transformable_rdd.list_facets_of(0)
        self.assertEquals(2, text_facets.count())

    def test_list_facets_should_give_facets_of_given_column_indexes(self):
        rdd = self.sc.parallelize(["Ram,23,Male", "Ram,23,Male", "Jill,45,Female", "Soa,,Female,"])
        transformable_rdd = TransformableRDD(rdd, 'csv')
        duplicates = transformable_rdd.list_facets([0, 1, 2])
        highest = duplicates.highest()
        self.assertEqual("Ram\n23\nMale", highest[0]._1())

    def test_replace_values_should_replace_cluster_values_with_given_text(self):
        initial_dataset = self.sc.parallelize(["XA,Y", "A,B", "AX,Z", "A,Q", "A,E"])
        transformable_rdd = TransformableRDD(initial_dataset)
        clusters = transformable_rdd.clusters(0, NGramFingerprintAlgorithm(1))
        one_cluster = clusters.get_all_clusters()[0]
        values = transformable_rdd.replace_values(one_cluster, "Hello", 0).collect()
        self.assertTrue(values.__contains__("Hello,B"))

    def test_exception_for_text_Facets(self):
        initial_dataset = self.sc.parallelize(["1,2", "1,2", "1,3"])
        transformable_rdd = TransformableRDD(initial_dataset, "csv")
        self.assertRaises(ApplicationException, transformable_rdd.list_facets_of, 4)
