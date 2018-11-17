import pandas as pd
import numpy as np

import dataclean
df1 = dataclean.processMainDataset()
# print(df1.columns)
# print(df1.head())

df2 = dataclean.processLookupDataset()
# print(df2.columns)
# print(df2.shape)

#creating the required np array
rate_sheet = np.array(df1)
lookup = np.array(df2)
#Reading the expected resultant dataset
dataset3 = pd.read_excel("rate_sheet.xlsx","Sheet3")
#converting the resultant dataset to numpy array for further processing
final = np.array(dataset3)
val = (int) (final[0].shape[0])
final = np.delete(final,slice(0,val),axis = 0)
#numpy array to store invalid port number
invalid_port = np.array([])
list1 = np.array(['ABC', 000])
invalid_port = np.hstack((invalid_port, list1))
count = 0
for i in range(0,len(rate_sheet)):
    pod_avail = True
    index = np.where(lookup == rate_sheet[i,2]) #get the index of POD_CODE from lookup
    if not lookup[index]:
        #if POD_CODE is not available in Lookup
        pod_avail = False
        #add Port into invalid sheet
        invalid_port = np.vstack((invalid_port, np.array([rate_sheet[i,2],i+1])))
    rate_sheet[i,1] = rate_sheet[i,1].replace('\n',' ')     #Treating values of POL as multivariable
    for pol in rate_sheet[i,1].split('/'):
        index = np.where(lookup == pol) #get the index of individual POL from lookup
        if not lookup[index]:
            #if POL is not available in Lookup
            invalid_port = np.vstack((invalid_port, np.array([pol,i+1])))
        else:#if both are available in Lookup
            if pod_avail:
                count +=1
                # ['TRADE', 'POL ', 'POD CODE', 'TT', '20'Ft', '40'Ft', '40'HC', 'remarks','VALIDITY']
                data = np.array([count,lookup[index[0],1][0],rate_sheet[i,2],rate_sheet[i,4],rate_sheet[i,5],rate_sheet[i,6],rate_sheet[i,7], rate_sheet[i,0],rate_sheet[i,3],rate_sheet[i,8]])
                final = np.vstack((final,data))

df = pd.DataFrame(final)
df.columns = ['s.No', 'POL', 'POD', '20ft', '40ft', '40HC', 'All Remarks', 'Trade', 'TT', 'Validity']
df.to_excel('result_file.xlsx',index=False)
invalid_port = np.delete(invalid_port,(0), axis=0) #removing the dummy value
df = pd.DataFrame(invalid_port)
df.columns = ['Port not Found', 'Position']
df.to_excel('missing_port_file.xlsx',index = False)