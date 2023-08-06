# Import modules
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


__author__ = 'Loris Mularoni'


class Visualize:

    def __init__(self):
        pass

    @staticmethod
    def put_data(database):
        conn = sqlite3.connect(database)
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)''')

        # Insert a row of data
        c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

        # Save (commit) the changes
        conn.commit()

        # Close the connection
        conn.close()

    def get_data(self, database):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        self.results = [row for row in c.execute('SELECT * FROM stocks ORDER BY price')]
        #c.execute('SELECT * FROM stocks WHERE symbol=?', t)

    def create_plot(self, output):

        # Do plot in two parts
        fig = plt.figure(figsize=(14, 7))
        ax1 = plt.subplot2grid((5, 5), (0, 0), rowspan=4, colspan=4)
        ax2 = plt.subplot2grid((5, 5), (4, 0), colspan=4)
        ax3 = plt.subplot2grid((5, 5), (0, 4), rowspan=2)
        ax4 = plt.subplot2grid((5, 5), (3, 4), rowspan=2)

        # Mutations
        ax1.scatter(range(10), range(10), c='r')
        # Remove ticks
        ax1.tick_params(axis='both', which='both', bottom='off', top='off',
                        left='on', right='off', labelbottom='off', labelleft='on',
                        labelsize=14)

        ax1.set_ylim([0, 10])

        # Remove line
        #ax1.spines['bottom'].set_color('none')
        ax1.spines['bottom'].set_visible(False)

        # Gene
        ax2.scatter(range(10), range(10), c='b')
        # Remove ticks
        ax2.tick_params(axis='both', which='both', bottom='off', top='off',
                        left='off', right='off', labelbottom='off', labelleft='off')
        # Remove line
        ax2.spines['top'].set_color('grey')
        ax2.spines['top'].set_linestyle('dashed')


        # FM cache
        ax3.scatter(range(10), range(10), c='g')
        # Remove ticks
        ax3.tick_params(axis='both', which='both', bottom='off', top='off',
                        left='off', right='off', labelbottom='off', labelleft='off')

        # CLUST cache
        ax4.axis('off')

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, hspace=0, wspace=0.3)

        # Only show ticks on the left and bottom spines
        #ax3.yaxis.set_ticks_position('left')
        #ax3.xaxis.set_ticks_position('bottom')

        #plt.show()
        plt.savefig(output)