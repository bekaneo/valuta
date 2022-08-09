import os
from datetime import datetime
from typing import List, Generator

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
import csv

URL = "https://www.akchabar.kg/ru/exchange-rates/"


def get_response(url: str) -> requests:
    return requests.get(url)


def get_html(response: requests) -> requests:
    return response.text


def get_table(html: requests) -> ResultSet:
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("table", {'id': 'rates_table'})


def get_headers(table: ResultSet) -> List[str]:
    headers = []
    for item in table:
        table_header = item.find_all('th')
        if table_header:
            for th in table_header:
                th = th.text.strip()
                if th in ['USD', 'EURO', 'RUB', 'KGZ']:
                    headers.append(th)
                    headers.append('')
                else:
                    headers.append(th)
    return headers


def get_tr(tables: ResultSet) -> Generator:
    for table in tables:
        table_rows = table.find_all("tr")
        for row in table_rows:
            if row.find_all("td"):
                yield row.find_all("td")


def get_td(table_data: Generator) -> Generator:
    for rows in table_data:
        row_data = []
        for td in rows:
            row_data.append(td.text.strip())
        if row_data:
            yield row_data


def write_csv(headers: List[str], data: Generator) -> None:
    with open(f"{datetime.now().date()}_valuta.csv", "a+", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([str(datetime.now().time())[:5]] + ['––––––' for x in range(8)])
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)


def main(url: str) -> None:
    response = get_response(url)
    html = get_html(response)
    table = get_table(html)
    headers = get_headers(table)
    trs = get_tr(table)
    tds = get_td(trs)
    write_csv(headers, tds)


if __name__ == "__main__":
    main(URL)
