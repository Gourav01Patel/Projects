import pandas as pd
import tkinter as tk
from tkinter import messagebox
import os


print("""Press "1" for Snap1.
      Press "2" for Snap2.
      Press "3" for Snap3.
      Press "4" for Snap4.
      Press "5" for Snap5.
      Press "6" for Snap6.
      Press "7" for Snap7.
      Press "8" for Snap8.
      Press "9" for Final EOD Report. """)

Command = int(input('Press Number of Snap :-'))
Date = input("Please enter Date for Report (DDMMYYYY):-")

if Command == 1:
    print('Prepraring Report for Snap 1.......')
    curr1= r'D:\Live_Snap\Input\CDX_INTRADAY_SHRTCOLL_0313_'+Date+'_01.csv'
    EQ1=r'D:\Live_Snap\Input\EQ_INTRADAY_SHRTCOLL_0313_'+Date+'_01.csv'
    FO1=r'D:\Live_Snap\Input\EDX_INTRADAY_SHRTCOLL_0313_'+Date+'_01.CSV'
    MCX1=r'D:\Live_Snap\Input\MCX_PeakMargin56565_'+Date[4:] + Date[2:4] +Date[:2]+'_01.csv'
    NCDX1 = r'D:\Live_Snap\Input\NCCL_MARGIN_REP_01274_'+Date[4:] + Date[2:4] +Date[:2]+'_01.csv'
    Snap1 = r'D:\Live_Snap\Output\Snap01'+Date+'.csv'
    Snap1_ICCL_Shortage=r'D:\Live_Snap\Output\Snap01_ICCL_Shortage'+Date+'.csv'
    Snap1_Total_Shortage=r'D:\Live_Snap\Output\Snap01_Total_Shortage'+Date+'.csv'

    file_paths = {curr1,EQ1,FO1,MCX1,NCDX1}

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            # Display a warning pop-up message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning("File Not Found", f"The file is not available at: {file_path}.\nPlease ensure the file is available at the specified path.")
    
    
    Head=['Date','Segment','CM Code','TM Code','Client Code','CP Code','Cash','Non Cash Value','Total (Cash+Non Cash)','Margin','Shortage']
    Dtype={'Date':str,'Segment':str,'CM Code':str,'TM Code':str,'Client Code':str,'CP Code':str,'Cash':float,'Non Cash Value':float,'Total (Cash+Non Cash)':float,'Margin':float,'Shortage':float}
    MCX_head=['Business Date','Snapshot Interval','CM ID','TM ID','CLIENT ID','INTIAL MARGIN','ELM','Net Buy Premium','Total Upfront Margin','Client margin allocation','Client other collaterals','Short allocation']
    MCX_dtype= {'Business Date':str,'Snapshot Interval':str,'CM ID':str,'TM ID':str,'CLIENT ID':str,'INTIAL MARGIN':float,'ELM':float,'Net Buy Premium':float,'Total Upfront Margin':float,'Client margin allocation':float,'Client other collaterals':float,'Short allocation':float}
    
    curr2=pd.read_csv(curr1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    curr2=curr2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Currency Total','Margin':'Currency Margin','Shortage':'Currency Shortage'})

    EQ2=pd.read_csv(EQ1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    EQ2=EQ2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Equity Total','Margin':'Equity Margin','Shortage':'Equity Shortage'})

    FO2=pd.read_csv(FO1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    FO2=FO2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Future Total','Margin':'Future Margin','Shortage':'Future Shortage'})

    MCX2=pd.read_csv(MCX1,header=None,names=MCX_head,dtype=MCX_dtype,usecols=['CLIENT ID','Client margin allocation','Total Upfront Margin','Short allocation'])
    MCX2 = MCX2.rename(columns={'CLIENT ID': 'Client Code', 'Client margin allocation': 'MCX Total', 'Total Upfront Margin': 'MCX Margin', 'Short allocation': 'MCX Shortage'})

    NCDX2=pd.read_csv(NCDX1,usecols=['Client Code','Collateral_Value_Snapshot','Initial Margin','ELM Margin','Short_allocation_SnapShot'])
    NCDX2['Margin'] = NCDX2['Initial Margin']+ NCDX2['ELM Margin']
    NCDX3=NCDX2[['Client Code','Collateral_Value_Snapshot','Margin','Short_allocation_SnapShot']]
    NCDX3 = NCDX3.rename(columns={'Client Code':'Client Code','Collateral_Value_Snapshot': 'NCDX Total','Margin':'NCDX Margin','Short_allocation_SnapShot': 'NCDX Shortage'})
    
    merged_df = curr2.merge(EQ2, on='Client Code', how='outer')
    merged_df = merged_df.merge(FO2, on='Client Code', how='outer')
    merged_df = merged_df.merge(MCX2, on='Client Code', how='outer')
    merged_df = merged_df.merge(NCDX3, on='Client Code', how='outer')
    merged_df = merged_df.fillna(0)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(Snap1, index=False)

    merged_df['Total Shortage ICCL'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin']) -  (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total'])
    filtered_df = merged_df[merged_df['Total Shortage ICCL'] > 0]
    
    filtered_df.to_csv(Snap1_ICCL_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage ICCL'], index=False)
    
    merged_df['Total Shortage All Seg'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin'] + merged_df['MCX Margin'] + merged_df['NCDX Margin']) - (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total']+merged_df['MCX Total']+merged_df['NCDX Total'])
    
    filtered_df = merged_df[merged_df['Total Shortage All Seg'] > 0]

    filtered_df.to_csv(Snap1_Total_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage All Seg'], index=False)

    print('Snap 1 File Generated to path :-',Snap1)
    input('Press Any Key For Exit........')



elif Command == 2:
    print('Prepraring Report for Snap 2.......')
    
    curr1=r'D:\Live_Snap\Input\CDX_INTRADAY_SHRTCOLL_0313_'+Date+'_02.csv'
    EQ1=r'D:\Live_Snap\Input\EQ_INTRADAY_SHRTCOLL_0313_'+Date+'_02.csv'
    FO1=r'D:\Live_Snap\Input\EDX_INTRADAY_SHRTCOLL_0313_'+Date+'_02.CSV'
    MCX1=r'D:\Live_Snap\Input\MCX_PeakMargin56565_'+Date[4:] + Date[2:4] +Date[:2]+'_02.csv'
    NCDX1 = r'D:\Live_Snap\Input\NCCL_MARGIN_REP_01274_'+Date[4:] + Date[2:4] +Date[:2]+'_02.csv'
    Snap1 = r'D:\Live_Snap\Output\Snap02'+Date+'.csv'
    Snap1_ICCL_Shortage=r'D:\Live_Snap\Output\Snap02_ICCL_Shortage'+Date+'.csv'
    Snap1_Total_Shortage=r'D:\Live_Snap\Output\Snap02_Total_Shortage'+Date+'.csv'
    
    file_paths = {curr1,EQ1,FO1,MCX1,NCDX1}

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            # Display a warning pop-up message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning("File Not Found", f"The file is not available at: {file_path}.\nPlease ensure the file is available at the specified path.")

    Head=['Date','Segment','CM Code','TM Code','Client Code','CP Code','Cash','Non Cash Value','Total (Cash+Non Cash)','Margin','Shortage']
    Dtype={'Date':str,'Segment':str,'CM Code':str,'TM Code':str,'Client Code':str,'CP Code':str,'Cash':float,'Non Cash Value':float,'Total (Cash+Non Cash)':float,'Margin':float,'Shortage':float}
    MCX_head=['Business Date','Snapshot Interval','CM ID','TM ID','CLIENT ID','INTIAL MARGIN','ELM','Net Buy Premium','Total Upfront Margin','Client margin allocation','Client other collaterals','Short allocation']
    MCX_dtype= {'Business Date':str,'Snapshot Interval':str,'CM ID':str,'TM ID':str,'CLIENT ID':str,'INTIAL MARGIN':float,'ELM':float,'Net Buy Premium':float,'Total Upfront Margin':float,'Client margin allocation':float,'Client other collaterals':float,'Short allocation':float}
    
    curr2=pd.read_csv(curr1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    curr2=curr2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Currency Total','Margin':'Currency Margin','Shortage':'Currency Shortage'})

    EQ2=pd.read_csv(EQ1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    EQ2=EQ2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Equity Total','Margin':'Equity Margin','Shortage':'Equity Shortage'})

    FO2=pd.read_csv(FO1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    FO2=FO2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Future Total','Margin':'Future Margin','Shortage':'Future Shortage'})

    MCX2=pd.read_csv(MCX1,header=None,names=MCX_head,dtype=MCX_dtype,usecols=['CLIENT ID','Client margin allocation','Total Upfront Margin','Short allocation'])
    MCX2 = MCX2.rename(columns={'CLIENT ID': 'Client Code', 'Client margin allocation': 'MCX Total', 'Total Upfront Margin': 'MCX Margin', 'Short allocation': 'MCX Shortage'})

    NCDX2=pd.read_csv(NCDX1,usecols=['Client Code','Collateral_Value_Snapshot','Initial Margin','ELM Margin','Short_allocation_SnapShot'])
    NCDX2['Margin'] = NCDX2['Initial Margin']+ NCDX2['ELM Margin']
    NCDX3=NCDX2[['Client Code','Collateral_Value_Snapshot','Margin','Short_allocation_SnapShot']]
    NCDX3 = NCDX3.rename(columns={'Client Code':'Client Code','Collateral_Value_Snapshot': 'NCDX Total','Margin':'NCDX Margin','Short_allocation_SnapShot': 'NCDX Shortage'})
    
   
    merged_df = curr2.merge(EQ2, on='Client Code', how='outer')
    merged_df = merged_df.merge(FO2, on='Client Code', how='outer')
    merged_df = merged_df.merge(MCX2, on='Client Code', how='outer')
    merged_df = merged_df.merge(NCDX3, on='Client Code', how='outer')
    merged_df = merged_df.fillna(0)



    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(Snap1, index=False)
    merged_df['Total Shortage ICCL'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin']) -  (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total'])
    filtered_df = merged_df[merged_df['Total Shortage ICCL'] > 0]
    
    filtered_df.to_csv(Snap1_ICCL_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage ICCL'], index=False)
    
    merged_df['Total Shortage All Seg'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin'] + merged_df['MCX Margin'] + merged_df['NCDX Margin']) - (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total']+merged_df['MCX Total']+merged_df['NCDX Total'])
    
    filtered_df = merged_df[merged_df['Total Shortage All Seg'] > 0]

    filtered_df.to_csv(Snap1_Total_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage All Seg'], index=False)


    print('Snap 2 File Generated to path :-',Snap1)
    input('Press Any Key For Exit........')

elif Command == 3:
    print('Prepraring Report for Snap 3.......')
    
    curr1                   =   r'D:\Live_Snap\Input\CDX_INTRADAY_SHRTCOLL_0313_'+Date+'_03.csv'
    EQ1                     =   r'D:\Live_Snap\Input\EQ_INTRADAY_SHRTCOLL_0313_'+Date+'_03.csv'
    FO1                     =   r'D:\Live_Snap\Input\EDX_INTRADAY_SHRTCOLL_0313_'+Date+'_03.CSV'
    MCX1                    =   r'D:\Live_Snap\Input\MCX_PeakMargin56565_'+Date[4:] + Date[2:4] +Date[:2]+'_03.csv'
    NCDX1                   =   r'D:\Live_Snap\Input\NCCL_MARGIN_REP_01274_'+Date[4:] + Date[2:4] +Date[:2]+'_03.csv'
    Snap1                   =   r'D:\Live_Snap\Output\Snap03'+Date+'.csv'
    Snap1_ICCL_Shortage     =   r'D:\Live_Snap\Output\Snap03_ICCL_Shortage'+Date+'.csv'
    Snap1_Total_Shortage    =   r'D:\Live_Snap\Output\Snap03_Total_Shortage'+Date+'.csv'

    
    file_paths = {curr1,EQ1,FO1,MCX1,NCDX1}

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            # Display a warning pop-up message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning("File Not Found", f"The file is not available at: {file_path}.\nPlease ensure the file is available at the specified path.")

    Head                    =   ['Date','Segment','CM Code','TM Code','Client Code','CP Code','Cash','Non Cash Value','Total (Cash+Non Cash)','Margin','Shortage']
    Dtype                   =   {'Date':str,'Segment':str,'CM Code':str,'TM Code':str,'Client Code':str,'CP Code':str,'Cash':float,'Non Cash Value':float,'Total (Cash+Non Cash)':float,'Margin':float,'Shortage':float}
    MCX_head                =   ['Business Date','Snapshot Interval','CM ID','TM ID','CLIENT ID','INTIAL MARGIN','ELM','Net Buy Premium','Total Upfront Margin','Client margin allocation','Client other collaterals','Short allocation']
    MCX_dtype               =   {'Business Date':str,'Snapshot Interval':str,'CM ID':str,'TM ID':str,'CLIENT ID':str,'INTIAL MARGIN':float,'ELM':float,'Net Buy Premium':float,'Total Upfront Margin':float,'Client margin allocation':float,'Client other collaterals':float,'Short allocation':float}
    
    curr2                   =   pd.read_csv(curr1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    curr2                   =   curr2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Currency Total','Margin':'Currency Margin','Shortage':'Currency Shortage'})

    EQ2                     =   pd.read_csv(EQ1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    EQ2                     =   EQ2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Equity Total','Margin':'Equity Margin','Shortage':'Equity Shortage'})

    FO2                     =   pd.read_csv(FO1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    FO2                     =   FO2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Future Total','Margin':'Future Margin','Shortage':'Future Shortage'})

    MCX2                    =   pd.read_csv(MCX1,header=None,names=MCX_head,dtype=MCX_dtype,usecols=['CLIENT ID','Client margin allocation','Total Upfront Margin','Short allocation'])
    MCX2                    =   MCX2.rename(columns={'CLIENT ID': 'Client Code', 'Client margin allocation': 'MCX Total', 'Total Upfront Margin': 'MCX Margin', 'Short allocation': 'MCX Shortage'})

    NCDX2                   =   pd.read_csv(NCDX1,usecols=['Client Code','Collateral_Value_Snapshot','Initial Margin','ELM Margin','Short_allocation_SnapShot'])
    NCDX2['Margin']         =   NCDX2['Initial Margin']+ NCDX2['ELM Margin']
    NCDX3                   =   NCDX2[['Client Code','Collateral_Value_Snapshot','Margin','Short_allocation_SnapShot']]
    NCDX3                   =   NCDX3.rename(columns={'Client Code':'Client Code','Collateral_Value_Snapshot': 'NCDX Total','Margin':'NCDX Margin','Short_allocation_SnapShot': 'NCDX Shortage'})
    
    
    merged_df               =   curr2.merge(EQ2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(FO2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(MCX2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(NCDX3, on='Client Code', how='outer')
    merged_df               =   merged_df.fillna(0)

       # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(Snap1, index=False)
    merged_df['Total Shortage ICCL'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin']) -  (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total'])
    
    filtered_df             =   merged_df[merged_df['Total Shortage ICCL'] > 0]
    
    filtered_df.to_csv(Snap1_ICCL_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage ICCL'], index=False)
    
    merged_df['Total Shortage All Seg'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin'] + merged_df['MCX Margin'] + merged_df['NCDX Margin']) - (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total']+merged_df['MCX Total']+merged_df['NCDX Total'])
    
    filtered_df             = merged_df[merged_df['Total Shortage All Seg'] > 0]

    filtered_df.to_csv(Snap1_Total_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage All Seg'], index=False)

    print('Snap 3 File Generated to path :-',Snap1)
    input('Press Any Key For Exit........')



elif Command == 4:
    print('Prepraring Report for Snap 4.......') 
    curr1                   =   r'D:\Live_Snap\Input\CDX_INTRADAY_SHRTCOLL_0313_'+Date+'_04.csv'
    EQ1                     =   r'D:\Live_Snap\Input\EQ_INTRADAY_SHRTCOLL_0313_'+Date+'_04.csv'
    FO1                     =   r'D:\Live_Snap\Input\EDX_INTRADAY_SHRTCOLL_0313_'+Date+'_04.CSV'
    MCX1                    =   r'D:\Live_Snap\Input\MCX_PeakMargin56565_'+Date[4:] + Date[2:4] +Date[:2]+'_04.csv'
    NCDX1                   =   r'D:\Live_Snap\Input\NCCL_MARGIN_REP_01274_'+Date[4:] + Date[2:4] +Date[:2]+'_04.csv'
    Snap1                   =   r'D:\Live_Snap\Output\Snap04'+Date+'.csv'
    Snap1_ICCL_Shortage     =   r'D:\Live_Snap\Output\Snap04_ICCL_Shortage'+Date+'.csv'
    Snap1_Total_Shortage    =   r'D:\Live_Snap\Output\Snap04_Total_Shortage'+Date+'.csv'

    
    file_paths = {curr1,EQ1,FO1,MCX1,NCDX1}

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            # Display a warning pop-up message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning("File Not Found", f"The file is not available at: {file_path}.\nPlease ensure the file is available at the specified path.")

    Head                    =   ['Date','Segment','CM Code','TM Code','Client Code','CP Code','Cash','Non Cash Value','Total (Cash+Non Cash)','Margin','Shortage']
    Dtype                   =   {'Date':str,'Segment':str,'CM Code':str,'TM Code':str,'Client Code':str,'CP Code':str,'Cash':float,'Non Cash Value':float,'Total (Cash+Non Cash)':float,'Margin':float,'Shortage':float}
    MCX_head                =   ['Business Date','Snapshot Interval','CM ID','TM ID','CLIENT ID','INTIAL MARGIN','ELM','Net Buy Premium','Total Upfront Margin','Client margin allocation','Client other collaterals','Short allocation']
    MCX_dtype               =   {'Business Date':str,'Snapshot Interval':str,'CM ID':str,'TM ID':str,'CLIENT ID':str,'INTIAL MARGIN':float,'ELM':float,'Net Buy Premium':float,'Total Upfront Margin':float,'Client margin allocation':float,'Client other collaterals':float,'Short allocation':float}
    
    curr2                   =   pd.read_csv(curr1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    curr2                   =   curr2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Currency Total','Margin':'Currency Margin','Shortage':'Currency Shortage'})

    EQ2                     =   pd.read_csv(EQ1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    EQ2                     =   EQ2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Equity Total','Margin':'Equity Margin','Shortage':'Equity Shortage'})

    FO2                     =   pd.read_csv(FO1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    FO2                     =   FO2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Future Total','Margin':'Future Margin','Shortage':'Future Shortage'})

    MCX2                    =   pd.read_csv(MCX1,header=None,names=MCX_head,dtype=MCX_dtype,usecols=['CLIENT ID','Client margin allocation','Total Upfront Margin','Short allocation'])
    MCX2                    =   MCX2.rename(columns={'CLIENT ID': 'Client Code', 'Client margin allocation': 'MCX Total', 'Total Upfront Margin': 'MCX Margin', 'Short allocation': 'MCX Shortage'})

    NCDX2                   =   pd.read_csv(NCDX1,usecols=['Client Code','Collateral_Value_Snapshot','Initial Margin','ELM Margin','Short_allocation_SnapShot'])
    NCDX2['Margin']         =   NCDX2['Initial Margin']+ NCDX2['ELM Margin']
    NCDX3                   =   NCDX2[['Client Code','Collateral_Value_Snapshot','Margin','Short_allocation_SnapShot']]
    NCDX3                   =   NCDX3.rename(columns={'Client Code':'Client Code','Collateral_Value_Snapshot': 'NCDX Total','Margin':'NCDX Margin','Short_allocation_SnapShot': 'NCDX Shortage'})
    
    
    merged_df               =   curr2.merge(EQ2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(FO2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(MCX2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(NCDX3, on='Client Code', how='outer')
    merged_df               =   merged_df.fillna(0)


    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(Snap1, index=False)
    merged_df['Total Shortage ICCL'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin']) -  (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total'])
    filtered_df = merged_df[merged_df['Total Shortage ICCL'] > 0]
    
    filtered_df.to_csv(Snap1_ICCL_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage ICCL'], index=False)
    
    merged_df['Total Shortage All Seg'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin'] + merged_df['MCX Margin'] + merged_df['NCDX Margin']) - (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total']+merged_df['MCX Total']+merged_df['NCDX Total'])
    
    filtered_df = merged_df[merged_df['Total Shortage All Seg'] > 0]

    filtered_df.to_csv(Snap1_Total_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage All Seg'], index=False)

    print('Snap 4 File Generated to path :-',Snap1)
    input('Press Any Key For Exit........')

elif Command == 5:
    print('Prepraring Report for Snap 5.......') 
    curr1                   =   r'D:\Live_Snap\Input\CDX_SHRTCOLL_0313_'+Date+'.csv'
    EQ1                     =   r'D:\Live_Snap\Input\EQ_SHRTCOLL_0313_'+Date+'.csv'
    FO1                     =   r'D:\Live_Snap\Input\EDX_SHRTCOLL_0313_'+Date+'.CSV'
    MCX1                    =   r'D:\Live_Snap\Input\MCX_PeakMargin56565_'+Date[4:] + Date[2:4] +Date[:2]+'_05.csv'
    NCDX1                   =   r'D:\Live_Snap\Input\NCCL_MARGIN_REP_01274_'+Date[4:] + Date[2:4] +Date[:2]+'_05.csv'
    Snap1                   =   r'D:\Live_Snap\Output\Snap05'+Date+'.csv'
    Snap1_ICCL_Shortage     =   r'D:\Live_Snap\Output\Snap05_ICCL_Shortage'+Date+'.csv'
    Snap1_Total_Shortage    =   r'D:\Live_Snap\Output\Snap05_Total_Shortage'+Date+'.csv'

    
    file_paths = {curr1,EQ1,FO1,MCX1,NCDX1}

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            # Display a warning pop-up message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning("File Not Found", f"The file is not available at: {file_path}.\nPlease ensure the file is available at the specified path.")

    Head                    =   ['Date','Segment','CM Code','TM Code','Client Code','CP Code','Cash','Non Cash Value','Total (Cash+Non Cash)','Margin','Shortage']
    Dtype                   =   {'Date':str,'Segment':str,'CM Code':str,'TM Code':str,'Client Code':str,'CP Code':str,'Cash':float,'Non Cash Value':float,'Total (Cash+Non Cash)':float,'Margin':float,'Shortage':float}
    MCX_head                =   ['Business Date','Snapshot Interval','CM ID','TM ID','CLIENT ID','INTIAL MARGIN','ELM','Net Buy Premium','Total Upfront Margin','Client margin allocation','Client other collaterals','Short allocation']
    MCX_dtype               =   {'Business Date':str,'Snapshot Interval':str,'CM ID':str,'TM ID':str,'CLIENT ID':str,'INTIAL MARGIN':float,'ELM':float,'Net Buy Premium':float,'Total Upfront Margin':float,'Client margin allocation':float,'Client other collaterals':float,'Short allo             cation':float}
    
    curr2                   =   pd.read_csv(curr1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    curr2                   =   curr2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Currency Total','Margin':'Currency Margin','Shortage':'Currency Shortage'})
    
    EQ2                     =   pd.read_csv(EQ1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    EQ2                     =   EQ2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Equity Total','Margin':'Equity Margin','Shortage':'Equity Shortage'})

    FO2                     =   pd.read_csv(FO1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    FO2                     =   FO2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Future Total','Margin':'Future Margin','Shortage':'Future Shortage'})

    MCX2                    =   pd.read_csv(MCX1,header=None,names=MCX_head,dtype=MCX_dtype,usecols=['CLIENT ID','Client margin allocation','Total Upfront Margin','Short allocation'])
    MCX2                    =   MCX2.rename(columns={'CLIENT ID': 'Client Code', 'Client margin allocation': 'MCX Total', 'Total Upfront Margin': 'MCX Margin', 'Short allocation': 'MCX Shortage'})

    NCDX2                   =   pd.read_csv(NCDX1,usecols=['Client Code','Collateral_Value_Snapshot','Initial Margin','ELM Margin','Short_allocation_SnapShot'])
    NCDX2['Margin']         =   NCDX2['Initial Margin']+ NCDX2['ELM Margin']
    NCDX3                   =   NCDX2[['Client Code','Collateral_Value_Snapshot','Margin','Short_allocation_SnapShot']]
    NCDX3                   =   NCDX3.rename(columns={'Client Code':'Client Code','Collateral_Value_Snapshot': 'NCDX Total','Margin':'NCDX Margin','Short_allocation_SnapShot': 'NCDX Shortage'})
    
    merged_df               =   curr2.merge(EQ2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(FO2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(MCX2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(NCDX3, on='Client Code', how='outer')
    merged_df               =   merged_df.fillna(0)


    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(Snap1, index=False)
    merged_df['Total Shortage ICCL'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin']) -  (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total'])
    filtered_df = merged_df[merged_df['Total Shortage ICCL'] > 0]
    
    filtered_df.to_csv(Snap1_ICCL_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage ICCL'], index=False)
    
    merged_df['Total Shortage All Seg'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin'] + merged_df['MCX Margin'] + merged_df['NCDX Margin']) - (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total']+merged_df['MCX Total']+merged_df['NCDX Total'])
    
    filtered_df = merged_df[merged_df['Total Shortage All Seg'] > 0]

    filtered_df.to_csv(Snap1_Total_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage All Seg'], index=False)

    print('Snap 5 File Generated to path :-',Snap1)
    input('Press Any Key For Exit........')

elif Command == 6:
    print('Prepraring Report for Snap 6.......') 
    curr1                   =   r'D:\Live_Snap\Input\CDX_SHRTCOLL_0313_'+Date+'.csv'
    EQ1                     =   r'D:\Live_Snap\Input\EQ_SHRTCOLL_0313_'+Date+'.csv'
    FO1                     =   r'D:\Live_Snap\Input\EDX_SHRTCOLL_0313_'+Date+'.CSV'
    MCX1                    =   r'D:\Live_Snap\Input\MCX_PeakMargin56565_'+Date[4:] + Date[2:4] +Date[:2]+'_06.csv'
    NCDX1                   =   r'D:\Live_Snap\Input\CLIENT_EFFECTIVE_DEPOSITS_TM_01274_'+Date+'.csv'
    Snap1                   =   r'D:\Live_Snap\Output\Snap06'+Date+'.csv'
    Snap1_ICCL_Shortage     =   r'D:\Live_Snap\Output\Snap06_ICCL_Shortage'+Date+'.csv'
    Snap1_Total_Shortage    =   r'D:\Live_Snap\Output\Snap06_Total_Shortage'+Date+'.csv'

    
    file_paths = {curr1,EQ1,FO1,MCX1,NCDX1}

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            # Display a warning pop-up message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning("File Not Found", f"The file is not available at: {file_path}.\nPlease ensure the file is available at the specified path.")

    Head                    =   ['Date','Segment','CM Code','TM Code','Client Code','CP Code','Cash','Non Cash Value','Total (Cash+Non Cash)','Margin','Shortage']
    Dtype                   =   {'Date':str,'Segment':str,'CM Code':str,'TM Code':str,'Client Code':str,'CP Code':str,'Cash':float,'Non Cash Value':float,'Total (Cash+Non Cash)':float,'Margin':float,'Shortage':float}
    MCX_head                =   ['Business Date','Snapshot Interval','CM ID','TM ID','CLIENT ID','INTIAL MARGIN','ELM','Net Buy Premium','Total Upfront Margin','Client margin allocation','Client other collaterals','Short allocation']
    MCX_dtype               =   {'Business Date':str,'Snapshot Interval':str,'CM ID':str,'TM ID':str,'CLIENT ID':str,'INTIAL MARGIN':float,'ELM':float,'Net Buy Premium':float,'Total Upfront Margin':float,'Client margin allocation':float,'Client other collaterals':float,'Short allocation':float}
    NCDX_head               =   ['TM Code/CP Code','Client/CP Code','Cash Equivalent','Securities Cash Component','Total Cash Component','Securities Non cash','Commodities Non Cash','Other Non Cash',
                                'Total Non Cash','Total Collateral (Cash and Non Cash)','Commodities Considered','Total Non Cash Considered','Gross Effective Deposits','Blocked Amount','Net Effective Deposits Before Member Excess Cash ALC',
                                'Excess Cash','Excess Non Cash','Member Cash Allocation Limit','TM Excess Cash Allocation','CM Excess Cash Allocation','Net Effective Deposits After Member Excess Cash ALC','Margin']
    
    curr2                   =   pd.read_csv(curr1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    curr2                   =   curr2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Currency Total','Margin':'Currency Margin','Shortage':'Currency Shortage'})
    
    EQ2                     =   pd.read_csv(EQ1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    EQ2                     =   EQ2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Equity Total','Margin':'Equity Margin','Shortage':'Equity Shortage'})

    FO2                     =   pd.read_csv(FO1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    FO2                     =   FO2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Future Total','Margin':'Future Margin','Shortage':'Future Shortage'})
    
    MCX2                    =   pd.read_csv(MCX1,header=None,names=MCX_head,dtype=MCX_dtype,usecols=['CLIENT ID','Client margin allocation','Total Upfront Margin','Short allocation'])
    MCX2                    =   MCX2.rename(columns={'CLIENT ID': 'Client Code', 'Client margin allocation': 'MCX Total', 'Total Upfront Margin': 'MCX Margin', 'Short allocation': 'MCX Shortage'})
    
    NCDX2                   =   pd.read_csv(NCDX1,header=None,names=NCDX_head,usecols=['Client/CP Code','Total Collateral (Cash and Non Cash)','Margin'])
    NCDX2['NCDX Shortage']  =   NCDX2['Total Collateral (Cash and Non Cash)'] - NCDX2['Margin']
    NCDX3                   =   NCDX2[['Client/CP Code','Total Collateral (Cash and Non Cash)','Margin','NCDX Shortage']]
    NCDX3                   =   NCDX3.rename(columns={'Client/CP Code':'Client Code','Total Collateral (Cash and Non Cash)': 'NCDX Total','Margin':'NCDX Margin','NCDX Shortage': 'NCDX Shortage'})
    
    merged_df               =   curr2.merge(EQ2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(FO2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(MCX2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(NCDX3, on='Client Code', how='outer')
    merged_df               =   merged_df.fillna(0)


    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(Snap1, index=False)

    merged_df['Total Shortage ICCL'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin']) -  (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total'])
    filtered_df = merged_df[merged_df['Total Shortage ICCL'] > 0]
    
    filtered_df.to_csv(Snap1_ICCL_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage ICCL'], index=False)
    
    merged_df['Total Shortage All Seg'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin'] + merged_df['MCX Margin'] + merged_df['NCDX Margin']) - (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total']+merged_df['MCX Total']+merged_df['NCDX Total'])
    
    filtered_df = merged_df[merged_df['Total Shortage All Seg'] > 0]

    filtered_df.to_csv(Snap1_Total_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage All Seg'], index=False)

    print('Snap 6 File Generated to path :-',Snap1)
    input('Press Any Key For Exit........')


elif Command == 7:
    print('Prepraring Report for MCX Snap 7.......')
    curr1                   =   r'D:\Live_Snap\Input\CDX_SHRTCOLL_0313_'+Date+'.csv'
    EQ1                     =   r'D:\Live_Snap\Input\EQ_SHRTCOLL_0313_'+Date+'.csv'
    FO1                     =   r'D:\Live_Snap\Input\EDX_SHRTCOLL_0313_'+Date+'.CSV'
    MCX1                    =   r'D:\Live_Snap\Input\MCX_PeakMargin56565_'+Date[4:] + Date[2:4] +Date[:2]+'_07.csv'
    NCDX1                   =   r'D:\Live_Snap\Input\CLIENT_EFFECTIVE_DEPOSITS_TM_01274_'+Date+'.csv'
    Snap1                   =   r'D:\Live_Snap\Output\Snap07'+Date+'.csv'
    Snap1_ICCL_Shortage     =   r'D:\Live_Snap\Output\Snap07_ICCL_Shortage'+Date+'.csv'
    Snap1_Total_Shortage    =   r'D:\Live_Snap\Output\Snap07_Total_Shortage'+Date+'.csv'

    
    file_paths = {curr1,EQ1,FO1,MCX1,NCDX1}

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            # Display a warning pop-up message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning("File Not Found", f"The file is not available at: {file_path}.\nPlease ensure the file is available at the specified path.")

    Head                    =   ['Date','Segment','CM Code','TM Code','Client Code','CP Code','Cash','Non Cash Value','Total (Cash+Non Cash)','Margin','Shortage']
    Dtype                   =   {'Date':str,'Segment':str,'CM Code':str,'TM Code':str,'Client Code':str,'CP Code':str,'Cash':float,'Non Cash Value':float,'Total (Cash+Non Cash)':float,'Margin':float,'Shortage':float}
    MCX_head                =   ['Business Date','Snapshot Interval','CM ID','TM ID','CLIENT ID','INTIAL MARGIN','ELM','Net Buy Premium','Total Upfront Margin','Client margin allocation','Client other collaterals','Short allocation']
    NCDX_head               =   ['TM Code/CP Code','Client/CP Code','Cash Equivalent','Securities Cash Component','Total Cash Component','Securities Non cash','Commodities Non Cash','Other Non Cash',
                                'Total Non Cash','Total Collateral (Cash and Non Cash)','Commodities Considered','Total Non Cash Considered','Gross Effective Deposits','Blocked Amount','Net Effective Deposits Before Member Excess Cash ALC',
                                'Excess Cash','Excess Non Cash','Member Cash Allocation Limit','TM Excess Cash Allocation','CM Excess Cash Allocation','Net Effective Deposits After Member Excess Cash ALC','Margin']
    MCX_dtype               =   {'Business Date':str,'Snapshot Interval':str,'CM ID':str,'TM ID':str,'CLIENT ID':str,'INTIAL MARGIN':float,'ELM':float,'Net Buy Premium':float,'Total Upfront Margin':float,'Client margin allocation':float,'Client other collaterals':float,'Short allocation':float}
    curr2                   =   pd.read_csv(curr1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    curr2                   =   curr2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Currency Total','Margin':'Currency Margin','Shortage':'Currency Shortage'})
    EQ2                     =   pd.read_csv(EQ1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    EQ2                     =   EQ2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Equity Total','Margin':'Equity Margin','Shortage':'Equity Shortage'})
    FO2                     =   pd.read_csv(FO1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    FO2                     =   FO2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Future Total','Margin':'Future Margin','Shortage':'Future Shortage'})
    MCX2                    =   pd.read_csv(MCX1,header=None,names=MCX_head,dtype=MCX_dtype,usecols=['CLIENT ID','Client margin allocation','Total Upfront Margin','Short allocation'])
    MCX2                    =   MCX2.rename(columns={'CLIENT ID': 'Client Code', 'Client margin allocation': 'MCX Total', 'Total Upfront Margin': 'MCX Margin', 'Short allocation': 'MCX Shortage'})
    NCDX2                   =   pd.read_csv(NCDX1,header=None,names=NCDX_head,usecols=['Client/CP Code','Total Collateral (Cash and Non Cash)','Margin'])
    NCDX2['NCDX Shortage']  =   NCDX2['Total Collateral (Cash and Non Cash)'] - NCDX2['Margin']
    NCDX3                   =   NCDX2[['Client/CP Code','Total Collateral (Cash and Non Cash)','Margin','NCDX Shortage']]
    NCDX3                   =   NCDX3.rename(columns={'Client/CP Code':'Client Code','Total Collateral (Cash and Non Cash)': 'NCDX Total','Margin':'NCDX Margin','NCDX Shortage': 'NCDX Shortage'})

    merged_df               =   curr2.merge(EQ2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(FO2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(MCX2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(NCDX3, on='Client Code', how='outer')
    merged_df               =   merged_df.fillna(0)


    merged_df.to_csv(Snap1, index=False)

    merged_df['Total Shortage ICCL'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin']) -  (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total'])
    filtered_df = merged_df[merged_df['Total Shortage ICCL'] > 0]
    
    filtered_df.to_csv(Snap1_ICCL_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage ICCL'], index=False)
    
    merged_df['Total Shortage All Seg'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin'] + merged_df['MCX Margin'] + merged_df['NCDX Margin']) - (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total']+merged_df['MCX Total']+merged_df['NCDX Total'])
    
    filtered_df = merged_df[merged_df['Total Shortage All Seg'] > 0]

    filtered_df.to_csv(Snap1_Total_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage All Seg'], index=False)

    print('Snap 7 File Generated to path :-',Snap1)
    input('Press Any Key For Exit........')


elif Command == 8:
    print('Prepraring Report for MCX Snap 8.......')
    
    curr1                   =   r'D:\Live_Snap\Input\CDX_SHRTCOLL_0313_'+Date+'.csv'
    EQ1                     =   r'D:\Live_Snap\Input\EQ_SHRTCOLL_0313_'+Date+'.csv'
    FO1                     =   r'D:\Live_Snap\Input\EDX_SHRTCOLL_0313_'+Date+'.CSV'
    NCDX1                   =   r'D:\Live_Snap\Input\CLIENT_EFFECTIVE_DEPOSITS_TM_01274_'+Date+'.csv'
    MCX1                    =   r'D:\Live_Snap\Input\MCX_PeakMargin56565_'+Date[4:] + Date[2:4] +Date[:2]+'_08.csv'
    Snap1                   =   r'D:\Live_Snap\Output\Snap08'+Date+'.csv'
    Snap1_ICCL_Shortage     =   r'D:\Live_Snap\Output\Snap08_ICCL_Shortage'+Date+'.csv'
    Snap1_Total_Shortage    =   r'D:\Live_Snap\Output\Snap08_Total_Shortage'+Date+'.csv'

    
    file_paths = {curr1,EQ1,FO1,MCX1,NCDX1}

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            # Display a warning pop-up message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning("File Not Found", f"The file is not available at: {file_path}.\nPlease ensure the file is available at the specified path.")


    Head                    =   ['Date','Segment','CM Code','TM Code','Client Code','CP Code','Cash','Non Cash Value','Total (Cash+Non Cash)','Margin','Shortage']
    Dtype                   =   {'Date':str,'Segment':str,'CM Code':str,'TM Code':str,'Client Code':str,'CP Code':str,'Cash':float,'Non Cash Value':float,'Total (Cash+Non Cash)':float,'Margin':float,'Shortage':float}
    MCX_head                =   ['Business Date','Snapshot Interval','CM ID','TM ID','CLIENT ID','INTIAL MARGIN','ELM','Net Buy Premium','Total Upfront Margin','Client margin allocation','Client other collaterals','Short allocation']
    MCX_dtype               =   {'Business Date':str,'Snapshot Interval':str,'CM ID':str,'TM ID':str,'CLIENT ID':str,'INTIAL MARGIN':float,'ELM':float,'Net Buy Premium':float,'Total Upfront Margin':float,'Client margin allocation':float,'Client other collaterals':float,'Short allocation':float}
    NCDX_head               =   ['TM Code/CP Code','Client/CP Code','Cash Equivalent','Securities Cash Component','Total Cash Component','Securities Non cash','Commodities Non Cash','Other Non Cash',
                                'Total Non Cash','Total Collateral (Cash and Non Cash)','Commodities Considered','Total Non Cash Considered','Gross Effective Deposits','Blocked Amount','Net Effective Deposits Before Member Excess Cash ALC',
                                'Excess Cash','Excess Non Cash','Member Cash Allocation Limit','TM Excess Cash Allocation','CM Excess Cash Allocation','Net Effective Deposits After Member Excess Cash ALC','Margin']
    curr2                   =   pd.read_csv(curr1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    curr2                   =   curr2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Currency Total','Margin':'Currency Margin','Shortage':'Currency Shortage'})
    EQ2                     =   pd.read_csv(EQ1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    EQ2                     =   EQ2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Equity Total','Margin':'Equity Margin','Shortage':'Equity Shortage'})
    FO2                     =   pd.read_csv(FO1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    FO2                     =   FO2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Future Total','Margin':'Future Margin','Shortage':'Future Shortage'})

    NCDX2                   =   pd.read_csv(NCDX1,header=None,names=NCDX_head,usecols=['Client/CP Code','Total Collateral (Cash and Non Cash)','Margin'])
    NCDX2['NCDX Shortage']  =   NCDX2['Total Collateral (Cash and Non Cash)'] - NCDX2['Margin']
    NCDX3                   =   NCDX2[['Client/CP Code','Total Collateral (Cash and Non Cash)','Margin','NCDX Shortage']]
    NCDX3                   =   NCDX3.rename(columns={'Client/CP Code':'Client Code','Total Collateral (Cash and Non Cash)': 'NCDX Total','Margin':'NCDX Margin','NCDX Shortage': 'NCDX Shortage'})
    MCX2                    =   pd.read_csv(MCX1,header=None,names=MCX_head,dtype=MCX_dtype,usecols=['CLIENT ID','Client margin allocation','Total Upfront Margin','Short allocation'])
    MCX2                    =   MCX2.rename(columns={'CLIENT ID': 'Client Code', 'Client margin allocation': 'MCX Total', 'Total Upfront Margin': 'MCX Margin', 'Short allocation': 'MCX Shortage'})

    merged_df               =   curr2.merge(EQ2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(FO2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(MCX2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(NCDX3, on='Client Code', how='outer')
    merged_df               =   merged_df.fillna(0)
    
    merged_df.to_csv(Snap1, index=False)

    merged_df['Total Shortage ICCL'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin']) -  (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total'])
    filtered_df = merged_df[merged_df['Total Shortage ICCL'] > 0]
    
    filtered_df.to_csv(Snap1_ICCL_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage ICCL'], index=False)
    
    merged_df['Total Shortage All Seg'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin'] + merged_df['MCX Margin'] + merged_df['NCDX Margin']) - (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total']+merged_df['MCX Total']+merged_df['NCDX Total'])
    
    filtered_df = merged_df[merged_df['Total Shortage All Seg'] > 0]

    filtered_df.to_csv(Snap1_Total_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage All Seg'], index=False)

    print('Snap 8 File Generated to path :-',Snap1)
    input('Press Any Key For Exit........')

elif Command==9:
    print('Prepraring EOD Report Of all Segment.......')
    curr1                   =   r'D:\Live_Snap\Input\CDX_SHRTCOLL_0313_'+Date+'.csv'
    EQ1                     =   r'D:\Live_Snap\Input\EQ_SHRTCOLL_0313_'+Date+'.csv'
    FO1                     =   r'D:\Live_Snap\Input\EDX_SHRTCOLL_0313_'+Date+'.CSV'
    NCDX1                   =   r'D:\Live_Snap\Input\CLIENT_EFFECTIVE_DEPOSITS_TM_01274_'+Date+'.csv'
    MCX1                    =   r'D:\Live_Snap\Input\MCX_WebAllocationDeallocation56565_'+Date[4:] + Date[2:4] +Date[:2]+'.csv'
    Snap1                   =   r'D:\Live_Snap\Output\Final_EOD_File'+Date+'.csv'
    Snap1_Total_Shortage    =   r'D:\Live_Snap\Output\Final_EOD_Total_Shortage'+Date+'.csv'
    Snap1_ICCL_Shortage     =   r'D:\Live_Snap\Output\Final_EOD_ICCL_Shortage'+Date+'.csv'

    
    file_paths = {curr1,EQ1,FO1,MCX1,NCDX1}

    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            # Display a warning pop-up message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showwarning("File Not Found", f"The file is not available at: {file_path}.\nPlease ensure the file is available at the specified path.")

    
    Head                    =   ['Date','Segment','CM Code','TM Code','Client Code','CP Code','Cash','Non Cash Value','Total (Cash+Non Cash)','Margin','Shortage']
    Dtype                   =   {'Date':str,'Segment':str,'CM Code':str,'TM Code':str,'Client Code':str,'CP Code':str,'Cash':float,'Non Cash Value':float,'Total (Cash+Non Cash)':float,'Margin':float,'Shortage':float}    
    NCDX_head               =   ['TM Code/CP Code','Client/CP Code','Cash Equivalent','Securities Cash Component','Total Cash Component','Securities Non cash','Commodities Non Cash','Other Non Cash',
                                'Total Non Cash','Total Collateral (Cash and Non Cash)','Commodities Considered','Total Non Cash Considered','Gross Effective Deposits','Blocked Amount','Net Effective Deposits Before Member Excess Cash ALC',
                                'Excess Cash','Excess Non Cash','Member Cash Allocation Limit','TM Excess Cash Allocation','CM Excess Cash Allocation','Net Effective Deposits After Member Excess Cash ALC','Margin']    
    MCX_head1                =   ['Clearing Member Code','Trading Member Code','Client Code','Allocation at BOD','Allocations during the Day','Deallocation during the Day','Allocation at EOD',
                                'Own Collateral at BOD','Own Collateral added during Day','Own Collateral reduced during Day','Own Collateral EOD','Own Others Collateral at BOD','Own Other Collateral added during Day',
                                'Own Other Collateral  reduced during Day','Own Others Collateral at EOD','MCX Total','Eligible collateral at EOD','MCX Margin','MCX Shortage']
    
    curr2                   =   pd.read_csv(curr1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    curr2                   =   curr2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Currency Total','Margin':'Currency Margin','Shortage':'Currency Shortage'})
    EQ2                     =   pd.read_csv(EQ1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    EQ2                     =   EQ2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Equity Total','Margin':'Equity Margin','Shortage':'Equity Shortage'})
    FO2                     =   pd.read_csv(FO1,header=None,names=Head,dtype=Dtype,usecols=['Client Code','Total (Cash+Non Cash)','Margin','Shortage'])
    FO2                     =   FO2.rename(columns={'Client Code':'Client Code','Total (Cash+Non Cash)':'Future Total','Margin':'Future Margin','Shortage':'Future Shortage'})

    NCDX2                   =   pd.read_csv(NCDX1,header=None,names=NCDX_head,usecols=['Client/CP Code','Total Collateral (Cash and Non Cash)','Margin'])
    NCDX2['NCDX Shortage']  =   NCDX2['Margin'] - NCDX2['Total Collateral (Cash and Non Cash)']
    NCDX3                   =   NCDX2[['Client/CP Code','Total Collateral (Cash and Non Cash)','Margin','NCDX Shortage']]
    NCDX3                   =   NCDX3.rename(columns={'Client/CP Code':'Client Code','Total Collateral (Cash and Non Cash)': 'NCDX Total','Margin':'NCDX Margin','NCDX Shortage': 'NCDX Shortage'})
    
    MCX2                    =   pd.read_csv(MCX1,header=None, names=MCX_head1, usecols=['Client Code','MCX Total','MCX Margin'])
    MCX2['MCX Shortage']    =   MCX2['MCX Margin'] - MCX2['MCX Total']
    MCX3                    =   MCX2[['Client Code','MCX Total','MCX Margin','MCX Shortage']]
    

    merged_df               =   curr2.merge(EQ2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(FO2, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(MCX3, on='Client Code', how='outer')
    merged_df               =   merged_df.merge(NCDX3, on='Client Code', how='outer')
    merged_df               =   merged_df.fillna(0)
    
    merged_df.to_csv(Snap1, index=False)

    merged_df['Total Shortage ICCL'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin']) -  (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total'])
    filtered_df = merged_df[merged_df['Total Shortage ICCL'] > 0]
    
    filtered_df.to_csv(Snap1_ICCL_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage ICCL'], index=False)
    
    merged_df['Total Shortage All Seg'] = (merged_df['Currency Margin'] + merged_df['Equity Margin'] + merged_df['Future Margin'] + merged_df['MCX Margin'] + merged_df['NCDX Margin']) - (merged_df['Currency Total']+merged_df['Equity Total']+merged_df['Future Total']+merged_df['MCX Total']+merged_df['NCDX Total'])
    
    filtered_df = merged_df[merged_df['Total Shortage All Seg'] > 0]

    filtered_df.to_csv(Snap1_Total_Shortage,columns=['Client Code','Currency Shortage','Equity Shortage','Future Shortage','MCX Shortage','NCDX Shortage','Total Shortage All Seg'], index=False)


    print('Final EOQ File Generated to path :-',Snap1)
    
    input('Press Any Key For Exit........')



















    