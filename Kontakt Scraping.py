import requests
from bs4 import BeautifulSoup
import pandas as pd

HTML='https://kontakt.az/telefoniya/telefonlar/smartfonlar'
headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

response=requests.get(HTML,headers=headers)

soup=BeautifulSoup(response.content, 'html.parser')

product_link=soup.find_all('div',class_='prodItem product-item')

product_name_text=[]
price_text=[]
discount_price_text=[]
parametr_combined_texts=[]

for i in product_link:
    result=i.find('a',class_='prodItem__img label-image-wrapper').get('href')
    full_link=f"{result}"
    
    product_response = requests.get(full_link, headers=headers)
    product_soup = BeautifulSoup(product_response.content, 'html.parser')

    product_name=product_soup.find('div', class_='page-title-wrapper product')
    if product_name:
        product_name_text.append(product_name.h1.span.get_text(strip=True))
    else:
        product_name_text.append("No name")
    
    price=product_soup.find('span',class_='price-container price-final_price tax weee')
    if price:
        price_text.append(price.span.get_text(strip=True))
    else:
        price_text.append("No number")

    discount_price=product_soup.find('div',class_='prodCart__prices product-desktop-block')
    if discount_price:
        discount_price_text.append(discount_price.span.get_text(strip=True))
    else:
        discount_price_text.append("No number")    
       
    features = product_soup.find_all('div', class_='har__row')
    parametr_text = []
    parametr_nəticə_text = []
    for feature in features:
        title = feature.find('div', class_='har__title')
        value = feature.find('div', class_='har__znach')
        if title and value:
            parametr_text.append(title.get_text(strip=True))
            parametr_nəticə_text.append(value.get_text(strip=True))
    combined_parametr = [f"{param}: {value}" for param, value in zip(parametr_text, parametr_nəticə_text)]
    parametr_combined_texts.append("; ".join(combined_parametr))

dataset={
    'Product name': product_name_text,
    'Price': price_text,
    'Discount price': discount_price_text,
    'Parametrlər': parametr_combined_texts
}

data=pd.DataFrame(dataset)
print(data)
data.to_excel('Kontak mehsul.xlsx')

