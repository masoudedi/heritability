args <- commandArgs(trailingOnly = TRUE)
input1 <- args[1] #base file for MAF
maf_freq <- read.table(paste(input1, "frq", sep = "."), header =TRUE, as.is=T)
pdf(paste(input1, "distribution.pdf", sep = "."))
hist(maf_freq[,5],main = "MAF distribution", xlab = "MAF")
dev.off()


