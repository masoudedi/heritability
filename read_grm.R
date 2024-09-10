ReadGRMBin <- function(prefix, AllN=F, size=4, output_file=NULL) {
  sum_i=function(i){
    return(sum(1:i))
  }
  BinFileName=paste(prefix,".grm.bin",sep="")
  NFileName=paste(prefix,".grm.N.bin",sep="")
  IDFileName=paste(prefix,".grm.id",sep="")
  id = read.table(IDFileName)
  n=dim(id)[1]
  BinFile=file(BinFileName, "rb")
  grm=readBin(BinFile, n=n*(n+1)/2, what=numeric(0), size=size)
  NFile=file(NFileName, "rb")
  if(AllN==T){
    N=readBin(NFile, n=n*(n+1)/2, what=numeric(0), size=size)
  } else {
    N=readBin(NFile, n=1, what=numeric(0), size=size)
  }
  i=sapply(1:n, sum_i)
  result <- list(diag=grm[i], off=grm[-i], id=id, N=N)
  
  if (!is.null(output_file)) {
    write.table(result, file=output_file, row.names=FALSE, col.names=TRUE, quote=FALSE, sep="\t")
  }
  
  return(result)
}

prefix <- "/home/edizadehm/02.tutorials/07.gcta/SCZ_Fam_data/SCZ_Fam_autosomes"
output_file <- "output.txt"
ReadGRMBin(prefix, output_file=output_file)
