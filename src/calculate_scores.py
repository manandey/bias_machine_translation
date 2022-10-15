import pandas as pd
import statistics


model = "m2m"
lang = "de"
dataset = "bug"

orig_path = f"../results/{dataset}/orig"
CSS_Analysis_path = f'../results/{dataset}/CSS Analysis'


css_df_orig = pd.read_csv(f'{CSS_Analysis_path}/{lang}_{model}.csv')
css_df = css_df_orig[css_df_orig["gender_signal"]==css_df_orig["Orig Gender"]] #Filtering the examples where correct gender context was added 
df_orig = pd.read_csv(f'{orig_path}/{model}/{lang}.pred.csv')

def calculate_accuracies():
  correct=0
  corrected=0
  biased=0
  neutral = 0
  all_corrected=0
  avg_corrected = 0
  u=0
  t=0 



  for _, r in df_orig.iterrows():
    if r["Orig Gender"]==r["Predicted gender"]: #the sentence is already correct
      correct+=1
    elif r["Orig Gender"]!="neutral":
      df = css_df[(css_df["Source Sentence"]==r["Source Sentence"]) ]
      if not (df.shape[0]>0):
        continue
      else:
        biased+=1
      v = df
      u+=v.shape[0]
      df = df[(df["is_correct_gender"]==1)]
      if df.shape[0]>0: # the bias was corrected atleast once
        corrected+=1 
      if (v.shape[0]==df.shape[0]):
        all_corrected+=1 # all templates corrected the bias
      avg_corrected+= df.shape[0]
    else:
      neutral+=1

    
  print(f'{lang}_{model}')
  print("greedy_acc", (correct+corrected)/df_orig.shape[0])
  print("au", corrected/biased)
  print("al", (all_corrected)/biased)

def calculate_css_score():

  data = css_df_orig
  filter_css_data = data[data["gender_signal"]!=data["actual"]]
  filter_acc_data = data[data["gender_signal"]==data["Orig Gender"]]


  css_score = []
  acc_score = []
  gender_signal_acc=[]
  sent_length = []
  for sent in df_orig["Source Sentence"]:
    sent_length.append(len(sent.split(' ')))
    df = filter_css_data[filter_css_data["Source Sentence"]==sent]
    css_score.append(sum(df["sensitive"])/df.shape[0])
    df = filter_acc_data[filter_acc_data["Source Sentence"]==sent]
    acc_score.append(sum(df["is_correct_gender"])/df.shape[0])
    df = data[data["Source Sentence"]==sent]
    gender_signal_acc.append((sum(df["gender_signal"]==df["Predicted gender"]))/df.shape[0])

  print(f'CSS Score: {statistics.mean(css_score)}')

calculate_accuracies()
calculate_css_score()