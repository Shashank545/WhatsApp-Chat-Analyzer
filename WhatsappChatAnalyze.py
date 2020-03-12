# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 17:23:27 2019
@author: Shashank Shekhar Sahoo
"""

"""
#Awesome features of your own WhatsApp Chat Analyzer:

MS1: Read your chat file using your Python program
MS2: Feature #1 -- count the total number of messages from both parties
MS3: Feature #2 -- count the total number of words from both parties
MS4: Feature #3 -- calculate the average length of messages sent by each party
MS5: Feature #4 -- most common words
MS6: Feature #5 -- print all of the above in pretty, neat tables

"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
from nltk.corpus import stopwords
import emoji
import regex
from wordcloud import WordCloud, STOPWORDS 



#For local execution and testing 
'''
dir_path = os.path.dirname(os.path.realpath("SDasSha2nk.txt"))
chatfile_name = dir_path+"\\file2.txt"
'''

#For console application based execution
chatfile_name = sys.argv[1]

if len(sys.argv)>=3:
    chat_date = sys.argv[2]
    

def chat_persons_name(filename):
  """
  Analyses the chat file.
  :param: filename: name of the chat file
  :response: Names of person undertaking chat
  """
  fptr = open(filename,'r',encoding="utf8")
  ftext = fptr.read()
  fmsg = ftext.splitlines()
    
  if fmsg[0].split()[3]=="Messages":
     fmsg = fmsg[1:]
         
  names = [p.split()[3].split(":")[0] for p in fmsg]
  unique_names = list(set(names))
  return unique_names



def chat_preprocessing(filename, search_string, replace_string):
  """
  Analyses the chat file.
  :param: filename: name of the chat file
  :param: search_string - name of person to be replaced
  :param: replace_string - pseudo name to be replaced with
  :response: No response
  """
    # Read in the file
    with open(filename, 'r', encoding="utf8") as file :
        filedata = file.read()

    
    search_string = search_string + ":"
    replace_string = replace_string + ":"
    
    if search_string in filedata:
        # Replace the target string
        filedata = filedata.replace(search_string, replace_string)
            
            # Write the file out again
        with open(filename, 'w', encoding="utf8") as file:
            file.write(filedata)
            
    else:
        print("{0} not found in {1}".format(search_string, filename))
        
        
        
   
def chatfile_analysis(filename):
  """
  Analyses the chat file.
  :param filename: name of the chat
  :response: Summary of chat insights
  """

  fptr = open(filename,'r',encoding="utf8")
  ftext = fptr.read()
  fmsg = ftext.splitlines()
  
  unique_names = chat_persons_name(filename)
        
  daterange_start = fmsg[1].split(",")[0]
  daterange_end = fmsg[len(fmsg)-1].split(",")[0]
  
  sd_total_messages = [k.split().count(unique_names[0]) for k in fmsg if unique_names[0] in k]
  sha2nk_total_messages = [m.split().count(unique_names[1]) for m in fmsg if unique_names[1] in m]
  
  sd_messages_bucket = [p.split()[4:] for p in fmsg if p.split()[3].split(":")[0] == unique_names[0]]
  sha2nk_messages_bucket = [q.split()[4:] for q in fmsg if q.split()[3].split(":")[0] == unique_names[1]]
  
  sd_messages_words = [x for w in sd_messages_bucket for x in w]
  sha2nk_messages_words = [x for w in sha2nk_messages_bucket for x in w]
  
  sd_messages_word_lengths = [len(w) for w in sd_messages_bucket]
  sha2nk_messages_word_lengths = [len(w) for w in sha2nk_messages_bucket]
  
  print("================================== The CHAT FILE SUMMARY =====================================")
  print("1. This conversation is taking place between Mr. {0} & Mr. {1} .".format(unique_names[0], unique_names[1]))
  print("2. This chat file contains {0} lines of text conversations .".format(len(fmsg)))
  print("3. This chat file contains text conversations in the date range from {0} to {1} .".format(daterange_start, daterange_end))
  print("4. Total messages sent by Mr. {0} = {1} .".format(unique_names[0], len(sd_total_messages)))
  print("5. Total messages sent by Mr. {0} = {1} .".format(unique_names[1], len(sha2nk_total_messages)))
  print("6. Total english words used by Mr. {0} = {1} ." .format(unique_names[0], sum(sd_messages_word_lengths)))
  print("8. Total english words used by Mr. {0} = {1} ." .format(unique_names[1], sum(sha2nk_messages_word_lengths)))
  print("9. Average number of words used by Mr. {0} per message = {1} .". format(unique_names[0], np.mean(sd_messages_word_lengths)))
  print("10. Average number of words used by Mr. {0} per message = {1} .". format(unique_names[1], np.mean(sha2nk_messages_word_lengths)))
  
  fptr.close()
  


def feature_one_datewise_summary(filename):
  """
  Analyses the chat file.
  :param filename: name of the chat
  :response: chat stats for a given date
  """
  desired_date = input("Enter the desired date for chat insights in DD/MM/YYYY = ")
  persons = chat_persons_name(filename)
  fptr = open(filename,'r',encoding="utf8")
  ftext = fptr.read()
  fmsg = ftext.splitlines()
  
  count_SD_date = count_SSS_date = 0

  for i in fmsg:
      if persons[0] in i:       
          if desired_date in i:
              count_SD_date = count_SD_date+1

  print("Mr. {0} messaged {1} number of time on {2}".format(persons[0], count_SD_date, desired_date))


  for j in fmsg:
      if persons[1] in j:
          if desired_date in j:
              count_SSS_date = count_SSS_date+1
        
  print("Mr. {0} messaged {1} number of time on {2}".format(persons[1], count_SSS_date, desired_date))
  
  person_count_dict = dict({"Name":[persons[0], persons[1]], "Message_count":[count_SD_date, count_SSS_date]})
  
  date_chat_df = pd.DataFrame(person_count_dict)
  date_chat_df.to_csv("data_df.csv")
  
  return date_chat_df



def dominant_word_feature(filename):
      """
  Analyses the chat file.
  :param: filename: name of the chat file
  :response: custom words used by both persons in chat
  """
    
    fptr = open(filename,'r',encoding="utf8")
    ftext = fptr.read()
    fmsg = ftext.splitlines()
    
    unique_names = chat_persons_name(filename)
    sd_messages_bucket = [p.split()[4:] for p in fmsg if p.split()[3].split(":")[0] == unique_names[0]]
    sha2nk_messages_bucket = [q.split()[4:] for q in fmsg if q.split()[3].split(":")[0] == unique_names[1]]
  
    sd_messages_words = [x for w in sd_messages_bucket for x in w]
    sha2nk_messages_words = [x for w in sha2nk_messages_bucket for x in w]
    
    #  to quickly test if a word is not a stop word, use a set:
    stop_word_list = stopwords.words('english')
    stop_word_set = set(stop_word_list)
    
    sd_custom_words = [word for word in sd_messages_words if word.lower() not in stop_word_set]
    sha2nk_custom_words = [word for word in sha2nk_messages_words if word.lower() not in stop_word_set]
    
    sd_global_word_bank = sd_custom_words
    sha2nk_global_word_blank = sha2nk_custom_words
    
    sd_re_data = regex.findall(r'\X', str(sd_custom_words))
    sha2nk_re_data = regex.findall(r'\X', str(sha2nk_custom_words))
    
    sd_emojis = [word for word in sd_re_data if any(char in emoji.UNICODE_EMOJI for char in word)]
    sha2nk_emojis = [word for word in sha2nk_re_data if any(char in emoji.UNICODE_EMOJI for char in word)]
    
    word_count_dict = dict({"Name":[unique_names[0], unique_names[1]], "Emoji_count":[len(sd_emojis), len(sha2nk_emojis)], "Other_words":[(len(sd_custom_words)-len(sd_emojis)), (len(sha2nk_custom_words)-len(sha2nk_emojis))]})
  
    date_chat_df = pd.DataFrame(word_count_dict)
    date_chat_df.to_csv("emoji_data_df.csv")
    
    return date_chat_df
    
    

def words_cluster(filename):
      """
  Analyses the chat file.
  :param: filename: name of the chat file
  :response: word_cluster
  """
    
    fptr = open(filename,'r',encoding="utf8")
    ftext = fptr.read()
    fmsg = ftext.splitlines()
    
    unique_names = chat_persons_name(filename)
    sd_messages_bucket = [p.split()[4:] for p in fmsg if p.split()[3].split(":")[0] == unique_names[0]]
    sha2nk_messages_bucket = [q.split()[4:] for q in fmsg if q.split()[3].split(":")[0] == unique_names[1]]
  
    sd_messages_words = [x for w in sd_messages_bucket for x in w]
    sha2nk_messages_words = [x for w in sha2nk_messages_bucket for x in w]
    
    #  to quickly test if a word is not a stop word, use a set:
    stop_word_list = stopwords.words('english')
    stop_word_set = set(stop_word_list)
    
    sd_custom_words = [word for word in sd_messages_words if word.lower() not in stop_word_set]
    sha2nk_custom_words = [word for word in sha2nk_messages_words if word.lower() not in stop_word_set]
    
    #convert list to string and generate
    unique_string=(" ").join(sd_custom_words)
    wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("sd_word_cloud"+".png", bbox_inches='tight')
    plt.show()
    plt.close()
    
    #convert list to string and generate
    unique_string=(" ").join(sha2nk_custom_words)
    wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("sha2nk_word_cloud"+".png", bbox_inches='tight')
    plt.show()
    plt.close()
        
            
        

def main():
  """
  Main function that serves as an entrypoint for the program. 
  Reads the chat file from the command line when the program is 
  executed from the terminal and passed it to the `analyse()` method. 

  For example, if the file is "chat_file.txt", the command that needs to be run is:
  ```
  $>> python3 <main.py> chat_file.txt
  OR
  ```
  """
  #Preprocessing to replace actual names of persons in chat file with randomized strings for name abstraction
  chat_persons = chat_persons_name(chatfile_name)
  #Optional way to either abstract to keep the actual names of persons in chat
  #chat_preprocessing(chatfile_name, chat_persons[0], "ABCD")
  #chat_preprocessing(chatfile_name, chat_persons[1], "XYZ")
      

  while(1):
      print("***************************************************************************************")
      print("***************************************************************************************")
      print("***************************WHATSAPP CHAT ANALYZER**************************************")
      print("***************************************************************************************")
      print("***************************************************************************************")
     
      print("This is your magic application to get WhatsApp chat insights in an intriguing manner")
      print("***************************************************************************************")
      print("***************************************************************************************")
      print("Following are the various features you can give a shot")
      print("1. Summary of Chats in file")
      print("2. Datewise summary of Chats in file")
      print("3. See your chat style with graphics")
      print("4. Holistic Chat Visualization")
      print("Please choose an option above to procced ahead")
      
      option = int(input("Enter an option here = "))
      
      if option == 1:
          chatfile_analysis(chatfile_name)
      elif option == 2:
          chat_result = feature_one_datewise_summary(chatfile_name)
          chat_result.plot( x='Name', y='Message_count', kind='bar')
      elif option == 3:
          emoji_result = dominant_word_feature(chatfile_name)
          emoji_result.plot( x='Name', y='Emoji_count', kind='bar')
          
      elif option == 4:
          words_cluster(chatfile_name)
      else:
          print("Invalid Option !! Choose the right option.")
          
      
      


if __name__ == "__main__":
  main()



