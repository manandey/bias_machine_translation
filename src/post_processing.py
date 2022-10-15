
import pandas as pd
import os

model = "m2m"
lang = "de"
dataset = "bug"

path = f"../results/{dataset}/orig/{model}/{lang}.pred.csv"
CSS_Analysis_path = f'../results/{dataset}/CSS Analysis'
if not os.path.exists(CSS_Analysis_path):
    os.makedirs(CSS_Analysis_path)


def add_accuracy(df):
  return (df["Orig Gender"] == df["Predicted gender"]).astype('int')

def create_data(path, correctness = None):
  df = pd.read_csv(path)
  opp= {"male":"female", "female":"male"}
  df["is_correct_gender"] = add_accuracy(df)
  if correctness:
    if correctness==1:
      df["gender_signal"] = df["Orig Gender"]
    elif correctness==2:
      df["gender_signal"] = df["Orig Gender"].map(lambda ds: opp[ds])
  return df

def add_sensitivity(df):
  corr = []
  actual_gender = []
  sentence_gender_map = {sent: gender for sent, gender in zip(data_orig["Source Sentence"], data_orig["Predicted gender"])}
  for _, row in df.iterrows():
    sent = row["Source Sentence"]
    actual = sentence_gender_map[sent]
    actual_gender.append(actual)
    corr.append(int(row["Predicted gender"]!=actual))
    
  return corr, actual_gender

data_orig = create_data(path)

# profs_list = list(set(data_orig['Orig Prof']))
profs_list = ["accountant"]
df_all = pd.DataFrame()

for prof in profs_list:
  corr_path = f"../results/{dataset}/{prof}/{model}/{lang}.pred.csv"
  incorr_path = f"../results/{dataset}/{prof}/css/{model}/{lang}.pred.csv"
  df_correct = create_data(corr_path, 1)
  df_incorrect = create_data(incorr_path,  2)
  df_all= df_all.append(df_correct)
  df_all= df_all.append(df_incorrect)

df_all["sensitive"], df_all["actual"] = add_sensitivity(df_all)
df_all.to_csv(f'{CSS_Analysis_path}/{lang}_{model}.csv')



# out = '/content/drive/MyDrive/Research/MT Bias/Final Experiments/Results/WinoMT/CSS Analysis/sentence_wise'

# #de
# lang = "de"
# data = df_all
# print(data.shape)
# filter_css_data = data[data["gender_signal"]!=data["actual"]]
# filter_acc_data = data[data["gender_signal"]==data["Orig Gender"]]

# filter_css_data.shape

# (sum(filter_css_data["sensitive"])/filter_css_data.shape[0])*100

# css_score = []
# acc_score = []
# gender_signal_acc=[]
# sent_length = []
# for sent in data_de_orig_m2m["Source Sentence"]:
#   sent_length.append(len(sent.split(' ')))
#   df = filter_css_data[filter_css_data["Source Sentence"]==sent]
#   css_score.append(sum(df["sensitive"])/df.shape[0])
#   df = filter_acc_data[filter_acc_data["Source Sentence"]==sent]
#   acc_score.append(sum(df["is_correct_gender"])/df.shape[0])
#   df = data[data["Source Sentence"]==sent]
#   gender_signal_acc.append((sum(df["gender_signal"]==df["Predicted gender"]))/df.shape[0])

# data_de_orig_m2m["css_score"] = css_score
# data_de_orig_m2m["sent_len"] = sent_length
# data_de_orig_m2m["acc_score"] = acc_score
# data_de_orig_m2m["gender_signal_acc"] = gender_signal_acc
# # data_de_orig_m2m.to_csv(f'{out}/{lang}_{model}_new.csv')

# statistics.mean(data_de_orig_m2m['css_score'])

