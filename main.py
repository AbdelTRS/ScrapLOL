import requests
from bs4 import BeautifulSoup
import requests_cache
requests_cache = requests_cache.install_cache('cache')

page = r'https://leagueoflegends.fandom.com/wiki/List_of_champions'


class IMDBScraper():
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
  
    def get_top(self):

        title= self.soup.find('h1', class_='page-header__title').text
        print(title)
        desc = self.soup.find('div', class_='mw-parser-output')
        para = desc.find('p').text
        print(para)

    def get_championlist(self):
        sub_row = self.soup.find('table', class_='article-table').find('tbody').find_all('tr')
        del sub_row[0]
        for row in sub_row:
            if(row.find_all('td')[4].find('span') != None and row.find_all('td')[5].find('span') != None):
                champion = {
                    'Champions': row.find_all('td')[0]['data-sort-value'],
                    'Classes': row.find_all('td')[1]['data-sort-value'],
                    'Release date': row.find_all('td')[2].text.replace('\n',''),
                    'Patch version': row.find_all('td')[3].find('a')['title'],
                    'BE': row.find_all('td')[4].find('span').text,
                    'Riot Points': row.find_all('td')[5].find('span').text,
                }
                print(champion)

    def get_upcomingreduction(self):
        title = self.soup.find('h3').find('span', class_=('mw-headline')).text
        exerpt = self.soup.find('dd').find('div', class_=('dablink')).text
        price = self.soup.dl.find_next('ul').find('li').text
        
        print(title,exerpt,price)

    def get_scrapedChampion(self):
        scrapped = self.soup.find('span', {"id": "List_of_Scrapped_Champions"}).text
        ul= self.soup.find("div",class_="columntemplate").find("ul").find_all("li")
        for row in ul:
            title = row.find('a')["title"]
            print(title, scrapped)

    def get_trivia(self):
        trivia = self.soup.find('span', {"id": "Trivia"}).text
        print(trivia)

    def get_urf(self):
        urf = self.soup.find('div', class_=('columntemplate')).find_next('h2').find_next('ul').find_all("li")
        for row in urf:
            subtitle = row.find('a')["title"]
            print(subtitle)


top = IMDBScraper(page).get_top()
championlist = IMDBScraper(page).get_championlist()
reducs = IMDBScraper(page).get_upcomingreduction()
list = IMDBScraper(page).get_scrapedChampion()
trivia = IMDBScraper(page).get_trivia()
urf = IMDBScraper(page).get_urf()
print(top, championlist, reducs, list, trivia, urf)