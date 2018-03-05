library(here)
library(tidyr)
library(dplyr)
library(readr)
library(maftools)
library(TCGAbiolinks)

source(here::here("scripts","get_barcode.R"))

#Read in id to filename crosswalk
crosswalk <- read_delim(here::here("raw_data/gdc_manifest.txt"), delim = '\t')

#Select only the 6084 observations. Keep around the rest without ids. 
no_ids <- crosswalk[6085:6258,]
crosswalk <- crosswalk[1:6084,]

# Each row in the Manifest.txt has a folder and then a filename. That filename is broken up into some strange 
# 'identifier' and then a suffix broken apart by three periods

files <- as.data.frame(crosswalk$filename)
colnames(files) <- 'V1'

crosswalk %>%
  separate('filename', into = c('identifier', 'a', 'b', 'c'), sep = '\\.', extra = 'merge') %>%
  select(-md5, -size, -state) -> sep_files

#=================
# Loading and cleaning the mRNA expression data
#=================
sep_files %>%
  filter(a == "FPKM") -> mRNA_data_sep

# rebuilding filename from separate columns
mRNA_data_sep %>%
  mutate(filename = paste(identifier,a, b, c, sep = ".")) %>%
  select(folder = id, filename) -> mRNA_data

mRNA_data_sep %>%
  select(folder = id, filename = identifier) -> mRNA_data_sep

# unpacking and joining TCGA data (takes a little while)
get_expression <- function(x) {
  folder <- as.character(x[1])
  filename <- as.character(x[2])
  obv <- read_delim(here::here("raw_data/TCGA", folder, filename),
                    delim = '\t',
                    col_names = c("Gene", folder))
  return(obv)
}

full_data <- do.call(cbind, apply(mRNA_data, MARGIN = 1, get_expression))
full_data <- full_data[, !duplicated(colnames(full_data))] # dropping duplicate "Gene" columns
write_csv(full_data, here::here("derived_data", "cleaned_TCGA_mRNA.csv"))

#=================
# Cleaning the sequencing data
#=================

sep_files %>%
  filter(a == "BRCA") -> mut_data_sep

mut_data_sep %>%
  mutate(filename = paste(identifier,a, b, c, sep = ".")) %>%
  select(folder, filename) -> mut_data

gene_varscan <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[1,1]), as.character(mut_data[1,2])))
gene_somaticsniper <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[2,1]), as.character(mut_data[2,2])))
gene_mutect <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[3,1]), as.character(mut_data[3,2])))
gene_muse <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[4,1]), as.character(mut_data[4,2])))


#=================
# UUID to TCGA BARCODE CROSSWALK
#=================

UUIDS <- as.data.frame(mRNA_data_sep$folder)
colnames(UUIDS) <- "UUID"

get_barcode <- function(x) {
  return(as.character(getBarcode(print(x), legacy = FALSE)[,2]))
}

UUIDS$barcode <- sapply(as.character(UUIDS$UUID), get_barcode, USE.NAMES = FALSE)
write_csv(UUIDS, here::here("derived_data", "gdc_uuids.txt"), col_names = TRUE)

# Priority: mutect, somaticsniper, muse, varscan

parse_barcode <- function(barcode_data) {
  barcode_data %>%
    separate('barcode', into = c('project', 'tss', 'participant', 'sample', 'portion', 'plate', 'center'), 
             sep = '-', extra = 'merge') %>%
    mutate(tcid = paste(participant, sample, sep = '_')) %>%
    select(-project, -tss, -participant, -sample, -portion, -plate, -center) -> parsed_barcode
  return(parsed_barcode)
}

uuid_tcid <- parse_barcode(uuid_to_barcode) 

mutect_data <- gene_mutect@data

mutect_data %>%
  select("hugo" = Hugo_Symbol, "barcode" = Tumor_Sample_Barcode) -> mutect_data

mutect_data <- parse_barcode(mutect_data)

mutect_data %>%
  inner_join(uuid_tcid, by = "tcid") -> mutect_data


mutect_data[1:30,] -> test


test %>%
  spread(hugo, 1,fill = 0)-> what

mutect_data %>%
  spread(hugo, 1, fill = 0) -> what

mutect_data[26902:26904,] -> why

obv_mutect <- data.frame("barcode" = unique(mutect_data$Tumor_Sample_Barcode))
parse_obv_mutect <- parse_barcode(obv_mutect)
parse_uuid_to_barcode <- parse_barcode(uuid_to_barcode)

parse_obv_mutect %>%
  inner_join(parse_uuid_to_barcode, by = "participant") -> joined


