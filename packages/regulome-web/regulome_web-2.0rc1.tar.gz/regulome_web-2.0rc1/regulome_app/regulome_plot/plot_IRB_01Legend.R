##########################
## plot_IRB_01Lengend.R ##
##########################
##-----------------------------------------------------------------------------------------------
## This script generates the legend drawn in plot_IRB_main.
##-----------------------------------------------------------------------------------------------

##-----------------------------------------------------------------------------------------------
## Set the margins and open plot
##-----------------------------------------------------------------------------------------------
par(oma=c(3, 5, 1, 5))
par(mar=c(1, 0, 0, 0))
par(bty = 'n')

plot(1, xlim=c(1, 10), ylim=c(1, 10), col='white', ylab="", yaxt='n', xaxt='n', xlab="", type='n')

##-----------------------------------------------------------------------------------------------
## Define variables depending on drawn dataset
##-----------------------------------------------------------------------------------------------
if (mapRegion == "adult") {
  legend <- c(levels(regRegions[,4]), "Enhancer Cluster", "TF-bound site", "Islet motif")
  col <- c(palette[1:length(levels(regRegions[,4]))], G3c, TFregions, "black")
  names(col)=legend
} else if (mapRegion == "adultStretch") {
  legend <- c(levels(regRegions[,4]), "Stretch Enhancers", "TF-bound site", "Islet motif")
  col <- c(palette[1:length(levels(regRegions[,4]))], G3c, TFregions, "black")
  names(col)=legend
} else {
  legend <- c(levels(regRegions[,4]), "TF-bound site", "islet motif")
  col <- c(palette[3], TFregions, "black")
  names(col)=legend
}

len <- length(legend)-2

# Points to draw/write
if (input_user_regions != "FALSE" & input_user_regions != FALSE & input_user_regions != "") {
  legend <- c(legend, "User region")
  col <- c(col, col_user_regions)
  ys_2 <- c(6, 2.5)
  ys_3 <- c(4.8)
} else {
  ys_2 <- c(4)
  ys_3 <- c(3.3)
}

if (len <= 3) {
  xs_1 <- c(1, 3.6, 6.2)
  ys_1 <- c(4)
} else if ((len > 3) & (len <=6)) {
  xs_1 <- c(1, 3.6, 6.2)
  ys_1 <- c(6, 2.5)
} else if ((len > 6) & (len <=9)) {
  xs_1 <- c(1, 3.6, 6.0)
  ys_1 <- c(6.5, 4, 1.5)
}

# Legend "Open chromatin class"
count=0
for (x in xs_1) {
  for (y in ys_1) {
    count=count+1
    if (mapRegion == "adult" | mapRegion == "adultStretch") {
      if (count < len) {
        rect(x, y, x + 0.18, y + 2, col=col[count])
      } else if (count == len) {
        lines(c(x - 0.05, x + 0.23), c(y+0.7, y+0.7), col=col[count], lwd=3)
      }
      text(x + 0.2, y + 0.7, labels=legend[count], pos=4, cex=1.5)
    } else {
      if (count <= len) {
        rect(x, y, x + 0.18, y + 2, col=col[count])
        text(x + 0.2, y + 0.7, labels=legend[count], pos=4, cex=1.5)
      }
    }
  }
}

# Legend "Other"
xs_2 <- c(8.5)
lines(c(xs_2 - 0.05, xs_2 + 0.23), c(ys_2[1] + 0.7, ys_2[1] + 0.7), col=col["TF-bound site"], lwd=3) #ys_2
text(xs_2 + 0.3, ys_2[1] + 0.7, labels="TF-bound site", pos=4, cex=1.5)

# lines(c(xs_2 - 0.05, xs_2 + 0.23), c(ys_2[2] + 0.7, ys_2[2] + 0.7), col=col["islet motif"], lwd=3)
# text(xs_2 + 0.3, ys_2[2] + 0.7, labels="islet motif", pos=4, cex=1.5)

if (input_user_regions != "FALSE" & input_user_regions != FALSE & input_user_regions != "") {
  rect(xs_2, ys_2[2], xs_2+0.18, ys_2[2]+2, col=col[length(col)])
  text(xs_2+0.3, ys_2[2]+0.7, labels=legend[length(legend)], pos=4, cex=1.5)
}
# Add the info icon
#points(9.9, ys_3, pch=1, cex=3)
#text(9.9, ys_3, labels="i", cex=1)

# Borders of the main figure
abline(h=par('usr')[3])
lines(rep(par('usr')[1], 2), par('usr')[3:4] - c(0, 0.1))
lines(rep(par('usr')[2], 2), par('usr')[3:4] - c(0, 0.1))
abline(h=par('usr')[4] - 0.1)

# Divide the legend in two parts
rect(8, 0, 8.15, 10.5, col='white', border='white')
lines(rep(8, 2), par('usr')[3:4] - c(0, 0.1))
lines(rep(8.15, 2), par('usr')[3:4] - c(0, 0.1))

# Title of the legend
if (mapRegion == "adult") {
  rect(2.9, 9.5, 6.1, 10.5, col='white', border='white')
  mtext(side=3, line=-0.7, text="Open Chromatin Class/Adult Islet", at=4.5, cex=1, font=2)
  rect(8.8, 9.5, 9.6, 10.5, col='white', border='white')
  mtext(side=3, line=-0.7, text="Other", at=9.2, cex=1, font=2)
} else if (mapRegion == "adultStretch") {
  rect(2.9, 9.5, 6.1, 10.5, col='white', border='white')
  mtext(side=3, line=-0.7, text="Chromatin State/Adult Islet", at=4.5, cex=1, font=2)
  rect(8.8, 9.5, 9.6, 10.5, col='white', border='white')
  mtext(side=3, line=-0.7, text="Other", at=9.2, cex=1, font=2)
} else if (mapRegion == "progenitor") {
  rect(2.5, 9.5, 6.5, 10.5, col='white', border='white')
  mtext(side=3, line=-0.7, text="Regulatory Element/Pancreatic Progenitor", at=4.5, cex=1, 
        font=2)
  rect(8.8, 9.5, 9.6, 10.5, col='white', border='white')
  mtext(side=3, line=-0.7, text="Other", at=9.2, cex=1, font=2)
}
