import os
import sys
import yaml

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(DIR_PATH + "/../src/")

from scraping_funcs import get_scraped_df
from cleaning_funcs import clean_scraped_df, group_scraped_df

CONFIG_FILE = DIR_PATH + "/../data/lottery.yml"

with open(CONFIG_FILE) as stream:
    YAML_DATA = yaml.safe_load(stream)
    
lottery_url = YAML_DATA.get("lottery_url")

if __name__ == '__main__':
    scraped_df = get_scraped_df(lottery_url)
    scraped_df = clean_scraped_df(scraped_df)
    grouped_df = group_scraped_df(scraped_df)
    