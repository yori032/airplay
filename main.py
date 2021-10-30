#!/usr/bin/env python
# coding: utf-8
import io

import requests
import pandas as pd
import toml
from bs4 import BeautifulSoup


def scrape_radio_channel_filter(name, date, hour):
    page = requests.get('http://www.airplay.ch/playlist.asp',
                        params={'radio': name, 'datum': date, 'zeit': hour})
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        table = soup.find('table')
        df = pd.read_html(str(table))
        df[2].to_csv('data/{}.csv'.format(name), mode='a', header=False)
        return df
    except IndexError:
        pass


def main():
    with io.open('stations.toml') as stations_file:
        config = toml.load(stations_file)
    for station_name in config['stations']:
        for station_date in config['months']:
            for station_day in config['days']:
                for station_hour in config['hours']:
                    print('Scraping', station_name, 'in', station_date, station_day, 'on Hour:', station_hour)
                    scrape_radio_channel_filter(station_name, str(station_date+station_day), station_hour)


if __name__ == '__main__':
    main()

