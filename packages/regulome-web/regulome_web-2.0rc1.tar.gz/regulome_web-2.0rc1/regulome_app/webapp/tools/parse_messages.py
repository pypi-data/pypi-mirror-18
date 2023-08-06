# Import modules
import os
import json
import math
from regulome_app.webapp import models as models
from regulome_app.config import configs


# Global variables
MIN_PLOT_LENGTH = 10
MAX_PLOT_LENGTH = 5 * 10 ** 6
MAX_CHROMATIN_PROFILE_LENGTH = 5 * 10 ** 5


class ParseMessage:
    """Class to parse the Flask messages"""

    GENES_COORDS = os.path.join(configs['data']['data'], '{}', '{}_UCSC_RefSeq_genes_simple.txt')

    def __init__(self, messages):
        """Initiate the class"""
        self.messages = json.loads(messages)
        self.messages['gene'] = self._check_gene()
        self.set_chromosome(self.messages['chromosome'])
        self.messages['start'] = self._check_start(self.messages['start'])
        self.messages['end'] = self._check_end(self.messages['end'])
        range_region = int(self.messages['range_region'])
        self.messages['start_range'] = max(1, self.messages['start'] - range_region)
        self.messages['end_range'] = min(models.CHROMOSOME_LENGTHS[self.messages['build']][self.messages['chromosome']],
                                         self.messages['end'] + range_region)
        self.messages['length'] = self._calculate_length()
        self._calculate_zoom()
        self._calculate_moves()
        self._calculate_chromatin_profile()

    def set_chromosome(self, chromosome):
        """Set the value of end"""
        if chromosome.startswith('chromosome'):
            self.messages['chromosome_number'] = chromosome.split()[1]
        else:
            self.messages['chromosome'] = models.CHROMOSOMES_DICT_R[chromosome]
            self.messages['chromosome_number'] = chromosome[3:]

    def set_start(self, start):
        """Set the value of start"""
        self.messages['start'] = start

    def set_end(self, end):
        """Set the value of end"""
        self.messages['end'] = end

    def _check_gene(self):
        """Check the existence of the gene"""
        if 'gene' not in self.messages.keys():
            return ''
        elif self.messages['gene'] == '' or self.messages['gene'] == []:
            return ''
        else:
            return self.get_gene_coordinates()

    def _check_start(self, start):
        """Validate the start position"""
        try:
            start = int(start)
        except ValueError as e:
            start = 1
        finally:
            if int(start) <= 0:
                start = 1
        return start

    def _check_end(self, end):
        """Validate the start position"""
        try:
            end = int(end)
        except ValueError as e:
            end = self.messages['start'] + 10**6  # 1Mb
        finally:
            if int(end) > models.CHROMOSOME_LENGTHS[self.messages['build']][self.messages['chromosome']]:
                end = models.CHROMOSOME_LENGTHS[self.messages['build']][self.messages['chromosome']]
        return end

    def _calculate_length(self):
        """Calculate the length of the plot"""
        length = self.messages['end_range'] - self.messages['start_range']
        if length >= 10 ** 6:
            return '{0:.1f} Mb'.format(length / 10 ** 6)
        elif length >= 10 ** 3:
            return '{0:.1f} Kb'.format(length / 10 ** 3)
        else:
            return '{} bp'.format(length)

    def _calculate_zoom(self):
        """Calculate the coordinates of the zooms"""
        start = self.messages['start_range']
        end = self.messages['end_range']
        width = end - start
        length_chromosome = models.CHROMOSOME_LENGTHS[self.messages['build']][self.messages['chromosome']]
        zoom_in = lambda x: (width - (width / x)) / 2
        zoom_out = lambda x: (width * (x - 1)) / 2

        for key_in, key_out, value in zip(('zoom_in_1.5x', 'zoom_in_3x', 'zoom_in_10x'),
                                          ('zoom_out_1.5x', 'zoom_out_3x', 'zoom_out_10x'),
                                          (1.5, 3, 10)):
            self.messages[key_in] = {}
            self.messages[key_out] = {}
            self.messages[key_in]['start'] = max(int(math.floor(start + zoom_in(value))), 1)
            self.messages[key_in]['end'] = min(int(math.ceil(end - zoom_in(value))),
                                               length_chromosome)
            self.messages[key_out]['start'] = max(int(math.ceil(start - zoom_out(value))), 1)
            self.messages[key_out]['end'] = min(int(math.floor(end + zoom_out(value))),
                                                length_chromosome)
            # Disabled
            self.messages[key_in]['disabled'] = 'enabled' if int(math.ceil(end - zoom_in(value))) - int(math.floor(start + zoom_in(value))) >= MIN_PLOT_LENGTH else 'disabled'
            self.messages[key_out]['disabled'] = 'enabled' if int(math.floor(end + zoom_out(value))) - int(math.ceil(start - zoom_out(value))) <= MAX_PLOT_LENGTH else 'disabled'

    def _calculate_chromatin_profile(self):
        """Enable or disable the chromatin profile option in the R script"""
        length = self.messages['end_range'] - self.messages['start_range']
        if length <= MAX_CHROMATIN_PROFILE_LENGTH:
            self.messages['chromatin_profile'] = 'enabled'
        else:
            self.messages['chromatin_profile'] = 'disabled'

    def _calculate_moves(self):
        """Calculate the coordinates of the left and right moves"""
        start = self.messages['start_range']
        end = self.messages['end_range']
        width = end - start
        length_chromosome = models.CHROMOSOME_LENGTHS[self.messages['build']][
            self.messages['chromosome']]
        move_left = lambda pos, x: pos - int(width * x)
        move_right = lambda pos, x: pos + int(width * x)

        for key_left, key_right, value in zip(('left_25', 'left_50', 'left_75'),
                                              ('right_25', 'right_50', 'right_75'),
                                              (0.25, 0.5, 0.75)):
            # Coordinates
            self.messages[key_left] = {}
            self.messages[key_right] = {}
            self.messages[key_left]['start'] = max(move_left(start, value), 1)
            self.messages[key_left]['end'] = max(move_left(end, value), 1)
            self.messages[key_right]['start'] = min(move_right(start, value), length_chromosome)
            self.messages[key_right]['end'] = min(move_right(end, value), length_chromosome)
            # Disabled
            self.messages[key_left]['disabled'] = 'enabled' if move_left(start, value) > 0 else 'disabled'
            self.messages[key_right]['disabled'] = 'enabled' if move_right(end, value) < length_chromosome else 'disabled'

    def get_genes(self):
        """Return the genes corresponding to the submitted gene_name"""
        return self.messages['gene']

    def _check_gene_coordinates(self, gene):
        """Check if the name and/or the coordinates of the gene are correct"""
        gene_name, features = gene.split()
        gene_chromosome = features.split(':')[0][1:]
        gene_start, gene_end = features[:-1].split(':')[1].split('-')
        with open(self.GENES_COORDS.format(self.messages['build'], self.messages['build']), 'r') as fi:
            for line in fi:
                name, chromosome, strand, start, end, _ = line.split('\t')
                if (gene_name.upper() == name.upper() and
                    gene_chromosome == chromosome and
                    gene_start == start and
                    gene_end == end):
                    return True
        return False

    def get_gene_coordinates(self):
        """Return the coordinates of a gene.
        If the gene is not found, returns an empty list.
        """
        gene = ''
        # Only gene name
        if len(self.messages['gene'].split()) == 1:
            with open(self.GENES_COORDS.format(self.messages['build'], self.messages['build']), 'r') as fi:
                for line in fi:
                    name, chromosome, strand, start, end, _ = line.split('\t')
                    if self.messages['gene'].upper() == name.upper():
                        gene = "{} ({}:{}-{})".format(name, chromosome, start, end)
                        break

        # Gene name and coordinates
        elif (len(self.messages['gene'].split()) == 2
              and ":" in self.messages['gene']
              and '-' in self.messages['gene']):
            if self._check_gene_coordinates(self.messages['gene']):
                gene = self.messages['gene']
        return gene

    def get_json(self):
        """Return the json dump of messages"""
        return json.dumps(self.messages)
