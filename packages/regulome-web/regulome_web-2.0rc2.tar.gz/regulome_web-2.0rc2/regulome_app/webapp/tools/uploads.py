__author__ = 'Loris Mularoni'


class Upload:
    """Check the validity of the uploaded files"""

    def __init__(self, input_file, type_of_file, output_file):
        """Initiate the class."""
        self.type_of_file = type_of_file
        self.input_file = input_file
        self.output_file = output_file
        self.msg = ''
        if type_of_file == 'region_file':
            self.validator = self.regions_file_validator()
            self.columns = ["CHR", "START", "END"]
        elif type_of_file == 'snps_file':
            self.validator = self.snp_file_validator()
            self.columns = ["CHR", "POS", "PVAL", "SNP"]

        if self.validator:
            self.save_file()

    def regions_file_validator(self):
        """Validate an uploaded regions file"""
        with open(self.input_file, 'r') as fi:
            num_columns = set([])

            try:
                for i, line in enumerate(fi):
                    # Remove header and empty lines
                    if line.startswith('#') or line.strip() == '':
                        continue
                    line = line.strip().split()
                    num_columns.add(len(line))
                    if len(line) < 3:
                        self.msg = 'Line {} of the uploaded file has {} '.format(i + 1, len(line)) + \
                                   'columns instead of the expected 3 (or more)'
                        return False
                    if not line[0].startswith('chr'):
                        self.msg = 'The first column of the uploaded file should contain the ' + \
                                   'chromosome\'s name.'
                        return False
                    try:
                        start = int(line[1])
                        if start <= 0:
                            self.msg = 'The second column of the uploaded file should contain ' + \
                                       'positive numerical values'
                            return False
                    except ValueError as e:
                        self.msg = 'The second column of the uploaded file should contain ' + \
                                   'positive numerical values'
                        return False
                    try:
                        end = int(line[2])
                        if end <= 0:
                            self.msg = 'The third column of the uploaded file should contain ' + \
                                       'positive numerical values'
                            return False
                    except ValueError as e:
                        self.msg = 'The third column of the uploaded file should contain ' + \
                                   'positive numerical values'
                        return False
                    if start >= end:
                        self.msg = 'The values of the second column (start) should be smaller ' + \
                                   'than the values of the third column (end)'
                        return False
            except UnicodeDecodeError:
                self.msg = 'The uploaded file is not a text file'
                return False
            except Exception:
                self.msg = 'An error occurred uploading the file'
                return False

            if len(num_columns) > 1:
                self.msg = 'The lines of the uploaded file do not have the same number of columns'
                return False
            elif len(num_columns) == 0:
                self.msg = 'The uploaded file seems to be empty'
                return False
        return min(list(num_columns)[0], 3)

    def snp_file_validator(self):
        """Validate an uploaded snp file"""
        with open(self.input_file, 'r') as fi:
            num_columns = set([])

            try:
                for i, line in enumerate(fi):
                    # Remove header and empty lines
                    if line.startswith('#') or line.strip() == '':
                        continue
                    line = line.strip().split()
                    num_columns.add(len(line))
                    if len(line) < 3:
                        self.msg = 'Line {} of the uploaded file has {} '.format(i + 1, len(line)) + \
                                   'columns instead of the expected 3 (or more)'
                        return False
                    if not line[0].startswith('chr'):
                        self.msg = 'The first column of the uploaded file should contain the ' + \
                                   'chromosome\'s name.'
                        return False
                    try:
                        start = int(line[1])
                        if start <= 0:
                            self.msg = 'The second column of the uploaded file should contain ' + \
                                       'positive numerical values'
                            return False
                    except ValueError as e:
                        self.msg = 'The second column of the uploaded file should contain ' + \
                                   'positive numerical values'
                        return False
                    try:
                        pvalue = float(line[2])
                        if pvalue < 0.0 or pvalue > 1.0:
                            self.msg = 'The third column of the uploaded file should contain ' + \
                                       'values comprised between 0.0 and 1.0'
                            return False
                    except ValueError as e:
                        self.msg = 'The third column of the uploaded file should contain ' + \
                                   'positive numerical values'
                        return False
            except UnicodeDecodeError:
                self.msg = 'The uploaded file is not a text file'
                return False
            except Exception:
                self.msg = 'An error occurred uploading the file'
                return False

            if len(num_columns) > 1:
                self.msg = 'The lines of the uploaded file do not have the same number of columns'
                return False
            elif len(num_columns) == 0:
                self.msg = 'The uploaded file seems to be empty'
                return False
        return min(list(num_columns)[0], 4)

    def save_file(self):
        """Add the header to the file and save it"""
        with open(self.input_file, 'r') as fi, open(self.output_file, 'w') as fo:
            header = '{}\n'.format('\t'.join(self.columns[:self.validator]))
            fo.write(header)
            for i, line in enumerate(fi):
                if line.startswith('#') or line.strip() == '':
                    continue
                line = line.strip().split("\t")
                if self.type_of_file == 'snps_file' and len(line) < 4:
                    line.append('snp_{}'.format(i + 1))
                fo.write("\t".join(line[:self.validator]) + "\n")

    def get_errors(self):
        """Return the result of the upload"""
        return False if self.validator else self.msg
