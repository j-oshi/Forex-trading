import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os, sys

parent_dir = os.path.abspath('..')
forex_file = parent_dir + '\datas\currencies.csv'

def get_all_currencies():

    """dataframe of info of all currency code in the world"""
    try:

        url = 'https://www.fxexchangerate.com/currency-symbols.html'
        request = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs(request.text, "lxml")        
        table = soup.find('table', class_='fxtable')        
        header = table.find("tr")
        
        # empty list
        list_header = []
        for items in header.findAll('th'):
            try:
                list_header.append(items.get_text())
            except:
                continue
        
        # for getting the data
        HTML_data = table.find_all("tr")[1:]
 
        output_rows = []
        for table_row in HTML_data:
            columns = table_row.findAll('td')
            output_row = []
            for column in columns:
                output_row.append(column.text)
            output_rows.append(output_row)
            
        dataFrame = pd.DataFrame(data = output_rows, columns = list_header)        

        # Converting Pandas DataFrame
        # into CSV file
        dataFrame.to_csv(forex_file, index=False)
        print('Currencies list download complete')
    except requests.exceptions.Timeout:
      print("Timeout occurred")
