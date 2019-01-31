library(here)
library(CePa)
library(tidyverse)
filepath <- here::here("raw_data", "GTEx", "GTEx_Analysis_2016-01-15_v7_RNASeQCv1.1.8_gene_tpm.gct")
X <- read.gct(filepath)
gtex <- as.data.frame(X)

gtex %>%
  mutate(Gene = rownames(gtex)) -> gtex

write_csv(gtex, here::here("derived_data", "cleaned_gtex_mrna.csv"))