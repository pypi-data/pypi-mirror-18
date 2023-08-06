##########################################################
# Authors	: Loris Mularoni and Mireia Ramos            #
##########################################################
# This script draws the main plot for the Islet Regulome #
# Browser, using SNPs, motifs, enhancers and TFs data    #
# contained in data/ folder. Needs to be called with     #
# another program and the variables to create the plot   #
# are provided as command line arguments.                #
##########################################################


##########################################################
## Load the config file
##--------------------------------------------------------
initial_dir <- getwd()

getScriptPath <- function(){
  cmd.args <- commandArgs()
  m <- regexpr("(?<=^--file=).+", cmd.args, perl=TRUE)
  script.dir <- dirname(regmatches(cmd.args, m))
  if (length(script.dir) == 0) stop("can't determine script dir: please call the script with Rscript")
  if (length(script.dir) > 1) stop("can't determine script dir: more than one '--file' argument detected")
  return(script.dir)
}
.dir <- getScriptPath()
setwd(.dir)
source("plot_IRB_config.R")


##########################################################
## Sets default values for variables
##--------------------------------------------------------
output_plot <- ""
output_file <- ""
output_snp <- ""
output_motifs <- ""
input_window <- 10
format_plot <- "pdf"
start <- FALSE
stop <- FALSE
build <- FALSE
chromosome <- FALSE
ranges <- 0
mapTF <- 'adult'
mapRegion <- 'adult'
mapChrom <- FALSE
input_user_regions <- FALSE
input_user_snps <- FALSE
plot_diagram <- TRUE
plot_magic <- FALSE


##########################################################
## Read command line arguments
##--------------------------------------------------------
readCommandLineArgs <- function() {
  args <- commandArgs(TRUE)
  # Set usage message if less than 4 arguments are provided.
  if (length(args) < 4) {
    message(paste(term.cyan, "\nThis program creates a plot with the density of TF binding site.\n", sep=""))
    message(paste(term.yellow, "Usage:\n", term.green, "\tplot_IRB_main.R
                  -p,  output_plot
                  -o,  output_file
                  -s,  output_snp
                  -M,  output_motifs
                  -f,  format_plot
                  -B,  build
                  -c,  chromosome
                  -b,  start
                  -e,  stop
                  -r,  ranges
                  -Mt, mapTF
                  -Mr, mapRegion
                  -Mc, mapChromatin
                  -d,  plot_diagram
                  -m,  plot_magic
                  -u,  input_user_regions
                  -U,  input_user_snps
                  -w,  input_window" , sep="")) #-i,  input_file
    
    message(paste(term.yellow, "where:", sep=""))
    message(paste(term.green, "\toutput_plot          : name of the plot to save with results."), sep="")
    message("\toutput_file          : name of the text file to save with the results.")
    message("\toutput_snp           : name of the text file to save with the snp results.")
    message("\toutput_motifs        : name of the text file to save with the motif results.")
    message("\tformat_plot          : format of the plot (pdf, bitmap, or jpeg). Default is pdf.")
    message("\tbuild                : human build used (hg18, hg19, or hg38).")
    message("\tchromosome           : specify which chromosome to analize.")
    message("\tstart                : define in which point of the chromosome the plot will start.")
    message("\tstop                 : define in which point of the chromosome the plot will end.")
    message("\tranges               : extend the plot around start and stop.")
    message("\tmapTF                : select map of transcription factors to use. Available: 'progenitor' and 'adult' (default).")
    message("\tmapRegion            : select map of regions to plot. Available: 'progenitor', 'adultStretch' and 'adult' (default).")
    message("\tmapChromatin         : select map of chromatin regions to plot. Available: 'alpha', 'beta' (optional).")
    message("\tplot_diagram         : plot the DIAGRAM dataset of snps (TRUE or FALSE). Default is TRUE.")
    message("\tplot_magic           : plot the MAGIC dataset of snps (TRUE or FALSE). Default is FALSE.")
    message("\tinput_user_regions   : file with regions to represent in the plot. The file should have 3 colums.")
    message("\tinput_user_snps      : file with snps to represent in the plot. The file should have at least 3 colums.")
    message("\t                       The maximum number of SNP datasets that can be plotted is two, so this option")
    message("\t                       will be ignored if the DIAGRAM and MAGIC datasets will be used.")
    message("\tinput_window         : window to calculate the density. Not functional yet.")
    message(paste("\t                       Default is 100.\n", term.normal, sep=""))
    q()
  }
  
  # Assigning values from command line arguments to variables.
  i <- 1
  while (i < length(args)) {
    opt <- args[i]
    val <- args[i + 1]
    if (opt == "-p") { output_plot <<- val }
    if (opt == "-o") { output_file <<- val }
    if (opt == "-s") { output_snp <<- val }
    if (opt == "-M") { output_motifs <<- val }
    if (opt == "-w") { input_window <<- as.numeric(val) }
    if (opt == "-f") { format_plot <<- val }
    if (opt == "-B") { build <<- val }
    if (opt == "-c") { chromosome <<- as.character(val) }
    if (opt == "-b") { start <<- as.numeric(val) }
    if (opt == "-e") { stop <<- as.numeric(val) }
    if (opt == "-r") { ranges <<- as.numeric(val)}
    if (opt == "-Mt") { mapTF <<- as.character(val)}
    if (opt == "-Mr") { mapRegion <<- as.character(val)}
    if (opt == "-Mc") { mapChrom <<- as.character(val)}
    if (opt == "-d") { plot_diagram <<- val}
    if (opt == "-m") { plot_magic <<- val}
    if (opt == "-u") { input_user_regions <<- val}
    if (opt == "-U") { input_user_snps <<- val}
    if (opt != "-o" & opt != "-s" & opt != "-w" & opt != "-p" & opt != "-f" & opt != "-b" &
        opt != "-e" & opt != '-B' & opt != '-c' & opt != '-r' & opt != "-u" & opt != "-U" &
        opt != "-Mt" & opt != "-Mr" & opt!="-Mc" & opt != "-d" & opt != "-m" & opt != "-M") {
            message(paste("Argument", opt, "is not a valid option", sep = " "))
            q()
        }
    i <- i + 2
  }
  
  # Setting error messages if need variables are empty/incorrect
  if (output_plot == "") {
      message("One or some of the arguments are missing"); q()
  }
  if (format_plot != "bitmap" & format_plot != "pdf" & format_plot != 'jpeg') {
      message("The format of the plot is not valid"); q()
  }
  if (build == FALSE) {
      message("You have to specify the human build to use in the analysis (hg18, hg19, or hg38)")
      q()
  }
  if (build != "hg18" & build != "hg19" & build != "hg38") {
      message("The human build (-B) should be hg18, hg19, or hg38"); q()
  }
  if (mapTF != "adult" & mapTF != "progenitor") {
      message("The chosen map (-Mt) should be 'adult' or 'progenitor'"); q()
  }
  if (mapRegion != "adult" & mapRegion != "progenitor" & mapRegion != "adultStretch") {
      message("The chosen map (-Mr) should be 'adult', 'adultStretch' or 'progenitor'"); q()
  }
  if (mapChrom != FALSE & mapChrom != "alpha" & mapChrom != "beta") {
      message("The chosen map (-Mc) should be 'alpha' or 'beta'"); q()
  }
  if (chromosome == FALSE) {
      message("You have to specify a chromosome to plot"); q()
  }
  if (plot_diagram != FALSE & plot_diagram != TRUE) {
      message("plot_diagram (-d) should be TRUE or FALSE"); q()
  }
  if (plot_magic != FALSE & plot_magic != TRUE) {
      message("plot_magic (-m) should be TRUE or FALSE"); q()
  }
  if (plot_diagram == TRUE & plot_magic == TRUE) {
      input_user_snps <<- FALSE
  }
}

readCommandLineArgs()
# source("plot_IRB_testVariables.R")  # variables for testing plot


##########################################################
## Load and create needed data objects
##--------------------------------------------------------
source("plot_IRB_00LoadAndCreateObjects.R")


##########################################################
## DRAWING MAIN PLOT
##########################################################
##--------------------------------------------------------
## Open the image
##--------------------------------------------------------
if (format_plot == "bitmap") {
	bitmap(file=output_plot, width=10, height=8, res=300, pointsize=12)
} else {
	if (format_plot == "pdf") {
		#postscript(file=output_plot, onefile=FALSE, horizontal=FALSE, width=10, height=8, paper="special")
		pdf(file=output_plot, onefile=FALSE, width=10, height=8, paper="special", bg="white")
	} else {
		jpeg(file=output_plot, width=600, height=480, res=300, pointsize=12)
	}
}


##--------------------------------------------------------
## Define layout of the plot
##--------------------------------------------------------
# layout(matrix(1:8, 8, 1), heights=c(2, 1.5, 5, 3, 0.8, 6, 2, 1))
layout(matrix(1:7, 7, 1), heights=c(2, 1.5, 8, 0.8, 5, 2, 1))


##--------------------------------------------------------
## Create legend
##--------------------------------------------------------
source("plot_IRB_01Legend.R")


##--------------------------------------------------------
## Create header of plot (chr ideogram and genomic info)
##--------------------------------------------------------
source("plot_IRB_02IdeogramHeader.R")


##--------------------------------------------------------
## Top plot (SNPs and MOTIFS (<=1000bp))
##--------------------------------------------------------
source("plot_IRB_03SNPmotifOpenChrom.R")


##--------------------------------------------------------
## Middle plot (regions)
##--------------------------------------------------------
source("plot_IRB_04PlotRegions.R")


##--------------------------------------------------------
## Bottom plot (TF and binding lines)
##--------------------------------------------------------
source("plot_IRB_05PlotTFBS.R")


##--------------------------------------------------------
## Draw genes (darker grey = more specific to HI)
##--------------------------------------------------------
source("plot_IRB_06PlotGenes.R")


##--------------------------------------------------------
## Output files
##--------------------------------------------------------
if (output_file != "") {
  if (mapRegion == "adult") {
    # Order the regions and delete column 5
    cluster[, 4] <- rep("C3 cluster", nrow(cluster))
    regions <- rbind(regions, cluster)
    regions <- regions[order(regions[, 2], -regions[, 3]), -c(5)]
    colnames(regions) <- c("CHR", "START", "END", "CHROMATIN_CLASS", "TF")
    regions$Build <- rep(build, nrow(regions))
    
    if (nrow(regions) > 0) {
      # Write to the output file
      write.table(file=output_file, regions, quote=F, row.names=F, col.names=T, sep="\t")
    }
  } else if (mapRegion == "adultStretch") {
    cluster[, 4] <- rep("Stretch Enhancer", nrow(cluster))
    regions <- rbind(regions, cluster)
    regions <- regions[order(regions[, 2], -regions[, 3]),]
    colnames(regions) <- c("CHR", "START", "END", "CHROMATIN_STATE")
    regions$Build <- rep(build, nrow(regions))
    
    if (nrow(regions) > 0) {
      # Write to the output file
      write.table(file=output_file, regions, quote=F, row.names=F, col.names=T, sep="\t")
    }
  } else if (mapRegion == "progenitor") {
    regions <- regions[order(regions[, 2], -regions[, 3]), -c(5)]
    colnames(regions) <- c("CHR", "START", "END", "REGULATORY_ELEMENT", "TF")
    regions$Build <- rep(build, nrow(regions))
    
    if (nrow(regions) > 0) {
      # Write to the output file
      write.table(file=output_file, regions, quote=F, row.names=F, col.names=T, sep="\t")
    }
  }
}

if (output_snp != "") {
	written <- FALSE
	# Write to the output file
	if (nrow(subdiagram) > 0) {
		subdiagram$DATASET <- rep("diagram", nrow(subdiagram))
		subdiagram$BUILD <- rep(build, nrow(subdiagram))
		write.table(file=output_snp, subdiagram, quote=F, row.names=F,
				col.names=ifelse(!written, TRUE, FALSE), sep="\t",
				append=written)
		written <- TRUE
	}
	if (nrow(submagic) > 0) {
		submagic$DATASET <- rep("magic", nrow(submagic))
		submagic$BUILD <- rep(build, nrow(submagic))
		write.table(file=output_snp, submagic, quote=F, row.names=F,
				col.names=ifelse(!written, TRUE, FALSE), sep="\t",
				append=written)
		written <- TRUE
	}
	if (nrow(sub_user_snp) > 0) {
		if (ncol(sub_user_snp) < 4) {sub_user_snp <- cbind(rep("-", nrow(sub_user_snp)), sub_user_snp)}
		sub_user_snp$DATASET <- rep("user", nrow(sub_user_snp))
		sub_user_snp$BUILD <- rep(build, nrow(sub_user_snp))
		write.table(file=output_snp, sub_user_snp, quote=F, row.names=F,
				col.names=ifelse(!written, TRUE, FALSE), sep="\t",
				append=written)
		written <- TRUE
	}
}

if (output_motifs != "") {
	if (nrow(motifs) > 0) {
		motifs$Build <- rep(build, nrow(motifs))
		write.table(file=output_motifs, cbind(seq(1, nrow(motifs)), motifs), quote=F, row.names=F, col.names=T, sep="\t")
    }
}

#################
# ENF OF SCRIPT #
#################
