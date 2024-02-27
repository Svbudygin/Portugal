import json

from bs4 import BeautifulSoup
import requests

from config import cookies, headers


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
    print(data_for_bot)
    return data_for_bot


def pars(URL):
    # URL = 'https://www.imovirtual.com/arrendar/'

    response = requests.get(URL, cookies=cookies, headers=headers)

    html = BeautifulSoup(response.text, 'lxml')
    list_with_all = list(map(lambda x: x.get('data-url'),
                             html.find('div', class_="row section-listing__row").find('div',
                                                                                      class_="col-md-content section-listing__row-content").find_all(
                                 'article')))
    return list_with_all


if __name__ == "__main__":
    pass
# pars_exact_flat('https://www.imovirtual.com/pt/anuncio/arrendamento-de-loja-escritorios-em-setubal-ID1dUzP.html#5381dae35a')
pars_exact_flat('https://www.imovirtual.com/pt/anuncio/arrendamento-espaco-comercial-ID1e0q0.html#5381dae35a')
