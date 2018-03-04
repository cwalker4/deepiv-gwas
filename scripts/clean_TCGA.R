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



# CLEANING THE DATA
sep_files %>%
  filter(a == "FPKM") -> mRNA_data_sep

length(unique(mRNA_data_sep$identifier))


mRNA_data_sep %>%
  mutate(filename = paste(identifier,a, b, c, sep = ".")) %>%
  select(folder, filename) -> mRNA_data

         
full_data <-data.frame('Gene'= 'filler')

#THIS IS TOO SLOW, SOMEHOW NEED TO VECTORIZE (LAPPLY)
for(i in 1:nrow(mRNA_data)) {
  obv <- read_delim(here::here("raw_data", "TCGA", as.character(mRNA_data[i,1]), as.character(mRNA_data[i,2])), delim = '\t', col_names = c("Gene", "Expression"), progress = FALSE)
  full_data <- full_join(full_data, obv, 'Gene')
  print(i)
}

full_data <- full_data[-1,]
colnames(full_data) <- c("Gene", 1:nrow(mRNA_data))

write_csv(full_data, here::here("derived_data", "cleaned_TCGA_mRNA.csv"))

