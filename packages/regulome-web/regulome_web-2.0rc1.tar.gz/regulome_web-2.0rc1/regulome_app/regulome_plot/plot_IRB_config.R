library(ini)

# Define terminal colors
term.red <- '\033[31m'
term.green <- '\033[32m'
term.yellow <- '\033[33m'
term.blue <- '\033[34m'
term.purple <- '\033[35m'
term.cyan <- '\033[36m'
term.white <- '\033[37m'
term.normal <- '\033[0m'

# Load the configuration file
configFile <- file.path(initial_dir, 'regulome.cfg')
conf <- read.ini(configFile)
base_name <- conf$data$data
separator <- .Platform$file.sep

# Add the separator at the end of the base_name
bn <- unlist(strsplit(base_name, ''))
if (bn[length(bn)] != separator) {
    base_name <- paste0(base_name, separator)
}

# These files require to be completed with the full path and build
regRegions <- '_regions_'
tfs <- '_tfs_'
chromatin <- '_chromatin_'
lncRNA <- '_lncRNA.rda'
specific_genes <- file.path(base_name, 'shared', 'specific_genes.rda')
genes <- '_genes_'
diagram <- '_diagram_'
magic <- '_magic_'
ideogram <- '_ideogram.rda'
clusterG3 <- '_clusters_G3.rda'
clusterS <- '_clusters_stretch.rda'
motifs <- '_motifs.rda'

# Color codes
palette <- c("#000000", "#ABD9E9", "#D7191C", "#2C7BB6",
             "#FDAE61", "#4DAF4A", "#984EA3", "#A65628")
G3c <- rgb(152, 17, 53, maxColorValue=255) #dark red
TFregions <- rgb(44, 65, 182, maxColorValue=255) # darkest blue
GENE_SPEC <- rgb(100, 100, 100, maxColorValue = 255)
GENE_UNSPEC <- rgb(200, 200, 200, maxColorValue = 255)

# Strength colors 
binding_color <- paste('grey', rev(seq(0, 80, 20)), sep='')

# Snp colors
snp_colors <- hsv(0, seq(0, 1, by=0.1), 1)

# User colors
col_user_regions <- rgb(0, 100, 0, alpha=125, maxColorValue=255)
user_snp_colors <- hsv(0.6, seq(0, 1, by=0.1), 1)

# Maximum distance to show details
MAX_DIST_SHOW = 200000

# Karyotype colors
karyotype_color_names <- c("gpos100", "gpos", "gpos75", "gpos66",
                           "gpos50", "gpos33", "gpos25", "gvar",
                           "gneg", "acen", "stalk")

karyotype_color_rgb <- c(rgb(0,0,0, maxColorValue = 255), 
			rgb(0,0,0, maxColorValue = 255),
			rgb(130,130,130, maxColorValue = 255),
			rgb(160,160,160, maxColorValue = 255), 
			rgb(200,200,200, maxColorValue = 255),
			rgb(210,210,210, maxColorValue = 255), 
			rgb(200,200,200, maxColorValue = 255),
			rgb(220,220,220, maxColorValue = 255), 
			rgb(255,255,255, maxColorValue = 255),
			rgb(14,199,20, maxColorValue = 255), 
			rgb(100,127,164, maxColorValue = 255)) # original color for acen: 217,47,39

# Chromosome length
chromosome_lengths_hg18 <- c(247249719, 242951149, 199501827, 191273063, 180857866, 170899992,
				158821424, 146274826, 140273252, 135374737, 134452384, 132349534,
				114142980, 106368585, 100338915, 88827254, 78774742, 76117153,
				63811651, 62435964, 46944323, 49691432, 154913754, 57772954, 16571)

chromosome_lengths_hg19 <- c(249250621, 243199373, 198022430, 191154276, 180915260, 171115067,
				159138663, 146364022, 141213431, 135534747, 135006516, 133851895, 
				115169878, 107349540, 102531392, 90354753, 81195210, 78077248, 
				59128983, 63025520, 48129895, 51304566, 155270560, 59373566, 16571)

chromosome_lengths_hg38 <- c(248956422, 242193529, 198295559, 190214555, 181538259, 170805979, 
				159345973, 145138636, 138394717, 133797422, 135086622, 133275309,  
				114364328, 107043718, 101991189, 90338345, 83257441, 80373285, 
				58617616, 64444167, 46709983, 50818468, 156040895, 57227415, 16569)

# Chromosome names
chromosome_names <- c('chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10',
			'chr11','chr12','chr13', 'chr14','chr15','chr16','chr17','chr18','chr19',
			'chr20','chr21','chr22','chrX','chrY','chrM')

