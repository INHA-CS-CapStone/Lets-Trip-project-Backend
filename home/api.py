import requests
import ast
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from .models import Place, UserChoice


'''
Encoding
KWyscPcYr1noVXPOVDIQaqTO%2Fjx61sgGZhTagP0jJQyIWQhZaWLY%2FwzdUpgKkZ%2BDB83gnI%2BDd7OgXJm3NQHDIg%3D%3D

Decoding
KWyscPcYr1noVXPOVDIQaqTO/jx61sgGZhTagP0jJQyIWQhZaWLY/wzdUpgKkZ+DB83gnI+Dd7OgXJm3NQHDIg==

<대분류> cat1
A01: 자연
A02: 인문
A03: 레포츠
A04: 쇼핑

<contenttypeid>
관광지 12
문화 시설 14
레포츠 28
쇼핑 38

관광지명 리스트:name - api 태그명 title
관광 타입 리스트:typeId - api 태그명 contenttypeid
대분류 리스트:big - api 태그명 cat1
중분류 리스트:middle - api 태그명 cat2
소분류 리스트:small - api 태그명 cat3
<typeId>
1. 자연 
2. 역사 
3. 인문
4. 레포츠 
5. 쇼핑 
'''

def weighted_rating(x, m, C, user_types):
    v = x['review_count']
    R = x['rating']

    type_weight = 0.05 if x['type'] in user_types else 0

    return ((v / (v + m) * R) + (m / (m + v) * C)) * (1 + type_weight)

def get_similar_places(name):
    places = Place.objects.filter(name__in=name)

    places_info = [
        {
            'name': place.name,
            'rating': place.rating,
            'type': place.type,
            'keyword': ast.literal_eval(place.keyword),
            'review_count': place.review_count,
        }
        for place in places
    ]

    user_choice = UserChoice.objects.get(id=1)
    user_keywords = ' '.join([tag.replace('#', '') for tag in user_choice.tag_names])
    
    keywords = [user_keywords] + [' '.join(info['keyword']) for info in places_info]
    
    count_vec = CountVectorizer()
    v = count_vec.fit_transform(keywords)
    v.toarray()

    sim = cosine_similarity(v, v)
    sim_sorted_ind = sim.argsort()[:, ::-1][0, 1:9]
    sim_sorted_ind = [i-1 for i in sim_sorted_ind]

    similar_places_info = [places_info[i] for i in sim_sorted_ind]
    df = pd.DataFrame(similar_places_info)

    all_places = pd.DataFrame(list(Place.objects.values('rating', 'review_count')))

    C = all_places['rating'].mean()
    m = all_places['review_count'].quantile(0.6)

    df['weighted_rating'] = df.apply(weighted_rating, args=(m, C, user_choice.tourism_types), axis=1)
    df = df.sort_values(by='weighted_rating', ascending=False)

    print(user_choice.tourism_types, user_choice.tag_names)
    
    return df

def api(x, y):
    name = []
    small = []

    url = "http://apis.data.go.kr/B551011/KorService1/locationBasedList1"
    paramDict = {
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "serviceKey": "KWyscPcYr1noVXPOVDIQaqTO/jx61sgGZhTagP0jJQyIWQhZaWLY/wzdUpgKkZ+DB83gnI+Dd7OgXJm3NQHDIg==",
        "mapX": x,
        "mapY": y,
        "radius": 10000,
        "numOfRows": 1000,
        "pageNo": 1,
        "arrange": "E",
        "listYN": "Y"
    }

    idx1 = 0
    idx2 = -1
    res = requests.get(url, params=paramDict)
    xml = res.text
    soup = BeautifulSoup(xml, 'html.parser')
    for tag in soup.find_all('title'):
        name.append(tag.text)
    for tag in soup.find_all('cat3'):
        small.append(tag.text)
    for tag in soup.find_all('contenttypeid'):
        idx2 = idx2 + 1
        if tag.text == '12' or tag.text == '14' or tag.text == '28' or tag.text == '38':
            if "정보센터" in name[idx1] or small[idx2] == 'A04011000' or small[idx2] == 'A04010600':
                del name[idx1]
            else:
                idx1 = idx1 + 1
        else:
            del name[idx1]

    df = get_similar_places(name)
    return df