library(here)

filename <- here::here("raw_data", "raw_TB_truth.csv")
raw_data <- read.csv(filename, header = FALSE)
raw_data <- raw_data[2:nrow(raw_data), 2:ncol(raw_data)]
colnames(raw_data) = as.character(unlist(raw_data[1, ]))
cleaned_data = raw_data[-1, ]   

write.csv(cleaned_data, here::here("derived_data", "cleaned_TB_truth.csv"))

