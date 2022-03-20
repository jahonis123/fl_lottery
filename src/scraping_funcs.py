from tokenize import group
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
from sqlalchemy import over

def get_scraped_df(lottery_url):
    re = requests.get(lottery_url)

    soup = BeautifulSoup(re.text, 'html.parser')

    overall_df = pd.DataFrame()

    amounts =['1','2','3','5','10','20','30']


    for amount in amounts:
        tickets = soup.find_all("div", {"class": f"ticket amount{amount}"})

        for ticket in tickets:

            try:        
                title = ticket.find('span', {'class': 'h1Alt'}).text

                odds_table = ticket.find('table', {'class':"scratchOdds"})

                columns = [x.text for x in odds_table.find('thead').find_all('th')]

                other_dict = {}

                count = 0
                
                if len(odds_table.find('tbody').find_all('tr')[0].find_all('td')) == 5:
                    for odd in odds_table.find('tbody').find_all('tr'):
                        for x, y in zip(columns,odd):
                            if x not in other_dict.keys():
                                other_dict[x] = []
                                other_dict[x].append(y.text)
                            else:
                                other_dict[x].append(y.text)
                else:
                    for odd in odds_table.find('tbody').find_all('tr')[0].find_all('td'):
                        if len(odd.find_all('td')) > 0:
                            little_list = [x.text for x in odd.find_all('td')]
                            other_dict[columns[count]] = little_list
                            count += 1
                
                inter_df = pd.DataFrame(other_dict)
                

                inter_df['Title'] = title
                inter_df['Ticket Cost'] = amount

                overall_df = pd.concat([overall_df, inter_df])
            
            except:
                pass


    return overall_df

