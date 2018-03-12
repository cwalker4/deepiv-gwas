library(here)
library(tidyverse)


tcga_genes <- read_csv(here::here("derived_data/cleaned_tcga_genes.csv"))
gtex_genes <- read_csv(here::here("derived_data/cleaned_gtex_genes.csv"))
tcga_mrna <- read_csv(here::here("derived_data/cleaned_tcga_mrna.csv"))
gtex_mrna <- read_csv(here::here("derived_data/cleaned_gtex_mrna.csv"))

# don't need info after the period
delete_extra_info <- function(data) {
  data %>%
    separate('Gene', into = c('mrna', 'version'), sep = '\\.', extra = 'merge') %>%
    select(-version) -> modified_data
  
  return(modified_data)
}

gtex_mrna <- delete_extra_info(gtex_mrna)
tcga_mrna <- delete_extra_info(tcga_mrna)

tcga_mrna %>%
  select(names(tcga_genes[,2:979]),  mrna) -> tcga_mrna

### Join on hugo to create our Z matrix
gtex_genes %>%
  inner_join(tcga_genes, by = 'hugo') %>%
  group_by(hugo) %>%
  summarize_all(sum) %>%
  select(-X1) -> genes

### Join on mrna (Ensemble ids) to create our P matrix

gtex_mrna %>%
  inner_join(tcga_mrna, by = 'mrna') -> mrna

write_csv(genes, here::here("derived_data", "gene_variants.csv"))
write_csv(mrna, here::here("derived_data", "expression_levels.csv"))

