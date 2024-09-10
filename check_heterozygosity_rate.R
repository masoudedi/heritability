args <- commandArgs(trailingOnly = TRUE)
input1 <- args[1] #file with  'R_check.het'
het <- read.table(paste(input1, "het", sep = "."), head=TRUE)
pdf(paste(input1, "pdf", sep = "."))
het$HET_RATE = (het$"N.NM." - het$"O.HOM.")/het$"N.NM."
hist(het$HET_RATE, xlab="Heterozygosity Rate", ylab="Frequency", main= "Heterozygosity Rate")
dev.off()
