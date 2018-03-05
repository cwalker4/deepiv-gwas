library(here)
library(dplyr)
library(readr)
library(tidyverse)
library(maftools)
library(BgeeDB)

gtex_filename <- "GTEx_Analysis_2016-01-15_v7_WholeGenomeSeq_635Ind_PASS_AB02_GQ20_HETX_MISS15_PLINKQC.lookup_table.txt"


hi <- data.table::fread(here::here("raw_data", "GTEx", gtex_filename), sep = "\t", stringsAsFactors = FALSE, verbose = FALSE, data.table = TRUE, showProgress = TRUE, header = TRUE)


bgee_rna <- Bgee$new(species = "Homo_sapiens", dataType = "rna_seq")
bgee_genes <- Bgee$new(species = "Homo_sapiens", dataType = "affymetrix")
