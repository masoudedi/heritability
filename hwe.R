args <- commandArgs(trailingOnly = TRUE)
input1 <- args[1] #base file for missingness
hwe<-read.table (file=paste(input1, "hwe", sep = "."), header=TRUE)
pdf(paste(input1, "histhwe.pdf", sep = "."))
hist(hwe[,9],main="Histogram HWE")
dev.off()

hwe_zoom<-read.table (file=paste(input1, "plinkzoomhwe.hwe", sep = "."), header=TRUE)
pdf(paste(input1, "histhwe_below_theshold.pdf", sep = "."))
hist(hwe_zoom[,9],main="Histogram HWE: strongly deviating SNPs only")
dev.off()
