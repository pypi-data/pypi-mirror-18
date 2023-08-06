####################################
## plot_IRB_03SNPmotifOpenChrom.R ##
####################################
##-----------------------------------------------------------------------------------------------
## This script draws the top plot in plot_IRB_main.R, which contains: SNPs (magic and/or diagram),
## motifs (if region <1kb) and open chromatin densities.
##-----------------------------------------------------------------------------------------------

#################################################################################################
## FUNCTIONS TO BE CALLED LATER
##-----------------------------------------------------------------------------------------------
PlotSideLegend <- function(range.p, max.pos, size.pos, real_y, user=FALSE) {
##-----------------------------------------------------------------------------------------------
  
  PlotBlock <- function(x, y) {
    points(x.pos.r2, range.p - x, pch=22, cex=4, bg=y, col=y)
  }
  
  WriteText <- function(step, label) {
    text(x.pos.r2, range.p - step, labels=label, pos=1)
  }
  
  step.y <- range.p / 25
  step.ry <- real_y / 25
  x.pos.r2 <- max.pos - (size.pos * 0.005)
  
  range.steps <- step.y * 11:1
  if (user == FALSE) {hsvs <- snp_colors} else {hsvs <- user_snp_colors}
  mapply(PlotBlock, range.steps, hsvs)
  
  text.steps <- step.y * c(0, 5, 10.3, 12)
  # Put real_y to rescale
  labels <- c(as.character(round(y, 1)), as.character(round(y / 2, 1)), "0", "pvalue\n-log10")
  mapply(WriteText, text.steps, labels)
}

##-----------------------------------------------------------------------------------------------
PlotSnp <- function(y, x, real_y, user=FALSE) {
##-----------------------------------------------------------------------------------------------
  # use y instead of real_y to get the same scale in all the datasets
  range.steps <- seq(0, y, y / 10)
  range.steps[11] <- y
  if (user == FALSE) {hsvs <- snp_colors} else {hsvs <- user_snp_colors}
  i <- as.numeric(cut(-log10(x$PVAL), range.steps))
  points(x$POS, -log10(x$PVAL), pch=21, cex=1, bg=hsvs[i], col=hsvs[ifelse(i > 5, i, 5)], lwd=0.5)
}

##-----------------------------------------------------------------------------------------------
parseSnps <- function(snps, y_snps, y, start, stop, d, label="", user=FALSE) {
##-----------------------------------------------------------------------------------------------
  if (nrow(snps) > 0) {
    # Snps
    tmp <- PlotSnp(y, snps, y_snps, user=user)
    
    # Side legend
    if (user==TRUE) {
      tmp <- PlotSideLegend(y, start - d, (stop - start + d + d), y_snps, user=TRUE)
      axis(2, cex.axis=1.5) 
      mtext(side=2, text=label, cex=1.5, line=3)
    } else {
      tmp <- PlotSideLegend(y, stop + d, (stop - start + d + d), y_snps, user=FALSE)
      axis(4, cex.axis=1.5)
      mtext(side=4, text=label, cex=1.5, line=3) #,col=snp_colors[length(snp_colors)]
    }
    
    # Best snp. check if the column SNP exists
    if ("SNP" %in% colnames(snps)) { #ncol(snps) > 3) 
      best.snp <- snps[order(snps$PVAL), ][1, ]
      if (best.snp$POS <= (start + stop) / 2) { pos = 4 } else { pos = 2 }
      text(best.snp$POS, -log10(best.snp$PVAL), labels=as.character(best.snp$SNP), pos=pos, cex=1.2)
    }
  }
}

##-----------------------------------------------------------------------------------------------
plot_motifs <- function(motifs, start, stop, p="lines") {
##-----------------------------------------------------------------------------------------------
  let <- strsplit(as.character(motifs[, 5]), "")     # Nucleotides of the motifs
  ll <- unlist(lapply(let, length))   # Length of the motifs
  cb <- cbind(motifs[, 2], ll)         # Position and length of the motifs
  ncb <- c()
  for (n in 1:nrow(cb)) { ncb <- c(ncb, seq(cb[n, 1], (cb[n, 1] - 1 + cb[n, 2]))) }
  max_overlap <- max(table(ncb)) * 2  # Temp
  # Matrix of bases x max_overlap
  matmot <- matrix(0, nrow=(stop - start) + 10, ncol=max_overlap)
  index = 1
  motifs_count = 1
  
  for (n in 1:nrow(cb)) {
    # Coordinates in bp
    X = seq(cb[n, 1], (cb[n, 1] - 1 + cb[n, 2]))
    
    # Coordinates of the matmot
    Xcords <- X - min(ncb) + 1
    
    # Decide which index to use
    for (i in max_overlap:1) {
      if (max(matmot[Xcords, i]) == 0) { index <- i }
    }
    
    # Look if the previous base is occuped
    if (min(Xcords) > 1) {
      if (matmot[min(Xcords) - 1, index] == 1) { index <- index + 1 }
    }
    
    # Update matrix
    matmot[(X - min(ncb) + 1), index] <- 1
    
    # Write the motif
    if (p == "lines") {
      lines(x=c(min(X), max(X)), y=rep(ytext[index], 2), lwd=2)
    } else {
      text(x=X, y=ytext[index], labels=unlist(let[[n]]), cex=1)
    }
    
    # Add an index
    text(x=mean(X), y=ytext[index], labels=motifs_count, cex=0.7, pos=3)
    
    # Add a point upsteam the motifs
    motifs_count <- motifs_count + 1  
  }
}

#################################################################################################
## CODE FOR DRAWING THE PLOT
##-----------------------------------------------------------------------------------------------
## Draw SNPs
##-----------------------------------------------------------------------------------------------
par(mar=c(0, 0, 0, 0))

y_user <- 1
y_diagram <- 1
y_magic <- 1
subdiagram <- matrix(numeric(0), 0, 0)
submagic <- matrix(numeric(0), 0, 0)
sub_user_snp <- matrix(numeric(0), 0, 0)

# User data
if (input_user_snps != FALSE) {
  # Look if the "rda" file exist, otherwise read a text file and save the "rda" file
#  if (file.exists(paste(input_user_snps, ".rda", sep=""))) {
#    load(paste(input_user_snps, ".rda", sep=""))
#  } else {
    user_snp <- read.delim(input_user_snps, sep="\t", header=T, stringsAsFactors=F)
#    colnames(user_snp) <- c("CHR", "POS", "PVAL", "NAME")
#    save(file=paste(input_user_snps, ".rda", sep=""), user_snp)
#  }
  
  sub_user_snp <- user_snp[user_snp$CHR == chromosome & user_snp$POS >= start & user_snp$POS <= stop, ]
  if (nrow(sub_user_snp) > 0) { y_user <- max(-log10(sub_user_snp$PVAL)) }
}

# Diagram data
if (plot_diagram == TRUE) {
  subdiagram <- diagram[diagram$CHR == chromosome & diagram$POS >= start & diagram$POS <= stop, ]
  if (nrow(subdiagram) > 0) { y_diagram <- max(-log10(subdiagram$PVAL)) }
}

# Magic data
if (plot_magic == TRUE) {
  submagic <- magic[magic$CHR == chromosome & magic$POS >= start & magic$POS <= stop, ]
  if (nrow(submagic) > 0) { y_magic <- max(-log10(submagic$PVAL)) }
}

# Absolute higher y-value
y <- ceiling(max(y_diagram, y_user, y_magic))

# Plot data
if (nrow(subdiagram) > 0 | nrow(submagic) > 0 | nrow(sub_user_snp) > 0) {
  # Open plot
  plot(1, xlim=c(start - d, stop + d), ylim=c(0, y), col='white', ylab="", yaxt='n', xlab="", xaxt='n', type='n')
  
  # Diagram
  if (nrow(subdiagram) > 0) {parseSnps(subdiagram, y_diagram, y, start, stop, d, label="Diagram", user=FALSE);}
  
  # Magic
  if (nrow(submagic) > 0) {
    if (nrow(subdiagram) > 0) { user=TRUE } else { user=FALSE }
    parseSnps(submagic, y_magic, y, start, stop, d, label="Magic", user=user)
  }
  
  # User
  if (nrow(sub_user_snp) > 0 & mapChrom == FALSE) {
    if (nrow(subdiagram) > 0 | nrow(submagic) > 0) { user=TRUE } else { user=FALSE }
    parseSnps(sub_user_snp, y_magic, y, start, stop, d, label="User dataset", user=user)
  } else {
    if (nrow(subdiagram) > 0 | nrow(submagic) > 0) { user=TRUE } else { user=FALSE }
    parseSnps(sub_user_snp, y_magic, y, start, stop, d, label="", user=user)
  }
  
} else {
  # Open plot
  plot(1, xlim=c(start - d, stop + d), ylim=c(0, 1), col='white', ylab="", yaxt='n', xlab="", xaxt='n', type='n')
}

##-----------------------------------------------------------------------------------------------
## Plot motifs if the plot <= 1kb long
##-----------------------------------------------------------------------------------------------
if ((stop - start) <= 1000) { 
  # Load the motifs file
  motifs <- paste(base_name, separator, motifs, sep=build)
  load(file=motifs)
  motifs <- motifs[motifs[, 1] == chromosome & motifs[, 2] >= start & motifs[, 2] <= stop, ]
  motifs <- motifs[order(motifs[, 2]), ] 
  # y measure for the motifs
  ytext <- seq(0, y, y / 10)
  yt2 = y / 23
  if (nrow(motifs) > 0) {
    # 100bp
    if (((stop - start) <= 100)) { plot_motifs(motifs=motifs, start=start, stop=stop, p="characters") }
    # 100bp - 1000bp
    if (((stop - start) <= 1000) & ((stop - start) > 100)) { 
      plot_motifs(motifs=motifs, start=start, stop=stop, p="lines") 
    }
  }
} else {
  output_motifs = ""
}

# Borders of the main figure
abline(v=par('usr')[1:2])

##-----------------------------------------------------------------------------------------------
## Open chromatin plot
##-----------------------------------------------------------------------------------------------
if (mapChrom != FALSE) {
  region <- GenomicRanges::GRanges(seqnames=chromosome,
                    ranges=IRanges::IRanges(start, stop)
                    )

  ## Only one bedgraph
  # Define colors for the plot (transparency does not work if you use color names directly)
  transparency = 0.5
  col1 = col2rgb("dark green")
  finalcolor1 = rgb(col1[1],col1[2],col1[3],alpha=transparency * 255, maxColorValue = 255)

  # Import tabix file
  tab <- Rsamtools::TabixFile(chromatin, paste0(chromatin, ".tbi"))
  regChromatin <- rtracklayer::import(tab, genome=build, which=region)
  df <- GenomicRanges::as.data.frame(regChromatin)[,c(1,2,3,6)]
  # df$score <- df$score*5/max(df$score)

  # Draw plot
  par(new=TRUE) # Draw in same plot, use new axis
  plot(1, xlim=c(start - d, stop + d), ylim=c(0,(max(df$score)+sd(df$score))), col='white', ylab="", yaxt='n', xlab="", xaxt='n', type='n')
  Sushi::plotBedgraph(df, chromosome, start, stop, overlay=T, color=finalcolor1, reescaleoverlay=T, ylim=c(0, (max(df$score+1))))

  lab <- round(seq(0, max(df$score)+sd(df$score), by=1),0) #by=((max(df$score)+sd(df$score))/5)), 0)
  axis(2, lab, cex.axis=1.3) #at=lab,
  mtext(side=2, text=paste0("Open chromatin/", mapChrom, " cell"), cex=1.4, line=3) #col=finalcolor1
}
# 
# 
# 
# ## With two bedgraphs
# # col2 = col2rgb("#E5001B")
# # finalcolor2 = rgb(col2[1],col2[2],col2[3],alpha=transparency * 255,maxColorValue = 255)
# # color <- c(finalcolor2, finalcolor1)
# 
# # cont=1
# # transp <- c(0.5, 1)
# # for (chro in chromatin) {
# #   tab <- TabixFile(chro, paste0(chro, ".tbi"))
# #   regChromatin <- import(tab, genome=build, which=region)
# #   df <- as.data.frame(regChromatin)[,c(1,2,3,6)]
# #   plotBedgraph(df, chromosome, start, stop, overlay=T, color=color[cont], transparency=transp[cont], reescaleoverlay=T, alpha=0.5)
# #   cont=cont+1
# # }
# # axis(4, cex.axis=1.3) 
# # mtext(side=4, text="Open chrom", cex=1.4, line=3)
