library(here)
library(CePa)
library(tidyverse)
filepath <- here::here("raw_data", "GTEx", "All_Tissue_Site_Details.combined.reads.gct")
X <- read.gct(filepath)
gtex <- as.data.frame(X)

gtex %>%
  mutate(Gene = rownames(gtex)) -> gtex

write_csv(gtex, here::here("derived_data", "cleaned_gtex_mrna.csv"))