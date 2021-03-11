# -*- coding: utf-8 -*-
"""HW1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tsSjxpBeZAVi6wEBcgqMAUixoh6tvDYK
"""

import numpy as np
from numpy import genfromtxt
from io import StringIO
import csv
import math
def main():
  datafile = open('tokenized_corpus.csv', 'r')
  datareader = csv.reader(datafile)
  data = []
  temp = 0
  for row in datareader:
    data+=( row )
    temp = temp+1

  temp_x = temp
  uniqueList = []
  [uniqueList.append(x) for x in data if x not in uniqueList]

  matrix = np.zeros( (temp, len(uniqueList)) )

  temp = 0
  datafile = open('tokenized_corpus.csv', 'r')
  datareade = csv.reader(datafile)
  for row in datareade:
    for x in row:
      matrix[temp][uniqueList.index(x)] += 1
    temp += 1

  np.savetxt("feature_set.csv", matrix, delimiter=",")
  training = matrix[:4460]
  test = matrix[4460:]

  datafile = open('labels.csv', 'r')
  datareader = csv.reader(datafile)
  label = []
  temp = 0
  for row in datareader:
    label+= row 
    temp = temp+1

  #for spam
  spamList = np.zeros( len(uniqueList) )
  totalSpam = 0
  x = 0
  datafile = open('tokenized_corpus.csv', 'r')
  datareade = csv.reader(datafile)
  for i in datareade:
    if x < 4460:
      if label[x] == '1':
        for j in i:
          spamList[uniqueList.index(j)] += 1
        totalSpam += 1
      x += 1

  spamTheeta = np.zeros( len(uniqueList) )
  spamTheeta_laplace = np.zeros( len(uniqueList) )
  x = 0
  for i in spamList:
    spamTheeta_laplace[x]= (i+1)/(sum(spamList)+len(uniqueList))
    spamTheeta[x]= (i)/(sum(spamList))
    x += 1

  #for ham
  hamList = np.zeros( len(uniqueList) )
  totalHam = 0
  x = 0
  datafile = open('tokenized_corpus.csv', 'r')
  datareade = csv.reader(datafile)
  for i in datareade:
    if x < 4460:
      if label[x] == '0':
        for j in i:
          hamList[uniqueList.index(j)] += 1
        totalHam += 1
      x+=1

  hamTheeta = np.zeros( len(uniqueList) )
  hamTheeta_laplace = np.zeros( len(uniqueList) )
  x = 0
  for i in hamList:
    hamTheeta_laplace[x]= (i+1)/(sum(hamList)+len(uniqueList))
    hamTheeta[x]= (i)/(sum(hamList))
    x += 1

  spamTheeta = np.log(spamTheeta)
  hamTheeta = np.log(hamTheeta)
  spamTheeta_laplace = np.log(spamTheeta_laplace)
  hamTheeta_laplace = np.log(hamTheeta_laplace)
  piSpam = totalSpam/(totalSpam + totalHam)
  piHam = totalHam/(totalSpam + totalHam)

  piSpam = math.log(piSpam)
  piHam = math.log(piHam)


  datafile = open('tokenized_corpus.csv', 'r')
  datareader = csv.reader(datafile)
  x = 0
  count = 0
  hamResult = 0
  spamResult = 0
  predictions = []

  hamtt = test*hamTheeta
  hamtt = np.nan_to_num(hamtt)
  hamtt = np.sum(hamtt,axis = 1)
  hamm = hamtt + piHam

  hamtt_l = test*hamTheeta_laplace
  hamtt_l = np.nan_to_num(hamtt_l)
  hamtt_l = np.sum(hamtt_l,axis = 1)
  hamm_l = hamtt_l + piHam

  spamtt = test*spamTheeta
  spamtt = np.nan_to_num(spamtt)
  spamtt = np.sum(spamtt,axis = 1)
  spamm = spamtt + piSpam

  spamtt_l = test*spamTheeta_laplace
  spamtt_l = np.nan_to_num(spamtt_l)
  spamtt_l = np.sum(spamtt_l,axis = 1)
  spamm_l = spamtt_l + piSpam

  predict = []
  predict_l = []
  for i in range (0,1112):
    if spamm[i] >= hamm[i]:
      predict.append('1')
    else:
      predict.append('0')
    if spamm_l[i] >= hamm_l[i]:
      predict_l.append('1')
    else:
      predict_l.append('0')

  x = 0
  correct = 0
  total = 0
  correct_l = 0
  for i in range(4460,len(label)):
    if label[i] == predict[x]:
      correct += 1  
    if label[i] == predict_l[x]:
      correct_l += 1
    x += 1
    total += 1

  print("accuracy for Q 2.2")
  print(correct/1112)
  print("accuracy for Q 2.3")
  print(correct_l/1112)
  me = (correct/1112)*100
  me_l = (correct_l/1112)*100
  with open('test_accuracy.csv', 'w') as outfile:
    mywriter = csv.writer(outfile)
    mywriter.writerow([me])
  with open('test_accuracy_laplace.csv', 'w') as outfile:
    mywriter = csv.writer(outfile)
    mywriter.writerow([me_l])


  ################################################################################################
  ####Part  3.1
  ################################################################################################

  uniqueList_ten = []
  cnt = []
  for x in uniqueList:
    if data.count(x) > 9:
      uniqueList_ten.append(x)
      cnt.append(data.count(x))


  matrix_ten = np.zeros( (temp_x, len(uniqueList_ten)) )
  temp = 0
  datafile = open('tokenized_corpus.csv', 'r')
  datareade = csv.reader(datafile)
  for row in datareade:
    for x in row:
      if x in uniqueList_ten:
        matrix_ten[temp][uniqueList_ten.index(x)] += 1
    temp += 1

  training_ten = matrix_ten[:4460]
  test_ten = matrix_ten[4460:]

  #for spam
  spamList = np.zeros( len(uniqueList_ten) )
  totalSpam = 0
  x = 0
  datafile = open('tokenized_corpus.csv', 'r')
  datareade = csv.reader(datafile)
  for i in datareade:
    if x < 4460:
      if label[x] == '1':
        for j in i:
          if j in uniqueList_ten:
            spamList[uniqueList_ten.index(j)] += 1
        totalSpam += 1
      x += 1

  spamTheeta_laplace_ten = np.zeros( len(uniqueList_ten) )
  x = 0
  for i in spamList:
    spamTheeta_laplace_ten[x]= (i+1)/(sum(spamList)+len(uniqueList_ten))
    x += 1

  #for ham
  hamList = np.zeros( len(uniqueList_ten) )
  totalHam = 0
  x = 0
  datafile = open('tokenized_corpus.csv', 'r')
  datareade = csv.reader(datafile)
  for i in datareade:
    if x < 4460:
      if label[x] == '0':
        for j in i:
          if j in uniqueList_ten:
            hamList[uniqueList_ten.index(j)] += 1
        totalHam += 1
      x+=1

  hamTheeta_laplace_ten = np.zeros( len(uniqueList_ten) )
  x = 0
  for i in hamList:
    hamTheeta_laplace_ten[x]= (i+1)/(sum(hamList)+len(uniqueList_ten))
    x += 1

  spamTheeta_laplace_ten = np.log(spamTheeta_laplace_ten)
  hamTheeta_laplace_ten = np.log(hamTheeta_laplace_ten)

  piSpam = totalSpam/(totalSpam + totalHam)
  piHam = totalHam/(totalSpam + totalHam)
  piSpam = math.log(piSpam)
  piHam = math.log(piHam)

  i = 0
  training_ten = matrix_ten[:4460]
  test_ten = matrix_ten[4460:]
  accuracy = 0
  tt = 0
  acc = 0
  gg = 0
  visited = []
  done = []
  jumping = np.zeros( len(hamTheeta_laplace_ten) )
  sr = 0
  for x in range (0,len(spamTheeta_laplace_ten)):
    j = i+1
    for x in range (0,len(spamTheeta_laplace_ten)):
      asd = np.append(np.array(test_ten[:,0:i]), np.array(test_ten[:,j-1:j]), axis=1)
      ham_asd = np.append(np.array(hamTheeta_laplace_ten[0:i]), np.array(hamTheeta_laplace_ten[j-1:j]))
      spam_asd = np.append(np.array(spamTheeta_laplace_ten[0:i]), np.array(spamTheeta_laplace_ten[j-1:j]))

      hamtt = asd*ham_asd
      hamtt = np.nan_to_num(hamtt)
      hamtt = np.sum(hamtt,axis = 1)
      hamm = hamtt + piHam

      spamtt = asd*spam_asd
      spamtt = np.nan_to_num(spamtt)
      spamtt = np.sum(spamtt,axis = 1)
      spamm = spamtt + piSpam

      predict = []
      for g in range (0,1112):
        if spamm[g] >= hamm[g]:
          predict.append('1')
        else:
          predict.append('0')
      
      h = 0
      correct = 0
      total = 0
      for g in range(4460,len(label)):
        if label[g] == predict[h]:
          correct += 1  
        h += 1
        total += 1
      if accuracy < correct:
        accuracy = correct
        tt = j-1
      j += 1
    #change i index with tt index
    
    sr = tt
    if sr in visited:
      sr = jumping[sr]
      jumping[tt] = i
      done.append(sr)
    else:
      visited.append(sr)
      jumping[sr] = i
      done.append(tt)
    
    test_ten[:,[i,tt]] = test_ten[:,[tt,i]]
    hamTheeta_laplace_ten[i], hamTheeta_laplace_ten[tt] = hamTheeta_laplace_ten[tt], hamTheeta_laplace_ten[i]
    spamTheeta_laplace_ten[i], spamTheeta_laplace_ten[tt] = spamTheeta_laplace_ten[tt], spamTheeta_laplace_ten[i]

    i += 1
    if acc >= accuracy:
      break
    if acc < accuracy:
      acc = accuracy
      gg = i
    
  print("accuracy for Q 3.1")
  print(acc/1112)

  with open('forward_selection.csv', 'w') as outfile:
      mywriter = csv.writer(outfile)
      for d in done:
          mywriter.writerow([d])

  ################################################################################################
  ####Part  3.2
  ################################################################################################


  uniqueList_ten = []
  cnt = []
  for x in uniqueList:
    if data.count(x) > 9:
      uniqueList_ten.append(x)
      cnt.append(data.count(x))

  unq = []
  for x in range(0,len(cnt)):
    hh = cnt.index(max(cnt))
    if max(cnt) == 0:
      break
    cnt[hh] = 0
    unq.append(uniqueList_ten[hh])

  uniqueList_ten = unq

  matrix_ten = np.zeros( (temp_x, len(uniqueList_ten)) )
  temp = 0
  datafile = open('tokenized_corpus.csv', 'r')
  datareade = csv.reader(datafile)
  for row in datareade:
    for x in row:
      if x in uniqueList_ten:
        matrix_ten[temp][uniqueList_ten.index(x)] += 1
    temp += 1

  training_ten = matrix_ten[:4460]
  test_ten = matrix_ten[4460:]

  #for spam
  spamList = np.zeros( len(uniqueList_ten) )
  totalSpam = 0
  x = 0
  datafile = open('tokenized_corpus.csv', 'r')
  datareade = csv.reader(datafile)
  for i in datareade:
    if x < 4460:
      if label[x] == '1':
        for j in i:
          if j in uniqueList_ten:
            spamList[uniqueList_ten.index(j)] += 1
        totalSpam += 1
      x += 1

  spamTheeta_laplace_ten = np.zeros( len(uniqueList_ten) )
  x = 0
  for i in spamList:
    spamTheeta_laplace_ten[x]= (i+1)/(sum(spamList)+len(uniqueList_ten))
    x += 1

  #for ham
  hamList = np.zeros( len(uniqueList_ten) )
  totalHam = 0
  x = 0
  datafile = open('tokenized_corpus.csv', 'r')
  datareade = csv.reader(datafile)
  for i in datareade:
    if x < 4460:
      if label[x] == '0':
        for j in i:
          if j in uniqueList_ten:
            hamList[uniqueList_ten.index(j)] += 1
        totalHam += 1
      x+=1

  hamTheeta_laplace_ten = np.zeros( len(uniqueList_ten) )
  x = 0
  for i in hamList:
    hamTheeta_laplace_ten[x]= (i+1)/(sum(hamList)+len(uniqueList_ten))
    x += 1

  spamTheeta_laplace_ten = np.log(spamTheeta_laplace_ten)
  hamTheeta_laplace_ten = np.log(hamTheeta_laplace_ten)

  piSpam = totalSpam/(totalSpam + totalHam)
  piHam = totalHam/(totalSpam + totalHam)
  piSpam = math.log(piSpam)
  piHam = math.log(piHam)

  i = 1
  training_ten = matrix_ten[:4460]
  test_ten = matrix_ten[4460:]
  accuracy = 0
  tt = 0
  for_whom = []
  for x in range (0,len(spamTheeta_laplace_ten)):
    hamtt = test_ten[:,0:i]*hamTheeta_laplace_ten[0:i]
    hamtt = np.nan_to_num(hamtt)
    hamtt = np.sum(hamtt,axis = 1)
    hamm = hamtt + piHam

    spamtt = test_ten[:,0:i]*spamTheeta_laplace_ten[0:i]
    spamtt = np.nan_to_num(spamtt)
    spamtt = np.sum(spamtt,axis = 1)
    spamm = spamtt + piSpam

    predict = []
    for g in range (0,1112):
      if spamm[g] >= hamm[g]:
        predict.append('1')
      else:
        predict.append('0')
    
    h = 0
    correct = 0
    total = 0
    for g in range(4460,len(label)):
      if label[g] == predict[h]:
        correct += 1  
      h += 1
      total += 1

    for_whom.append(correct/1112)
    if accuracy < correct:
      accuracy = correct
      tt = i
    i += 1

  print("accuracy for Q3.2")
  print(accuracy/1112)

  with open('frequency_selection.csv', 'w') as outfile:
      mywriter = csv.writer(outfile)
      for d in for_whom:
          mywriter.writerow([d*100])


if __name__ == "__main__":
    main()