# install.packages("BiocManager")
# BiocManager::install("rhdf5")

library(rhdf5)

# more examples: https://www.bioconductor.org/packages/devel/bioc/vignettes/rhdf5/inst/doc/rhdf5.html

# list contents of h5 file
h5ls("create_sband_timeseries/data/parcels/belgium_extract.h5")

# read/get on of the data sets
h5read("create_sband_timeseries/data/parcels/belgium_extract.h5", 'belgium_extract/block0_values')

# doesn't look like R likes the data format --- it's likely pythonic