from datetime import datetime
import os

import requests
from bs4 import BeautifulSoup
import csv

url = r"https://www.akchabar.kg/ru/exchange-rates/"

response = requests.get(url)
html_page = response.text

soup = BeautifulSoup(html_page, 'html.parser')
tables = soup.find_all("table", {'id': 'rates_table'})
for index, table in enumerate(tables):

    table_rows = table.find_all("tr")

    with open(f"{datetime.now().date()}_valuta_kg.csv", "a+", newline="") as file:
        writer = csv.writer(file)
        file.seek(0, os.SEEK_END)
        if file.tell():
            writer.writerow([datetime.now().date()] + ['–––––––––––' for x in table_rows])
        for row in table_rows:
            row_data = []
            if row.find_all("th"):
                table_headings = row.find_all("th")
                header_th = []
                for item in table_headings:
                    item = item.text.strip()
                    if item in ['USD', 'EURO', 'RUB', 'KGZ']:
                        header_th.append(item)
                        header_th.append('')
                    else:
                        header_th.append(item)
                for th in header_th:
                    row_data.append(th)
            else:
                table_data = row.find_all("td")
                for td in table_data:
                    row_data.append(td.text.strip())
            writer.writerow(row_data)
