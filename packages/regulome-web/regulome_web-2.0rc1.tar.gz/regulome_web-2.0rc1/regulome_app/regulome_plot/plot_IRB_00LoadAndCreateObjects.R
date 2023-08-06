#######################################
## plot_IRB_00LoadAndCreateObjects.R ##
#######################################
##-----------------------------------------------------------------------------------------------
## This script needs to be called by plot_IRB_main.R in order to load and generate the
## new data objects using given arguments to draw the plot.
##-----------------------------------------------------------------------------------------------

##-----------------------------------------------------------------------------------------------
## Fixing start and stop coordinates
##-----------------------------------------------------------------------------------------------
start <- start - ranges
stop <- stop + ranges
ws <- input_window

##-----------------------------------------------------------------------------------------------
## Fixing path of the files
##-----------------------------------------------------------------------------------------------
tfs <- paste(base_name, separator, paste0(tfs, mapTF, ".rda"), sep=build)
regRegions <- paste(base_name, separator, paste0(regRegions, mapRegion, ".rda"), sep=build)
chromatin <- paste(base_name, separator, paste0(chromatin, mapChrom, ".bedgraph.gz"), sep=build)
lncRNA <- paste(base_name, separator, lncRNA, sep=build)
ideogram <- paste(base_name, separator, ideogram, sep=build)
if (mapRegion == "adult") {
  cluster <- paste(base_name, separator, clusterG3, sep=build)
  load(file=cluster)
} else if (mapRegion == "adultStretch") {
  cluster <- paste(base_name, separator, clusterS, sep=build)
  load(file=cluster)
} else {
  cluster <- c()
}
genes <- paste(base_name, separator, genes, sep=build)

##-----------------------------------------------------------------------------------------------
## Read in data: hard coded
##-----------------------------------------------------------------------------------------------
load(file=regRegions)
load(file=lncRNA)
load(file=specific_genes)
load(file=tfs)
load(file=ideogram)
load(file=paste0(genes, chromosome, '.rda')) 
# Read the diagram file
if (plot_diagram == TRUE) {
  diagram <- paste(base_name, separator, diagram, sep=build)
  if (chromosome != "chrX" & chromosome != "chrY") {
    load(file=paste0(diagram, chromosome, '.rda'))
  } else {
    load(file=paste0(diagram, 'chr0.rda'))
  }
}

# Read the magic file
if (plot_magic == TRUE) {
  magic <-  paste(base_name, separator, magic, sep=build)
  if (chromosome != "chrX" & chromosome != "chrY") {
    load(file=paste0(magic, chromosome, '.rda'))
  } else {
    load(file=paste0(magic, 'chr0.rda'))
  }
}
# The motifs data will be loaded eventually if the plot is <= 1000bp

##-----------------------------------------------------------------------------------------------
## Generate variables of interest
##-----------------------------------------------------------------------------------------------
# Vector of the TF analyzed (automatically length of TFs in dataset)
head <- names(tfs)[4:ncol(tfs)]

# Locus
if (!chromosome %in% unique(tfs$chr)) {message(paste("Cannot find chromosome", chromosome, "in the file", sep=" ")); q()}
if (!start) {start <- min(tfs[tfs$chr == chromosome,])}
if (!stop) {stop <- max(tfs[tfs$chr == chromosome,])}

# Chromosome length
if (build == "hg18") {
  chromosome.length <- chromosome_lengths_hg18[which(chromosome_names == chromosome)]
} else if (build == "hg19") {
  chromosome.length <- chromosome_lengths_hg19[which(chromosome_names == chromosome)]
} else if (build == "hg38") {
  chromosome.length <- chromosome_lengths_hg38[which(chromosome_names == chromosome)]
} else {
  message("The human build (-B) should be hg18, hg19, or hg38"); q()
}

# Limit the start between 0 <= start <= chromosome.length - 100
if (start < 0) {start = 0}
if (start > chromosome.length) {start = chromosome.length - 100}

# Limit the stop between 10 <= stop <= chromosome.length
if (stop < 10) {stop = 10}
if (stop > chromosome.length) {stop = chromosome.length}

# TFs comprised in the region of interest
locus <- tfs[tfs$chr == chromosome & tfs$Start >= start & tfs$End <= stop, ]
d = (stop - start) / 20

locus2 <- tfs[tfs$chr == chromosome, ]
locus2 <- locus2[(locus2$Start >= start & locus2$Start <= stop) | 
                   (locus2$End >= start & locus2$End <= stop) |
                   (locus2$Start <= start & locus2$End >= stop), ]

# These are the coordinates where the TFs will be drawn
intervals <- seq(start, stop, (stop - start) / (length(head) * 2))
intervals <- intervals[seq(2, length(intervals), 2)]

# Regulatory regions comprised in the region of interest
regions <- regRegions[regRegions[, 1] == chromosome,]
regions <- regions[(regions[, 2] >= start & regions[, 2] <= stop) | 
                     (regions[, 3] >= start & regions[, 3] <= stop) | 
                     (regions[, 2] <= start & regions[, 3] >= stop), ]

# Cluster C3 
if (mapRegion == "adult" | mapRegion == "adultStretch") {
  cluster <- cluster[cluster[, 1] == chromosome, ]
  cluster <- cluster[(cluster[, 2] >= start & cluster[, 2] <= stop) |
                       (cluster[, 3] >= start & cluster[, 3] <= stop) |
                       (cluster[, 2] <= start & cluster[, 3] >= stop), ]
}


# Strength of the binding: how many TFs bind per regions
locus$Binding <- rowSums(locus[, 4:ncol(locus)])
locus2$Binding <- rowSums(locus2[, 4:ncol(locus2)])
