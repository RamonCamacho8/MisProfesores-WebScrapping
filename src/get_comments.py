import requests
from bs4 import BeautifulSoup
import pandas as pd

def getCommentsFromProfessors(profesores):
    
    profesores = profesores

    all_comments = []
    all_tags = []
    scores = []
    clases = []
    fechas = []
    calificaciones = []
    
    index = 1
    for url_profesor in profesores:
        page_number = 1

        while True:
            url = f"{url_profesor}?pag={page_number}"
            response = requests.get(url)
            html_content = response.content

            soup = BeautifulSoup(html_content, "html.parser")

            # Find and process elements on this page
            comment = soup.find_all("p", class_="commentsParagraph")
            tag = soup.find_all("span", class_="rating-type")
            score = soup.find_all("span", class_="score")
            response_spans = soup.find_all('span', class_='name')
            date = soup.find_all("div", class_="date")
            calificacion = soup.find_all("span", class_="grade")

            calificaciones_list = []

            for span in calificacion:
                if "Calificación Recibida: " in span.text:
                    response = span.find('span', class_='response')
                    calificaciones_list.append(response)


            all_comments.extend(comment)
            all_tags.extend(tag)
            scores.extend(score)
            clases.extend(response_spans)
            fechas.extend(date)
            calificaciones.extend(calificaciones_list)


            # Check for next page or exit the loop
            next_page_link = soup.find("a", href=True, string=str(page_number + 1))
            if next_page_link:
                page_number += 1
            else:
                break

            #print (f"Processing page {page_number} of {url_profesor}")
        
        #print(f"Profesor {index} de {len(profesores)}")
        index += 1
            
    calidad_list = []
    facilidad_list = []

    for i, value in enumerate(scores):
        if i % 2 == 0:
            calidad_list.append(value)
        else:
            facilidad_list.append(value)

    #Obtenemos los textos de los elementos htmls
    comment_array = [element.get_text(strip=True) for element in all_comments]
    tag_array = [element.get_text(strip=True) for element in all_tags]
    calidad_array = [element.get_text(strip=True) for element in calidad_list]
    facilidad_array = [element.get_text(strip=True) for element in facilidad_list]
    clases_array = [element.get_text(strip=True) for element in clases]
    fechas_array = [element.get_text(strip=True) for element in fechas]
    calificaciones_array = [element.get_text(strip=True) for element in calificaciones]
    
    # Creación del dataframe
    data = {'Comment': comment_array, 'Tag': tag_array, 'Calidad': calidad_array, 'Facilidad': facilidad_array, 'Clase': clases_array, 'Calificación' : calificaciones_array, 'Fecha' : fechas_array}
    df = pd.DataFrame(data)
    print('Tamaño del Corpus: ', len(df), ' filas.')

    return df
