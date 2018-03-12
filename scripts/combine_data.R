library(here)
library(tidyverse)

tcga_genes <- read_csv(here::here("derived_data/cleaned_tcga_genes.csv"))
gtex_genes <- read_csv(here::here("derived_data/cleaned_gtex_genes.csv"))
tcga_mrna <- read_csv(here::here("derived_data/cleaned_tcga_mrna.csv"))
gtex_mrna <- read_csv(here::here("derived_data/cleaned_gtex_mrna.csv"))


gtex_genes %>%
  inner_join(tcga_genes, by = 'hugo') %>%
  group_by(hugo) %>%
  summarize_all(sum) -> genes











### Exploratory on hugo join
tcga_hugo <- as.data.frame(tcga_genes$hugo)
gtex_hugo <- as.data.frame(gtex_genes$hugo)

colnames(tcga_hugo) <- "hugo"
colnames(gtex_hugo) <- "hugo"

length(unique(gtex_hugo$hugo))

gtex_hugo %>%
  inner_join(tcga_hugo, by = 'hugo', copy = TRUE) -> matched_hugo

gtex_hugo %>%
  anti_join(tcga_hugo, by = 'hugo', copy = TRUE) -> unmatched_gtex

tcga_hugo %>%
  anti_join(gtex_hugo, by = 'hugo', copy = TRUE) -> unmatched_tcga

full_join(tcga_hugo, gtex_hugo, by = 'hugo')
