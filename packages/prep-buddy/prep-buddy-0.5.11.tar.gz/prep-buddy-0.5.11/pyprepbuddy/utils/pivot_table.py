class PivotTable(object):
    """
    Represents a table of organized and summarized selected columns and rows of data.
    """
    def __init__(self, java_pivot_table):
        self.__table = java_pivot_table

    def add_entry(self, row_key, column_key, value):
        self.__table.addEntry(row_key, column_key, value)

    def value_at(self, row_key, column_key):
        return self.__table.valueAt(row_key, column_key)
