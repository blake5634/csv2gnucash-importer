#!/usr/bin/python3

import csv
import sys
import regex as re

ars = sys.argv

if len(ars) != 4:
    print('Usage time_to_gnucash.py  FILENAME  CUSTOMER_NUM  INV_NUM')
    print('Exampe:    >time_to_gnucash   G_Job.csv   21     127')
    print('     G_Job.csv matches export format for Hours Tracker Android App (cribasoft LLC)')
    print('       (numbers are gnucash customer and invoice numbers respectively')
    quit()
    
filename    = ars[1]
customerNUM = ars[2].zfill(6)
invoiceNUM  = ars[3].zfill(6)

filereader = csv.reader(open(filename,'r'))

#
#   This stuff is needed for output  (https://www.gnucash.org/docs/v4/C/gnucash-guide/busnss-imp-bills-invoices.html)
#   Required gnucash fields
fieldinfo = '''id - The invoice number. All lines must contain this or the line will be rejected.
    date_opened - Use the same date format as setup in Preferences. Today's date is inserted if this is blank.
    owner_id - ID number of the vendor or customer. All lines must contain this or the line will be rejected.
    billingid - Billing ID.
    notes - Invoice notes.
    date - The date of the item line. Can be left blank for todays date.
    desc - Description as per normal invoice or bill.
    action - For bills usually “ea”.
    account - Account to which the item is attributed.
    quantity - Quantity of each item. Must contain a value or the line will be rejected.
    price - Price of each item. Must contain a value or the line will be rejected.
    disc_type - Type of discount, either “%” or “TODO”, only applies to invoices. Some experimentation may be required here as may be currency dependent.
    disc_how - Only applies to invoices.
    discount - Amount of discount to be applied. only applies to invoices.
    taxable - Will tax be applied to the item? “yes” or blank.
    taxincluded - Is tax included in the item price? “yes” or blank.
    tax_table - Tax table to apply to item.
    date_posted - If posted, what date. Normally left blank for manual posting after editing the invoice. Use the same date format as setup in Preferences.
    due_date - Date payment is due. Use the same date format as setup in Preferences.
    account_posted - Posted to what account.
    memo_posted - If posted insert memo here.
    accu_splits - Accumulate splits? “yes” or blank.
''' 
fieldinfo = fieldinfo.splitlines()
fieldnames = []
fielddefs = []
nfields = 0
for i,f in enumerate(fieldinfo):
    a = f.split('-')
    fieldnames.append(a[0].strip())
    fielddefs.append( a[1].strip())
    nfields += 1
##########    end of output fields work


#
#    Read input data
#
next(filereader)   # skip header

#
# Job,Clocked In,Clocked Out,Duration,Hourly Rate,Earnings,Comment,Tags,Breaks,Adjustments,Mileage
#


FIRSTROWFLAG = True
nrows = 0
for r in filereader: 
    nrows += 1
    job = r[0]     ##   customize for different input file formats
    tIn = r[1]
    tOut = r[2]
    Dur = r[3]
    Rate = r[4]
    Desc = r[6]
    miles = r[9]
    if FIRSTROWFLAG:
        outfilename = job + '_Inv'+ str(invoiceNUM) + '.csv'    
        fd = open(outfilename,'w')   
        output = csv.writer(fd, delimiter=';',quotechar='"')
        FIRSTROWFLAG = False
    #for i in range(len(fieldnames)):
        #print('{:15} | {:}'.format(fieldnames[i],fielddefs[i]))
    fdict = {}
    for f in fieldnames:
        fdict[f] = ''

    # populate an output row
    datere = re.compile('(\d+/\d+/\d+)')
    entrydate = datere.search(tIn).group(1)
    #print('entrydate:  ',entrydate)
    fdict['date'] = entrydate
    fdict['action']    = 'hours'
    fdict['id']       = invoiceNUM
    fdict['owner_id'] = customerNUM   # beuss gilbert hack
    fdict['desc']     = Desc
    fdict['quantity'] = Dur
    fdict['price']    = Rate
    fdict['account']  = 'Income:Sales'
    

    row = []
    for n in fieldnames:
        row.append(fdict[n])
    #
    #    Write the output file 
    #
    output.writerow(row)
    
## Check for correct output ??
#for i,n in enumerate(fieldnames):
    #print('{:15} {:}'.format(n,fdict[n]))
    
print('{:} entries processed to output file: {:}'.format(nrows,outfilename))
fd.close()
    
