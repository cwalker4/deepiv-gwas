library(here)
library(biomaRt)
library(tidyverse)
library(dplyr)


data <- read_csv(here::here("derived_data", "cleaned_gtex_genes.csv"))

rs_hugo_cross <- read_csv(here::here("crosswalks", "rsids_to_hugo.csv"))


data %>%
  select(-rs_id_dbSNP147_GRCh37p13) %>%
  summarise_all(sum) -> sums

gtex_ids <- as.data.frame(colnames(data))

as.data.frame(gtex_ids[3:11690,]) -> gtex_ids

as.data.frame(unique(data$rs_id_dbSNP147_GRCh37p13)) -> rs_ids

what <- listMarts()

ensembl = useMart("ensembl", dataset="hsapiens_gene_ensembl")
snp = useMart("ENSEMBL_MART_SNP", dataset = "hsapiens_snp")
listDatasets(snp)

listAttributes(ensembl)

getENSG <- function(rs = rs_ids[2,1], mart = snp) {
  results <- getBM(attributes = c("refsnp_id", "ensembl_gene_stable_id"),
                   filters    = "snp_filter", values = rs, mart = mart)
  return(results)
}


# default parameters
test <- as.data.frame(getENSG())
getENSG(rs = "rs224550") -> test


rs_id_cross <- read_csv(here::here("derived_data", "reference_gene_table.csv"))

rs_id_cross %>%
  

SNPgeneMapTEST.snp<-getBM(attributes=c("refsnp_id", "chr_name", "chrom_start", "ensembl_gene_stable_id", "associated_gene"), 
                            
                            filters=c("snp_filter", "chr_name", "chrom_start", "chrom_end"),
                            
                            values=as.list(rs_id_cross[1:10000,c('rsID', 'chr', 'startBP', 'endBP')]), mart=snp)

# user  system elapsed 

test %>%
  select(ensembl_gene_stable_id) -> ensembl_id


hgnc <- getBM(attributes=c('ensembl_gene_id','ensembl_transcript_id','hgnc_symbol','hgnc_id'),filters = 'ensembl_gene_id', values = ensembl_id[3,], mart = ensembl)



vars(starts_with(test, "E")) -> what

# or supply rs ID
getENSG(rs = "rs224550") -> test


## hgnc_gene_symbols.txt is the file that has the list of gene symbols one per line.
genes <- read.table("~/hgnc_gene_symbols.txt")



getHGNC2ENSG = getBM(attributes=c('chromosome_name', 'start_position', 'end_position', 'strand', 'ensembl_gene_id', 'hgnc_symbol', 'refseq_mrna'),  filters ='hgnc_symbol', values = genes, mart = ensembl)

write.table(getHGNC2ENSG, file="~/hgnc_gene_symbols.txt.ensg.coord.tsv", sep="\t", col.names=T, row.names=T, append = F, quote=FALSE)

getRSid4ENSG <- getBM(c('refsnp_id', 'allele', 'snp', 'chr_name', 'chrom_start', 'chrom_strand', 'associated_gene', 'ensembl_gene_stable_id', 'synonym_name', 'consequence_type_tv'), filters = 'ensembl_gene',  values = genes, mart = dbsnp)

write.table(getRSid4ENSG, file="~/hgnc_gene_symbols.txt.ensg.RSid.coord.tsv", sep="\t", col.names=T, row.names=T, append = F, quote=FALSE)
