"""
@FileName: 001. Data Extraction.py
@Description: The main program file for commodity data extraction, main capability is to extract the latest price
   and historical prices for the specified time period

@Author: Satsawat N.
@Version:
   01/03/2019 (SN): Initial version

@Note:
   First version is only supported London gas oil future price

"""

import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup
import urllib

# Global variable for https://www.investing.com/commodities/london-gas-oil-historical-data
# this can get from inspecting the html elements on the web
CFD = {
    'name': 'CFD',
    'curr_id': 8861,
    'smlID': 300084,
    'header': 'London Gas Oil Futures',
    'sort_col': 'date',
    'action': 'historical_data',
    'url': 'https://www.investing.com/commodities/london-gas-oil-historical-data'
}

# Global variable to set https header parameters
HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'referer': 'https://www.investing.com',
    'host': 'www.investing.com',
    'X-Requested-With': 'XMLHttpRequest'
}


class IndexHistoricalData:
    """
    A Class to represent the index data from investing.com

    Attributes
    ----------
    api_url: str
       The string of API URL
    headers: dict
       The dictionary contains the header information
    data: dict
       The dictionary contains the detail data for index scraping
    query_time: string
       The current time of the query is being called
    response: string
       The string contains the request post from the API URL and specified data
    observations:
       The pandas data frame of historical index price of the specified commodity
    latest_price: float
       The latest price of the selected index / commodity

    Methods
    -------
    set_headers(headers)
       Method to set up the header in making API requests
    set_form_data(data)
       Method to set up the data
    set_time_frame_frequency(frequency)
       Method to set up the time frame for the web to scrape
    set_start_end_date(starting_date, ending_date=datetime.datetime.now().strftime("%m/%d/%Y"))
       Method to set the desired time period to scrape from/to
    set_sort_order(sorting_order)
       Method to set the data sorting order
    get_historical_price()
       Method to make the post request and retrieve the historical price from the designated API url
    get_latest_price()
       Method to get the latest price for the current run time
    print_data()
       Method to print the query time, latest price for that time, and historical prices for the specified starting
       and ending time onto the console
    save_historical_data_to_csv()
       Method to save the historical to the csv file

    """

    def __init__(self, api_url):
        """
        Initialize the class variables
        :param api_url: the string of API URL
        :return:
        """
        self.api_url = api_url
        self.headers = None
        self.data = None
        self.query_time = datetime.datetime.now()
        self.response = None
        self.observations = None
        self.latest_price = 0

    def set_headers(self, headers):
        """
        Method to set up the header in making API requests
        :param headers:  dictionary contains the header information
        :return:
        """
        self.headers = headers

    def set_form_data(self, data):
        """
        Method to set up the data
        :param data: the dictionary contains the detail data for index scraping
        :return:
        """
        self.data = data

    def set_time_frame_frequency(self, frequency):
        """
        Method to set up the time frame for the web to scrape
        :param frequency: time frame period of the index price; possible values are Monthly, Weekly, or Daily
        :return:
        """
        self.data['frequency'] = frequency

    def set_start_end_date(self, starting_date, ending_date=datetime.datetime.now().strftime("%m/%d/%Y")):
        """
        Method to set the desired time period to scrape from/to
        :param starting_date: the starting date to scrape; format is MM/DD/YYYY
        :param ending_date: the ending date to scrape; format is MM/DD/YYYY, default is the current run date
        :return:
        """
        self.data['st_date'] = starting_date
        self.data['end_date'] = ending_date

    def set_sort_order(self, sorting_order):
        """
        Method to set the data sorting order
        :param sorting_order: the sorting order of the returned historical data; possible values are DESC, or ASC
        :return:
        """
        self.data['sort_ord'] = sorting_order

    def get_historical_price(self):
        """
        Method to make the post request and retrieve the historical price from the designated API url
        :return:
        """
        self.response = requests.post(self.api_url, data=self.data, headers=self.headers).content
        # parse tables with pandas - [0] probably there is only one html table in response
        self.observations = pd.read_html(self.response)[0]
        return self.observations

    def get_latest_price(self):
        """
        Method to get the latest price for the current run time
        :except URLError: if the web page cannot be requested
        :except ValueError: if the current price cannot be scraped
        :return:
        """
        req = urllib.request.Request(self.data['url'], headers=self.headers)
        web_page = None
        try:
            web_page = urllib.request.urlopen(req).read()

        except urllib.error.URLError as err:
            print(err.reason)

        if web_page is not None:
            try:
                bs = BeautifulSoup(web_page, 'lxml')
                spans = bs.find_all('span', id='last_last')
                lines = [span.get_text() for span in spans]
                str_price = lines[0]
                if ',' not in str_price:
                    current_price = float(str_price)
                else:
                    current_price = float(str_price.replae(',', ''))

            except ValueError:
                print('Fail to parse the latest price')
                return

            self.latest_price = current_price

        else:
            return

    def print_data(self):
        """
        Method to print the query time, latest price for that time, and historical prices for the specified starting
          and ending time onto the console (top 10 records only)
        :return:
        """
        print("%s: The latest price of %s is %s" % (self.query_time.strftime("%Y-%m-%d %H:%M:%S"), self.data["name"],
                                                    self.latest_price))
        print("The retrieved historical prices (top 10) are shown below:")
        print(self.observations.head(10))

    def save_historical_data_to_csv(self):
        """
        Method to save the historical to the csv file
        :return:
        """
        self.observations.to_csv(self.data['name'] + '_' + self.query_time.strftime('%Y%m%d_%H%M%S') + '.csv',
                                 sep=',', index=False)
        print("Save completed!")


if __name__ == "__main__":
    # initialize the index, headers and data
    ihd = IndexHistoricalData('https://www.investing.com/instruments/HistoricalDataAjax')
    ihd.set_headers(HEADERS)
    ihd.set_form_data(CFD)
    # initialize scraping mechanics
    ihd.set_time_frame_frequency('Daily')
    ihd.set_sort_order('DESC')
    ihd.set_start_end_date('1/1/2017')
    # retrieve the data
    ihd.get_latest_price()
    ihd.get_historical_price()
    # data presentation
    ihd.print_data()
    ihd.save_historical_data_to_csv()
