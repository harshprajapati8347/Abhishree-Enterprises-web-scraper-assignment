import requests
from bs4 import BeautifulSoup
from datetime import datetime 
import csv
import sqlite3

class VergeScrapping:
    def __init__(self):
        self.url="https://www.theverge.com/"
        self.articles=[]

    def findArticles(self):
        r=requests.get(self.url)
        soup=BeautifulSoup(r.content,'html.parser')

        # find top stories on the page
        articles = soup.find_all('a', class_='group-hover:shadow-underline-franklin')
        authors=soup.find_all('a',class_='text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8')
        dates=soup.find_all('span',class_='text-gray-63 dark:text-gray-94')

        for i, article in enumerate(articles):
            # extract the URL
            url = "https://www.theverge.com/" + article.get('href')

            # extract the headline
            headline = article.text

            # extract the author
            author=authors[i].text
            
            # extract the date
            date=dates[i].text

            # adding details of article in list 
            self.articles.append([i+1,url,headline,author,date])

    def addToCSV(self, file_name):
        header = ["id", "URL", "headline", "author", "date"]
        with open(file_name,'w') as csv_file:
            w=csv.writer(csv_file)
            w.writerow(header)

            for i in self.articles:
                w.writerow(i)


    def addToSqlite(self,sql_file):
        # database connection
        conn=sqlite3.connect(sql_file)
        c=conn.cursor()

        # create table if not exists
        query="CREATE TABLE IF NOT EXISTS ARTICLES (ID INTEGER PRIMARY KEY, URL TEXT,HEADLINE TEXT, AUTHOR TEXT, DATE TEXT)"
        c.execute(query)
        for i in self.articles:
            query=f"INSERT OR IGNORE INTO ARTICLES VALUES ({i[0]},'{i[1]}','{i[2]}','{i[3]}','{i[4]}')"
            c.execute(query)
        conn.commit()
        conn.close()


if __name__=='__main__':
    # today's date
    csv_file=datetime.now().strftime('%d%m%Y')+"_verge.csv"
    sql_file=datetime.now().strftime('%d%m%Y')+"_verge.sqlite3"
    obj= VergeScrapping()
    obj.findArticles()
    obj.addToCSV(csv_file)
    obj.addToSqlite(sql_file)
