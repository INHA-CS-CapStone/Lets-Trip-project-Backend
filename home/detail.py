import requests
from bs4 import BeautifulSoup

def detail(content_id):
    url = "http://apis.data.go.kr/B551011/KorService1/detailCommon1"

    paramDict = {
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "serviceKey": "KWyscPcYr1noVXPOVDIQaqTO/jx61sgGZhTagP0jJQyIWQhZaWLY/wzdUpgKkZ+DB83gnI+Dd7OgXJm3NQHDIg==",
        "contentId": content_id,
        "firstImageYN": "Y",
        "overviewYN": "Y"
    }

    res = requests.get(url, params=paramDict)
    xml = res.text
    soup = BeautifulSoup(xml, 'html.parser')

    image = soup.find('firstimage').text if soup.find('firstimage') else None
    overview = soup.find('overview').text if soup.find('overview') else None

    return image, overview