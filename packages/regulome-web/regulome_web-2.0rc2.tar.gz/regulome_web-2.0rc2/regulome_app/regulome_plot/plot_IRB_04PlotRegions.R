##############################
## plot_IRB_04PlotRegions.R ##
##############################
##-----------------------------------------------------------------------------------------------
## This script draws the middle plot in plot_IRB_main.R, which contains a chromosome ideogram
## with different type of regions colored, clusters, user regions and TF binding regions.
##-----------------------------------------------------------------------------------------------


##-----------------------------------------------------------------------------------------------
## Open plot
##-----------------------------------------------------------------------------------------------
par(mar=c(0, 0, 0, 0))
plot(1, xlim=c(start - d, stop + d), ylim=c(0, 1.4), col='white', ylab="", yaxt='n', xlab="", 
     xaxt='n', type='n')


##-----------------------------------------------------------------------------------------------
## Fill the locus with the cluster regions
##-----------------------------------------------------------------------------------------------
if (mapRegion == "adult" | mapRegion == "adultStretch") {
  if (nrow(cluster) > 0) {
    for (n in 1:nrow(cluster)) {
      line <- cluster[n,]
      # Define start and stop
      startPol = ifelse(line[2] >= start, line[2], start - d)
      stopPol = ifelse(line[3] <= stop, line[3], stop + d)
      y0 = 1.2
      y1 = 1.4
      polygon(c(startPol, stopPol, stopPol, startPol, startPol), c(y0, y0, y1, y1, y0), col=G3c, border=G3c)	
    }
  }
}


##-----------------------------------------------------------------------------------------------
## Fill the locus with the regulatory regions
##-----------------------------------------------------------------------------------------------
if (nrow(regions) > 0) {
  for (n in 1:nrow(regions)) {
    line <- regions[n, ]
    lineCol <- col[as.character(line[,4])]
    # Define start and stop
    startPol = ifelse(line[2] >= start, line[2], start - d)
    stopPol = ifelse(line[3] <= stop, line[3], stop + d)
    polygon(c(startPol, stopPol, stopPol, startPol, startPol), c(0.2, 0.2, 1.2, 1.2, 0.2), 
            col=lineCol, border=lineCol)
  }
}


##-----------------------------------------------------------------------------------------------
## Fill the locus with the USER regions
##-----------------------------------------------------------------------------------------------
if (input_user_regions != FALSE) {
  # Look if the "rda" file exist, otherwise read a text file and save the "rda" file
  if (file.exists(paste(input_user_regions, ".rda", sep=""))) {
    load(paste(input_user_regions, ".rda", sep=""))
  } else {
    user_regions <- read.delim(input_user_regions, sep="\t", header=FALSE,
                               stringsAsFactors=F)
    colnames(user_regions) <- c("CHR", "START", "END")
    save(file=paste(input_user_regions, ".rda", sep=""), user_regions)
  }
  
  sub_user_regions <- user_regions[user_regions$CHR == chromosome, ]
  sub_user_regions <- sub_user_regions[(sub_user_regions$START >= start & sub_user_regions$START <= stop) | 
                                         (sub_user_regions$START <= start & sub_user_regions$END >= stop) |
                                         (sub_user_regions$END >= start & sub_user_regions$END <= stop), ]
  
  if (nrow(sub_user_regions) > 0) {
    for (n in 1:nrow(sub_user_regions)) {
      line <- sub_user_regions[n, ]
      polygon(c(line[2], line[3], line[3], line[2], line[2]), c(0.2, 0.2, 1.2, 1.2, 0.2), col=col_user_regions, border=col_user_regions)
    }
  }
}


##-----------------------------------------------------------------------------------------------
## Fill the locus with the TF binding regions
##-----------------------------------------------------------------------------------------------
if (nrow(locus2) > 0) {
  for (n in 1:nrow(locus2)) {
    line <- locus2[n, ]
    # Define start and stop
    startPol = ifelse(line[2] >= start, line[2], start - d)
    stopPol = ifelse(line[3] <= stop, line[3], stop + d)
    y0 = 0
    y1 = 0.2
    polygon(c(startPol, stopPol, stopPol, startPol, startPol), c(y0, y0, y1, y1, y0), col=TFregions, border=TFregions)
  }
}

# Shape of the locus
polygon(c(start - d, stop + d, stop + d, start - d, start - d), c(0.2, 0.2, 1.2, 1.2, 0.2), border="black")


##-----------------------------------------------------------------------------------------------
## Borders of the main figure
##-----------------------------------------------------------------------------------------------
abline(v=par('usr')[1:2])
