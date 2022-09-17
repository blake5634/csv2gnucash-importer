#!/usr/bin/python3

import csv
import datetime as dt
from dateutil import parser

import sys
import regex as re
''' A program to convert time record exports from phone-based time-keeper
to a format that can be  imported to Gnucash "import invoice" function.
Currently works with Android Hours Tracker App.

'''
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


#   get a date to screen out old entries from log file
ds = input('Please enter oldest record date ("x" for none):')
if ds == 'x':
    d_earliest = parser.parse('01-Jan-1900')
else:
    d_earliest = parser.parse(ds)

#
#    Read input data
#
next(filereader)   # skip header

#
# Job,Clocked In,Clocked Out,Duration,Hourly Rate,Earnings,Comment,Tags,Breaks,Adjustments,Mileage
#


FIRSTROWFLAG = True
nrows = 0

# information and debug:
#for i in range(len(fieldnames)):
#   print('{:15} | {:}'.format(fieldnames[i],fielddefs[i]))

# This field dictionary will hold each record
fdict = {}
# make at least an empty entry for each gnucash field
for f in fieldnames:
    fdict[f] = ''

# use this to parse dates
datere = re.compile('(\d+/\d+/\d+) (\d+:\d+ [A,P]M)')
prevdate = 'x'
serial = 0
for r in filereader: 
    nrows += 1
    job = r[0]     ##   customize here for different input file formats
    tIn = r[1]     # time in
    tOut = r[2]    # time out
    Dur = r[3]     # duration (hrs)
    Rate = r[4]    # $/hr
    Desc = r[6]    # description of work
    miles = r[9]   # auto miles driven

    # understand the date of this entry
    entrydate = datere.search(tIn).group(1)
    entrytime = datere.search(tIn).group(2)

    if parser.parse(entrydate) < d_earliest:
        continue  # ignore before starting date
    # we have to use this trick for filename generation because
    #  'job' title is not known prior to reading first row!
    if FIRSTROWFLAG:
        # set up an output .csv file
        outfilename = job + '_Inv'+ str(invoiceNUM) + '.csv'
        fd = open(outfilename,'w')
        output = csv.writer(fd, delimiter=';',quotechar='"')
        FIRSTROWFLAG = False


    # populate an output row
    #print('Debug: '+entrytime)

    #print('entrydate:  ',entrydate)
    fdict['date']     = entrydate
    fdict['action']   = 'hours'
    fdict['id']       = invoiceNUM
    fdict['owner_id'] = customerNUM
    # help gnucash sort multiple entries in single date
    description = ': ' + Desc
    fdict['desc'] = entrytime.rjust(8,'0') + description
    #if entrydate != prevdate:
        #serial = 0
        #fdict['desc']     = description
    #else:
        #fdict['desc']     = str(serial) + ' ' + description
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
    prevdate = entrydate
    
## Check for correct output ??
#for i,n in enumerate(fieldnames):
    #print('{:15} {:}'.format(n,fdict[n]))
    
print('{:} entries processed to output file: {:}'.format(nrows,outfilename))
fd.close()
    
