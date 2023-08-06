############################
## plot_IRB_06PlotGenes.R ##
############################
##-----------------------------------------------------------------------------------------------
## This script draws the bottom plot in plot_IRB_main.R, which contains the ideograms for genes, 
## and a color scale of grey representing specificity of the gene to the adult islet.
##-----------------------------------------------------------------------------------------------

##-----------------------------------------------------------------------------------------------
## Open plot
##-----------------------------------------------------------------------------------------------
par(mar=c(0, 0, 0, 0))
plot(1, xlim=c(start - d, stop + d), ylim=c(0, 10), col='white', ylab="", yaxt='n', xaxt='n', xlab="", type='n')

##-----------------------------------------------------------------------------------------------
## Plot genes
##-----------------------------------------------------------------------------------------------
# Select and order the genes
genes <- genes[(genes$Start >= start & genes$Start <= stop) | 
                 (genes$Stop >= start & genes$Stop <= stop) | 
                 (genes$Start <= start & genes$Stop >= stop), ]

genes <- genes[order(genes$Start), ]

len_reg <- stop - start

# Min. space required to plot the strand of a gene
w <- len_reg / 50

occupancy <- matrix(-1, ncol=3, nrow=sum(genes$Type == "GENE"))
gene_count <- 0

if (nrow(genes) >= 1) {
  for (gene_name in unique(genes$Gene)) {
    for (numgene in 1:nrow(genes[genes$Gene == gene_name & genes$Type == "GENE", ])) {
      gene <- genes[genes$Gene == gene_name & genes$Type == "GENE", ][numgene, ]
      gene_count <- gene_count + 1
      
      # Characteristics of the gene
      gene_id <- gene[, 1]
      gene_strand <- gene[, 3]
      gene_start <- gene[, 4]
      gene_stop <- gene[, 5] 
      gene_middle <- mean(c(gene_start, gene_stop))
      gene_overlap <- gene[, 7]
      
      # Gene length
      gene_length <- gene_stop - gene_start
      
      # Color of the gene
      if (gene_id %in% spec_genes) {
        specificity <- GENE_SPEC
      } else {
        specificity <- GENE_UNSPEC
      }
      
      # Strand
      y <- c(8.5, 8, 7.5)
      if (gene_strand == "+") {
        x <- c(gene_start, gene_start + w / 2, gene_start)
      } else {
        x <- c(gene_stop, gene_stop - w / 2, gene_stop)
      }
      
      border <- specificity #'NA'
      
      # Draw the gene - First draws a line representing the introns
      lines(c(gene_start, gene_stop), rep(y[2], 2), col=border)
      
      # Draw the strand if the gene is big enough
      if (gene_length >= w / 2) {
        j <- floor(gene_length/(w)) - 1
        for (k in 0:j) {
          if (k < 0) next
          col <- border
          if (gene_strand == "+") {
            nx <- as.numeric(x) + w * k
          } else {
            nx <- as.numeric(x) - w * k
          }
          lines(nx, y, col=col)
        }
      }
      
      # Write the name of the gene 
      occ <- nchar(as.character(gene_id)) * w
      
      start_text <- as.integer(gene_middle - occ / 2)
      stop_text <- as.integer(gene_middle + occ / 2)
      
      # Check if the name of the gene will overlap with an already written gene's name
      traffic <- sum(start_text >= occupancy[, 1] & start_text <= occupancy[, 2]) + 
        sum(stop_text >= occupancy[, 1] & stop_text <= occupancy[, 2]) + 
        sum(start_text < occupancy[, 1] & stop_text > occupancy[, 2])
      
      if (traffic >= 2) {
        y <- 0
      } else {
        if (traffic == 1) {
          if (occupancy[(gene_count - 1), 3] == 4) {y <- 1} else {y <- 4}
        } else {
          y <- 4
        }
      }
      
      if (y > 0) {
        # Write the gene's name on the plot
        text(gene_middle, y, labels=c(as.character(gene_id)), cex=1.5, font=3)
        
        # Draw a dashed line from the gene to the text
        lines(rep(gene_middle, 2), c(y + 1, 7), lty=2, col="grey40")
      }
      
      # Update occupancy
      occupancy[gene_count, ] <- c(start_text, stop_text, y)
      
      # Now draw the exons
      cds <- genes[genes$Gene == gene_name & genes$Type == "EXON", ]
      rect(cds[, 4], rep(7, nrow(cds)), cds[, 5], rep(9, nrow(cds)), col=specificity, border=border)
    }
  }
}

##-----------------------------------------------------------------------------------------------
## lncRNA
##-----------------------------------------------------------------------------------------------
# Select and order the lncRNA
lncRNA <- lncRNA[(lncRNA[, 1] == chromosome & lncRNA[, 2] >= start & lncRNA[, 2] <= stop) |
                   (lncRNA[, 1] == chromosome & lncRNA[, 3] >= start & lncRNA[, 3] <= stop) | 
                   (lncRNA[, 1] == chromosome & lncRNA[, 2] <= start & lncRNA[, 3] >= stop), ]

lncRNA <- lncRNA[order(lncRNA[, 2]), ]

occupancy_tmp <- matrix(-1, ncol=3, nrow=nrow(lncRNA))
occupancy <- rbind(occupancy, occupancy_tmp)

# Pointer of the genes data in the occupancy matrix
mark <- sum(genes$Type == "GENE")

if (nrow(lncRNA) >= 1) {
  for (i in 1:nrow(lncRNA)) {
    line <- lncRNA[i, ]
    lncRNA_name <- as.character(as.matrix(line[4])) #paste("hincRNA", unlist(strsplit(as.matrix(line[4]), "_"))[2], sep="")
    lncRNA_start <- as.numeric(line[2])
    lncRNA_stop <- as.numeric(line[3])
    lncRNA_middle <- mean(c(lncRNA_start, lncRNA_stop))
    lncRNA_length <- lncRNA_stop - lncRNA_start
    strand <- line[5] 
    
    y <- c(8.5, 8, 7.5)
    if (strand == "+") {
      x <- c(lncRNA_start, lncRNA_start + w / 2, lncRNA_start)
    } else {
      x <- c(lncRNA_stop, lncRNA_stop - w / 2, lncRNA_stop)
    }
    
    # Draw the lncRNA
    rect(lncRNA_start, 7.5, lncRNA_stop, 8.5, col='black', border='black')
    
    # Draw the strand if the gene is big enough
    if (lncRNA_length >= w/2) {
      j <- as.integer(floor(lncRNA_length/w)) - 1
      for (k in 0:j) {
        if (strand == "+") {
          nx <- as.numeric(x) + w * k
        } else {
          nx <- as.numeric(x) - w * k
        }
        lines(nx, y, col='white')
      }
    }
    
    # Write the name of the gene 
    occ <- nchar(lncRNA_name) * w
    
    start_text <- as.integer(lncRNA_middle - occ / 2)
    stop_text <- as.integer(lncRNA_middle + occ / 2)
    
    # Check if the name of the lncRNA will overlap with an already written lncRNA's name
    traffic <- sum(start_text >= occupancy[, 1] & start_text <= occupancy[, 2]) + 
      sum(stop_text >= occupancy[, 1] & stop_text <= occupancy[, 2]) + 
      sum(start_text < occupancy[, 1] & stop_text > occupancy[, 2])
    if (traffic >= 2) {
      y <- 0
    } else {
      if (traffic == 1) {
        if (occupancy[(mark + i - 1), 3] == 4) {y <- 1} else {y <- 4}
      } else {
        y <- 4
      }
    }
    
    if (y > 0) {
      # Write the lncRNA's name on the plot
      text(lncRNA_middle, y, labels=c(lncRNA_name), cex=1.5)
      
      # Draw a dashed line from the gene to the text
      lines(rep(lncRNA_middle, 2), c(y + 1, 7.5), lty=2, col="grey40")
    }
    
    # Update occupancy
    occupancy[(mark + i),] <- c(start_text, stop_text, y)	
  }
}

# Axis
a <- axis(1, cex.axis=2, label=F)
rng <- a[length(a)] - a[1]

# Format the axis
if (rng / 1000000 >= 1) {
  div <- 1000000
  b <- "Mb"
} else if (rng / 1000000 < 1 & rng / 1000 >= 1) {
  div <- 1000
  b <- "Kb"
} else {
  div <- 1
  b <- "bp"
}
mtext(side=1, at=a, text=a/div, line=1.5, cex=1.3)
mtext(side=1, paste0("Position ", "(", b, ")"), line=4, cex=1.5)

# Borders of the main figure
abline(v=par('usr')[1:2])
abline(h=par('usr')[3])

# Close the image
dev.off()

