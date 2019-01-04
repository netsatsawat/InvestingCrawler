# InvestingCrawler
The intention of this project is to scrape the commodity or other asset data from investing.com, which utilizes Python to get date, price (open, close), volume, and movement (change in %).

### Usage
The code can run using various Python IDEs (i.e. PyCharm, Spyder) or using command line __(python DataExtraction.py)__. The console output when executing the below code section in **main**.

```python

ihd.print_data()  # display the results on console
ihd.save_historical_data_to_csv()  # save to csv

```

__Output via console___

![output 1](https://github.com/netsatsawat/InvestingCrawler/blob/master/Image/console_output.PNG)


### CSV file

One of the output of the __DataExtraction.py__ is to extract the data onto csv file for future usage. The sample file can be found in the __output__ directory.

![output 2](https://github.com/netsatsawat/InvestingCrawler/blob/master/Image/file_output.PNG)
