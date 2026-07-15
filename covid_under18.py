import pandas as pd
import requests
url = "https://data.cdc.gov/resource/pwn4-m3yp.json"
count_response = requests.get(url, params={"$select": "count(*)"})
print(count_response.json())
response = requests.get(url, params = {"$limit": 10380, "$order": "state, date_updated"})
covid = pd.DataFrame(response.json())
print(covid.shape)
print(covid.head())

# Fix data types for date and numeric columns
covid['date_updated'] = pd.to_datetime(covid['date_updated'], errors='coerce')
covid['tot_cases'] = pd.to_numeric(covid['tot_cases'], errors='coerce')
covid['tot_deaths'] = pd.to_numeric(covid['tot_deaths'], errors='coerce')

 # Isolate data for 4 distinct states and restrict to 2021 only
covid_2021 = covid[covid['date_updated'].dt.year == 2021].copy()
states_of_interest = ['AZ', 'CA', 'NY', 'FL']
covid_2021_subset = covid_2021[covid_2021['state'].isin(states_of_interest)].sort_values('date_updated')
year_end_totals = covid_2021_subset.groupby('state').last()[['tot_cases', 'tot_deaths']]


#Import estimated state populations for 2021 to compute cumulative incidence rates
state_populations = {
    "AZ": 7400000,
    "CA": 39000000,
    "NY": 19500000,
    "FL": 22600000
}
year_end_totals['population'] = year_end_totals.index.map(state_populations)

# Calculate cumulative incidence rates and cases per 1000 for each state and print results
year_end_totals['incidence_rate'] = year_end_totals['tot_cases'] / year_end_totals['population']
year_end_totals['cases_per_1000'] = year_end_totals['incidence_rate'] * 1000
print(year_end_totals)

# State (out of the 4 analyzed) with the highest cumulative incidence rate
highest = year_end_totals['cases_per_1000'].idxmax()
print(f"The state with the highest cumulative incidence rate among these 4 states in 2021 is {highest} with a rate of {year_end_totals.loc[highest, 'cases_per_1000']:.4f} cases per 1000 people.")