library(here)
library(tidyr)
library(dplyr)
library(readr)
library(maftools)
library(TCGAbiolinks)

#Read in id to filename crosswalk
crosswalk <- read_delim(here::here("raw_data", "gdc_manifest.txt"), delim = '\t')

#Select only the 6084 observations. Keep around the rest without ids. 
no_ids <- crosswalk[6085:6258,]
crosswalk <- crosswalk[1:6084,]

# Figure out what's going on relating all these file and folder names
# Each row in the Manifest.txt has a folder and then a filename. That filename is broken up into some strange 
# 'identifier' and then a suffix broken apart by three periods

files <- as.data.frame(crosswalk$filename)
colnames(files) <- 'V1'

crosswalk %>%
  separate('filename', into = c('identifier', 'a', 'b', 'c'), sep = '\\.', extra = 'merge') %>%
  select(-md5, -size, -state) -> sep_files

# files %>%
# #  separate('V1', into = c("folder", "filename"), sep = '/', extra = 'merge') %>%
#   separate('V1', into = c('identifier', 'a', 'b', 'c'), sep = '\\.', extra = 'merge') -> sep_files

# Lets figure out if these are related somehow
length(unique(sep_files$folder)) 
length(unique(sep_files$identifier))
identifiers <- sep_files$identifier

# what do these things mean
unique(sep_files$a)
unique(sep_files$b)
unique(sep_files$c)

# Ultimately, looking at all of this, what are the actual files that we care about. It seems we probably 
# do not have 6048 observations. 

#---------------------------------------------------#

# CLEANING THE mRNA expression DATA
sep_files %>%
  filter(a == "FPKM") -> mRNA_data_sep

length(unique(mRNA_data_sep$identifier))

mRNA_data_sep %>%
  mutate(filename = paste(identifier,a, b, c, sep = ".")) %>%
  select(folder, filename) -> mRNA_data

full_data <-data.frame('Gene'= 'filler')

#THIS IS TOO SLOW, SOMEHOW NEED TO VECTORIZE (LAPPLY)
for(i in 1:nrow(mRNA_data)) {
  obv <- read_delim(here::here("raw_data", "TCGA", as.character(mRNA_data[i,1]), as.character(mRNA_data[i,2])), delim = '\t', col_names = c("Gene", "Expression"))
  full_data <- full_join(full_data, obv, 'Gene')
  print(i)
}

full_data <- full_data[-1,]
colnames(full_data) <- c("Gene", 1:nrow(mRNA_data))

write_csv(full_data, here::here("derived_data", "cleaned_TCGA_mRNA.csv"))

# Cleaning the sequencing data

sep_files %>%
  filter(a == "BRCA") -> mut_data_sep

mut_data_sep %>%
  mutate(filename = paste(identifier,a, b, c, sep = ".")) %>%
  select(folder, filename) -> mut_data

print(mut_data_sep$b)

gene_varscan <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[1,1]), as.character(mut_data[1,2])))
gene_somaticsniper <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[2,1]), as.character(mut_data[2,2])))
gene_mutect <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[3,1]), as.character(mut_data[3,2])))
gene_muse <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[4,1]), as.character(mut_data[4,2])))

as.character(mut_data[i,1])

# UUID to TCGA BARCODE CROSSWALK
 
manifest=read.table(here::here("raw_data", "gdc_manifest.txt"),header = T)
manifest_length= nrow(manifest)
id= toString(sprintf('"%s"', manifest$id))

Part1= '{"filters":{"op":"in","content":{"field":"files.file_id","value":[ '

Part2= '] }},"format":"TSV","fields":"file_id,file_name,cases.submitter_id,cases.case_id,data_category,data_type,cases.samples.tumor_descriptor,cases.samples.tissue_type,cases.samples.sample_type,cases.samples.submitter_id,cases.samples.sample_id,cases.samples.portions.analytes.aliquots.aliquot_id,cases.samples.portions.analytes.aliquots.submitter_id","size":'

Part3= paste(shQuote(manifest_length),"}",sep="")

Sentence= paste(Part1,id,Part2,Part3, collapse=" ")

write.table(Sentence,here::here("derived_data", "Payload.txt"),quote=F,col.names=F,row.names=F)

require(httr)

files_endpt = "https://gdc-api.nci.nih.gov/files"

body = list("filters" = list("op" = "in", "content" = list('field'='files.file_id', 'value'='af5085c1-5b4e-4b88-9f5f-3c049cdd981f')), 'format' = 'TSV', 'fields'="file_id,file_name,cases.case_id,cases.submitter_id,cases.samples.sample_id,cases.samples.submitter_id,cases.samples.portions.analytes.aliquots.aliquot_id,cases.samples.portions.analytes.aliquots.submitter_id,cases.samples.sample_type,cases.samples.tissue_type,data_category,data_type", 'size' = 1)

r <- POST(url = files_endpt, body = body, encode = 'json')

content(r, 'parsed')

content(r)$cases_0_submitter_id

