library(here)
library(dplyr)
library(tidyr)

clean_id_crosswalk <- function() {

  file <- "crosswalk.txt"

  crosswalk <- read.csv(here::here("raw_data", file))

  crosswalk %>%
    separate(paste(colnames(crosswalk)), into = c("id", "filename", "md5", "size", "state"), 
             extra = 'drop', sep = "\t", remove = TRUE) -> crosswalk
  
  return(crosswalk)
}

