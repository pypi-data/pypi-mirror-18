# Import modules
from collections import OrderedDict


MESSAGES = {
    'default': 'Islet Regulome intro page',
    'not_implemented': 'Not implemented yet'
}

SNPS = OrderedDict([
    ('diagram', 'T2D - DIAGRAM'),
    ('magic', 'Fasting glycemia – MAGIC')
])

BUILDS = OrderedDict([
    ('hg18', 'GRCh36/hg18'),
    ('hg19', 'GRCh37/hg19'),
    ('hg38', 'GRCh38/hg38')
])

REGIONS = OrderedDict([
    ('adult', 'Adult pancreatic islets - Open chromatin classes'),
    ('adultStretch', 'Adult pancreatic islets - Chromatin states'),
    ('progenitor', 'Pancreatic islet progenitors - Regulatory regions')
])

TFBS = OrderedDict([('adult', 'Adult pancreatic islets - TFs'),
                    ('progenitor', 'Pancreatic islet progenitors - TFs')
                    ])

CHROMATIN = OrderedDict([('alpha', 'FACS purified alpha cells – open chromatin profile'),
                         ('beta', 'FACS purified beta cells - open chromatin profile'),
                         ('none', 'None')
                         ])

RANGES = OrderedDict([(0, '0bp'),
                      (1000, '1Kb'),
                      (5000, '5Kb'),
                      (10000, '10Kb'),
                      (50000, '50Kb'),
                      (100000, '100Kb'),
                      (500000, '500Kb'),
                      (1000000, '1Mb')]
                     )
RANGES_R = {value: key for key, value in RANGES.items()}


CHROMOSOMES = [str(n) for n in range(1, 23)]
CHROMOSOMES.extend(["X", "Y"])
CHROMOSOMES_DICT = {'chromosome {}'.format(chromosome): 'chr{}'.format(chromosome)
                    for chromosome in CHROMOSOMES}
CHROMOSOMES_DICT_R = {value: key for key, value in CHROMOSOMES_DICT.items()}
CHROMOSOMES_DATASET = {'chromosome {}'.format(chromosome): '' for chromosome in CHROMOSOMES}
CHROMOSOMES_SORTED = ["chromosome {}".format(i) for i in CHROMOSOMES]
CHROMOSOME_LENGTHS = {
    "hg18": {
        'chromosome 1': 247249719,
        'chromosome 2': 242951149,
        'chromosome 3': 199501827,
        'chromosome 4': 191273063,
        'chromosome 5': 180857866,
        'chromosome 6': 170899992,
        'chromosome 7': 158821424,
        'chromosome 8': 146274826,
        'chromosome 9': 140273252,
        'chromosome 10': 135374737,
        'chromosome 11': 134452384,
        'chromosome 12': 132349534,
        'chromosome 13': 114142980,
        'chromosome 14': 106368585,
        'chromosome 15': 100338915,
        'chromosome 16': 88827254,
        'chromosome 17': 78774742,
        'chromosome 18': 76117153,
        'chromosome 19': 63811651,
        'chromosome 20': 62435964,
        'chromosome 21': 46944323,
        'chromosome 22': 49691432,
        'chromosome X': 154913754,
        'chromosome Y': 57772954,
        'chromosome M': 16571
    },
    "hg19": {
        'chromosome 1': 249250621,
        'chromosome 2': 243199373,
        'chromosome 3': 198022430,
        'chromosome 4': 191154276,
        'chromosome 5': 180915260,
        'chromosome 6': 171115067,
        'chromosome 7': 159138663,
        'chromosome 8': 146364022,
        'chromosome 9': 141213431,
        'chromosome 10': 135534747,
        'chromosome 11': 135006516,
        'chromosome 12': 133851895,
        'chromosome 13': 115169878,
        'chromosome 14': 107349540,
        'chromosome 15': 102531392,
        'chromosome 16': 90354753,
        'chromosome 17': 81195210,
        'chromosome 18': 78077248,
        'chromosome 19': 59128983,
        'chromosome 20': 63025520,
        'chromosome 21': 48129895,
        'chromosome 22': 51304566,
        'chromosome X': 155270560,
        'chromosome Y': 59373566,
        'chromosome M': 16571
    },
    "hg38": {
        'chromosome 1': 248956422,
        'chromosome 2': 242193529,
        'chromosome 3': 198295559,
        'chromosome 4': 190214555,
        'chromosome 5': 181538259,
        'chromosome 6': 170805979,
        'chromosome 7': 159345973,
        'chromosome 8': 145138636,
        'chromosome 9': 138394717,
        'chromosome 10': 133797422,
        'chromosome 11': 135086622,
        'chromosome 12': 133275309,
        'chromosome 13': 114364328,
        'chromosome 14': 107043718,
        'chromosome 15': 101991189,
        'chromosome 16': 90338345,
        'chromosome 17': 83257441,
        'chromosome 18': 80373285,
        'chromosome 19': 58617616,
        'chromosome 20': 64444167,
        'chromosome 21': 46709983,
        'chromosome 22': 50818468,
        'chromosome X': 156040895,
        'chromosome Y': 57227415,
        'chromosome M': 16569
    }
}

COLORS = {
    "adult": {
        "Promoter": (0, 0, 0),
        "Inactive enhancer": (171, 217, 233),
        "Active enhancer": (215, 25, 28),
        "C3 cluster": (152, 17, 53),
        "CTCF": (44, 123, 182),
        "Others": (253, 174, 97),
        "GENE_SPECIFIC": (100, 100, 100),
        "GENE_UNSPECIFIC": (200, 200, 200),
        "TFBS": (44, 65, 182)
    },
    "adultStretch": {
        "Insulator": (0, 0, 0),
        "Weak enhancer": (171, 217, 233),
        "Active promoter": (215, 25, 28),
        "Weak promoter": (44, 123, 182),
        "Strong enhancer": (253, 174, 97),
        "Repressed": (77, 175, 74),
        "Transcribed": (152, 78, 163),
        "Posied promoter": (166, 86, 40),
        "Stretch Enhancer": (152, 17, 53),
        "GENE_SPECIFIC": (100, 100, 100),
        "GENE_UNSPECIFIC": (200, 200, 200),
        "TFBS": (44, 65, 182)
    },
    "progenitor": {
        "Active enhancer": (0, 0, 0),
    }
}


# Table of colors
# name	        hex	    rgb	        adultIslet	        adultIsletStretch	progenitor
# ------------------------------------------------------------------------------------------
# black	        #000000	0,0,0	    Promoter	        Insulator	        Active enhancer
# light blue	#ABD9E9	171,217,233	Inactive enhancer	Weak enhancer	    -
# red	        #D7191C	215,25,28	Active enhancer	    Active promoter	    -
# blue	        #2C7BB6	44,123,182	CTCF	            Weak promoter	    -
# beige	        #FDAE61	253,174,97	Others	            Strong enhancer	    -
# green	        #4DAF4A	77,175,74	-	                Repressed	        -
# purple	    #984EA3	152,78,163	-	                Transcribed	        -
# brown	        #A65628	166,86,40	-	                Posied promoter	    -
# ------------------------------------------------------------------------------------------


default_messages = {
    'build': 'hg19',
    'region': 'adult',
    'tfbs': 'adult',
    'chromatin': 'none',
    'gene': '',
    'chromosome': 'chromosome 13',
    'chromosome_number': '13',
    'start': '',
    'end': '',
    'range_region': '50000',
    'select_snps': 'diagram_magic',
    'upload_regions': 'None',
    'upload_snps': 'None',
    'action': ''
}


