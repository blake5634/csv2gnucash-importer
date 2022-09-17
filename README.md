## gnucash import converter

Convert random .csv formats to allow importing invoice line items to Gnucash.  
This version works with export format for Hours Tracker Android App (cribasoft LLC) 
but it should be easy to customize to other .csv files. 

The *intended use case* is when you are invoicing a customer for hours worked.

## How to use:

1)   Open your CSVexport.csv file in LibreOffice

2)   If the csv export contains old work that is already in an invoice (from previous month for example),
make a note of the first 'valid' date you want to import.

3)   run

> time_to_gnucash.py   TestData2022.csv   CUST_NUM   INV_NUM

    CUST_NUM:   gnucash customer ID
    INV_NUM:    number of existing invoice
    (leading zeros not required in numeric params, they will be added because GC demands them)

You will be asked for date of the earliest record you want to use.   Enter 'x' for all records.

This produces a new CSV file which gnucash can import
