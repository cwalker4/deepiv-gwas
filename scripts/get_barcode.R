library(httr)
library(jsonlite)
getBarcode <- function(uuid, legacy = TRUE){
  # Get manifest using the API
  uuid <- tolower(uuid)    
  baseURL <- ifelse(legacy,"https://gdc-api.nci.nih.gov/legacy/files/?","https://gdc-api.nci.nih.gov/files/?")
  options.pretty <- "pretty=true"
  options.expand <- "expand=cases.samples.portions.analytes.aliquots"
  options.field <- "fields=cases.samples.portions.analytes.aliquots.submitter_id"
  option.size <- paste0("size=",length(uuid))
  option.format <- paste0("format=JSON")
  options.filter <- paste0("filters=",
                           URLencode('{"op":"and","content":[{"op":"in","content":{"field":"files.file_id","value":['),
                           paste0('"',paste(uuid,collapse = '","')),
                           URLencode('"]}}]}'))
  
  url <- paste0(baseURL,paste(options.pretty, options.expand,option.size, 
                              options.filter, options.field,
                              option.format, sep = "&"))
  json  <- tryCatch(
    fromJSON(url, simplifyDataFrame = TRUE),
    error = function(e) {
      fromJSON(content(GET(url), as = "text", encoding = "UTF-8"), simplifyDataFrame = TRUE)
    }
  )
  df <- stack(unlist(json$data$hits))
  barcode <- df[grep("TCGA",df[,1]),1]
  df <- data.frame(uuid = uuid, barcode = barcode)
  return(df)
}
getBarcode("ffa5fff7-6301-4cd8-8e63-a4d8294d1b0e", legacy = TRUE)
getBarcode("D04B63DE-03BA-4A63-92CA-D8054C3E238C", legacy = TRUE)
getBarcode(c("D04B63DE-03BA-4A63-92CA-D8054C3E238C","ffa5fff7-6301-4cd8-8e63-a4d8294d1b0e"), legacy = TRUE)
