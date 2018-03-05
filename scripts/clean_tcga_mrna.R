library(here)
library(tidyverse)

# loading parsed manifest, rebuilding filename from separate columns
read_csv(here::here('derived_data/manifest_parsed.csv')) %>%
  filter(type == "FPKM") %>%
  mutate(filename = paste(filename, type, ext_a, ext_b, sep = ".")) %>%
  select(folder, filename) -> mrna_data

# function to unpack and joining TCGA data (takes a little while)
get_expression <- function(x) {
  folder <- as.character(x[1])
  filename <- as.character(x[2])
  obv <- read_delim(here::here("raw_data/TCGA", folder, filename),
                    delim = '\t',
                    col_names = c("Gene", folder))
  return(obv)
}

full_data <- do.call(cbind, apply(mrna_data, MARGIN = 1, get_expression))
full_data <- full_data[, !duplicated(colnames(full_data))] # dropping duplicate "Gene" columns

write_csv(full_data, here::here("derived_data/cleaned_tcga_mrna.csv"))