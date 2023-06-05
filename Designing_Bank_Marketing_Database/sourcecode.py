import pandas as pd
import numpy as np

# Start coding here...
df_start = pd.read_csv('bank_marketing.csv')
df_client = df_start[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'housing', 'loan']]
df_campaign = df_start[[ 'client_id', 'campaign', 'duration', 'pdays', 'previous', 'poutcome', 'y', 'month', 'day']]
df_economics = df_start[[ 'client_id', 'emp_var_rate', 'cons_price_idx','euribor3m', 'nr_employed']]
df_client = df_client.rename(columns={'client_id': 'id'})
df_campaign = df_campaign.rename(columns={"duration": "contact_duration", "previous": "previous_campaign_contacts", "y": "campaign_outcome", "poutcome": "previous_outcome", "campaign": "number_contacts"})
df_economics = df_economics.rename(columns={"euribor3m": "euribor_three_months", "nr_employed": "number_employed"})
df_client['education'] = df_client['education'].str.replace('.', '_')
df_client['education'] = df_client['education'].replace('unknown', np.NaN)
df_client['job'] = df_client['job'].str.replace('.', '')
df_campaign['previous_outcome'] = df_campaign['previous_outcome'].replace('nonexistent', np.NaN)
df_campaign['previous_outcome'] = df_campaign['previous_outcome'].replace('success', 1)
df_campaign['previous_outcome'] = df_campaign['previous_outcome'].replace('failure', 0)
df_campaign['campaign_outcome'] = df_campaign['campaign_outcome'].replace('yes', 1)
df_campaign['campaign_outcome'] = df_campaign['campaign_outcome'].replace('no', 0)
df_campaign['campaign_id']=1
df_campaign['month']=df_campaign['month'].str.capitalize()
df_campaign['day']=df_campaign['day'].astype(str)
df_campaign['last_contact_date'] = '2022-' + df_campaign['month'] + '-' + df_campaign['day']
df_campaign['last_contact_date']=pd.to_datetime(df_campaign['last_contact_date'], format='%Y-%b-%d')
df_campaign.drop(['month', 'day'], axis='columns', inplace=True)
df_client.to_csv('client.csv', index=False)
df_campaign.to_csv('campaign.csv', index=False)
df_economics.to_csv('economics.csv', index=False)
client_table = """
CREATE TABLE client
(
	id SERIAL PRIMARY KEY,
    age integer,
    job TEXT,
	marital TEXT,
	education TEXT,
	credit_default boolean
	housing boolean,
	loan boolean
);
\copy client from 'client.csv' DELIMITER ',' CSV HEADER"""
campaign_table = """CREATE TABLE campaign
(
    campaign_id SERIAL PRIMARY KEY,
    client_id SERIAL references client (id),
    number_contacts INTEGER,
    contact_duration INTEGER,
    pdays INTEGER,
    previous_campaign_contacts INTEGER,
    previous_outcome BOOLEAN,
    campaign_outcome BOOLEAN,
    last_contact_date DATE    
);
\copy campaign from 'campaign.csv' DELIMITER ',' CSV HEADER
"""
economics_table = """CREATE TABLE economics
(
    client_id SERIAL references client (id),
    emp_var_rate FLOAT,
    cons_price_idx FLOAT,
    euribor_three_months FLOAT,
    number_employed FLOAT
);
\copy economics from 'economics.csv' DELIMITER ',' CSV HEADER
"""

