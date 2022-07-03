from bs4 import BeautifulSoup
import requests
import pandas as pd
from pathlib import Path

class Column:
    def __init__(self, column_header, data ,  category):
        self.column_header = column_header
        self.data = data
        self.categoty = category
        
def getConsesus():
    page = requests.get("https://www.census.gov/quickfacts/fact/table/NY,NJ,WA,unioncitycitynewjersey,US/PST045221") #can add new cities by searching for cities in the url and pasting the url here
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all(class_="type") # All 4 tables
    city_list = []#list for all data

    additional_city = Column('title', [], '')#to get title header
    city_list.append(additional_city)

    table_header = tables[0] # header
    cityNames = table_header.find_all(class_="qf-geobox") #div with following class name in header
    for cities in cityNames :
        temp = cities.find('span').get_text()
        city = Column(temp, [], '')
        city_list.append(city)

    #for idx, td in enumerate(tables[1:]):

    table1 = tables[1]
    catRows = table1.findAll('tr')

    for oneRow in catRows:
        elements =  oneRow.findAll('td')
        for idx, td in enumerate(elements):
            element =  td.get_text().strip()
            ind = element.find('\n')#finding index of \n for every cell text to remove special character

#Special character coming before new line so removing if exist
            if ind != -1:
                element = element[ind+1:]

            city_list[idx].data.append(element)


    datadictionary = {}
    for everyCity in city_list:
        datadictionary[everyCity.column_header] = everyCity.data

    data = pd.DataFrame(datadictionary)
    filepath = Path('folder/subfolder/out3.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(filepath)
    print("Data  created successfully")
    
if __name__ == '__main__':
    print_hi('Taiyo')
    getConsesus()
