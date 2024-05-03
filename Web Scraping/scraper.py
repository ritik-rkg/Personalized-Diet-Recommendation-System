import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import pickle

def get_category_links():
    url = 'https://www.allrecipes.com/recipes/breakfast-and-brunch/'
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"})
    html_content = response.text
    #print(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    ul_element = soup.find('ul', {'class': "comp mntl-taxonomy-nodes__list mntl-block"})
    list_items = ul_element.find_all('li')
    links = []
    for item in list_items:
        link = item.find('a')['href']
        links.append(link)
    return links

def get_recipe_links(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"})
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    elements_with_class = soup.find_all(class_='comp tax-sc__recirc-list card-list mntl-universal-card-list mntl-document-card-list mntl-card-list mntl-block') 
    recipe_links = []
    for element in elements_with_class:
        links = element.find_all('a')
        for link in links:
            href = link.get('href')
            recipe_links.append(href)
    return recipe_links

def add_breakfast_df_row(id, url):
    df = {}
    columns = ['RecipeID', 'Name', 'Ingredients', 'Servings Per Recipe', 'Calories', 'Protein', 'Total Carbohydrate','Total Fat', 'Saturated Fat', 'Cholesterol', 'Dietary Fiber', 'Sodium', 'Rating', 'Number of Ratings', 'URL']
    for col in columns:
        df[col] = None
    df['RecipeID'] = id
    df['URL'] = url
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"})
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    name = soup.find('h1', {'class': "article-heading type--lion"})
    df['Name'] = name.text
    ul_element = soup.find_all('ul', {'class': "mntl-structured-ingredients__list"})
    ingredients = ""
    for i in range (len(ul_element)):
        list_items = ul_element[i].find_all('li')
        for item in list_items:
            x = item.text.strip('\n')
            ingredients = ingredients + x + " "
    df['Ingredients'] = ingredients
    table_element = soup.find('table', {'class': "mntl-nutrition-facts-label__table"})
    if (table_element == None):
        return
    nutrition = table_element.find_all('tr')
    for row in nutrition:
        s = row.text.strip('\n')
        if ('\n' in s):
            s = s.split('\n\n\n')[0]
            l = s.split('\n')
            quantity = l[1].rstrip('g')
            quantity = quantity.rstrip('m')
            if (l[0] in columns):
                df[l[0]] = int(quantity)
    avg = soup.find('div', {'class': "comp mntl-recipe-review-bar__rating mntl-text-block type--squirrel-bold"})
    count = soup.find('div', {'class': "comp mntl-recipe-review-bar__rating-count mntl-text-block type--squirrel"})
    if avg != None:
        df['Rating'] = float(avg.text)
    else:
        df['Rating'] = 0
    if count != None:
        df['Number of Ratings'] = int(count.text.strip('()').replace(",", ""))
    else:
        df['Number of Ratings'] = 0
    df = pd.DataFrame([df])
    return df

url_categories = get_category_links()
print("Got category links!")
recipe_links = []
for category in url_categories:
    category_recipe_links = get_recipe_links(category)
    recipe_links.extend(category_recipe_links)
print("Got all recipe links!")
print(len(recipe_links))
old_df = pd.DataFrame()
columns = ['RecipeID', 'Name', 'Ingredients', 'Servings Per Recipe', 'Calories', 'Protein', 'Total Carbohydrate','Total Fat', 'Saturated Fat', 'Cholesterol', 'Dietary Fiber', 'Sodium', 'Rating', 'Number of Ratings', 'URL']
for col in columns:
    old_df[col] = None
id = 1
for recipe_link in recipe_links:
    print(recipe_link)
    row = add_breakfast_df_row(id, recipe_link)
    old_df = pd.concat([old_df, row], ignore_index = True)
    id += 1
old_df.to_csv('breakfast.csv')


