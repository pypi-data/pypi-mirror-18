class Cluster(object):
    """
    Cluster contains groups of values by their specified key
    """
    def __init__(self, cluster):
        self.__cluster = cluster

    def __contains__(self, item):
        return self.__cluster.containsValue(item)

    def size(self):
        return self.__cluster.size()

    def get_cluster(self):
        return self.__cluster
