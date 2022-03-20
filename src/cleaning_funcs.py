from tokenize import group
import numpy as np

def clean_scraped_df(scraped_df):
    
    scraped_df.columns = [x.replace(' ','_').lower() for x in scraped_df.columns]

    float_cols = ['prize_amount', 'odds_of_winning', 'total_prizes', 'prizes_remaining',
                  'prizes_paid', 'ticket_cost', 'odds_denominator']

    scraped_df = scraped_df.apply(lambda x: x.str.replace('$','').str.replace(',',''))

    scraped_df['odds_denominator'] = scraped_df['odds_of_winning'].apply(lambda x: float(x.split('-in-')[1]))
    scraped_df['odds_of_winning'] = scraped_df['odds_of_winning'].apply(lambda x: float(x.split('-in-')[0])/float(x.split('-in-')[1]))

    #Error handling
    l = []
    for x in scraped_df['prize_amount']:
        try:
            l.append(float(x))
        except:
            l.append(np.NaN)
    scraped_df['prize_amount'] = l

    for col in float_cols:
        scraped_df[col] = scraped_df[col].astype(float, errors = 'ignore')

    scraped_df['initial_expected_value'] = scraped_df['prize_amount'] * scraped_df['odds_of_winning']


    grouped_df = scraped_df.groupby(['title','ticket_cost']).sum().sort_values('initial_expected_value', ascending = False).reset_index()
    grouped_df['exp_ratio'] = grouped_df['initial_expected_value'] / grouped_df['ticket_cost']

    grouped_df[grouped_df['ticket_cost'] == 10].sort_values('exp_ratio', ascending = False)

    return scraped_df

def group_scraped_df(scraped_df):
    
    grouped_scraped_df = scraped_df.groupby(['title','ticket_cost']).sum().reset_index()
    grouped_scraped_df['exvalue_cost_ratio'] = grouped_scraped_df['initial_expected_value'] / grouped_scraped_df['ticket_cost']
    grouped_scraped_df.sort_values('exvalue_cost_ratio', inplace = True)

    return grouped_scraped_df