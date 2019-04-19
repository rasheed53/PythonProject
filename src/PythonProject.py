#
# Python Project (PythonProject.py)
#
#   Author(s): Scott Gillis, Maryam Zabadneh and Hashim Rasheed
#
#   ABC Bank has multiple data files with a consistent data format [Id, name, last, balance, acc type]
#   This program Summarize the following tasks - 
#   1. Summarizes how many total data files are in a data folder.
#   2. Summarizes how many total data records are in each data file.
#   3. Summarizes in each data file, customers first and last name who has a max and min balance
#   4. Summarizes in all the data files, customers first and last name who has a max and min balance
#   5. Summarizes how many total Savings and Checking accounts are there.
#   6. Summarizes how much total amount bank has in its Savings and Checking accounts
#   7. Summarizes all the outputs in 'Summary.txt' file and outputs to the screen.
#
#   Extra credit:
#   8. Merges all the data files (data1.csv, data2.csv, data3.csv) into 'account.txt' that contains
#      all the data records.
#
import os
import csv
import re
import datetime

#
# This function merges all the data files into a text file after cleaning the data -
# leading or trailing whitespaces
#
def mergeRecords(absfilelist):
    outputfile="C:\\data\\account.txt"
    outfile=None
    try:
        outfile=open(outputfile,"w")

        for file in absfilelist:
            datafile=open(file)
            next(datafile)
            for row in datafile:
                data=re.sub(r'\s+',"",row)
                outfile.write(data+"\n")

        # Close the file                
        outfile.close()
        
    except IOError:
        print("IOError: Unable to create/write file")
        
filelist=[]
absfilelist=[]
dirpath="C:\\Users\\Hashim\\Desktop\\PyProject\\abc_bank\\data"

for root, dirs, files in os.walk(dirpath):
    for filename in files:
        filelist.append(filename)
        absfilelist.append(dirpath+"\\"+filename)        

# Get time and date
#
now=datetime.datetime.now()

# Setup the Summary file
#
summaryfile="C:\\data\\summary.txt"
summaryout=open(summaryfile,"w")

dash="="*80
print(" Summary Report ".center(80,"="))
print("Date:", now.strftime("%Y-%m-%d"))
print("Time:", now.strftime("%H:%M"))
print("File name:",summaryfile)
print()
print(" Individual Data File Summary ".center(80,"*"))

# List number of files in a directory
#
print("Total number of Data files:",len(filelist))
print()

summaryout.write(" Summary Report ".center(80,"="))
summaryout.write("\n")
summaryout.write(("Date: "+ now.strftime("%Y-%m-%d")))
summaryout.write("\n")
summaryout.write("Time: "+ now.strftime("%H:%M"))
summaryout.write("\n")
summaryout.write("File name: "+summaryfile)
summaryout.write("\n\n")
summaryout.write(" Individual Data File Summary ".center(80,"*"))
summaryout.write("\n")
summaryout.write("Total number of Data files: "+str(len(filelist)))
summaryout.write("\n")

num_savings_acct=0
num_chk_acct=0
tot_amt_sav=0
tot_amt_chk=0
balance_bank=[]
for file in absfilelist:
    min_bal=0
    max_bax=0
    with open(file, 'r') as csvfile:
        readCSV = csv.reader(csvfile, skipinitialspace=True,delimiter=',',quoting=csv.QUOTE_NONE)

        # skip header [Id, name, last, balance, acc type]
        next(readCSV); 
        
        numrec=0
        balance_perfile=[]
        for row in readCSV:
            numrec+=1
            first_last=row[1]+" "+row[2]
            balance_perfile.append(((first_last),row[3]))
            balance_bank.append(((first_last),row[3]))

            if (row[4] == 'saving'):
                num_savings_acct+=1
                tot_amt_sav+=int(row[3])
            elif (row[4] == 'checking'):
                num_chk_acct+=1
                tot_amt_chk+=int(row[3])
            else:
                print("Error: invalid acct_type")
                break
            
        # lambda function returns the total from a given col    
        # find the min balance and create a list [first and last name,balance] of
        # minimum balance for multiple owners within each data file
        min_bal=min(balance_perfile, key=lambda col: int(col[1]))
        min_bal_list=[val for val in balance_perfile if (val[1]==min_bal[1]) ] 
   
        # lambda function returns the total from a given col    
        # find the max balance and create a list [first and last name,balance] of
        # maximum balance for multiple owners within each data file
        max_bal=max(balance_perfile, key=lambda col: int(col[1]))
        max_bal_list=[val for val in balance_perfile if (val[1]==max_bal[1]) ] 

        print("Data file:", file)
        print("\tTotal # of records:",numrec)
        print("\tOwner(s) of account who has the minimum balance:")
        for name in min_bal_list:
            print("\t\t",name[0].title())
            
        print("\tOwner(s) of account who has the maximum balance:")
        for name in max_bal_list:
            print("\t\t",name[0].title())
        
        print()

        summaryout.write("Data file: "+ file)
        summaryout.write("\n")
        summaryout.write("\tTotal # of records: "+str(numrec))
        summaryout.write("\n")
        summaryout.write("\tOwner(s) of account who has the minimum balance:")
        for name in min_bal_list:
            summaryout.write("\n\t\t"+name[0].title())
        summaryout.write("\n")
        summaryout.write("\tOwner(s) of account who has the maximum balance:")
        for name in max_bal_list:
            summaryout.write("\n\t\t"+name[0].title())
        summaryout.write("\n\n")

# lambda function returns the total from a given col    
# find the min balance and create a list [first and last name,balance] of
# minimum balance for multiple owners across multiple data files
min_bal=min(balance_bank, key=lambda col: int(col[1]))
min_bal_list=[val for val in balance_bank if (val[1]==min_bal[1]) ] 

# Print/output the summary report
print(" ABC Bank Summary ".center(80,"*"))
print("\tOwner(s) of account who has the minimum balance:")
for name in min_bal_list:
    print("\t\t",name[0].title())

# lambda function returns the total from a given col    
# find the max balance and create a list [first and last name,balance] of
# maximum balance for multiple owners across multiple data files
max_bal=max(balance_bank, key=lambda col: int(col[1]))
max_bal_list=[val for val in balance_bank if (val[1]==max_bal[1]) ]
        
print("\tOwner(s) of account who has the maximum balance:")
for name in max_bal_list:
    print("\t\t",name[0].title())
            
print("\tTotal number of Savings account(s): ",num_savings_acct)
print("\tTotal number of Checking account(s):", num_chk_acct)
print("\tTotal amount in Savings account: ", '${:,}'.format(tot_amt_sav))
print("\tTotal amount in Checking account: ", '${:,}'.format(tot_amt_chk))
print(dash)

summaryout.write(" ABC Bank Summary ".center(80,"*"))
summaryout.write("\n")
summaryout.write("\tOwner(s) of account who has the minimum balance:")
for name in min_bal_list:
    summaryout.write("\n\t\t"+name[0].title())
    
summaryout.write("\n")
summaryout.write("\tOwner(s) of account who has the maximum balance:")
for name in max_bal_list:
    summaryout.write("\n\t\t"+name[0].title())
    
summaryout.write("\n\n")
summaryout.write("\tTotal number of Savings account(s): "+str(num_savings_acct))
summaryout.write("\n")
summaryout.write("\tTotal number of Checking account(s):"+str(num_chk_acct))
summaryout.write("\n")
summaryout.write("\tTotal amount in Savings account: "+str('${:,}'.format(tot_amt_sav)))
summaryout.write("\n")
summaryout.write("\tTotal amount in Checking account: "+str('${:,}'.format(tot_amt_chk)))
summaryout.write("\n")
summaryout.write(dash)

# Merge all the records
mergeRecords(absfilelist)

# Close the file
summaryout.close()


