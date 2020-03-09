# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:23:27 2019

@author: ss20228
"""

"""
#WhatsApp Chat Analyzer Steps:
1) MS1: Read your chat file using your Python program
2) MS2: Features #1 - count the total number of messages
2) MS3: Features #2 — count thevtotal number of words
3) MS4: Feature #3 — calculate the average length of messages sent by each party
4) MS5: Feature #4 — count number of first texts, and show them
5) MS6: Feature #5 — chatting time patterns (hourly, daily, and monthly)
6) MS7: Feature #7 — most-shared websites
7) MS8: Feature #8 — most common words
8) MS9: Print all of the above in pretty, neat tables
9) MS10: Make all of this work for group chat files


"""


import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



chatfile_name = sys.argv[1]

if len(sys.argv)>=3:
    chat_date = sys.argv[2]

def chatfile_analysis(filename):
  """
  Analyses the chat file.
  :param filename: name of the chat
  """

  fptr = open(filename,'r',encoding="utf8")
  ftext = fptr.read()
  fmsg = ftext.splitlines()
  #print(type(fmsg))
  #print(type(fmsg[1]))
  #print(fmsg[2].split())
  #print(fmsg[1].split())
  #print(fmsg)
  
  daterange_start = fmsg[1].split(",")[0]
  daterange_end = fmsg[len(fmsg)-1].split(",")[0]
  
  sd_total_messages = [k.split().count('Swagatika') for k in fmsg if "Swagatika Das Js" in k]
  sha2nk_total_messages = [m.split().count('SHA2NK:') for m in fmsg if "SHA2NK" in m]
  
  
  
  
  print("================================== The CHAT FILE SUMMARY =====================================")
  print("1. This chat file contains {0} lines of text conversations".format(len(fmsg)))
  print("2. This chat file contains text conversations in the date range from {0} to {1}".format(daterange_start, daterange_end))
  print("3. Total messages sent by Swagatika Das = {0}".format(len(sd_total_messages)))
  print("4. Total messages sent by Shashank Sahoo = {0}".format(len(sha2nk_total_messages)))
  
  
  
  fptr.close()
  

def feature_one_datewise_summary(filename):
  """
  Analyses the chat file.

  :param filename: name of the chat
  """
  desired_date = input("Enter the desired date for chat insights in DD/MM/YYYY = ")
  fptr = open(filename,'r',encoding="utf8")
  ftext = fptr.read()
  fmsg = ftext.splitlines()
  

  count_SD_date = count_SSS_date = 0

  for i in fmsg:
      if "Swagatika Das Js" in i:
          
          if desired_date in i:
              count_SD_date = count_SD_date+1

  print("Swagatika messaged {0} number of time on {1}".format(count_SD_date, desired_date))

  for j in fmsg:
      if "SHA2NK" in j:
          
          if desired_date in j:
              count_SSS_date = count_SSS_date+1
        
  print("Shashank messaged {0} number of time on {1}".format(count_SSS_date, desired_date))
  

  fptr.close()



def feature_two_mean_chat_length(filename):
    
  fptr = open(filename,'r',encoding="utf8")
  ftext = fptr.read()
  fmsg = ftext.splitlines()
  
  print(fmsg[7].split())
  print(fmsg[6].split())
  
  #sd_messages = [(len(i.split()) - i.split().index(j) +1) for i in fmsg for j in i.split() if j == 'Js:']
  sd_messages = [len(i.split()) for i in fmsg for j in i.split() if j == 'Js:']
  print(sd_messages)
  print(np.mean(sd_messages))
  
  #sha2nk_messages = [(len(i.split())-i.split().index(j)) for i in fmsg for j in i.split() if j == 'SHA2NK:']
  sha2nk_messages = [len(i.split()) for i in fmsg for j in i.split() if j == 'SHA2NK:']
  print(sha2nk_messages)
  print(np.mean(sha2nk_messages))
  
  
    
    

def main():
  """
  Main function that serves as an entrypoint for the program. 
  Reads the chat file name from the command line when the program is run from the terminal and passed it to the `analyse()` method. 

  For example, if the file is called "chat_file.txt", the command that needs to be run is:
  ```
  python3 main.py chat_file.txt
  ```
  """
  print("***************************WHATSAPP CHAT ANALYZER**************************************")
  print("***************************************************************************************")
  print("This is a magic application to get WhatsApp chat insights in an intriguing manner")
  print("***************************************************************************************")
  print("***************************************************************************************")
  print("Following are the various features you can give a shot")
  print("1. Summary of Chats in file")
  print("2. Datewise summary of Chats in file")
  print("3. Calculate the average length mesaages from each parties")
  print("4. See your chat pattern and style with graphics")
  print("Please choose an option above to procced ahead")
  
  option = int(input("Enter an option here = "))
  
  if option == 1:
      chatfile_analysis(chatfile_name)
  elif option == 2:
      feature_one_datewise_summary(chatfile_name)
  elif option == 3:
      feature_two_mean_chat_length(chatfile_name)
      
      




if __name__ == "__main__":
  main()



