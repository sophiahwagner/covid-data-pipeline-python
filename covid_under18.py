import pandas as pd
import requests
url = "https://data.cdc.gov/resource/pwn4-m3yp.json"
response = requests.get(url, params = {"$limit": 5000})
covid = pd.DataFrame(response.json())
print(covid.shape)
print(covid.head())

covid['date_updated'] = pd.to_datetime(covid['date_updated'], errors='coerce')
covid['new_historic_cases'] = pd.to_numeric(covid['new_historic_cases'], errors='coerce')
covid['new_historic_deaths'] = pd.to_numeric(covid['new_historic_deaths'], errors='coerce')

covid_az = covid[covid['state'] == 'AZ'].copy()
print(covid_az)

cases_az = pd.to_numeric(covid_az['new_historic_cases'], errors='coerce').sum()
deaths_az = pd.to_numeric(covid_az['new_historic_deaths'], errors='coerce').sum()
print("Total cases in AZ:", cases_az)
print("Total deaths in AZ:", deaths_az)


state_populations = {
    "AZ": 7400000,
    "CA": 39000000,
    "NY": 19500000,
    "FL": 22600000
}

total_cases_az = covid_az["new_historic_cases"].sum()
az_population = state_populations["AZ"]
incidence_rate_az = total_cases_az / az_population
print(f"Cumulative incidence rate in AZ: {incidence_rate_az:.2%}")

incidence_rate_per_1000_az = incidence_rate_az * 1000
print(f"Cumulative incidence rate in AZ: {incidence_rate_per_1000_az:.2f} cases per 1,000 population")

state_summary = covid.groupby('state')["new_historic_cases"].sum()
print(state_summary.sort_values(ascending = False).head(10))