## gnucash import converter

Convert random .csv formats to allow importing invoice line items to Gnucash.  
This version works with export format for Hours Tracker Android App (cribasoft LLC) 
but it should be easy to customize to other .csv files. 

The *intended use case* is when you are invoicing a customer for hours worked. 

## How to use:

1)   Open your CSVexport.csv file in LibreOffice
2)   Edit out all rows that have already been invoiced
3)   Sort by clock_in time (should add time to descrip for sorting)
4)   run

> time_to_gnucash.py   CSVExport.csv   CUST_NUM   INV_NUM

    CUST_NUM:   gnucash customer ID
    INV_NUM:    number of existing invoice
    (leading zeros not required in numeric params)

This produces a new CSV file which gnucash can import
