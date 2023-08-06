__author__ = 'Loris Mularoni'


# Import modules
import sqlite3
import pandas as pd


class GetFromDB:
    """Class to get data from the DB."""
    def __init__(self, db):
        """Initialize the class."""
        self.db = db
        self.connection = None
        self._connect()

    def _connect(self):
        """Connect to the database file."""
        self.connection = sqlite3.connect(self.db)

    def close(self):
        """Close the connection to the database."""
        self.connection.close()

    def _do_query(self, query):
        """Execute the query. Return a dataframe."""
        # index_col specifies which column to make the DataFrame index
        data = pd.io.sql.read_sql(query, self.connection)#, index_col='index')
        return data

    def retrieve_all(self, table_name):
        """Query all records in the database."""
        query = "SELECT * FROM {};".format(table_name)
        return self._do_query(query)

    def retrieve_by_chromosome_start(self, table_name, chromosome, start, end):
        """Query by chromosome and position"""
        query = "SELECT * FROM {} WHERE CHROMOSOME='{}' AND START BETWEEN {} AND {};".format(table_name,
                                                                                             chromosome,
                                                                                             start,
                                                                                             end)
        return self._do_query(query)

    def retrieve_by_chromosome_start_end(self, table_name, chromosome, start, end):
        """Query by chromosome and position"""
        query = "SELECT * FROM {} WHERE CHROMOSOME='{}' AND START>={} AND [END]<={};".format(table_name,
                                                                                         chromosome,
                                                                                         start,
                                                                                         end)
        return self._do_query(query)

    def retrieve_by_symbol(self, table_name, symbol):
        """Query by symbol"""
        query = "SELECT * FROM {} WHERE SYMBOL='{}';".format(table_name, symbol)
        return self._do_query(query)


# MAGIC, DIAGRAM, table: diagram, magic
# CHROMOSOME, START, SNP, PVALUE
# coords: CHROMOSOME, START

# GENE, table: genes
# SYMBOL, CHROMOSOME, START, END, ENSEMBL_ID, STRAND, TYPE, COPIES, OVERLAP
# coords: CHROMOSOME, START, END
# ix_genes_SYMBOL: SYMBOL

# ex:
# from readDB import GetFromDB
# obj = GetFromDB("../data/hg18/hg18_magic.db")
# df = obj.retrieve_by_chromosome_start('magic', 'chr1', 766980, 866990)
# obj.close()

# df = obj.retrieve_by_chromosome_start_end('genes', 'chr1', 1000000, 2000000)
# df = obj.retrieve_by_symbol('genes', 'TP53')