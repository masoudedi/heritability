args <- commandArgs(trailingOnly = TRUE)
input1 <- args[1] #file with  'R_check.het'
het <- read.table(paste(input1, "het", sep = "."), head=TRUE)
het$HET_RATE = (het$"N.NM." - het$"O.HOM.")/het$"N.NM."
het_fail = subset(het, (het$HET_RATE < mean(het$HET_RATE)-3*sd(het$HET_RATE)) | (het$HET_RATE > mean(het$HET_RATE)+3*sd(het$HET_RATE)));
het_fail$HET_DST = (het_fail$HET_RATE-mean(het$HET_RATE))/sd(het$HET_RATE);
write.table(het_fail, paste(input1, "fail-het-qc.txt", sep = "."), row.names=FALSE)
