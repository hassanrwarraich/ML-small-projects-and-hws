# -*- coding: utf-8 -*-
"""hw2_ml.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UOmfWOPIpvwFpu0o3fVoYOmS4pGFxmPs
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from numpy import genfromtxt
from io import StringIO
import csv
import math
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import seaborn as sns
# %matplotlib inline
import matplotlib.pyplot as plt 
import scipy.io as sio
from sklearn.utils import shuffle
from sklearn.svm import SVC
import time
import random

!unzip datasets.zip
!unzip q1_dataset.zip

print("-----part 1-------------------------")
images = []
for filename in os.listdir("van_gogh"):
  img = np.array(Image.open(os.path.join("van_gogh",filename)))
  #img = (cv2.imread(os.path.join("van_gogh",filename),-1))
  if (img.ndim) == 2:
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    np.expand_dims(img, axis=0) 
  images.append(img)

#images = np.array(images)
X = []
for img in images:
  g = img
  g = g.flatten().reshape(4096, 3)
  X.append(g)
X = np.array(X)
X1 = X[:,:,0]
X2 = X[:,:,1]
X3 = X[:,:,2]

Ur, sr, Vr = np.linalg.svd(X1)

Ug, sg, Vg = np.linalg.svd(X2)

Ub, sb, Vb = np.linalg.svd(X3)

sr_100 = sr[0:100]
sb_100 = sb[0:100]
sg_100 = sg[0:100] 
x_axis = np.arange(100)  
   
fig = plt.figure(figsize = (9, 5)) 
plt.bar(x_axis, sr_100, color ='grey',  width = 0.5)  
plt.ylabel("Singular values") 
plt.title("Red color") 
plt.show()

   
fig = plt.figure(figsize = (9, 5)) 
plt.bar(x_axis, sb_100, color ='grey',  width = 0.5)  
plt.ylabel("Singular values") 
plt.title("Blue color") 
plt.show() 

   
fig = plt.figure(figsize = (9, 5)) 
plt.bar(x_axis, sg_100, color ='grey',  width = 0.5)  
plt.ylabel("Singular values") 
plt.title("green color") 
plt.show() 

var_explained = sr**2/np.sum(sr**2)
top_ten = var_explained[0:10]
print("Variance explained For Red")
print(top_ten)

var_explained = sb**2/np.sum(sb**2)
top_ten = var_explained[0:10]
print("Variance explained For Blue")
print(top_ten)

var_explained = sg**2/np.sum(sg**2)
top_ten = var_explained[0:10]
print("Variance explained For green")
print(top_ten)

mean_images = np.mean(np.array(images), axis=0)
var_images = np.var(np.array(images), axis=0)
noisy_images = images[:] + np.random.normal(mean_images, np.sqrt(var_images), np.shape(mean_images))*0.01

Xn = []
for img in noisy_images:
  g = img
  g = g.flatten().reshape(4096, 3)
  Xn.append(g)
Xn = np.array(Xn)
X1n = Xn[:,:,0]
X2n = Xn[:,:,1]
X3n = Xn[:,:,2]

Ur, sr, Vr = np.linalg.svd(X1n)

Ug, sg, Vg = np.linalg.svd(X2n)

Ub, sb, Vb = np.linalg.svd(X3n)

sr_100 = sr[0:100]
sb_100 = sb[0:100]
sg_100 = sg[0:100] 
x_axis = np.arange(100)  
   
fig = plt.figure(figsize = (9, 5)) 
plt.bar(x_axis, sr_100, color ='grey',  width = 0.5)  
plt.ylabel("Singular values") 
plt.title("Red color") 
plt.show()

   
fig = plt.figure(figsize = (9, 5)) 
plt.bar(x_axis, sb_100, color ='grey',  width = 0.5)  
plt.ylabel("Singular values") 
plt.title("Blue color") 
plt.show() 

   
fig = plt.figure(figsize = (9, 5)) 
plt.bar(x_axis, sg_100, color ='grey',  width = 0.5)  
plt.ylabel("Singular values") 
plt.title("green color") 
plt.show() 

var_explained = sr**2/np.sum(sr**2)
top_ten = var_explained[0:10]
print("Variance explained For Red")
print(top_ten)

var_explained = sb**2/np.sum(sb**2)
top_ten = var_explained[0:10]
print("Variance explained For Blue")
print(top_ten)

var_explained = sg**2/np.sum(sg**2)
top_ten = var_explained[0:10]
print("Variance explained For green")
print(top_ten)

####################################
#part2
#####################################
print("-----part 2-------------------------")
datafile = open('q2_dataset.csv', 'r')
datareader = csv.reader(datafile)
students = []
i = 0;
for row in datareader:
  i+=1;
  if(i>1):
    students.append(row)

x = 0
y = 0
for i in students:
  for j in i:
    students[x][y] = float(students[x][y])
    y+=1
  x+=1
  y = 0
students = np.array(students)
np.random.shuffle(students)
students_f = students[:, :-1]
students_labels = students[:,-1]


x = []
for i in range(0,5):
  trainF = students_f
  trainL = students_labels
  arr = np.arange(int(i*100),int((i+1)*100))
  trainF = np.delete(trainF, arr, 0)
  trainL = np.delete(trainL, arr, 0)
  g = trainF.transpose()
  w = np.matmul(g, trainF)
  w = np.matmul(np.linalg.inv(w), g)
  w = np.matmul(w, trainL)
  x.append(w)

for i in range(0,5):
  testF = students_f[i*100:(i+1)*100]
  testL = students_labels[i*100:(i+1)*100]
  testF = np.array(testF)
  testL = np.array(testL)
  predicted = (testF * np.array(x[i])).sum(axis=1)
  predicted = np.array(predicted)
  print("for fold ",i," as test")
  d = (testL) - (predicted)
  r2_f = 1-(sum(d**2)/sum(((testL)-np.mean(testL))**2))
  print("R square: ", r2_f)
  mse_f = np.mean(d**2)
  print("Mean squared error: ", mse_f)
  mae_f = np.mean(abs(d))
  print("Mean absolute error: ", mae_f)
  M = ((np.abs(d/testL)).sum(axis=0)) / len(testL)
  print("Mean absolute percentage error: ", M)




########################################
#part3
########################################
print("-----part 3-------------------------")
datafile = open('q3_train_dataset.csv', 'r')
datareader = csv.reader(datafile)
passengers = []
i = 0;
for row in datareader:
  i+=1;
  if(i>1):
    passengers.append(row)

x = 0
for i in passengers:
  if passengers[x][2] == "male":
    passengers[x][2] = 1
  else:
    passengers[x][2] = 0
  if passengers[x][7] == "S":
    passengers[x][7] = 0
  elif passengers[x][7] == "C":
    passengers[x][7] = 1
  elif passengers[x][7] == "Q":
    passengers[x][7] = 2
  x+=1

x = 0
y = 0
for i in passengers:
  for j in i:
    passengers[x][y] = float(passengers[x][y])
    y+=1
  x+=1
  y = 0

passengers = np.array(passengers)
np.random.shuffle(passengers)
passengers_f = passengers[:, 1:]
passengers_labels = passengers[:,0:1]

t1 = time.time()

wese = [-4,-3,-2]
nikal = []
for i in wese:
  w = np.random.normal(scale = 0.01 , size = 8)
  for j in range(0,1000):
    temp = passengers_f.shape[0]/32
    rando = random.randint(0, int(temp)-1)
    begin = rando*32
    end = (rando+1)*32
    Lpy1 = np.zeros(32)

    new = np.sum(w[1:8]*passengers_f[begin:end, :], axis = 1)
    exps = np.exp(w[0]+ new)
      
    py1 = np.zeros(passengers_f.shape[0])

    py1[begin:end] = exps/(1 + exps)
     
    Lpy1 = ((passengers_labels)[begin:end,0])-py1[begin:end]
    w_t = ((10**i)*(np.sum(Lpy1)))/32
    w[0] = w[0] + w_t
    Lpy1 = np.reshape(Lpy1, (-1,32))
    Ls2_t = np.repeat(Lpy1, 7, axis =0)
    Ls2 = np.transpose(Ls2_t)
    g_t = (10**i)*np.reshape(np.sum(passengers_f[begin:end,:]*Ls2 , axis = 0), (-1,7))
    w[1:] = w[1:] + g_t/32
  nikal.append(w)

t0 = time.time()

####################testing##########
datafile = open('q3_test_dataset.csv', 'r')
datareader = csv.reader(datafile)
test_passengers = []
i = 0;
for row in datareader:
  i+=1;
  if(i>1):
    test_passengers.append(row)

x = 0
for i in test_passengers:
  if test_passengers[x][2] == "male":
    test_passengers[x][2] = 1
  else:
    test_passengers[x][2] = 0
  if test_passengers[x][7] == "S":
    test_passengers[x][7] = 0
  elif test_passengers[x][7] == "C":
    test_passengers[x][7] = 1
  elif test_passengers[x][7] == "Q":
    test_passengers[x][7] = 2
  x+=1

x = 0
y = 0
for i in test_passengers:
  for j in i:
    test_passengers[x][y] = float(test_passengers[x][y])
    y+=1
  x+=1
  y = 0

test_passengers = np.array(test_passengers)
test_passengers_f = test_passengers[:, 1:]
test_passengers_labels = test_passengers[:,0:1]

great = 0
ind = 0
w1 = nikal[0]
w2 = nikal[1]
w3 = nikal[2]

labl1 = np.zeros(8)
labl1 = (w1[0]+np.sum(w1[1:]*test_passengers_f,axis=1))>0
a1 = (np.sum(labl1 == test_passengers_labels[:,0])/test_passengers_f.shape[0])*100

labl2 = np.zeros(8)
labl2 = (w2[0]+np.sum(w2[1:]*test_passengers_f,axis=1))>0
a2 = (np.sum(labl2 == test_passengers_labels[:,0])/test_passengers_f.shape[0])*100

labl3 = np.zeros(8)
labl3 = (w3[0]+np.sum(w3[1:]*test_passengers_f,axis=1))>0
a3 = (np.sum(labl3 == test_passengers_labels[:,0])/test_passengers_f.shape[0])*100

labl = [labl1,labl2,labl3]
garam = [a1,a2,a3]
chor = np.argmax(garam)
accuraci = np.max(garam)
labl =  labl[chor]
print("The learning rate choosen is: 10 to power ",wese[chor])
print("-----minibatch gradient ascent----------------")
print('Time for minibatch gradient ascent training: ', t0-t1)


TP = np.sum(test_passengers_labels[labl[:]==0,0]==0)
TN = np.sum(test_passengers_labels[labl[:]==1,0]==1)
FP = np.sum(test_passengers_labels[labl[:]==1,0]==0)
FN = np.sum(test_passengers_labels[labl[:]==0,0]==1)

Prec = TP/(TP+FP)
Rec = TP/(TP+FN)
NPV = TN/(TN+FN)
FPR = FP/(TN+FP)
FDR = FP/(FP+TP)
F1 = (2*Prec*Rec)/(Prec+Rec)
F2 = (5*Prec*Rec)/(4*Prec +Rec)
confusionmtarix = np.zeros((2,2))
confusionmtarix[0,0] = TP
confusionmtarix[1,1] = TN
confusionmtarix[0,1] = FP
confusionmtarix[1,0] = FN
classP = TP/(TP+FP)
classN  = TN/(TN+FN)
print('Class based accuracy for P class: ', classP)
print('Class based accuracy for N class: ', classN)
print('Accuracy: ', accuraci)
print('Precision: ', Prec)
print('Recall: ', Rec)
print('NPV: ', NPV )
print('FPR: ', FPR)
print('FDR: ', FDR)
print('F1: ', F1)
print('F2: ', F2)
print('Confusion Matrix:   ') 
print(confusionmtarix)

print("-----stochastic gradient ascent----------------")
t1 = time.time()
w = np.random.normal(scale = 0.01 , size = 8)
for j in range(0,1000):
  temp = passengers_f.shape[0]
  rando = random.randint(0, int(temp)-1)
  begin = rando
  end = (rando+1)
  Lpy1 = np.zeros(1)

  new = np.sum(w[1:8]*passengers_f[begin:end, :], axis = 1)
  exps = np.exp(w[0]+ new)
      
  py1 = np.zeros(passengers_f.shape[0])

  py1[begin:end] = exps/(1 + exps)
     
  Lpy1 = ((passengers_labels)[begin:end,0])-py1[begin:end]
  w_t = ((10**wese[chor])*(np.sum(Lpy1)))
  w[0] = w[0] + w_t
  Lpy1 = np.reshape(Lpy1, (-1,1))
  Ls2_t = np.repeat(Lpy1, 7, axis =0)
  Ls2 = np.transpose(Ls2_t)
  g_t = (10**wese[chor])*np.reshape(np.sum(passengers_f[begin:end,:]*Ls2 , axis = 0), (-1,7))
  w[1:] = w[1:] + g_t

t0 = time.time()
print('Time for stochastic gradient ascent training: ', t0-t1)
labl = np.zeros(8)
labl = (w[0]+np.sum(w[1:]*test_passengers_f,axis=1))>0
accuraci = (np.sum(labl == test_passengers_labels[:,0])/test_passengers_f.shape[0])*100



TP = np.sum(test_passengers_labels[labl[:]==0,0]==0)
TN = np.sum(test_passengers_labels[labl[:]==1,0]==1)
FP = np.sum(test_passengers_labels[labl[:]==1,0]==0)
FN = np.sum(test_passengers_labels[labl[:]==0,0]==1)

Prec = TP/(TP+FP)
Rec = TP/(TP+FN)
NPV = TN/(TN+FN)
FPR = FP/(TN+FP)
FDR = FP/(FP+TP)
F1 = (2*Prec*Rec)/(Prec+Rec)
F2 = (5*Prec*Rec)/(4*Prec +Rec)
confusionmtarix = np.zeros((2,2))
confusionmtarix[0,0] = TP
confusionmtarix[1,1] = TN
confusionmtarix[0,1] = FP
confusionmtarix[1,0] = FN
classP = TP/(TP+FP)
classN  = TN/(TN+FN)
print('Class based accuracy for P class: ', classP)
print('Class based accuracy for N class: ', classN)
print('Accuracy: ', accuraci)
print('Precision: ', Prec)
print('Recall: ', Rec)
print('NPV: ', NPV )
print('FPR: ', FPR)
print('FDR: ', FDR)
print('F1: ', F1)
print('F2: ', F2)
print('Confusion Matrix:   ') 
print(confusionmtarix)

print("-----Full Batch gradient ascent----------------")
t1 = time.time()
w = np.random.normal(scale = 0.01 , size = 8)
for j in range(0,1000):
  temp = passengers_f.shape[0]/passengers_f.shape[0]
  rando = random.randint(0, int(temp)-1)
  begin = rando*passengers_f.shape[0]
  end = (rando+1)*passengers_f.shape[0]
  Lpy1 = np.zeros(passengers_f.shape[0])

  new = np.sum(w[1:8]*passengers_f[begin:end, :], axis = 1)
  exps = np.exp(w[0]+ new)
      
  py1 = np.zeros(passengers_f.shape[0])

  py1[begin:end] = exps/(1 + exps)
     
  Lpy1 = ((passengers_labels)[begin:end,0])-py1[begin:end]
  w_t = ((10**wese[chor])*(np.sum(Lpy1)))/passengers_f.shape[0]
  w[0] = w[0] + w_t
  Lpy1 = np.reshape(Lpy1, (-1,passengers_f.shape[0]))
  Ls2_t = np.repeat(Lpy1, 7, axis =0)
  Ls2 = np.transpose(Ls2_t)
  g_t = (10**wese[chor])*np.reshape(np.sum(passengers_f[begin:end,:]*Ls2 , axis = 0), (-1,7))
  w[1:] = w[1:] + g_t/passengers_f.shape[0]
  print("weights for iteration ",j," are: ",w)

t0 = time.time()
print('Time for fullbatch gradient ascent training: ', t0-t1)
labl = np.zeros(8)
labl = (w[0]+np.sum(w[1:]*test_passengers_f,axis=1))>0
accuraci = (np.sum(labl == test_passengers_labels[:,0])/test_passengers_f.shape[0])*100


TP = np.sum(test_passengers_labels[labl[:]==0,0]==0)
TN = np.sum(test_passengers_labels[labl[:]==1,0]==1)
FP = np.sum(test_passengers_labels[labl[:]==1,0]==0)
FN = np.sum(test_passengers_labels[labl[:]==0,0]==1)

Prec = TP/(TP+FP)
Rec = TP/(TP+FN)
NPV = TN/(TN+FN)
FPR = FP/(TN+FP)
FDR = FP/(FP+TP)
F1 = (2*Prec*Rec)/(Prec+Rec)
F2 = (5*Prec*Rec)/(4*Prec +Rec)
confusionmtarix = np.zeros((2,2))
confusionmtarix[0,0] = TP
confusionmtarix[1,1] = TN
confusionmtarix[0,1] = FP
confusionmtarix[1,0] = FN
classP = TP/(TP+FP)
classN  = TN/(TN+FN)
print('Class based accuracy for P class: ', classP)
print('Class based accuracy for N class: ', classN)
print('Accuracy: ', accuraci)
print('Precision: ', Prec)
print('Recall: ', Rec)
print('NPV: ', NPV )
print('FPR: ', FPR)
print('FDR: ', FDR)
print('F1: ', F1)
print('F2: ', F2)
print('Confusion Matrix:   ') 
print(confusionmtarix)
 
  


########################################
#part4
########################################
print("-----part 4a-------------------------")
data = sio.loadmat('q4_dataset.mat', squeeze_me=False, chars_as_strings=False, mat_dtype=True, struct_as_record=True)

inception_f = data['inception_features']
images = data['images']
labels = data['class_labels']

images = np.array(images)
labels = np.array(labels).ravel()
inception_f = np.array(inception_f)

inc_len = len(inception_f)/5
lab_len = len(labels)/5

images, labels, inception_f = shuffle(images, labels, inception_f)

t1 = time.time()

wese = [-6,-4,-2,0,1,10]
meanacc = np.zeros(6)
gg = 0
for val in wese:
  ix = 0 
  accu = np.zeros(5)
  for i in range(0,5):
    trainI = inception_f
    trainL = labels
    if (i==4):
      arr = np.arange(0, int(inc_len))
      arr1 = np.arange( int(i*inc_len), int((i+1)*inc_len))
      arr = np.append(arr,arr1)
    else:
      arr = np.arange(int(i*inc_len),int((i+2)*inc_len))
      
    
    trainI = np.delete(trainI, arr, 0)
    trainL = np.delete(trainL, arr, 0)
    
    svclassifier = SVC(kernel="linear", C = 10**(val))
    svclassifier.fit(trainI, trainL)
    
    if (i != 4):
      valI = inception_f[(i+1)*int(inc_len):(i+2)*int(inc_len)]
      valL = labels[(i+1)*int(lab_len):(i+2)*int(lab_len)]
    else:
      valI = inception_f[:int(inc_len)]
      valL = labels[:int(lab_len)]
    y_pred = svclassifier.predict(valI)
    accu[ix] = (np.sum(y_pred[:]== valL[:] ))/valL.shape
    
    ix+=1
  meanacc[gg] = np.mean(accu)
  print("mean accuracy for c value 10 to power ", val ," : ",meanacc[gg]*100)
  gg+=1

highest = 0
index = 0
for i in range(0,6):
  if meanacc[i]> highest:
    highest = meanacc[i]
    index = i

print("highest accuracy is for c value: ", wese[index])
ix = 0 
accu = np.zeros(5)
val = wese[index]

for i in range(0,5):
  trainI = inception_f
  trainL = labels
  
  arr = np.arange(int(i*inc_len),int((i+1)*inc_len))
       
  trainI = np.delete(trainI, arr, 0)
  trainL = np.delete(trainL, arr, 0)
    
  svclassifier = SVC(kernel="linear", C = 10**(val))
  svclassifier.fit(trainI, trainL)

  valI = inception_f[(i)*int(inc_len):(i+1)*int(inc_len)]
  valL = labels[(i)*int(lab_len):(i+1)*int(lab_len)]
 
  y_pred = svclassifier.predict(valI)
  accu[ix] = (np.sum(y_pred[:]== valL[:] ))/valL.shape    
  print("accuracy for selected c is : ",accu[ix]*100)
  ix+=1
  
haha = accu
highest = 0
index = 0
hahahaI = 0
for i in range(0,5):
  if accu[i]> highest:
    highest = accu[i]
    index = i
    hahahaI = i
print("highest accuracy is :", highest*100," for test : ", index)

t0 = time.time()
print('Time for running part 4a: ', t0-t1,"seconds")
  
print("-----part 4b-------------------------")
t1 = time.time()

wese = [-4,-2,0,1,10]
gam = [10**-4,10**-2,10**0,10**2,10**10,'scale']
meanacc = np.zeros(30).reshape(6,5)
gg = 0
ss = 0
for g in gam:
  for val in wese:
    ix = 0 
    accu = np.zeros(5)
    for i in range(0,5):
      trainI = inception_f
      trainL = labels
      if (i==4):
        arr = np.arange(0, int(inc_len))
        arr1 = np.arange( int(i*inc_len), int((i+1)*inc_len))
        arr = np.append(arr,arr1)
      else:
        arr = np.arange(int(i*inc_len),int((i+2)*inc_len))
        
      
      trainI = np.delete(trainI, arr, 0)
      trainL = np.delete(trainL, arr, 0)
      
      svclassifier = SVC(kernel="rbf", gamma = g, C = 10**(val))
      svclassifier.fit(trainI, trainL)
      
      if (i != 4):
        valI = inception_f[(i+1)*int(inc_len):(i+2)*int(inc_len)]
        valL = labels[(i+1)*int(lab_len):(i+2)*int(lab_len)]
      else:
        valI = inception_f[:int(inc_len)]
        valL = labels[:int(lab_len)]
      y_pred = svclassifier.predict(valI)
      accu[ix] = (np.sum(y_pred[:]== valL[:] ))/valL.shape
      
      ix+=1
    meanacc[ss][gg] = np.mean(accu)
    print("mean accuracy for c value 10 to power ", val ,"and gamma ",g," is : ",meanacc[ss][gg]*100)
    gg+=1
  ss+=1
  gg=0


highest = 0
indexI = 0
indexJ = 0
for i in range(0,6):
  for j in range(0,5):
    if meanacc[i][j] > highest:
      highest = meanacc[i][j]
      indexI = i
      indexJ = j

print("highest accuracy is for c value: 10 to power", wese[indexJ]," and gamma: ",gam[indexI])
val = wese[indexJ]
gVal = gam[indexI]


ix = 0 
accu = np.zeros(5)

for i in range(0,5):
  trainI = inception_f
  trainL = labels
  
  arr = np.arange(int(i*inc_len),int((i+1)*inc_len))
       
  trainI = np.delete(trainI, arr, 0)
  trainL = np.delete(trainL, arr, 0)
    
  svclassifier = SVC(kernel="rbf", gamma = gVal, C = 10**(val))
  svclassifier.fit(trainI, trainL)

  valI = inception_f[(i)*int(inc_len):(i+1)*int(inc_len)]
  valL = labels[(i)*int(lab_len):(i+1)*int(lab_len)]
 
  y_pred = svclassifier.predict(valI)
  accu[ix] = (np.sum(y_pred[:]== valL[:] ))/valL.shape    
  print("accuracy for selected c and gamma is : ",accu[ix]*100)
  ix+=1
 
  
highest = 0
index = 0
hahaI = 0
for i in range(0,5):
  if accu[i]> highest:
    highest = accu[i]
    hahaI = i
    index = i

print("highest accuracy is :", highest*100," for test : ", index)

t0 = time.time()
print('Time for running part 4b: ', t0-t1,"seconds")


data = [haha, accu]   
fig = plt.figure(figsize =(11, 8)) 
ax = fig.add_axes([0, 0, 1, 1]) 
bp = ax.boxplot(data) 
plt.show()

A





plt.boxplot(data) 
  
# show plot 
plt.show()

a = [[1,1],[1,1],[1,1]]
b = [2,2]
w = (np.array(a) @ np.array(b)) 
a=np.array(a) 
a = np.insert(a,0,2,axis=1)
print(a)

