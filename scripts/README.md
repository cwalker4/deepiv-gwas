- `parse_manifest.R` -- separates `gdc_manifest.txt` into more useable format (directory path of sample, filename, extensions)

- `create_uuid_crosswalk.R` -- crosswalk between UUIDs and TCGA barcode

- `clean_gtex_mrna.R` -- processes and formats policy variable

- `clean_gtex_genes.R` -- processes and formats instrumental variables

- `get_barcode.R` -- added by @billyf. From https://support.bioconductor.org/p/89021/. Pulls from https://wiki.nci.nih.gov/display/TCGA/TCGA+Barcode+to+UUID+Web+Service+User%27s+Guide to map UUID to TCGA barcode
