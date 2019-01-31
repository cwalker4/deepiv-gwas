library(here)
library(tidyverse)

source(here::here("scripts/get_barcode.R"))

# Load id->filename crosswalk (manifest)
manifest <- read_delim(here::here("raw_data/gdc_manifest.txt"), delim = '\t')

# Select only the 6084 observations. Keep around the rest without ids. 
no_ids <- manifest[6085:6258,] #FIXME@billyf: why do we need this line?
manifest <- manifest[1:6084,]

# Each row in the manifest.txt has a folder and then a filename. That filename is broken up into an 
# identifier and then a suffix broken apart by three periods
manifest %>%
  separate('filename', into = c('identifier', 'type', 'ext_a', 'ext_b'), sep = '\\.', extra = 'merge') %>%
  select(folder = id, filename = identifier, type, ext_a, ext_b) -> mrna_data_sep

write_csv(mrna_data_sep, here::here("derived_data/manifest_parsed.csv"))
