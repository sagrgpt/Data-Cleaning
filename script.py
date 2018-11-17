import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# Reading the main dataset
dataset1 = pd.read_excel('rate_sheet.xlsx','Table 1')
del dataset1['Country']
del dataset1['ROUTING']
dataset1['special remarks'] = dataset1['special remarks'].fillna('')
dataset1['remarks'] += ' '+dataset1['special remarks']
del dataset1['special remarks']
#converting the dataset to numpy array for further processing
# ['TRADE', 'POL ', 'POD CODE', 'POD', 'TT', '20'Ft', '40'Ft', '40'HC', 'remarks', 'VALIDITY']
rate_sheet = np.array(dataset1)

#Reading the secondary dataset
dataset2 = pd.read_csv("lookup (3).csv",names=['p_name','p_code','country'])
# ['port_name', 'port_code', 'country']
# remove duplicate port entry
dataset2 = dataset2.drop_duplicates(subset="p_code")
#converting the dataset to numpy array for further processing
lookup = np.array(dataset2)


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
# invalid_port = np.delete(invalid_port,(0), axis=0)
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
                data = np.array([count,lookup[index[0],1][0],rate_sheet[i,2],rate_sheet[i,5],rate_sheet[i,6],rate_sheet[i,7],rate_sheet[i,8], rate_sheet[i,0],rate_sheet[i,4],rate_sheet[i,9]])
                final = np.vstack((final,data))

df = pd.DataFrame(final)
df.columns = ['s.No', 'POL', 'POD', '20ft', '40ft', '40HC', 'All Remarks', 'Trade', 'TT', 'Validity']
df.to_csv('final_sheet.csv',index=False)