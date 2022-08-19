import requests
import psycopg2
from bs4 import BeautifulSoup as bs

connection = psycopg2.connect(
  database="cars",
  user="postgres",
  password="admin",
  host="127.0.0.1",
  port="5432"
)



for i in range(1, 1000):
  r = requests.get("https://kolesa.kz/cars/avtomobili-s-probegom/?year[from]=2015&page={}".format(i))
  html = bs(r.text, "html.parser")
  titles = html.find_all('a', class_ ='a-card__link')
  descriptions = html.find_all('p', class_='a-card__description')



cur = connection.cursor()



cur.execute("""
CREATE TABLE IF NOT EXISTS car (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL, 
  description TEXT NOT NULL
)
""")


postgres_insert_query_title = """ INSERT INTO car (name)
                                   VALUES (%s)"""

postgres_insert_query_description = """ INSERT INTO car (description)
                                   VALUES (%s)"""

cur.execute(postgres_insert_query_title, titles)
cur.execute(postgres_insert_query_description, descriptions)

# for el in html.select(".a-list > .a-list__item > .a-card--pay-yellow js__a-card > .a-card__info > .a-card__header > .a-card__title"):
#     title = el.select(".caption > h5 > a")
#     print(title[0].text)
