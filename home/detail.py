import requests
from bs4 import BeautifulSoup

def detail(contentid):
    image = []
    overview = []

    url = "http://apis.data.go.kr/B551011/KorService1/detailCommon1"

    for i in contentid:
        paramDict = {
            "MobileOS": "ETC",
            "MobileApp": "AppTest",
            "serviceKey": "KWyscPcYr1noVXPOVDIQaqTO/jx61sgGZhTagP0jJQyIWQhZaWLY/wzdUpgKkZ+DB83gnI+Dd7OgXJm3NQHDIg==",
            "contentId": i,
            "firstImageYN": "Y",
            "overviewYN": "Y"
        }
        res = requests.get(url, params=paramDict)
        xml = res.text
        soup = BeautifulSoup(xml, 'html.parser')
        for tag in soup.find('firstimage'):
            image.append(tag)
        for tag in soup.find('overview'):
            overview.append(tag)

    result = list(zip(image, overview))
    return result
