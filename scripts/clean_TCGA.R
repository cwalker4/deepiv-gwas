library(here)
library(tidyr)
library(dplyr)
library(readr)

#Read in id to filename crosswalk
crosswalk <- read_delim(here::here("raw_data", "TCGA", "Manifest.txt"), delim = '\t')

#Select only the 6084 observations. Keep around the rest without ids. 
no_ids <- crosswalk[6085:6258,]
crosswalk <- crosswalk[1:6084,]

full_data <-data.frame('Gene'= 'filler')

#THIS IS TOO SLOW, SOMEHOW NEED TO VECTORIZE (LAPPLY)
for(i in crosswalk$filename[1:500]) {
  obv <- read_delim(here::here("raw_data", "TCGA", i), delim = '\t', col_names = c("Gene", "Expression"))
  full_data <- full_join(full_data, obv, 'Gene')
}


#get_all_unique_genes names
names <- NA
for(i in crosswalk$filename) {
  obv <- read_delim(here::here("raw_data", "TCGA", i), delim = '\t', col_names = c("Gene", "Expression"))
  names <- union(names, obv$Gene)
}

# Some of the files are formatted differently about halfway through and it messes everything up. So, we need to figure that out
# what you see below just grabs the relevant gene names. 

see_names <- as.data.frame(names)
gene_names <- as.data.frame(see_names[1:60484,])
see <- as.data.frame(full_data[,1])




