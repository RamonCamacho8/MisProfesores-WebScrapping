# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os


schools = [{'name' : 'Universidad-de-Sonora',
              'url' : 'https://www.misprofesores.com/escuelas/Universidad-de-Sonora_1596'},
            {'name' : 'Universidad-Autonoma-de-Nuevo-Leon', 
            'url' : 'https://www.misprofesores.com/escuelas/Universidad-Autonoma-de-Nuevo-Leon_1097'},
            {'url' : 'https://www.misprofesores.com/escuelas/UNIVERSIDAD-NACIONAL-AUTONOMA-DE-MEXICO_1971',
             'name' : 'UNIVERSIDAD-NACIONAL-AUTONOMA-DE-MEXICO'},
            {'url': 'https://www.misprofesores.com/escuelas/BUAP-Benemerita-Universidad-Autonoma-de-Puebla_1147',
             'name' : 'Benemerita-Universidad-Autonoma-de-Puebla'}]


#Creamos la carpeta donde se guardaran los archivos
save_folder = "Universidades/"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)


def getProfessors():

    for school in schools:
        
        name = school['name']
        url = school['url']

        #join the first two letters of each word in the name, if the second letter is uppercase then lowercase it
        name = ''.join([word.capitalize() for word in name.split('-') if word[0].isupper()])

        #if the file already exists, skip it
        if os.path.exists(f'{save_folder}{name}.txt'):
            print(f'{name} already exists')
            continue
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(url)
        #link_elements = driver.find_elements(By.CLASS_NAME, "url hidden-xs sorting_1")
        link_elements = driver.find_elements(By.CLASS_NAME, "sorting_1")
        professors = []

        for element in link_elements:
            try:
                link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
                professors.append(link)
            except:
                pass

        #Number of professors
        print(f'{name} contiene : {len(professors)} profesores')
        with open(f'{save_folder}{name}.txt', 'w') as file:

            # Iterate through the list and write each element to the file
            for item in professors:
                file.write(item + '\n')
        driver.quit()

        return professors
