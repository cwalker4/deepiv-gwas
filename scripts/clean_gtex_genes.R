library(here)
library(biomaRt)
library(tidyverse)
library(dplyr)

data <- read_csv(here::here("raw_data/gtex/raw_gtex_genes.csv"))

rs_hugo_cross <- read_csv(here::here("crosswalks/rsids_to_hugo.csv"))

data %>%
  merge(rs_hugo_cross, by = 'X1') %>%
  dplyr::select(-rs_id_dbSNP147_GRCh37p13.x, -rs_id_dbSNP147_GRCh37p13.y, -gene_id) %>%
  rename(hugo = gene_name) -> data_hugo

write_csv(data_hugo, here::here("derived_data", "cleaned_gtex_genes.csv"))


