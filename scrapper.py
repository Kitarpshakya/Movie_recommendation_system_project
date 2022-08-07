import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import tqdm

"""
    Works for imdb pages recommend using all the pages with genres informations 
    discards all the ones wiht less then 3 genre type
"""



def get_all_titles(soup):
    result_topics = []
    all_topics = soup.find_all('h3', {'class': 'lister-item-header'})

    # print(all_topics)
    for topic in all_topics:
        # topic = topic.find('a').text //optional easy method
        topic = str(topic.find('a'))
        topic = topic.replace('<', '=')
        topic = topic.replace('>', '=')
        topic = topic.split('=')
        topic = topic[int(len(topic)/2)]
        result_topics.append(topic)
    # print(result_topics)
    return result_topics

def get_all_genres(soup):
    result_genres=[]
    all_genres = soup.find_all("p",{"class":'text-muted'})
    # print(all_genres)
    for genre in all_genres:
        genre = str(genre.find_all("span",{"class":"genre"}))
        if genre == '[]':
            pass
        else:
            genre = genre.replace("<","=")
            genre = genre.replace(">","=")
            genre = genre.split('=')
            genre = genre[int(len(genre)/2)]
            result_genres.append(genre)
    # print(result_genres)        
    return result_genres

def post_process(genres):
    post_process_gernres = []
    for i in genres:
        i = i.replace("\n","")
        i = i.replace(" ","")
        post_process_gernres.append(i)
    # print(post_process_gernres)
    return post_process_gernres

def check_repeated_comma(x):
    list_x=x.split(',')
    if len(list_x) == 3:
        return x
    else:
        return np.nan


def data_set(url):
    data_set = pd.DataFrame(columns = ["Movies", "Primary Genre", "Secondary Genre", "Tertiary Genre"])
    # Initially get the page from the url and from the content extract all the things properly so page is extracetd
    page = requests.get(url)
    # Soup is created where all the content is parsed as html format so it can be extracted as seen in webpages. 
    soup = BeautifulSoup(page.content, 'html.parser')   
    title = get_all_titles(soup)
    # print(title)
    genres = get_all_genres(soup)
    genres = post_process(genres)
    data_set["Movies"] = pd.Series(title)
    data_set["Primary Genre"] = pd.Series(genres)
    data_set["Primary Genre"] = data_set["Primary Genre"].apply(check_repeated_comma)
    data_set["Secondary Genre"] = data_set["Secondary Genre"].fillna('To be Filled')
    data_set["Tertiary Genre"] = data_set["Tertiary Genre"].fillna('To be Filled')
    data_set = data_set.loc[data_set['Primary Genre']!= np.NaN]
    data_set = data_set.dropna(how = "any")
    print(data_set)
    data_set[["Primary Genre","Secondary Genre","Tertiary Genre"]] = data_set["Primary Genre"].str.split(',',expand = True)
    data_set.to_csv("Dataset_"+Genre+".csv", mode = 'a', header = False, index = False)


if __name__ == "__main__":
    import os
    os.system('cls')
    print('IMDB Scraper')
    Genre = str(input('Enter your favourite Genre:  '))
    number_of_pages = int(input('Enter the number of various pages to scrap: '))
    t = 1
    for i in tqdm.tqdm(range(number_of_pages)):
        # url = input('Enter a URL: ')
        url = "https://www.imdb.com/search/title/?title_type=feature&genres="+Genre+"&start="+str(t)+"&ref_=adv_nxt"
        t += 50
        data_set(url)
