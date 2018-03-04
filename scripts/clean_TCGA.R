library(here)
library(tidyr)
library(dplyr)
library(readr)

#Read in id to filename crosswalk
crosswalk <- read_delim(here::here("raw_data", "TCGA", "Manifest.txt"), delim = '\t')

#Select only the 6084 observations. Keep around the rest without ids. 
no_ids <- crosswalk[6085:6258,]
crosswalk <- crosswalk[1:6084,]

# Figure out what's going on relating all these file and folder names

files <- as.data.frame(crosswalk$filename)
colnames(files) <- 'V1'

# Each row in the Manifest.txt has a folder and then a filename. That filename is broken up into some strange 
# 'identifier' and then a suffix broken apart by three periods
files %>%
  separate('V1', into = c("folder", "filename"), sep = '/', extra = 'merge') %>%
  separate('filename', into = c('identifier', 'a', 'b', 'c'), sep = '\\.', extra = 'merge') -> sep_files

# Lets figure out if these are related somehow
length(unique(sep_files$folder)) 

length(unique(sep_files$identifier))
identifiers <- sep_files$identifier

# what do these things mean
unique(sep_files$a)
unique(sep_files$b)
unique(sep_files$c)

# Ultimately, looking at all of this, what are the actual files that we care about. It seems we probably 
# do not have 6048 observations. 



# CLEANING THE DATA, ALTHOUGHT ALL OF THIS WAS DONE NAIVELY BEFORE ANALYZING WHAT THE HELL ALL THE FILE
# NAMES WERE AND IS ALSO TOO SLOW

full_data <-data.frame('Gene'= 'filler')

#THIS IS TOO SLOW, SOMEHOW NEED TO VECTORIZE (LAPPLY)
for(i in crosswalk$filename[1:500]) {
  obv <- read_delim(here::here("raw_data", "TCGA", i), delim = '\t', col_names = c("Gene", "Expression"))
  full_data <- full_join(full_data, obv, 'Gene')
}


