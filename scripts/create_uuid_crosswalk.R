library(here)
library(tidyr)
library(dplyr)
library(readr)
library(maftools)
library(TCGAbiolinks)

read_csv(here::here('derived_data/manifest_parsed.csv')) %>%
  filter(type == "FPKM") %>%
  select(uuid = folder) -> uuids 

get_barcode <- function(x) {
  return(as.character(getBarcode(print(x), legacy = FALSE)[,2]))
}

uuids$barcode <- sapply(as.character(uuids$uuid), get_barcode, USE.NAMES = FALSE)
write_csv(uuids, here::here("derived_data/gdc_uuids.txt"), col_names = TRUE)