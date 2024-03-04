import csv
import json
import cloudscraper
from parsel import Selector
data_list = []

scraper = cloudscraper.create_scraper()

for i in range (1, 3):

    r = scraper.get(f'https://www.olx.com.br/imoveis/venda/estado-sp?o={i}')
    response = Selector(text=r.text)
    html = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
    houses = html.get('props').get('pageProps').get('ads')
    for house in houses:
        additional_properties = {prop['label']: prop['value'] for prop in house.get('properties', [])}
        images = house.get('images', [])
        url = house.get('url')
        first_image = images[0] if images else None
        data_list.append({
            'title': house.get('title'),
            'Preco': house.get('price'),
            'location': house.get('location'),
            'url': url,
            'additional_properties': additional_properties,
            'first_image': first_image
        })
print('dados baixados')


fields = ['title', 'price', 'location']

json_file_path = 'olx_houses.json'



with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=2)

print(f'Data saved to {json_file_path}')


