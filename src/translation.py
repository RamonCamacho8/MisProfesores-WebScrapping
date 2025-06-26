import requests
from transformers import AutoTokenizer, MarianMTModel
import pandas as pd
import torch
from tqdm.notebook import tqdm
tqdm.pandas()

def deepL_trad_pipe(message : str, source : str = 'ES', target : str = 'EN'):
  url = 'https://api-free.deepl.com/v2/translate'
  headers = {
      'Authorization': 'DeepL-Auth-Key 2ca7667d-eb26-5b58-fffc-b48e5c57b608:fx'
  }
  data = {
      'text': f'{message}',
      'source_lang' : 'ES',
      'target_lang': 'EN'
  }

  response = requests.post(url, headers=headers, data=data)
  translated_text = response.json()['translations'][0]['text']
  #print(response.json()['translations'])
  return(translated_text)

#Modelo de traducción de Español a Inglés
model_name = "Helsinki-NLP/opus-mt-es-en"
modelo_trad = MarianMTModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
device = "cuda:0" if torch.cuda.is_available() else "cpu"


def model_trad_pipe(message : str, model = modelo_trad, tokenizer = tokenizer, device = device):
  #print('Using: ' + device)
  modelo_trad = modelo_trad.to(device)
  batch = tokenizer([message], return_tensors="pt").to(device)
  generated_ids = modelo_trad.generate(**batch)
  result = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
  return result

def translate(row):
  if row['comentario_eng'] == None:
    row['comentario_eng'] = model_trad_pipe(row['comentario_esp'], modelo_trad, tokenizer, device)
  return row

def traduccion(df : pd.DataFrame):
    if not 'comentario_eng' in df:
        df['comentario_eng'] = None
    df = df.progress_apply(translate, axis = 1)
    return df

class TraduccionClass:
  
  def __init__(self):
    #Modelo de traducción de Español a Inglés
    self.model_name = "Helsinki-NLP/opus-mt-es-en"
    self.modelo_trad = MarianMTModel.from_pretrained(self.model_name)
    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
    self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
    
    
  def showDevice(self):
    print('Using: ' + self.device)
    
  def model_trad_pipe(self, message : str):
      modelo_trad = self.modelo_trad.to(self.device)
      batch = self.tokenizer([message], return_tensors="pt").to(self.device)
      generated_ids = modelo_trad.generate(**batch)
      result = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
      return result
  
  def translate(self, row):
    if row['comentario_eng'] == None:
      row['comentario_eng'] = self.model_trad_pipe(row['comentario_esp'])
    return row
  
  def traduccion(self, df : pd.DataFrame):
    print('Traduciendo...')
    if not 'comentario_eng' in df:
        df['comentario_eng'] = None
    df = df.progress_apply(self.translate, axis = 1)
    return df
