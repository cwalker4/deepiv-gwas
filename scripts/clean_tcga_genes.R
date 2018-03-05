library(here)
library(tidyverse)
library(maftools)
library(TCGAbiolinks)

read_csv(here::here("derived_data/manifest_parsed.csv")) %>%
  filter(type == "BRCA") %>%
  mutate(filename = paste(filename, type, ext_a, ext_b, sep = ".")) %>%
  select(folder, filename) -> mut_data

gene_varscan <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[1,1]), as.character(mut_data[1,2])))
gene_somaticsniper <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[2,1]), as.character(mut_data[2,2])))
gene_mutect <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[3,1]), as.character(mut_data[3,2])))
gene_muse <- read.maf(here::here("raw_data", "TCGA", as.character(mut_data[4,1]), as.character(mut_data[4,2])))

# Prioritize: mutect, somaticsniper, muse, varscan
parse_barcode <- function(barcode_data) {
  barcode_data %>%
    separate('barcode', into = c('project', 'tss', 'participant', 'sample', 'portion', 'plate', 'center'), 
             sep = '-', extra = 'merge') %>%
    mutate(tcid = paste(participant, sample, sep = '_')) %>%
    select(-project, -tss, -participant, -sample, -portion, -plate, -center) -> parsed_barcode
  return(parsed_barcode)
}

read_csv(here::here("derived_data", "gdc_uuids.txt"), col_names = TRUE) %>%
  parse_barcode() -> uuid_tcid

gene_mutect@data %>%
  select(hugo = Hugo_Symbol, barcode = Tumor_Sample_Barcode) %>%
  parse_barcode() %>%
  inner_join(uuid_tcid, by = "tcid") -> mutect_data

#=============
# BILLYS TEST CODE
#=============

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


