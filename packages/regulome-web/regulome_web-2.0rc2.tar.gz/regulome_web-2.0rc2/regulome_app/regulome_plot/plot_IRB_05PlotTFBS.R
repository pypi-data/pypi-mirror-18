###########################
## plot_IRB_05PlotTFBS.R ##
###########################
##-----------------------------------------------------------------------------------------------
## This script draws the bottom plot in plot_IRB_main.R, which contains the TF analyzed and 
## their connections and strength of binding to TFBS.
##-----------------------------------------------------------------------------------------------

#################################################################################################
## FUNCTIONS TO BE CALLED LATER
##-----------------------------------------------------------------------------------------------
draw_connections <- function(npoints) {                      
##-----------------------------------------------------------------------------------------------
  # Draw the TF circles
  for (n in npoints) {
    tf <- head[n]
    x <- intervals[n]
    points(x, 1, col='blue', bg="grey", pch=21, cex=12, lwd=3)
    text(x, 1, tf, cex=1)
  }
  
  # Now draw the lines, before the lighters and then the darkers
  for (j in 1:length(head)) {
    for (n in npoints) {
      tf <- head[n]
      x <- intervals[n]
      # Select those lines in locus that have the TF
      tmp <- locus2[which(locus2[, which(names(tfs) == tf)] == 1), ]
      if (nrow(tmp) == 0) { next }
      
      tf_binds <- c() #(tmp$Start + tmp$End)/2
      
      # Check every TF binding region
      for (z in 1:nrow(tmp)) {
        line <- tmp[z, ]
        # If the TF regions is bigger than the locus, take the mid point of the locus
        if ((line[2] <= start) & (line[3] >= stop)) { 
          tf_bind <- (start + stop) / 2 
        } else {
          # Middle point
          tf_bind <- (line[2] + line[3]) / 2
          if (length(tf_bind) == 0) { next }
          if (tf_bind > stop) {
            tf_bind <- ifelse((line[2] + stop) / 2 > start, (line[2] + stop) / 2, (start + stop) / 2)
          }
          if (tf_bind < start) {
            tf_bind <- ifelse((start + line[3]) / 2 < stop, (start + line[3]) / 2, (start + stop) / 2)
          }
        }
        tf_binds <- c(tf_binds, tf_bind)
      }
      if (length(tf_binds) == 0) { next }
      # Strength
      binding <- tmp$Binding
      if (length(binding) == 0) { next }
      # Points
      for (l in 1:length(tf_binds)) {
        if (j == binding[l]) {
          lines(c(x, tf_binds[l]), c(1.75, 4.2), col=binding_color[binding[l]])
        }
      }
    }
  }
}


#################################################################################################
## CODE FOR DRAWING THE PLOT
##-----------------------------------------------------------------------------------------------
## Open plot
##-----------------------------------------------------------------------------------------------
par(mar=c(0, 0, 0, 0))
plot(1, xlim=c(start - d, stop + d), ylim=c(0, 4), col='white', ylab="", yaxt='n', xaxt='n', xlab="", type='n')

##-----------------------------------------------------------------------------------------------
## Draw lines
##-----------------------------------------------------------------------------------------------
draw_connections(npoints=1:length(head))
mtext(side=2, text=paste0("TFBS/", mapTF, " islet"), cex=1.3, line=1)
abline(v=par('usr')[1:2])
