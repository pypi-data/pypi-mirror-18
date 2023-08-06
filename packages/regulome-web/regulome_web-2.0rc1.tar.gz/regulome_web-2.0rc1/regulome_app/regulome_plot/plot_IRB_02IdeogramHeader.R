#################################
## plot_IRB_02IdeogramHeader.R ##
#################################
##-----------------------------------------------------------------------------------------------
## This script generates the ideogram of the chromosome in the header of the plot and all the
## information of the length of the region and genome build used.
##-----------------------------------------------------------------------------------------------

##-----------------------------------------------------------------------------------------------
## Open plot
##-----------------------------------------------------------------------------------------------
par(mar=c(0, 0, 0, 0))
par(bty = 'n')

plot(1, xlim=c(start - d, stop + d), ylim=c(0, 2.5), col='white', ylab="", yaxt='n', xlab="", 
     xaxt='n', type='n')
a <- signif((stop - start), 1) / 10 

##-----------------------------------------------------------------------------------------------
## Draw the length scale
##-----------------------------------------------------------------------------------------------
lines(c(start - d, start - d + a), c(0.4, 0.4), col="black")
lines(c(start - d, start - d), c(0.3, 0.5), col="black")
lines(c(start - d + a, start - d + a), c(0.3, 0.5), col="black")

# Set the scale
if (a >= 1000) { div <- 1000; b <- "Kb"} else { div <- 1; b <- "bp"}
if (a >= 1000000) { div <- 1000000; b <- "Mb"}

text(start - d + a / 2, 0.9, paste0(a/div, b), cex=2, col="black")

##-----------------------------------------------------------------------------------------------
## Add a map of the whole chromosome
##-----------------------------------------------------------------------------------------------
chstart <- start + (stop - start) * 0.1; chstop <- stop - (stop - start) * 0.1
rect(chstart, 0.4, chstop, 1) 
i <- ideogram[ideogram$chrom == chromosome,]
i$color <- karyotype_color_rgb[match(i$gieStain, karyotype_color_names)]
idelta = chstop - chstart
rect(chstart + i$chromStart / chromosome.length * idelta, 0.4, chstart + 
       i$chromEnd / chromosome.length * idelta, 1, col=i$color)

# Add the actual position in the chromosome
rect(chstart + start / chromosome.length * idelta, 0.2, chstart + 
       stop / chromosome.length * idelta, 1.2, col=NA, lty=1, border="red", lwd=2)

# Write the chromosome
text(start + (stop - start) / 2, 1.8, chromosome, cex=2, col="black", adj=0.5)

# Write the build
text(stop, 0.7, build, cex=2, col="black", adj=0.5)

##-----------------------------------------------------------------------------------------------
## Borders of the main figure
##-----------------------------------------------------------------------------------------------
abline(h=par('usr')[4])
abline(v=par('usr')[1:2])