import requests
from bs4 import BeautifulSoup

def restaurant(x, y):
    name = []
    type = []
    url = "http://apis.data.go.kr/B551011/KorService1/locationBasedList1"
    paramDict = {
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "serviceKey": "KWyscPcYr1noVXPOVDIQaqTO/jx61sgGZhTagP0jJQyIWQhZaWLY/wzdUpgKkZ+DB83gnI+Dd7OgXJm3NQHDIg==",
        "mapX": x,
        "mapY": y,
        "radius": 1000,
        "numOfRows": 1000,
        "pageNo": 1,
        "arrange": "E",
        "listYN": "Y",
        "contentTypeId": 39
    }

    res = requests.get(url, params=paramDict)
    xml = res.text
    soup = BeautifulSoup(xml, 'html.parser')
    for tag in soup.find_all('title'):
        name.append(tag.text)
    for tag in soup.find_all('cat3'):
        if tag.text == 'A05020100':
            type.append('한식')
        elif tag.text == 'A05020200':
            type.append('양식')
        elif tag.text == 'A05020300':
            type.append('일식')
        elif tag.text == 'A05020400':
            type.append('중식')
        elif tag.text == 'A05020700':
            type.append('이색음식')
        elif tag.text == 'A05020900':
            type.append('카페')
        elif tag.text == 'A05021000':
            type.append('클럽')

    result = list(zip(name, type))

    return result
