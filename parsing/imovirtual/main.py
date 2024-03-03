import asyncio
import json
import time

from bs4 import BeautifulSoup
import requests

from portugal.Portugal.bot.config import cookies, headers


def pars_exact_flat(url: str) -> dict:
    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )

    html = BeautifulSoup(response.text, 'lxml')
    with open('bs.json', 'w') as f:
        json.dump(str(html), f)
    image_tag = html.find('picture').find('img')
    name = html.find('header', class_='css-sos826 efcnut31').find('h1', class_="css-1wnihf5 efcnut38").text
    main_data = html.find('div', class_="css-c078ty e17tijfc0")
    data = main_data.find_all('div', class_="css-1v52owc e1qm3vsd0")
    photo_link = image_tag.get('src') if image_tag else None
    price = html.find('header', class_='css-sos826 efcnut31').find('strong').text
    data_for_bot = {}
    for e in data:
        title = e.find('div', class_="css-o4i8bk e1qm3vsd1").text
        text = e.find('div', class_='css-1ytkscc e1qm3vsd3').text
        data_for_bot[title] = text
    data_for_bot['price'] = price
    data_for_bot['name'] = name
    data_for_bot['photo'] = photo_link
    return data_for_bot


def pars(from_date, to_date, city, area, type_topologia, min_price, max_price):
    print(city, area, type_topologia, min_price, max_price)
    topologia = []
    for t in type_topologia.split():
        try:
            topologia.append(str(int(t)))
        except Exception:
            pass
    data = []
    for i in range(1, 4):
        link, city_name = get_link_area(city, area)
        # URL = f'https://www.imovirtual.com/arrendar/{city_name}/{get_link( topologia, min_price, max_price)}{link}&page={i}'
        URL = f'https://www.imovirtual.com/arrendar/{get_link(topologia, min_price, max_price)}{link}&page={i}'
        print(URL)
        response = requests.get(URL, cookies=cookies, headers=headers)
        html = BeautifulSoup(response.text, 'lxml')
        list_with_all = list(map(lambda x: x.get('data-url'),
                                 html.find('div', class_="row section-listing__row").find('div',
                                                                                          class_="col-md-content section-listing__row-content").find_all(
                                     'article')))
        for i in list_with_all:
            data.append(i)
    print("return data")
    return data


'https://www.imovirtual.com/arrendar/lisboa/?search%5Bfilter_float_price%3Afrom%5D=1234&search%5Bfilter_enum_rooms_num%5D%5B0%5D=1&search%5Bfilter_enum_rooms_num%5D%5B1%5D=2&search%5Bregion_id%5D=11'
'https://www.imovirtual.com/arrendar/&locations%5B0%5D%5Bregion_id%5D=11&locations%5B0%5D%5Bsubregion_id%5D=0&locations%5B1%5D%5Bregion_id%5D=8'
'https://www.imovirtual.com/arrendar/lisboa/&search%5Border%5D=created_at_first%3Adesc&search%5Bregion_id%5D=11&search%5Bsubregion_id%5D=148&search%5Bcity_id%5D=11535378&page=1'


def get_link(topologia: list, price_from, price_to):
    ful_url = ''
    price = ''
    sortirovka = ''
    if price_from != '-':
        price += f'search%5Bfilter_float_price%3Afrom%5D={str(price_from)}'
    if price_to != '-':
        price += f'&search%5Bfilter_float_price%3Ato%5D={str(price_to)}'
    topologia = '&search%5Bfilter_enum_rooms_num%5D%5B2%5D='.join(topologia)[1:]
    # sortirovka = '&search%5Border%5D=created_at_first%3Adesc'  # сортировка по дате анонса
    ful_url += '?' + price + topologia + sortirovka
    return ful_url


def get_link_area(city, area):
    link = city_name = ''
    URL = f'https://www.imovirtual.com/ajax/geo6/autosuggest/?data={city}%20{area}&lowPriorityStreetsSearch=true&levels%5B0%5D=REGION&levels%5B1%5D=SUBREGION&levels%5B2%5D=CITY&levels%5B3%5D=DISTRICT&levels%5B4%5D=STREET&withParents=true'
    response = requests.get(URL, cookies=cookies, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            city_name = data[0].get('parents')[0].get('name').lower()
            print(city_name)
            region_id, subregion_id, city_id = data[0].get('region_id'), data[0].get('subregion_id'), data[0].get(
                'city_id')
            # link = f'&search%5Bregion_id%5D={region_id}&search%5Bsubregion_id%5D={subregion_id}&search%5Bcity_id%5D={city_id}'
            link = f'&locations%5B0%5D%5Bregion_id%5D={region_id}&locations%5B0%5D%5Bsubregion_id%5D={subregion_id}&locations%5B1%5D%5Bregion_id%5D={city_id}'
        except IndexError:
            pass
    return link, city_name


'https://www.imovirtual.com/arrendar/?search%5Bfilter_enum_rooms_num%5D%5B2%5D=10&locations%5B0%5D%5Bregion_id%5D=11&locations%5B0%5D%5Bsubregion_id%5D=163&locations%5B1%5D%5Bregion_id%5D=11550728'
'https://www.imovirtual.com/arrendar/?search%5Bfilter_enum_rooms_num%5D%5B0%5D=10&locations%5B0%5D%5Bregion_id%5D=11&locations%5B0%5D%5Bsubregion_id%5D=163&locations%5B1%5D%5Bregion_id%5D=11550728'


def my_pars():
    data = []
    for i in range(1, 4):
        URL = f'https://www.imovirtual.com/arrendar/?page={i}'
        response = requests.get(URL, cookies=cookies, headers=headers)
        html = BeautifulSoup(response.text, 'lxml')
        list_with_all = list(map(lambda x: x.get('data-url'),
                                 html.find('div', class_="row section-listing__row").find('div',
                                                                                          class_="col-md-content section-listing__row-content").find_all(
                                     'article')))
        data += list_with_all
    print(data)

    return data


def my_cont_pars(from_date, to_date, city, area, type_topologia, min_price, max_price):
    data = set(my_pars())
    # await asyncio.sleep(3600)
    time.sleep(10800)
    data_new = set(my_pars())
    data = (data | data_new) - (data & data_new)
    print(data)
    for e in data:
        response = requests.get(
            e,
            cookies=cookies,
            headers=headers,
        )
        html = BeautifulSoup(response.text, 'lxml')
        data = html.find_all('a', class_='css-1in5nid e19r3rnf1')
        city_get = data[1].text
        area_get = data[2].text
        type_get = html.find_all('div', class_='css-1v52owc e1qm3vsd0')[1].find('div', "css-1ytkscc e1qm3vsd3").text[1]
        price_get = html.find('header', class_='css-sos826 efcnut31').find('strong').text.split()
        real_price = ''
        for el in price_get:
            if el.isdigit():
                real_price += el

        if city == city_get and max_price >= int(
                real_price) >= min_price and type_get == type_topologia:
            print(city_get, area_get, real_price, type_get,e, sep="|")


my_cont_pars(1, 1, 'Porto', 'Vila Nova de Gaia', '2', 1000, 2000)
# arr1 = pars()
# arr1 = set(arr1)
# time.sleep(1800)
# arr2 = pars()
# time.sleep(1800)
# arr3 = pars()
# arr2 = set(arr2)
# arr3 = set(arr3)
# if len((arr1 | arr2 | arr3) - (arr1 & arr2 & arr3)) > 0:
#     print((arr1 | arr2 | arr3) - (arr1 & arr2 & arr3))
# else:
#     print('LOX')
