import cx_Oracle
import csv
import os
import numpy as np
import pandas as pd
from datetime import datetime
import openpyxl 
from openpyxl import workbook,load_workbook
from openpyxl.styles import Font, Color, PatternFill, Border, Side,Alignment
import tkinter as tk
from tkinter import messagebox

Date = input("Please Enter Report Required Date (DDMMYYYY format):- ")
date_obj = datetime.strptime(Date, "%d%m%Y")

# Format the datetime object as required
formatted_date_str = date_obj.strftime("%d-%m-%Y")



ICLLD = fr'D:\Segragation\Segragation_prg -Test\COMMONLD\ICL_AABCA6832G_{Date}_01.csv'
MCXLD = fr'D:\Segragation\Segragation_prg -Test\COMMONLD\MCX_AABCA6832G_{Date}_01.csv'
NCDEXLD = fr'D:\Segragation\Segragation_prg -Test\COMMONLD\NCDEX_AABCA6832G_{Date}_01.csv'
EQM = fr'D:\Segragation\Segragation_prg -Test\MARGIN\EQ_MGTM_0313_{Date}.CSV'
FOM = fr'D:\Segragation\Segragation_prg -Test\MARGIN\MGTM_313_{Date[-4:]}{Date[2:4]}{Date[:2]}.csv'
CurrM = fr'D:\Segragation\Segragation_prg -Test\MARGIN\BFX_MGTM_0313_{Date}.csv'
MCXM = fr'D:\Segragation\Segragation_prg -Test\MARGIN\MCX_MARGIN_56565_{Date[-4:]}{Date[2:4]}{Date[:2]}.csv'
NCDEXM = fr'D:\Segragation\Segragation_prg -Test\MARGIN\01274_MGN_{Date}.csv'
UniqueCFC = fr'D:\Segragation\Segragation_prg -Test\MARGIN\Unique_CFC.csv'
UniqueMCX = fr'D:\Segragation\Segragation_prg -Test\MARGIN\Unique_MCX.csv'
UniqueNCDEX = fr'D:\Segragation\Segragation_prg -Test\MARGIN\Unique_NCDEX.csv'
Test = fr'D:\Segragation\Segragation_prg -Test\MARGIN\Test.csv'
ICLLDF = fr'D:\Segragation\Segragation_prg -Test\Output\ICL_AABCA6832G_{Date}_01F.csv'
MCXLDF = fr'D:\Segragation\Segragation_prg -Test\Output\MCX_AABCA6832G_{Date}_01F.csv'
NCDEXLDF = fr'D:\Segragation\Segragation_prg -Test\Output\NCDEX_AABCA6832G_{Date}_01F.csv'
RequiredData = fr'D:\Segragation\Segragation_prg -Test\Required_data.csv'



# Connection details
username = 'username'
password = 'Password'
host = 'ip'
port = 'port'
service_name = 'service_name'

# Construct connection string
dsn = cx_Oracle.makedsn(host, port, service_name=service_name)

# Establish connection
connection = cx_Oracle.connect(username, password, dsn)

# Test connection
cursor = connection.cursor()

# Execute the SQL query
cursor.execute(f"""Select a.oowncode as CLIENTCODE,a.FIRMNUMBER,a.BRCODE AS Branch_Code ,b.pangir as PAN_Number,a.ctermcode as Terminal_Code
from accounts  a , accountaddressdetail b where a.oowncode=b.oowncode and a.firmnumber='ACML-00001' and b.firmnumber='ACML-00001'  order by a.oowncode""")

# Fetch all rows
rows = cursor.fetchall()

# Convert the fetched data into a pandas DataFrame
df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

# Export DataFrame to a CSV file
df.to_csv(RequiredData, index=False)

# Close cursor and connection
cursor.close()
connection.close()



RequiredData_head= ['CLIENTCODE','FIRMNUMBER','BRANCH_CODE','PAN_NUMBER','TERMINAL_CODE']
RequiredData_Dtype= {'CLIENTCODE':str,'FIRMNUMBER':str,'BRANCH_CODE':str,'PAN_NUMBER':str,'TERMINAL_CODE':str}

RequiredData1= pd.read_csv(RequiredData,header=None,names=RequiredData_head,dtype=RequiredData_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)





def check_file(filepath):
    if not os.path.exists(filepath):
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("File Not Found", f"The file is not available at: {filepath}.\nPlease ensure the file is available at the specified path.")

for filepath in [ICLLD, MCXLD, NCDEXLD, EQM, FOM, CurrM, MCXM, NCDEXM]:
    check_file(filepath)


EQM_Head = ['Date','Code','Intial','Other','ELM','Peak','Adhock','Total Margin','Sym','Margin required','Peak Required']
EQM_Dtype = {'Date':str,'Code':str,'Intial':float,'Other':float,'ELM':float,'Peak':float,'Adhock':float,'Total Margin':float,'Sym':str,'Margin required':float,'Peak Required':float}

EQM1 = pd.read_csv(EQM, header=None, names=EQM_Head, dtype=EQM_Dtype,na_values=[' ', 'NA', 'N/A'])
EQM1.replace('OWN','', inplace=True)
#Segment_fo= 'FO'
FOM_Head = ['Date',	'Code',	'Intital',	'Excposre',	'E',	'Other',	'G',	'H',	'Peak',	'Total Margin',	'K']
FOM_Dtype = {'Date':str,'Code':str,	'Intital':float,	'Excposre':float,	'E':float,	'Other':float,	'G':float,	'H':float,	'Peak':float,	'Total Margin':float,	'K':str}

FOM1 = pd.read_csv(FOM, header=None, names=FOM_Head, dtype=FOM_Dtype,na_values=[' ', 'NA', 'N/A'])
FOM1.replace('OWN','', inplace=True)
#FOM1.to_csv(Test,index=False)


#Segment_CD= 'CD'

CurrM_Head = ['Date',	'Code',	'Intital',	'Excposre',	'Other',	'MTM',	'G',	'Peak',	'Total Margin',	'J']
CurrM_Dtype = {'Date':str,'Code':str,'Intital':float,'Excposre':float,'Other':float,	'MTM':float,	'G':float,'Peak':float,'Total Margin':float,'J':str}

CurrM1 = pd.read_csv(CurrM, header=None, names=CurrM_Head, dtype=CurrM_Dtype,na_values=[' ', 'NA', 'N/A'])
CurrM1.replace('OWN','', inplace=True)
#CurrM1.to_csv(Test,index=False)

MCXM_Head = ['Date','Member','Code','Initial','Other','M2M','G','H','I','J','K','L','M','N','O','P','Q','R','S']
MCXM_Dtype = {'Date':str,'Member':str,'Code':str,'Initial':float,'Other':float,'M2M':float,'G':float,'H':float,
              'I':float,'J':float,'K':float,'L':float,'M':float,'N':float,'O':float,'P':float,'Q':float,'R':float,'S':float}


MCXM1 = pd.read_csv(MCXM, names=MCXM_Head, dtype=MCXM_Dtype,na_values=[' ', 'NA', 'N/A'])
#MCXM1.to_csv(Test,index=False)
MCXM1.replace('OWN','', inplace=True)

NCDEX_dtype = {'Trade Date':str,	'Trading Member ID':str,	'Client ID':str,'Initial Mrgin (Initial + Extreme Loss)':float,	'Peak Initial Mrgin':float,	'Other Mrgns':float,
               	'MTM (Gain/Loss)':float,'Upfront initial Mrgn Collected':float,	'Peak Initial Mrgn Collected':float,	'Other Margins Collected by T+2':float,
               	'MTM (Gains)/ Loss Collected By T+2':float,	'Shortfall in Initial Mrgn':float,	'Shortfall in Peak Mrgn':float,
               	'Shortfall in Other Mrgn':float,'Shortfall in MTM (Gain)/Loss':float,'Initial Margin at Peak Short Allocation (IM-PSA)':float,
               	'Collateral Value at EOD':float,'Collateral Value at Peak Short Allocation (PSA)':float,
               	'Excess Collateral With Other CCs (ICCL)':float,'Excess Collateral With Other CCs (MCXCCL)':float,
               	'Excess Collateral With Other CCs (NCL)':float,'Excess Collateral With Other CCs (Others)':float,
               	'Delay In Processing Allocation Request':float,	'Trade In Wrong Client Code':float,	'Total Shortfall (EOD Short Allocation)':float,
               	'Total Shortfall (Peak Short Allocation)':float}
NCDEX_head = ['Trade Date',	'Trading Member ID','Client ID','Initial Mrgin (Initial + Extreme Loss)',
            'Peak Initial Mrgin','Other Mrgns','MTM (Gain/Loss)','Upfront initial Mrgn Collected','Peak Initial Mrgn Collected',
            'Other Margins Collected by T+2','MTM (Gains)/ Loss Collected By T+2','Shortfall in Initial Mrgn',
            'Shortfall in Peak Mrgn','Shortfall in Other Mrgn','Shortfall in MTM (Gain)/Loss',
            'Initial Margin at Peak Short Allocation (IM-PSA)','Collateral Value at EOD','Collateral Value at Peak Short Allocation (PSA)',
            'Excess Collateral With Other CCs (ICCL)','Excess Collateral With Other CCs (MCXCCL)',
            'Excess Collateral With Other CCs (NCL)','Excess Collateral With Other CCs (Others)',
            'Delay In Processing Allocation Request','Trade In Wrong Client Code','Total Shortfall (EOD Short Allocation)',
            'Total Shortfall (Peak Short Allocation)']

NCDEXM1 = pd.read_csv(NCDEXM, header=None, names=NCDEX_head, dtype=NCDEX_dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)
NCDEXM1['Client ID'] = NCDEXM1['Client ID'].str.replace("'", '')
NCDEXM1.replace('OWN','', inplace=True)

ICLLD_Head = ['Date','Clearing Member PAN','Trading member PAN','CP CODE','CP PAN','Client PAN','Account Type','Segment Indicator','UCC Code',
'Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP','Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP','Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',
'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs','Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs','Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs',
'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs','Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs','Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs',
'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs','Credit entry in ledger in lieu of EPI for clients / TM Pro','Pool Account for clients / TM Pro','Cash Retained by TM',
'Bank Guarantee (BG) Retained by TM','Fixed Deposit Receipt (FDR) Retained by TM','Approved Securities Cash Component Retained by TM',
'Approved Securities Non-cash component Retained by TM','Non-Approved Securities Retained by TM','Value of CC approved Commodities Retained by TM','Other Collaterals Retained by TM',
'Cash placed with CM','Bank Guarantee (BG) placed with CM','Fixed deposit receipt (FDR) placed with CM','Approved Securities Cash Component placed with CM','Approved Securities Non-cash component placed with CM',
'Non-Approved Securities placed with CM','Value of CC approved Commodities placed with CM','Other Collaterals placed with CM','Cash Retained with CM',
'Bank Guarantee (BG) retained with CM','Fixed deposit receipt (FDR) retained with CM','Approved Securities Cash Component retained with CM','Approved Securities Non-cash component retained with CM',
'Non-Approved Securities retained with CM','Value of CC approved Commodities retained with CM','Other Collaterals Retained with CM','Cash placed with ICL',
'Bank Guarantee (BG) placed with ICL','Fixed deposit receipt (FDR) placed with ICL','Approved Securities Cash Component placed with ICL','Approved Securities Non-Cash Component placed with ICL',
'Value of CC approved Commodities placed with ICL','MTF /Non MTF indicator','Uncleared Receipts','Govt Securities / T-bills received by TM from clients and by CM from TM(Pro) and from CPs',
'Govt Securities /T-bills Retained by TM','Govt Securities/T-bills placed with CM','Govt Securities/T bills retained with CM','Govt Securities/T bills placed with ICL',
'Bank Guarantee (BG) Funded portion retained with CM','Bank Guarantee (BG) Non funded portion retained with CM','Bank Guarantee (BG) Funded portion placed with ICL','Bank Guarantee (BG) Non funded portion placed with ICL',
'Settlement Amount','Unclaimed/Unsettled Client Funds','Cash Collateral for MTF positions']
ICLLD_Dtype= {'Date':str,'Clearing Member PAN':str,'Trading member PAN':str,'CP CODE':str,'CP PAN':str,'Client PAN':str,'Account Type':str,'Segment Indicator':str,
'UCC Code':str,'Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,
'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs':float,
'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs':float,'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs':float,'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs':float,'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Credit entry in ledger in lieu of EPI for clients / TM Pro':float,'Pool Account for clients / TM Pro':float,'Cash Retained by TM':float,
'Bank Guarantee (BG) Retained by TM':float,'Fixed Deposit Receipt (FDR) Retained by TM':float,'Approved Securities Cash Component Retained by TM':float,'Approved Securities Non-cash component Retained by TM':float,
'Non-Approved Securities Retained by TM':float,'Value of CC approved Commodities Retained by TM':float,'Other Collaterals Retained by TM':float,'Cash placed with CM':float,
'Bank Guarantee (BG) placed with CM':float,'Fixed deposit receipt (FDR) placed with CM':float,'Approved Securities Cash Component placed with CM':float,'Approved Securities Non-cash component placed with CM':float,
'Non-Approved Securities placed with CM':float,'Value of CC approved Commodities placed with CM':float,'Other Collaterals placed with CM':float,'Cash Retained with CM':float,
'Bank Guarantee (BG) retained with CM':float,'Fixed deposit receipt (FDR) retained with CM':float,'Approved Securities Cash Component retained with CM':float,'Approved Securities Non-cash component retained with CM':float,
'Non-Approved Securities retained with CM':float,'Value of CC approved Commodities retained with CM':float,'Other Collaterals Retained with CM':float,'Cash placed with ICL':float,
'Bank Guarantee (BG) placed with ICL':float,'Fixed deposit receipt (FDR) placed with ICL':float,'Approved Securities Cash Component placed with ICL':float,'Approved Securities Non-Cash Component placed with ICL':float,
'Value of CC approved Commodities placed with ICL':float,'MTF /Non MTF indicator':str,'Uncleared Receipts':float,'Govt Securities / T-bills received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Govt Securities /T-bills Retained by TM':float,'Govt Securities/T-bills placed with CM':float,'Govt Securities/T bills retained with CM':float,'Govt Securities/T bills placed with ICL':float,
'Bank Guarantee (BG) Funded portion retained with CM':float,'Bank Guarantee (BG) Non funded portion retained with CM':float,'Bank Guarantee (BG) Funded portion placed with ICL':float,
'Bank Guarantee (BG) Non funded portion placed with ICL':float,'Settlement Amount':float,'Unclaimed/Unsettled Client Funds':str,'Cash Collateral for MTF positions':float}

ICLLD1 = pd.read_csv(ICLLD, header=None, names=ICLLD_Head, dtype=ICLLD_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)
ICLLD1['CP CODE'] = None
ICLLD1['CP PAN'] = None
ICLLD1.replace('OWN','', inplace=True)

ICLLD3 = pd.read_csv(ICLLD, header=None, names=ICLLD_Head, dtype=ICLLD_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)
ICLLD3['CP CODE'] = None
ICLLD3['CP PAN'] = None
ICLLD3.replace('OWN','', inplace=True)



#ICLLD1.to_csv(Test,index=False)
EQM1['EQMU'] = 'CM' + '_' + EQM1['Code']   #CM_code
FOM1['FOMU'] = 'FO' + '_' + FOM1['Code']   #FO_code
CurrM1['CurrMU'] = 'CD' + '_' + CurrM1['Code']  #CD_code
ICLLD1['ICLLDU'] = ICLLD1['Segment Indicator'] + '_' + ICLLD1['UCC Code'] 
UniqueCodes = pd.concat([EQM1['EQMU'], FOM1['FOMU'], CurrM1['CurrMU']], ignore_index=True)
ICLLDU_set = set(ICLLD1['ICLLDU'])
UniqueCodess=set(UniqueCodes)
not_matched_values = UniqueCodess.difference(ICLLDU_set)
Not_Matched_ICL_split = [code.split('_') for code in not_matched_values]
Not_Matched_ICL_df = pd.DataFrame(Not_Matched_ICL_split, columns=['Segment Indicator','UCC Code'])
Not_Matched_ICL_list = [{'Segment Indicator': item[0], 'UCC Code': item[1]} for item in Not_Matched_ICL_split]
Not_Matched_ICL_df = pd.DataFrame(Not_Matched_ICL_list)
Not_Matched_ICL_df.reset_index(drop=True, inplace=True)



if Not_Matched_ICL_df.empty:
    ICLLD3.to_csv(ICLLDF,index=False)
else:
    dataICLLD = { 'Date': Date,'Clearing Member PAN': 'AABCA6832G','Trading member PAN': 'AABCA6832G','CP CODE': '','CP PAN': '',    'Client PAN': '',    'Account Type': 'C',
    'Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP': '0',    'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP': '0',    'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP': '0',    'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs': '0',    'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs': '0',    'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs': '0',    'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs': '0',    'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs': '0',    'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs': '0',    'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs': '0',
    'Credit entry in ledger in lieu of EPI for clients / TM Pro': '0',    'Pool Account for clients / TM Pro': '0',    'Cash Retained by TM': '0',    'Bank Guarantee (BG) Retained by TM': '0',    'Fixed Deposit Receipt (FDR) Retained by TM': '0',    'Approved Securities Cash Component Retained by TM': '0',    'Approved Securities Non-cash component Retained by TM': '0',    'Non-Approved Securities Retained by TM': '0',    'Value of CC approved Commodities Retained by TM': '0',    'Other Collaterals Retained by TM': '0',
    'Cash placed with CM': '0',    'Bank Guarantee (BG) placed with CM': '0',    'Fixed deposit receipt (FDR) placed with CM': '0',    'Approved Securities Cash Component placed with CM': '0',    'Approved Securities Non-cash component placed with CM': '0',    'Non-Approved Securities placed with CM': '0',    'Value of CC approved Commodities placed with CM': '0',    'Other Collaterals placed with CM': '0',    'Cash Retained with CM': '0',
    'Bank Guarantee (BG) retained with CM': '0',    'Fixed deposit receipt (FDR) retained with CM': '0',    'Approved Securities Cash Component retained with CM': '0',    'Approved Securities Non-cash component retained with CM': '0',    'Non-Approved Securities retained with CM': '0',    'Value of CC approved Commodities retained with CM': '0',    'Other Collaterals Retained with CM': '0',    'Cash placed with ICL': '0',    'Bank Guarantee (BG) placed with ICL': '0',
    'Fixed deposit receipt (FDR) placed with ICL': '0',    'Approved Securities Cash Component placed with ICL': '0',    'Approved Securities Non-Cash Component placed with ICL': '0',    'Value of CC approved Commodities placed with ICL': '0',    'MTF /Non MTF indicator': 'NA',    'Uncleared Receipts': '0',    'Govt Securities / T-bills received by TM from clients and by CM from TM(Pro) and from CPs': '0',    'Govt Securities /T-bills Retained by TM': '0',
    'Govt Securities/T-bills placed with CM': '0',    'Govt Securities/T bills retained with CM': '0',    'Govt Securities/T bills placed with ICL': '0',    'Bank Guarantee (BG) Funded portion retained with CM': '0',    'Bank Guarantee (BG) Non funded portion retained with CM': '0',    'Bank Guarantee (BG) Funded portion placed with ICL': '0',    'Bank Guarantee (BG) Non funded portion placed with ICL': '0',
    'Settlement Amount': '0',    'Unclaimed/Unsettled Client Funds': 'NA',    'Cash Collateral for MTF positions': '0'}
    dfICL = pd.DataFrame([dataICLLD])
    dfICL = pd.concat([dfICL[['Date','Clearing Member PAN','Trading member PAN','CP CODE','CP PAN','Client PAN','Account Type']],(Not_Matched_ICL_df),dfICL[['Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',    'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP','Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP','Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs','Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs',    'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs',    'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs',    'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs',    'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs',    'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs',
    'Credit entry in ledger in lieu of EPI for clients / TM Pro',    'Pool Account for clients / TM Pro',    'Cash Retained by TM',    'Bank Guarantee (BG) Retained by TM',    'Fixed Deposit Receipt (FDR) Retained by TM',    'Approved Securities Cash Component Retained by TM',    'Approved Securities Non-cash component Retained by TM',    'Non-Approved Securities Retained by TM',    'Value of CC approved Commodities Retained by TM',    'Other Collaterals Retained by TM',
    'Cash placed with CM',    'Bank Guarantee (BG) placed with CM',    'Fixed deposit receipt (FDR) placed with CM',    'Approved Securities Cash Component placed with CM',    'Approved Securities Non-cash component placed with CM',    'Non-Approved Securities placed with CM',    'Value of CC approved Commodities placed with CM',    'Other Collaterals placed with CM',    'Cash Retained with CM',
    'Bank Guarantee (BG) retained with CM',    'Fixed deposit receipt (FDR) retained with CM',    'Approved Securities Cash Component retained with CM',    'Approved Securities Non-cash component retained with CM',    'Non-Approved Securities retained with CM',    'Value of CC approved Commodities retained with CM',    'Other Collaterals Retained with CM',    'Cash placed with ICL',    'Bank Guarantee (BG) placed with ICL',
    'Fixed deposit receipt (FDR) placed with ICL',    'Approved Securities Cash Component placed with ICL',    'Approved Securities Non-Cash Component placed with ICL',    'Value of CC approved Commodities placed with ICL',    'MTF /Non MTF indicator',    'Uncleared Receipts',    'Govt Securities / T-bills received by TM from clients and by CM from TM(Pro) and from CPs',    'Govt Securities /T-bills Retained by TM',
    'Govt Securities/T-bills placed with CM',    'Govt Securities/T bills retained with CM',    'Govt Securities/T bills placed with ICL',    'Bank Guarantee (BG) Funded portion retained with CM',    'Bank Guarantee (BG) Non funded portion retained with CM',    'Bank Guarantee (BG) Funded portion placed with ICL',    'Bank Guarantee (BG) Non funded portion placed with ICL',
    'Settlement Amount',    'Unclaimed/Unsettled Client Funds',    'Cash Collateral for MTF positions']]],axis=1)

#print(dfICL.columns)
    dfICL = dfICL.astype(ICLLD_Dtype)
    dfICL.fillna(0,inplace=True)
    dfICL['CP CODE'] = None
    dfICL['Date'] = formatted_date_str
    dfICL['Clearing Member PAN'] = 'AABCA6832G'
    dfICL['Trading member PAN'] = 'AABCA6832G'
    dfICL['Account Type'] = 'C'
    dfICL['CP PAN'] = None
    dfICL['Client PAN'] = dfICL['UCC Code'].map(RequiredData1.set_index('TERMINAL_CODE')['PAN_NUMBER'])
    dfICL['Unclaimed/Unsettled Client Funds'] = 'NA'
    dfICL['MTF /Non MTF indicator'] = 'NA'

    #FinalICL = pd.concat([ICLLD1, dfICL], ignore_index=True)

    dfICL.to_csv(UniqueCFC,index=False)

    ICLLD2 = pd.read_csv(ICLLD, header=None, names=ICLLD_Head, dtype=ICLLD_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)
    ICLLD2['CP CODE'] = None
    ICLLD2['CP PAN'] = None
    ICLLD2.replace('OWN','', inplace=True)
    if ICLLD2['Unclaimed/Unsettled Client Funds'].isnull().any():
        # Replace NaN values with 'NA'
        ICLLD2['Unclaimed/Unsettled Client Funds'].fillna('NA', inplace=True)
    else:
        # If there are no NaN values, replace any empty strings with 'NA'
        ICLLD2['Unclaimed/Unsettled Client Funds'].replace('', 'NA', inplace=True)


    ICLOut=ICLLD2._append(dfICL,ignore_index=True)
    ICLOut.to_csv(ICLLDF,index=False)

print("ICLLD File Generated to Path")

#All Okay Till Here
###################################################################################################################################################################
MCXLD_Head= ['Date','Clearing Member PAN','Trading member PAN','CP Code','CP PAN','Client PAN','Account Type','Segment Indicator ','UCC Code',
'Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro)  and in the books of CM for CP','Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',
'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP','Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs',
'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs','Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs','Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs',
'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs','Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs',
'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs ','Credit entry in ledger in lieu of EPI for clients / TM Pro',
'Pool Account for clients / TM Pro','Cash Retained by TM','Bank Guarantee (BG) Retained by TM','Fixed Deposit Receipt (FDR) Retained by TM',
'Approved Securities Cash Component Retained by TM','Approved Securities Non-cash component Retained by TM','Non-Approved Securities Retained by TM',
'Value of CC approved Commodities Retained by TM','Other Collaterals Retained by TM','Cash placed with CM','Bank Guarantee (BG) placed with CM',
'Fixed deposit receipt (FDR) placed with CM','Approved Securities Cash Component placed with CM','Approved Securities Non-cash component placed with CM',
'Non-Approved Securities placed with CM','Value of CC approved Commodities placed with CM','Other Collaterals placed with CM',
'Cash Retained with CM','Bank Guarantee (BG) retained with CM ','Fixed deposit receipt (FDR) retained with CM','Approved Securities Cash Component retained with CM',
'Approved Securities Non-cash component retained with CM','Non-Approved Securities retained with CM','Value of CC approved Commodities retained with CM',
'Other Collaterals Retained with CM','Cash placed with MCXCCL','Bank Guarantee (BG) placed with MCXCCL','Fixed deposit receipt (FDR) placed with MCXCCL',
'Approved Securities Cash Component placed with MCXCCL','Approved Securities Non-cash component placed with MCXCCL','Value of CC approved Commodities placed with MCXCCL',
'MTF /Non MTF indicator','Uncleared Receipts','Govt Securities â€“ T bills received by TM from clients and by CM from TM(Pro) and from CPs',
'Govt Securities â€“ T-bills Retained by TM','Govt Securitiesâ€“T bills placed with CM','Govt Securitiesâ€“T bills retained with CM',
'Govt Securitiesâ€“T bills placed with NCL','Bank Guarantee (BG) Funded portion retained with CM','Bank Guarantee (BG) Non funded portion retained with CM',
'Bank Guarantee (BG) Funded portion placed with MCXCCL','Bank Guarantee (BG) Non funded portion placed with MCXCCL','Settlement Amount',
'Unclaimed/Unsettled Client Funds','Cash Collateral for MTF positions']
MCXLD_Dtype = {'Date':str,'Clearing Member PAN':str,'Trading member PAN':str,'CP Code':str,'CP PAN':str,'Client PAN':str,'Account Type':str,
'Segment Indicator ':str,'UCC Code':str,'Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro)  and in the books of CM for CP':float,
'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,
'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs':float,'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs':float,'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs':float,'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs ':float,'Credit entry in ledger in lieu of EPI for clients / TM Pro':float,
'Pool Account for clients / TM Pro':float,'Cash Retained by TM':float,'Bank Guarantee (BG) Retained by TM':float,'Fixed Deposit Receipt (FDR) Retained by TM':float,
'Approved Securities Cash Component Retained by TM':float,'Approved Securities Non-cash component Retained by TM':float,'Non-Approved Securities Retained by TM':float,
'Value of CC approved Commodities Retained by TM':float,'Other Collaterals Retained by TM':float,'Cash placed with CM':float,'Bank Guarantee (BG) placed with CM':float,
'Fixed deposit receipt (FDR) placed with CM':float,'Approved Securities Cash Component placed with CM':float,'Approved Securities Non-cash component placed with CM':float,
'Non-Approved Securities placed with CM':float,'Value of CC approved Commodities placed with CM':float,'Other Collaterals placed with CM':float,
'Cash Retained with CM':float,'Bank Guarantee (BG) retained with CM ':float,'Fixed deposit receipt (FDR) retained with CM':float,'Approved Securities Cash Component retained with CM':float,
'Approved Securities Non-cash component retained with CM':float,'Non-Approved Securities retained with CM':float,'Value of CC approved Commodities retained with CM':float,
'Other Collaterals Retained with CM':float,'Cash placed with MCXCCL':float,'Bank Guarantee (BG) placed with MCXCCL':float,'Fixed deposit receipt (FDR) placed with MCXCCL':float,
'Approved Securities Cash Component placed with MCXCCL':float,'Approved Securities Non-cash component placed with MCXCCL':float,'Value of CC approved Commodities placed with MCXCCL':float,
'MTF /Non MTF indicator':str,'Uncleared Receipts':float,'Govt Securities â€“ T bills received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Govt Securities â€“ T-bills Retained by TM':float,'Govt Securitiesâ€“T bills placed with CM':float,'Govt Securitiesâ€“T bills retained with CM':float,
'Govt Securitiesâ€“T bills placed with NCL':float,'Bank Guarantee (BG) Funded portion retained with CM':float,'Bank Guarantee (BG) Non funded portion retained with CM':float,
'Bank Guarantee (BG) Funded portion placed with MCXCCL':float,'Bank Guarantee (BG) Non funded portion placed with MCXCCL':float,
'Settlement Amount':float,'Unclaimed/Unsettled Client Funds':str,'Cash Collateral for MTF positions':float}

MCXLD1 = pd.read_csv(MCXLD, header=None, names=MCXLD_Head, dtype=MCXLD_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)
MCXLD1['CP Code'] = None
MCXLD1['CP PAN'] = None
MCXLD1.replace('OWN', '', inplace=True)

MCXLD3 = pd.read_csv(MCXLD, header=None, names=MCXLD_Head, dtype=MCXLD_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)
MCXLD3['CP Code'] = None
MCXLD3['CP PAN'] = None
MCXLD3.replace('OWN', '', inplace=True)
#############################--------------------------------------------------

MCXM1['MCXMU'] = 'CO' + '_' + MCXM1['Code']
MCXLD1['MCXLDU'] = MCXLD1['Segment Indicator '] + '_' + MCXLD1['UCC Code']
MCXMCode = set(MCXM1['MCXMU'])
MCXLDCode = set(MCXLD1['MCXLDU'])
#Not_Matched_MCX = MCXMCode - MCXLDCode
Not_Matched_MCX = MCXMCode.difference(MCXLDCode)
#print('Not_Matched_MCX',Not_Matched_MCX)

Not_Matched_MCX_split = [code.split('_') for code in Not_Matched_MCX]
Not_Matched_MCX_df = pd.DataFrame(Not_Matched_MCX_split, columns=['Segment Indicator ', 'UCC Code'])
Not_Matched_MCX_list = [{'Segment Indicator ': item[0], 'UCC Code': item[1]} for item in Not_Matched_MCX_split]
Not_Matched_MCX_df = pd.DataFrame(Not_Matched_MCX_list)
Not_Matched_MCX_df.reset_index(drop=True, inplace=True)

if Not_Matched_MCX_df.empty:
    MCXLD3.to_csv(MCXLDF,index=False)
else:
    DataMCXLD = {'Date':Date,'Clearing Member PAN':'AABCA6832G','Trading member PAN':'AABCA6832G','CP Code':'','CP PAN':'','Client PAN':'','Account Type':'C','Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro)  and in the books of CM for CP':'0',
    'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':'0',
    'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':'0',
'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs':'0',
'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs ':'0',
'Credit entry in ledger in lieu of EPI for clients / TM Pro':'0',
'Pool Account for clients / TM Pro':'0','Cash Retained by TM':'0','Bank Guarantee (BG) Retained by TM':'0','Fixed Deposit Receipt (FDR) Retained by TM':'0',
'Approved Securities Cash Component Retained by TM':'0','Approved Securities Non-cash component Retained by TM':'0','Non-Approved Securities Retained by TM':'0',
'Value of CC approved Commodities Retained by TM':'0','Other Collaterals Retained by TM':'0','Cash placed with CM':'0','Bank Guarantee (BG) placed with CM':'0',
'Fixed deposit receipt (FDR) placed with CM':'0','Approved Securities Cash Component placed with CM':'0','Approved Securities Non-cash component placed with CM':'0',
'Non-Approved Securities placed with CM':'0','Value of CC approved Commodities placed with CM':'0','Other Collaterals placed with CM':'0',
'Cash Retained with CM':'0','Bank Guarantee (BG) retained with CM ':'0','Fixed deposit receipt (FDR) retained with CM':'0',
'Approved Securities Cash Component retained with CM':'0','Approved Securities Non-cash component retained with CM':'0','Non-Approved Securities retained with CM':'0',
'Value of CC approved Commodities retained with CM':'0','Other Collaterals Retained with CM':'0','Cash placed with MCXCCL':'0',
'Bank Guarantee (BG) placed with MCXCCL':'0','Fixed deposit receipt (FDR) placed with MCXCCL':'0','Approved Securities Cash Component placed with MCXCCL':'0',
'Approved Securities Non-cash component placed with MCXCCL':'0','Value of CC approved Commodities placed with MCXCCL':'0','MTF /Non MTF indicator':'NA',
'Uncleared Receipts':'0','Govt Securities â€“ T bills received by TM from clients and by CM from TM(Pro) and from CPs':'0','Govt Securities â€“ T-bills Retained by TM':'0',
'Govt Securitiesâ€“T bills placed with CM':'0','Govt Securitiesâ€“T bills retained with CM':'0','Govt Securitiesâ€“T bills placed with NCL':'0','Bank Guarantee (BG) Funded portion retained with CM':'0',
'Bank Guarantee (BG) Non funded portion retained with CM':'0','Bank Guarantee (BG) Funded portion placed with MCXCCL':'0','Bank Guarantee (BG) Non funded portion placed with MCXCCL':'0',
'Settlement Amount':'0','Unclaimed/Unsettled Client Funds':'NA','Cash Collateral for MTF positions':'0'}
    dfMCX = pd.DataFrame([DataMCXLD])

    dfMCX = pd.concat([dfMCX[['Date', 'Clearing Member PAN', 'Trading member PAN', 'CP Code', 'CP PAN', 'Client PAN', 'Account Type']],(Not_Matched_MCX_df),dfMCX[['Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro)  and in the books of CM for CP','Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',                  'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',
'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs',                  'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs',                  'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs',
'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs',                  'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs',                  'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs',
'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs ',                  'Credit entry in ledger in lieu of EPI for clients / TM Pro',                  'Pool Account for clients / TM Pro',
'Cash Retained by TM',                  'Bank Guarantee (BG) Retained by TM',                  'Fixed Deposit Receipt (FDR) Retained by TM',                  'Approved Securities Cash Component Retained by TM',
'Approved Securities Non-cash component Retained by TM',                  'Non-Approved Securities Retained by TM',                  'Value of CC approved Commodities Retained by TM',                  'Other Collaterals Retained by TM',                  'Cash placed with CM',
'Bank Guarantee (BG) placed with CM',                  'Fixed deposit receipt (FDR) placed with CM',                  'Approved Securities Cash Component placed with CM',                  'Approved Securities Non-cash component placed with CM',                  'Non-Approved Securities placed with CM',                  'Value of CC approved Commodities placed with CM',                  'Other Collaterals placed with CM',
'Cash Retained with CM',                  'Bank Guarantee (BG) retained with CM ',                  'Fixed deposit receipt (FDR) retained with CM',                  'Approved Securities Cash Component retained with CM',                  'Approved Securities Non-cash component retained with CM',                  'Non-Approved Securities retained with CM',                  'Value of CC approved Commodities retained with CM',                  'Other Collaterals Retained with CM',
'Cash placed with MCXCCL',                  'Bank Guarantee (BG) placed with MCXCCL',                  'Fixed deposit receipt (FDR) placed with MCXCCL',                  'Approved Securities Cash Component placed with MCXCCL',                  'Approved Securities Non-cash component placed with MCXCCL',                  'Value of CC approved Commodities placed with MCXCCL',
'MTF /Non MTF indicator',                  'Uncleared Receipts',                  'Govt Securities â€“ T bills received by TM from clients and by CM from TM(Pro) and from CPs',                  'Govt Securities â€“ T-bills Retained by TM',                  'Govt Securitiesâ€“T bills placed with CM',                  'Govt Securitiesâ€“T bills retained with CM',                  'Govt Securitiesâ€“T bills placed with NCL',
'Bank Guarantee (BG) Funded portion retained with CM',                  'Bank Guarantee (BG) Non funded portion retained with CM',
'Bank Guarantee (BG) Funded portion placed with MCXCCL',                  'Bank Guarantee (BG) Non funded portion placed with MCXCCL',                  'Settlement Amount',
'Unclaimed/Unsettled Client Funds',                  'Cash Collateral for MTF positions']]],axis=1)
    dfMCX = dfMCX.astype(MCXLD_Dtype)
    dfMCX.fillna(0,inplace=True)
    dfMCX['CP Code'] = None
    dfMCX['Date'] = formatted_date_str
    dfMCX['Clearing Member PAN'] = 'AABCA6832G'
    dfMCX['Trading member PAN'] = 'AABCA6832G'
    dfMCX['Account Type'] = 'C'
    dfMCX['CP PAN'] = None
    dfMCX['Client PAN'] = dfMCX['UCC Code'].map(RequiredData1.set_index('TERMINAL_CODE')['PAN_NUMBER'])
    dfMCX['Unclaimed/Unsettled Client Funds'] = 'NA'
    dfMCX['MTF /Non MTF indicator'] = 'NA'

    MCXLD2 = pd.read_csv(MCXLD, header=None, names=MCXLD_Head, dtype=MCXLD_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)
    MCXLD2['CP Code'] = None
    MCXLD2['CP PAN'] = None
    MCXLD2.replace('OWN', '', inplace=True)

    if MCXLD2['Unclaimed/Unsettled Client Funds'].isnull().any():
        # Replace NaN values with 'NA'
        MCXLD2['Unclaimed/Unsettled Client Funds'].fillna('NA', inplace=True)
    else:
        # If there are no NaN values, replace any empty strings with 'NA'
        MCXLD2['Unclaimed/Unsettled Client Funds'].replace('', 'NA', inplace=True)
        dfMCX.to_csv(UniqueMCX,index=False)

    MCXOut=MCXLD2._append(dfMCX,ignore_index=True)
    MCXOut.to_csv(MCXLDF,index=False)

print("MCX File Generated to Path")


#############################--------------------------------------------------
NCDEXLD_Head=['Date','Clearing Member PAN','Trading member PAN','CP Code','CP PAN','Client PAN','Account Type','Segment Indicator',
'UCC CODE','Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro) and in the books of CM for CP',
'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',
'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',
'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs','Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs',
'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs','Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs',
'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs','Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs',
'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs','Credit entry in ledger in lieu of EPI for clients / TM Pro',
'Pool Account for clients / TM Pro','Cash Retained by TM','Bank Guarantee (BG) Retained by TM','Fixed Deposit Receipt (FDR) Retained by TM',
'Approved Securities Cash Component Retained by TM','Approved Securities Non-cash component Retained by TM','Non-Approved Securities Retained by TM',
'Value of CC approved Commodities Retained by TM','Other Collaterals Retained by TM','Cash placed with CM','Bank Guarantee (BG) placed with CM',
'Fixed deposit receipt (FDR) placed with CM','Approved Securities Cash Component placed with CM','Approved Securities Non-cash component placed with CM',
'Non-Approved Securities placed with CM','Value of CC approved Commodities placed with CM','Other Collaterals placed with CM',
'Cash Retained with CM','Bank Guarantee (BG) retained with CM','Fixed deposit receipt (FDR) retained with CM','Approved Securities Cash Component retained with CM',
'Approved Securities Non-cash component retained with CM','Non-Approved Securities retained with CM','Value of CC approved Commodities retained with CM',
'Other Collaterals Retained with CM','Cash placed with NCL','Bank Guarantee (BG) placed with NCL','Fixed deposit receipt (FDR) placed with NCCL',
'Approved Securities Cash Component placed with NCCL','Approved Securities Non-cash component placed with NCCL','Value of CC approved Commodities placed with NCCL',
'MTF /Non MTF indicator','Uncleared Receipts','Govt Securities â€“ T bills received by TM from clients and by CM from TM(Pro) and from CPs',
'Govt Securities â€“ T-bills Retained by TM','Govt Securitiesâ€“T bills placed with CM','Govt Securitiesâ€“T bills retained with CM',
'Govt Securitiesâ€“T bills placed with NCL','Bank Guarantee (BG) Funded portion retained with CM','Bank Guarantee (BG) Non funded portion retained with CM',
'Bank Guarantee (BG) Funded portion placed with NCL','Bank Guarantee (BG) Non funded portion placed with NCL','Settlement Amount',
'Unclaimed/Unsettled Client Funds','Cash Collateral for MTF positions']
NCDEXLD_Dtype={'Date':str,'Clearing Member PAN':str,'Trading member PAN':str,'CP Code':str,'CP PAN':str,'Client PAN':str,'Account Type':str,
'Segment Indicator':str,'UCC CODE':str,'Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro) and in the books of CM for CP':float,
'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,
'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs':float,'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs':float,'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs':float,'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs':float,'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Credit entry in ledger in lieu of EPI for clients / TM Pro':float,'Pool Account for clients / TM Pro':float,
'Cash Retained by TM':float,'Bank Guarantee (BG) Retained by TM':float,'Fixed Deposit Receipt (FDR) Retained by TM':float,
'Approved Securities Cash Component Retained by TM':float,'Approved Securities Non-cash component Retained by TM':float,
'Non-Approved Securities Retained by TM':float,
'Value of CC approved Commodities Retained by TM':float,
'Other Collaterals Retained by TM':float,
'Cash placed with CM':float,
'Bank Guarantee (BG) placed with CM':float,
'Fixed deposit receipt (FDR) placed with CM':float,
'Approved Securities Cash Component placed with CM':float,
'Approved Securities Non-cash component placed with CM':float,
'Non-Approved Securities placed with CM':float,
'Value of CC approved Commodities placed with CM':float,
'Other Collaterals placed with CM':float,
'Cash Retained with CM':float,
'Bank Guarantee (BG) retained with CM':float,
'Fixed deposit receipt (FDR) retained with CM':float,
'Approved Securities Cash Component retained with CM':float,
'Approved Securities Non-cash component retained with CM':float,
'Non-Approved Securities retained with CM':float,
'Value of CC approved Commodities retained with CM':float,
'Other Collaterals Retained with CM':float,
'Cash placed with NCL':float,
'Bank Guarantee (BG) placed with NCL':float,
'Fixed deposit receipt (FDR) placed with NCCL':float,
'Approved Securities Cash Component placed with NCCL':float,
'Approved Securities Non-cash component placed with NCCL':float,
'Value of CC approved Commodities placed with NCCL':float,
'MTF /Non MTF indicator':str,
'Uncleared Receipts':float,
'Govt Securities â€“ T bills received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Govt Securities â€“ T-bills Retained by TM':float,
'Govt Securitiesâ€“T bills placed with CM':float,
'Govt Securitiesâ€“T bills retained with CM':float,
'Govt Securitiesâ€“T bills placed with NCL':float,
'Bank Guarantee (BG) Funded portion retained with CM':float,
'Bank Guarantee (BG) Non funded portion retained with CM':float,
'Bank Guarantee (BG) Funded portion placed with NCL':float,
'Bank Guarantee (BG) Non funded portion placed with NCL':float,
'Settlement Amount':float,
'Unclaimed/Unsettled Client Funds':str,
'Cash Collateral for MTF positions':float}

NCDEXLD1 = pd.read_csv(NCDEXLD, header=None, names=NCDEXLD_Head, dtype=NCDEXLD_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)
NCDEXLD1['CP Code'] = None
NCDEXLD1['CP PAN'] = None
NCDEXLD1.replace('OWN', '', inplace=True)

NCDEXLD3 = pd.read_csv(NCDEXLD, header=None, names=NCDEXLD_Head, dtype=NCDEXLD_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1)
NCDEXLD3['CP Code'] = None
NCDEXLD3['CP PAN'] = None
NCDEXLD3.replace('OWN', '', inplace=True)

NCDEXM1['NCDEXMU'] = 'CO' + '_' + NCDEXM1['Client ID']
NCDEXLD1['NCDEXLDU'] = NCDEXLD1['Segment Indicator'] + '_' + NCDEXLD1['UCC CODE']
NCDEXMCode = set(NCDEXM1['NCDEXMU'])
NCDEXLDCode = set(NCDEXLD1['NCDEXLDU'])
Not_Matched_NCDEX = NCDEXMCode - NCDEXLDCode
Not_Matched_NCDEX_split = [code.split('_') for code in Not_Matched_NCDEX]
Not_Matched_NCDEX_df = pd.DataFrame(Not_Matched_NCDEX_split, columns=['Segment Indicator', 'UCC CODE'])
Not_Matched_NCDEX_list = [{'Segment Indicator': item[0], 'UCC CODE': item[1]} for item in Not_Matched_NCDEX_split]
Not_Matched_NCDEX_df = pd.DataFrame(Not_Matched_NCDEX_list)
Not_Matched_NCDEX_df.reset_index(drop=True, inplace=True)

if Not_Matched_NCDEX_df.empty:
    NCDEXLD3.to_csv(NCDEXLDF,index=False)
else:
    DataNCDEXLD = {'Date':Date,'Clearing Member PAN':'AABCA6832G','Trading member PAN':'AABCA6832G','CP Code':'','CP PAN':'',
'Client PAN':'','Account Type':'C','Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro) and in the books of CM for CP':'0',
'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':'0',
'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':'0',
'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs':'0',
'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs':'0',
'Credit entry in ledger in lieu of EPI for clients / TM Pro':'0',
'Pool Account for clients / TM Pro':'0','Cash Retained by TM':'0','Bank Guarantee (BG) Retained by TM':'0','Fixed Deposit Receipt (FDR) Retained by TM':'0',
'Approved Securities Cash Component Retained by TM':'0','Approved Securities Non-cash component Retained by TM':'0','Non-Approved Securities Retained by TM':'0',
'Value of CC approved Commodities Retained by TM':'0','Other Collaterals Retained by TM':'0','Cash placed with CM':'0',
'Bank Guarantee (BG) placed with CM':'0','Fixed deposit receipt (FDR) placed with CM':'0','Approved Securities Cash Component placed with CM':'0',
'Approved Securities Non-cash component placed with CM':'0','Non-Approved Securities placed with CM':'0','Value of CC approved Commodities placed with CM':'0',
'Other Collaterals placed with CM':'0','Cash Retained with CM':'0','Bank Guarantee (BG) retained with CM':'0','Fixed deposit receipt (FDR) retained with CM':'0',
'Approved Securities Cash Component retained with CM':'0','Approved Securities Non-cash component retained with CM':'0','Non-Approved Securities retained with CM':'0',
'Value of CC approved Commodities retained with CM':'0','Other Collaterals Retained with CM':'0','Cash placed with NCL':'0',
'Bank Guarantee (BG) placed with NCL':'0','Fixed deposit receipt (FDR) placed with NCCL':'0','Approved Securities Cash Component placed with NCCL':'0',
'Approved Securities Non-cash component placed with NCCL':'0','Value of CC approved Commodities placed with NCCL':'0','MTF /Non MTF indicator':'NA',
'Uncleared Receipts':'0','Govt Securities â€“ T bills received by TM from clients and by CM from TM(Pro) and from CPs':'0','Govt Securities â€“ T-bills Retained by TM':'0',
'Govt Securitiesâ€“T bills placed with CM':'0','Govt Securitiesâ€“T bills retained with CM':'0','Govt Securitiesâ€“T bills placed with NCL':'0',
'Bank Guarantee (BG) Funded portion retained with CM':'0','Bank Guarantee (BG) Non funded portion retained with CM':'0','Bank Guarantee (BG) Funded portion placed with NCL':'0',
'Bank Guarantee (BG) Non funded portion placed with NCL':'0','Settlement Amount':'0','Unclaimed/Unsettled Client Funds':'NA',
'Cash Collateral for MTF positions':'0'}
    dfNCDEX = pd.DataFrame([DataNCDEXLD])
    dfNCDEX = pd.concat([ dfNCDEX[['Date', 'Clearing Member PAN', 'Trading member PAN', 'CP Code', 'CP PAN', 'Client PAN', 'Account Type']], Not_Matched_NCDEX_df, dfNCDEX[['Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro) and in the books of CM for CP',
 'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP', 'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',
 'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs', 'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs', 'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs',
 'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs', 'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs', 'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs',
 'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs', 'Credit entry in ledger in lieu of EPI for clients / TM Pro', 'Pool Account for clients / TM Pro',
 'Cash Retained by TM', 'Bank Guarantee (BG) Retained by TM', 'Fixed Deposit Receipt (FDR) Retained by TM', 'Approved Securities Cash Component Retained by TM', 'Approved Securities Non-cash component Retained by TM',
 'Non-Approved Securities Retained by TM', 'Value of CC approved Commodities Retained by TM', 'Other Collaterals Retained by TM', 'Cash placed with CM', 'Bank Guarantee (BG) placed with CM',
 'Fixed deposit receipt (FDR) placed with CM', 'Approved Securities Cash Component placed with CM', 'Approved Securities Non-cash component placed with CM', 'Non-Approved Securities placed with CM',
 'Value of CC approved Commodities placed with CM', 'Other Collaterals placed with CM', 'Cash Retained with CM', 'Bank Guarantee (BG) retained with CM',
 'Fixed deposit receipt (FDR) retained with CM', 'Approved Securities Cash Component retained with CM', 'Approved Securities Non-cash component retained with CM', 'Non-Approved Securities retained with CM', 'Value of CC approved Commodities retained with CM',
 'Other Collaterals Retained with CM', 'Cash placed with NCL', 'Bank Guarantee (BG) placed with NCL', 'Fixed deposit receipt (FDR) placed with NCCL', 'Approved Securities Cash Component placed with NCCL', 'Approved Securities Non-cash component placed with NCCL',
 'Value of CC approved Commodities placed with NCCL', 'MTF /Non MTF indicator', 'Uncleared Receipts', 'Govt Securities â€“ T bills received by TM from clients and by CM from TM(Pro) and from CPs', 'Govt Securities â€“ T-bills Retained by TM', 'Govt Securitiesâ€“T bills placed with CM',
 'Govt Securitiesâ€“T bills retained with CM', 'Govt Securitiesâ€“T bills placed with NCL', 'Bank Guarantee (BG) Funded portion retained with CM', 'Bank Guarantee (BG) Non funded portion retained with CM','Bank Guarantee (BG) Funded portion placed with NCL',
 'Bank Guarantee (BG) Non funded portion placed with NCL', 'Settlement Amount', 'Unclaimed/Unsettled Client Funds',
 'Cash Collateral for MTF positions']]], axis=1)
    print(dfNCDEX)
    
    dfNCDEX = dfNCDEX.astype(NCDEXLD_Dtype)
    dfNCDEX.fillna(0,inplace=True)
    dfNCDEX['CP Code'] = None
    dfNCDEX['CP PAN'] = None
    dfNCDEX['Date'] = formatted_date_str
    dfNCDEX['Clearing Member PAN'] = 'AABCA6832G'
    dfNCDEX['Trading member PAN'] = 'AABCA6832G'
    dfNCDEX['Account Type'] = 'C'
    # Remove leading and trailing whitespaces from 'PAN_NUMBER' column
    RequiredData1['PAN_NUMBER'] = RequiredData1['PAN_NUMBER'].str.strip()

    # Replace empty strings with NaN in 'PAN_NUMBER' column
    RequiredData1['PAN_NUMBER'].replace('', np.nan, inplace=True)

    # Now perform the mapping operation
    dfNCDEX['Client PAN'] = dfNCDEX['UCC CODE'].map(RequiredData1.set_index('TERMINAL_CODE')['PAN_NUMBER'])
    print('Here the data ')
    

    print(dfNCDEX['Client PAN'])
    dfNCDEX['Client PAN'].to_csv(Test)

    print('Here the data ')
    dfNCDEX['Unclaimed/Unsettled Client Funds'] = 'NA'
    dfNCDEX['MTF /Non MTF indicator'] = 'NA'
    NCDEXLD2 = pd.read_csv(NCDEXLD, header=None, names=NCDEXLD_Head, dtype=NCDEXLD_Dtype,na_values=[' ', 'NA', 'N/A'],skiprows=1) #na_values=['NA', 'NA', 'N/A']
    NCDEXLD2['CP Code'] = None
    NCDEXLD2['CP PAN'] = None
    NCDEXLD2.replace('OWN', '', inplace=True)

    if NCDEXLD2['Unclaimed/Unsettled Client Funds'].isnull().any():
    # Replace NaN values with 'NA'
        NCDEXLD2['Unclaimed/Unsettled Client Funds'].fillna('NA', inplace=True)
    else:
    # If there are no NaN values, replace any empty strings with 'NA'
        NCDEXLD2['Unclaimed/Unsettled Client Funds'].replace('', 'NA', inplace=True)
        
    NCDEXOut=NCDEXLD2._append(dfNCDEX,ignore_index=True)
    NCDEXOut.to_csv(NCDEXLDF,index=False)


print("NCDEX File Generated to Path")

input("Required Details Generated please check......Press Any Key To Exit : - ")
