import requests
from bs4 import BeautifulSoup

def restaurant(x, y):
    name = []
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

    return name

