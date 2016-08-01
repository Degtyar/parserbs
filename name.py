import sys
import argparse
import operator
import csv
# С какого файла читаем
f = open('tel.csv','r',encoding='UTF8')
# В какой пишем отчет
fw = open('nom.txt','w',encoding='UTF8')
f2 = open('report_li_sta.txt','r',encoding='UTF8')
name_mas = {}
err = 0
name_mas_av = {}
err2 = 0

for s in f:
 f_str = s.split(';')
 try:
  tel = int(f_str[3])
  name = [f_str[0], f_str[1], f_str[2]]
  name_tot = ''.join(name)
  name_mas[tel] = name_tot
 except Exception:
  err += 1
  
for k in f2:
 k_str = k.split(';')
 try:
  tel = int(k_str[0])
  name2 = [k_str[2]]
  name_mas_av[tel] = ''.join(name2)
 except Exception:
  err2 += 1