import numpy as np
import threading
import time
import os
import subprocess
import pandas as pd
from datetime import date
import openpyxl 
from openpyxl import workbook,load_workbook
from openpyxl.styles import Font, Color, PatternFill, Border, Side,Alignment
import tkinter as tk
from tkinter import messagebox

CE = r'D:\Balance Check Segregation\Input\Cash Equivalent Balances .csv'
SEG = r'D:\Balance Check Segregation\Input\Common Segregation Allocation.csv'
TB = r'D:\Balance Check Segregation\Input\Trial Balance for the F.Y. 2023-2024.csv'
SEG_Diff = r'D:\Balance Check Segregation\Output\Segragation_Difference.csv'
SEG_Check = r'D:\Balance Check Segregation\Output\Segragation_Check.csv'
SEG_O = r'D:\Balance Check Segregation\Input\Segragation_Required.csv'
SEG_F = r'D:\Balance Check Segregation\Output\Final_Check.csv'
Test = r'D:\Balance Check Segregation\Input\Test.csv'




CE_Head = ['Trading member PAN','Trans. Date','Unique Client Code','Client PAN','Client Name','Segment Indicator','Financial Ledger Balance-A',
'Financial Ledger Balance (Clear)-B','Peak Financial Ledger Balance','Financial Ledger Balance-MCX','Financial Ledger Balance-NCDEX',
'Financial Ledger Balance-ICEX','Bankg Guarantee (BG)','Fixed deposit Receipt (FDR)','Government of India Securities','Gilt Funds',
'Credit entry in Ledger in lieu of EPI','Pool Account','Uncleared Cheques','Value of Commodities','Last Settlement Date',
'Cash Collateral for MTF Positions','Unclaimed/Unsettled Client Funds','Client Bank Account No.','ES Information Type','Value','F']
CE_Dtype = {'Trading member PAN':str,'Trans. Date':str,'Unique Client Code':str,'Client PAN':str,'Client Name':str,'Segment Indicator':str,
'Financial Ledger Balance-A':float,'Financial Ledger Balance (Clear)-B':float,'Peak Financial Ledger Balance':float,'Financial Ledger Balance-MCX':float,
'Financial Ledger Balance-NCDEX':float,'Financial Ledger Balance-ICEX':float,'Bankg Guarantee (BG)':float,'Fixed deposit Receipt (FDR)':float,
'Government of India Securities':float,'Gilt Funds':float,'Credit entry in Ledger in lieu of EPI':float,'Pool Account':float,'Uncleared Cheques':float,
'Value of Commodities':float,'Last Settlement Date':str,'Cash Collateral for MTF Positions':float,'Unclaimed/Unsettled Client Funds':float,
'Client Bank Account No.':str,'ES Information Type':str,'Value':float,'F':float}

SEG_Head= ['CC Code','Client code','Client Name','Date','Clearing Member PAN','Trading member PAN','CP Code',
'CP PAN','Client PAN','Account Type','Segment Indicator','UCC Code','Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro) and in the books of CM for CP',
'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP','Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',
'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs','Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs','Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs',
'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs','Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs','Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs',
'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs','Credit entry in ledger in lieu of EPI for clients / TM Pro','Pool Account for clients / TM Pro',
'Cash Retained by TM','Bank Guarantee (BG) Retained by TM','Fixed Deposit Receipt (FDR) Retained by TM',
'Approved Securities Cash Component Retained by TM','Approved Securities Non-cash component Retained by TM','Non-Approved Securities Retained by TM',
'Value of CC approved Commodities Retained by TM','Other Collaterals Retained by TM','Cash placed with CM',
'Bank Guarantee (BG) placed with CM','Fixed deposit receipt (FDR) placed with CM','Approved Securities Cash Component placed with CM',
'Approved Securities Non-cash component placed with CM','Non-Approved Securities placed with CM','Value of CC approved Commodities placed with CM',
'Other Collaterals placed with CM','Cash Retained with CM','Bank Guarantee (BG) retained with CM',
'Fixed deposit receipt (FDR) retained with CM','Approved Securities Cash Component retained with CM','Approved Securities Non-cash component retained with CM',
'Non-Approved Securities retained with CM','Value of CC approved Commodities retained with CM','Other Collaterals Retained with CM',
'Cash placed with CC','Bank Guarantee (BG) placed with CC','Fixed deposit receipt (FDR) placed with CC','Approved Securities Cash Component placed with CC',
'Approved Securities Non-cash component placed with CC','MTF /Non MTF indicator','Uncleared Receipts','Govt Securities – T bills received by TM from clients and by CM from TM(Pro) and from CPs','Govt Securities – T-bills Retained by TM',
'Govt Securities–T bills placed with CM','Govt Securities–T bills retained with CM','Govt Securities–T bills placed with NCL','Bank Guarantee (BG) Funded portion retained with CM','Bank Guarantee (BG) Non funded portion retained with CM',
'Bank Guarantee (BG) Funded portion placed with NCL','Bank Guarantee (BG) Non funded portion placed with NCL',
'Settlement Amount','Unclaimed/Unsettled Client Fund','Cash Collateral for MTF positions','Difference']
SEG_Dtype = {'CC Code':str,'Client code':str,'Client Name':str,'Date':str,'Clearing Member PAN':str,'Trading member PAN':str,'CP Code':str,
'CP PAN':str,'Client PAN':str,'Account Type':str,'Segment Indicator':str,'UCC Code':str,'Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro) and in the books of CM for CP':float,'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,
'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs':float,'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs':float,'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs':float,'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs':float,'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs':float,'Credit entry in ledger in lieu of EPI for clients / TM Pro':float,'Pool Account for clients / TM Pro':float,
'Cash Retained by TM':float,'Bank Guarantee (BG) Retained by TM':float,'Fixed Deposit Receipt (FDR) Retained by TM':float,'Approved Securities Cash Component Retained by TM':float,
'Approved Securities Non-cash component Retained by TM':float,'Non-Approved Securities Retained by TM':float,'Value of CC approved Commodities Retained by TM':float,'Other Collaterals Retained by TM':float,
'Cash placed with CM':float,'Bank Guarantee (BG) placed with CM':float,'Fixed deposit receipt (FDR) placed with CM':float,'Approved Securities Cash Component placed with CM':float,
'Approved Securities Non-cash component placed with CM':float,'Non-Approved Securities placed with CM':float,'Value of CC approved Commodities placed with CM':float,'Other Collaterals placed with CM':float,
'Cash Retained with CM':float,'Bank Guarantee (BG) retained with CM':float,'Fixed deposit receipt (FDR) retained with CM':float,'Approved Securities Cash Component retained with CM':float,
'Approved Securities Non-cash component retained with CM':float,'Non-Approved Securities retained with CM':float,'Value of CC approved Commodities retained with CM':float,'Other Collaterals Retained with CM':float,
'Cash placed with CC':float,'Bank Guarantee (BG) placed with CC':float,'Fixed deposit receipt (FDR) placed with CC':float,'Approved Securities Cash Component placed with CC':float,
'Approved Securities Non-cash component placed with CC':float,'MTF /Non MTF indicator':str,'Uncleared Receipts':float,'Govt Securities – T bills received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Govt Securities – T-bills Retained by TM':float,'Govt Securities–T bills placed with CM':float,'Govt Securities–T bills retained with CM':float,'Govt Securities–T bills placed with NCL':float,
'Bank Guarantee (BG) Funded portion retained with CM':float,'Bank Guarantee (BG) Non funded portion retained with CM':float,'Bank Guarantee (BG) Funded portion placed with NCL':float,'Bank Guarantee (BG) Non funded portion placed with NCL':float,
'Settlement Amount':float,'Unclaimed/Unsettled Client Fund':str,'Cash Collateral for MTF positions':float,'Difference':float}
TB_Head=['A/C Code','Opening DR.','Opening CR.','Debit Total','Credit Total','Net Debit','Net Credit','Term Code','Net Balance']
TB_Dtype={'A/C Code':str,'Opening DR.':float,'Opening CR.':float,'Debit Total':float,'Credit Total':float,'Net Debit':float,'Net Credit':float,'Term Code':str,'Net Balance':float}


SEG1 = pd.read_csv(SEG, header=None, names=SEG_Head, dtype=SEG_Dtype,na_values=[' ', 'NA', 'N/A'], skiprows=6)
SEG1['Difference'] = np.round(np.where(SEG1['Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP'] > 0,
                                    SEG1['Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP'] 
                                    - SEG1['Cash Retained by TM'] 
                                    - SEG1['Cash placed with CC']
                                    - SEG1['Bank Guarantee (BG) placed with CC']
                                    - SEG1['Fixed deposit receipt (FDR) placed with CC'],
                                    # Provide a default value if the condition is not met
                                    0  # Assuming you want to assign 0 if the condition is not met
                                    ),decimals=4
                                    )


SEG1['Difference']=SEG1['Difference'].astype(float)

SEG1= SEG1.loc[SEG1['Difference'] != 0]

#Margin1 = Margin1.loc[Margin1['Total Shortage'] != 0]
SEG1 = SEG1.astype(SEG_Dtype)
SEG1.fillna(0,inplace=True)
SEG1.to_csv(SEG_Diff, index=False)
print("Difference File Generated To the Path",SEG_Diff)

SEG2 = pd.read_csv(SEG, header=None, names=SEG_Head, dtype=SEG_Dtype,na_values=[' ', 'NA', 'N/A'], skiprows=6)
grouped = SEG2.groupby('UCC Code')
sum_values_SEG = grouped.sum()
sum_values_SEG = sum_values_SEG.reset_index()

CE1 = pd.read_csv(CE, header=None, names=CE_Head, dtype=CE_Dtype,na_values=[' ', 'NA', 'N/A'], skiprows=6)
CE1.to_csv(Test,index=False)
grouped = CE1.groupby('Unique Client Code')
sum_values_CE = grouped.sum()
sum_values_CE = sum_values_CE.reset_index()
TB1 = pd.read_csv(TB, header=None, names=TB_Head, dtype=TB_Dtype,na_values=[' ', 'NA', 'N/A'], skiprows=6)

grouped = TB1.groupby('Term Code')
sum_values_TB = grouped.sum()
sum_values_TB = sum_values_TB.reset_index()
sum_values_SEG.to_csv(SEG_O,index=False)

SEG_O_Head=['UCC Code','CC Code','Client code','Client Name','Date','Clearing Member PAN','Trading member PAN','CP Code','CP PAN','Client PAN','Account Type','Segment Indicator',
'Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro) and in the books of CM for CP','Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP','Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP',
'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs','Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs','Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs','Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs','Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs',
'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs','Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs','Credit entry in ledger in lieu of EPI for clients / TM Pro','Pool Account for clients / TM Pro','Cash Retained by TM','Bank Guarantee (BG) Retained by TM',
'Fixed Deposit Receipt (FDR) Retained by TM','Approved Securities Cash Component Retained by TM','Approved Securities Non-cash component Retained by TM','Non-Approved Securities Retained by TM','Value of CC approved Commodities Retained by TM','Other Collaterals Retained by TM','Cash placed with CM',
'Bank Guarantee (BG) placed with CM','Fixed deposit receipt (FDR) placed with CM','Approved Securities Cash Component placed with CM','Approved Securities Non-cash component placed with CM','Non-Approved Securities placed with CM','Value of CC approved Commodities placed with CM','Other Collaterals placed with CM',
'Cash Retained with CM','Bank Guarantee (BG) retained with CM','Fixed deposit receipt (FDR) retained with CM','Approved Securities Cash Component retained with CM','Approved Securities Non-cash component retained with CM','Non-Approved Securities retained with CM','Value of CC approved Commodities retained with CM','Other Collaterals Retained with CM',
'Cash placed with CC','Bank Guarantee (BG) placed with CC','Fixed deposit receipt (FDR) placed with CC','Approved Securities Cash Component placed with CC','Approved Securities Non-cash component placed with CC','MTF /Non MTF indicator','Uncleared Receipts','Govt Securities – T bills received by TM from clients and by CM from TM(Pro) and from CPs','Govt Securities – T-bills Retained by TM',
'Govt Securities–T bills placed with CM','Govt Securities–T bills retained with CM','Govt Securities–T bills placed with NCL','Bank Guarantee (BG) Funded portion retained with CM',
'Bank Guarantee (BG) Non funded portion retained with CM','Bank Guarantee (BG) Funded portion placed with NCL','Bank Guarantee (BG) Non funded portion placed with NCL','Settlement Amount',
'Unclaimed/Unsettled Client Fund','Cash Collateral for MTF positions','Difference','Financial Ledger Balance (Clear)-B','Difference SEG-CE','Net Balance','TB-SEG-UR']
SEG_O_Dtype={'UCC Code':str,'CC Code':str,'Client code':str,'Client Name':str,'Date':str,'Clearing Member PAN':str,'Trading member PAN':str,'CP Code':str,'CP PAN':str,'Client PAN':str,'Account Type':str,'Segment Indicator':str,
'Financial Ledger balance-A in the books of TM for clients and in the books of CM for TM ( Pro) and in the books of CM for CP':float,'Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,'Peak Financial Ledger Balance (Clear)-C in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP':float,'Bank Guarantee (BG) received by TM from clients and by CM from TM (Pro) and from CPs':float,'Fixed Deposit Receipt (FDR) received by TM from clients and by CM from TM(Pro) and from CPs':float,'Approved Securities Cash Component received by TM from clients and by CM from TM(Pro) and from CPs':float,
'Approved Securities Non-cash component received by TM from clients and by CM from TM(Pro) and from CPs':float,'Non-Approved Securities received by TM from clients and by CM from TM(Pro) and from CPs':float,'Value of CC approved Commodities received by TM from clients and by CM from TM(Pro) and from CPs':float,'Other collaterals received by TM from clients and by CM from TM(Pro) and from CPs':float,'Credit entry in ledger in lieu of EPI for clients / TM Pro':float,'Pool Account for clients / TM Pro':float,
'Cash Retained by TM':float,'Bank Guarantee (BG) Retained by TM':float,'Fixed Deposit Receipt (FDR) Retained by TM':float,'Approved Securities Cash Component Retained by TM':float,'Approved Securities Non-cash component Retained by TM':float,'Non-Approved Securities Retained by TM':float,'Value of CC approved Commodities Retained by TM':float,'Other Collaterals Retained by TM':float,
'Cash placed with CM':float,'Bank Guarantee (BG) placed with CM':float,'Fixed deposit receipt (FDR) placed with CM':float,'Approved Securities Cash Component placed with CM':float,'Approved Securities Non-cash component placed with CM':float,'Non-Approved Securities placed with CM':float,'Value of CC approved Commodities placed with CM':float,'Other Collaterals placed with CM':float,
'Cash Retained with CM':float,'Bank Guarantee (BG) retained with CM':float,'Fixed deposit receipt (FDR) retained with CM':float,'Approved Securities Cash Component retained with CM':float,'Approved Securities Non-cash component retained with CM':float,'Non-Approved Securities retained with CM':float,'Value of CC approved Commodities retained with CM':float,
'Other Collaterals Retained with CM':float,'Cash placed with CC':float,'Bank Guarantee (BG) placed with CC':float,'Fixed deposit receipt (FDR) placed with CC':float,'Approved Securities Cash Component placed with CC':float,'Approved Securities Non-cash component placed with CC':float,'MTF /Non MTF indicator':str,'Uncleared Receipts':float,
'Govt Securities – T bills received by TM from clients and by CM from TM(Pro) and from CPs':float,'Govt Securities – T-bills Retained by TM':float,'Govt Securities–T bills placed with CM':float,'Govt Securities–T bills retained with CM':float,'Govt Securities–T bills placed with NCL':float,'Bank Guarantee (BG) Funded portion retained with CM':float,
'Bank Guarantee (BG) Non funded portion retained with CM':float,'Bank Guarantee (BG) Funded portion placed with NCL':float,'Bank Guarantee (BG) Non funded portion placed with NCL':float,
'Settlement Amount':float,'Unclaimed/Unsettled Client Fund':str,'Cash Collateral for MTF positions':float,'Difference':int,'Financial Ledger Balance (Clear)-B':float,'Difference SEG-CE':float,'Net Balance':float,'TB-SEG-UR':float}

SEG_O1=pd.read_csv(SEG_O,header=None,names=SEG_O_Head,dtype=SEG_O_Dtype,na_values=[' ', 'NA', 'N/A'], skiprows=1)

SEG_O1['Financial Ledger Balance (Clear)-B'] =  SEG_O1['UCC Code'].map(sum_values_CE.set_index('Unique Client Code')['Financial Ledger Balance (Clear)-B'])
SEG_O1['Difference SEG-CE'] = SEG_O1['Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP'] - SEG_O1['Financial Ledger Balance (Clear)-B']
SEG_O1['Net Balance'] =  SEG_O1['UCC Code'].map(sum_values_TB.set_index('Term Code')['Net Balance'])
SEG_O1['TB-SEG-UR'] = SEG_O1['Net Balance'] -  SEG_O1['Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP'] - SEG_O1['Uncleared Receipts']


SEG_O1.to_csv(SEG_F,columns=['UCC Code','Financial Ledger balance (clear)-B in the books of TM for clients and in the books of CM for TM (Pro) and in the books of CM for CP','Uncleared Receipts','Financial Ledger Balance (Clear)-B','Difference SEG-CE','Net Balance','TB-SEG-UR'],index=False)

print("Required File Generated to the Path",SEG_F)
input("Press Enter For Exit..................")

#'Term Code' TB  'Unique Client Code' CE  'Financial Ledger Balance (Clear)-B' CE  'Net Balance'
                                                                                               

