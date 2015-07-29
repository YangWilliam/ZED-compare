# ZED-compare
Differentially methylated regions locator pipeline for Zea Epigenomics Database (ZED)

# Dependencies

All depdencies should be included with the default installation of python

The pipeline was tested on Python 2.7.6

# Usage
```
zed-compare.py -a -b -o [-cgr] [-cgc] [-chgr] [-chgc] [-chhr] [-chhc]

-a    This is a file that contains the methylation ratios
-b    Same file format as the first file that you want compare
-o    Name for the output (Do not include extension)


The pipeline read the file line by line with the information divided by tabs (\t)
The pipeline requires the input file to have the following format:
- Chromosome name at the first block
- Start location on the second block
- End location on the third block

optional arguments:
    These arguments will only be used if the input file is in a different format
    than the output (.tab) from the ZED-align pipeline
    -cgr   the location where the information for the methylation ratio of CG is at
    -cgc   the location where the information for the methylation count of CG is at
    -chgr  the location where the information for the methylation ratio of CHG is at
    -chgc  the location where the information for the methylation count of CHG is at
    -chhr  the location where the information for the methylation ratio of CHH is at
    -chhc  the location where the information for the methylation count of CHH is at



```



# Output

- Sample_CG.bed
- Sample_CHG.bed
- Sample_CHH.bed

