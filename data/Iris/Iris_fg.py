import numpy as np
import scipy as sp
iris=open("C:\Users\YAN\Desktop\data\Iris\Iris.txt")
D=[]
for line in iris:
    D.append(line.split(',',4))

data=np.array(D)
data=data[:150]
data.reshape(150,1)
data1=[]
data2=[]
for i in range(150):
    data1.append([float(data[i][0]),float(data[i][1]),float(data[i][2]),float(data[i][3])])
    data2.append(data[i][4])

data_att=np.array(data1)
data_labels=np.array(data2)
for i in range(150):
    if (data_labels[i]== 'Iris-setosa\n' ):
        data_labels[i]=0
    elif (data_labels[i]== 'Iris-versicolor\n' ):
        data_labels[i]=1
    elif (data_labels[i]== 'Iris-virginica\n' ):
        data_labels[i]=2
    else:
        print("错误！")

print("特征数据---------------------------")
print data_att
print( "特征数据大小：")
print data_att.shape
print("labels数据--------------------------")
print data_labels
print("labels数据的大小：")
print data_labels.shape 



    
    
