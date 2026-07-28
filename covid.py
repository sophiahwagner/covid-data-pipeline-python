import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
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

# Set up seaborn theme and color palette
sns.set_theme(style = 'darkgrid')
sns.color_palette('rocket')

# Create a time series chart for total U.S. COVID cases in 2021
plt.figure(figsize = (8, 5))
time_series = sns.lineplot(data = covid_2021, x='date_updated',y='tot_cases')
plt.title('Total U.S. COVID-19 Cases in 2021', fontsize = 14, weight = 'bold')
plt.xlabel('Date')
plt.ylabel('Total U.S. Cases (in millions)')
time_series.set_xticks(['2021-01', '2021-02','2021-03','2021-04','2021-05','2021-06','2021-07','2021-08','2021-09','2021-10','2021-11','2021-12'])
time_series.set_xticklabels(['Jan','Feb','Mar','Apr','May','June','July','Aug','Sep','Oct','Nov','Dec'])
plt.show()
# This graph indicates that total U.S COVID cases increased steadily during the first several months of 2021 before plateauing from May through August then spiking up again in September and continuing a steady increase for the rest of the year.

# Create a bar chart shoingg cases per 1000 across the four states of interest
covid_plot = year_end_totals.reset_index()
plt.figure(figsize = (8, 5))
sns.barplot(data = covid_plot, x='state', y='cases_per_1000')
plt.title('Total COVID-19 Cases per 1000 People in Certain U.S States in 2021', fontsize = 14, weight = 'bold')
plt.xlabel('State')
plt.ylabel('Cases per 1000')
plt.show()
# This graph indicates that Arizona had the highest number of cases per 1000 of the four states of interest in 2021 and New York had the lowest