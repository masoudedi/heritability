args <- commandArgs(trailingOnly = TRUE)
input1 <- args[1] #base file for missingness
indmiss<-read.table(file=paste(input1, "imiss", sep = "."), header=TRUE)
snpmiss<-read.table(file= paste(input1, "lmiss", sep = "."), header=TRUE)
# read data into R 
pdf(paste(input1, "histimiss.pdf", sep = ".")) #indicates pdf format and gives title to file
hist(indmiss[,6],main="Histogram individual missingness") #selects column 6, names header of file

pdf(paste(input1, "histlmiss.pdf", sep = ".")) 
hist(snpmiss[,5],main="Histogram SNP missingness")  
dev.off() # shuts down the current device
