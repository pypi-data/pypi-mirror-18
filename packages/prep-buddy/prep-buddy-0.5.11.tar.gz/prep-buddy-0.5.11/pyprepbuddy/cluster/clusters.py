from pyprepbuddy.cluster.cluster import Cluster


class Clusters(object):
    """
    Clusters is a collection of cluster of a column.
    """
    def __init__(self, clusters):
        self.__clusters = []
        all_clusters = clusters.getAllClusters()
        for cluster in all_clusters:
            self.__clusters.append(Cluster(cluster))

    def get_all_clusters(self):
        return self.__clusters
