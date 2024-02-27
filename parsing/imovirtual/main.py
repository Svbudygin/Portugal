from bs4 import BeautifulSoup
import requests

from config import cookies, headers


def pars_exect_flat(*args):
    # URL = 'https://www.imovirtual.com/pt/anuncio/apartamento-t0-em-paranhos-ID1e0c3.html#71766add10'
    URL = 'https://www.imovirtual.com/pt/anuncio/apartamento-t1-perto-da-praia-com-vista-mar-e-garagem-em-quarteira-ID1bcgB.html#ab04badaa0'
    response = requests.get(
        URL,
        cookies=cookies,
        headers=headers,
    )

    html = BeautifulSoup(response.text, 'lxml')
    name = html.find('header', class_='css-sos826 efcnut31').find('h1', class_="css-1wnihf5 efcnut38").text
    main_data = html.find('div', class_="css-c078ty e17tijfc0")
    data = main_data.find_all('div', class_="css-1v52owc e1qm3vsd0")
    price = html.find('header', class_='css-sos826 efcnut31').find('strong').text
    data_for_bot = {}
    for e in data:
        title = e.find('div', class_="css-o4i8bk e1qm3vsd1").text
        text = e.find('div', class_='css-1ytkscc e1qm3vsd3').text
        data_for_bot[title] = text
    data_for_bot['price'] = price
    data_for_bot['name'] = name
    print(data_for_bot)


def pars(*args):
    URL = 'https://www.imovirtual.com/comprar/apartamento/'
    response = requests.get(
        URL,
        cookies=cookies,
        headers=headers,
    )

    html = BeautifulSoup(response.text, 'lxml')
    name = list(map(lambda x: x.get('data-url'),
                    html.find('div', class_="row section-listing__row").find('div',
                                                                             class_="col-md-content section-listing__row-content").find_all(
                        'article')))
    print(name)


if __name__ == "__main__":
    pass
pars()
