# Variables
output_plot <- paste0("plots/IRB_", gsub(" ", "_", Sys.time()), ".pdf")
output_file <- paste0("plots/IRB_", gsub(" ", "_", Sys.time()), ".txt")
output_snp <- paste0("plots/IRB_", gsub(" ", "_", Sys.time()), ".snp.txt")
output_motifs <- ""
input_window <- 100
format_plot <- "pdf"

# PDX1
start = 28494167
stop = 28500451
chromosome = "chr13"

build <- "hg19"
ranges <- 50000
mapTF <- 'adult'
mapRegion <- 'adult'
mapChrom <- "beta"  # 'HI08_1'
input_user_regions <- "input_reg_test.bed"
input_user_snps <- "input_snp.txt"
plot_diagram <- FALSE
plot_magic <- TRUE
