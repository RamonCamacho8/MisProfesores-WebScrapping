from .folder_creation import createOutputFolder
from .get_professors import getProfessors
from .get_comments import getCommentsFromProfessors
from .corpus_cleaning import limpiarCorpus
from .translation import TraduccionClass
import pandas as pd
import torch


rootFolder : str = 'Universidades/'
fileName : str =  'UniversidadAutonomaNuevoLeon'
ext : str ='.txt'

#getProfessors()
#createOutputFolder()
'''
profesores = []
print (rootFolder + fileName + ext)
full_path = rootFolder + fileName + ext

with open(full_path, 'r') as file:
    profesores = file.read().splitlines()

print(profesores)
df = getCommentsFromProfessors(profesores= profesores)
df = limpiarCorpus(df)
df = traduccion(df)

ext = '.csv'

df.to_csv('Corpus/'+fileName+'/Final_'+ fileName + ext, index=False)
'''

trad = TraduccionClass()
trad.showDevice()
df = pd.read_csv('Corpus/UniversidadSonora/L_MP_UniversidadSonora.csv  ')
df = trad.traduccion(df)