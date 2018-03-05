Folder for raw daw data (i.e. unfiltered, unprocessed; only what we download from the web)

- `gdc-client` -- added from https://gdc.cancer.gov/access-data/gdc-data-transfer-tool. GDCs tool to download large amounts of data from a manifest file 

- `get_gdc_data` -- downloads full data from manifest file and `gdc-client`

- `gdc_manifest.txt` -- manifest file to download data we want from gdc

- all GTEx data is found in the GTEx portal at https://www.gtexportal.org/home/datasets

- To get GTEx mRNA data download the `GTEx_Analysis_2016-01-15_v7_RSEMv1.2.22_transcript_expected_count.txt.gz` file labeled "Transcript TPMs" under the "RNA-Seq Data" section

- To get GTEx mutation data download the `GTEx_Analysis_2016-01-15_v7_WholeGenomeSeq_635Ind_PASS_AB02_GQ20_HETX_MISS15_PLINKQC.lookup_table.txt.gz` file labeled "Chromosome positions, REF and ALT alleles, RS IDs from dbSNP 147, and GTEx constructed IDs, for all variants in release V7." under the "Reference" section