import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Dictionary of sports team URLs
sports_teams = {
    'mens_volleyball': [
        'https://ccnyathletics.com/sports/mens-volleyball/roster',
        'https://lehmanathletics.com/sports/mens-volleyball/roster',
        'https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster',
        'https://johnjayathletics.com/sports/mens-volleyball/roster',
        'https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster',
        'https://mecathletics.com/sports/mens-volleyball/roster',
        'https://www.huntercollegeathletics.com/sports/mens-volleyball/roster',
        'https://yorkathletics.com/sports/mens-volleyball/roster',
        'https://ballstatesports.com/sports/mens-volleyball/roster'
    ],
    'mens_swimming': [
        'https://csidolphins.com/sports/mens-swimming-and-diving/roster',
        'https://yorkathletics.com/sports/mens-swimming-and-diving/roster',
        'https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster',
        'https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster',
        'https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster',
        'https://mckbearcats.com/sports/mens-swimming-and-diving/roster',
        'https://ramapoathletics.com/sports/mens-swimming-and-diving/roster',
        'https://oneontaathletics.com/sports/mens-swimming-and-diving/roster',
        'https://bubearcats.com/sports/mens-swimming-and-diving/roster/2021-22',
        'https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22'
    ],
    'womens_volleyball': [
        'https://bmccathletics.com/sports/womens-volleyball/roster',
        'https://yorkathletics.com/sports/womens-volleyball/roster',
        'https://hostosathletics.com/sports/womens-volleyball/roster',
        'https://bronxbroncos.com/sports/womens-volleyball/roster/2021',
        'https://queensknights.com/sports/womens-volleyball/roster',
        'https://augustajags.com/sports/wvball/roster',
        'https://flaglerathletics.com/sports/womens-volleyball/roster',
        'https://pacersports.com/sports/womens-volleyball/roster',
        'https://www.golhu.com/sports/womens-volleyball/roster'
    ],
    'womens_swimming': [
        'https://csidolphins.com/sports/womens-swimming-and-diving/roster',
        'https://queensknights.com/sports/womens-swimming-and-diving/roster',
        'https://yorkathletics.com/sports/womens-swimming-and-diving/roster',
        'https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster/2021-22?path=wswim',
        'https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster',
        'https://lindenwoodlions.com/sports/womens-swimming-and-diving/roster',
        'https://mckbearcats.com/sports/womens-swimming-and-diving/roster',
        'https://ramapoathletics.com/sports/womens-swimming-and-diving/roster',
        'https://keanathletics.com/sports/womens-swimming-and-diving/roster',
        'https://oneontaathletics.com/sports/womens-swimming-and-diving/roster'
    ]
}

# Function to scrape data from a list of URLs
def process_data(urls):
    names = []
    heights = []

    for url in urls:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            name_tags = soup.find_all('td', class_='sidearm-table-player-name')
            height_tags = soup.find_all('td', class_='height')

            for name_tag in name_tags:
                names.append(name_tag.get_text().strip())

            for height_tag in height_tags:
                raw_height = height_tag.get_text().strip()
                if '-' in raw_height:
                    parts = raw_height.split('-')
                    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                        feet = float(parts[0]) * 12
                        inches = float(parts[1])
                        height_in_inches = feet + inches
                        heights.append(height_in_inches)
                    else:
                        heights.append(None)
                else:
                    heights.append(None)

    df = pd.DataFrame({'Name': names, 'Height': heights})
    avg_height = df['Height'].mean()
    df['Height'] = df['Height'].fillna(avg_height)

    return df, avg_height

# Scrape data and calculate averages
mens_volleyball_df, mv_avg = process_data(sports_teams['mens_volleyball'])
mens_swimming_df, ms_avg = process_data(sports_teams['mens_swimming'])
womens_volleyball_df, wv_avg = process_data(sports_teams['womens_volleyball'])
womens_swimming_df, ws_avg = process_data(sports_teams['womens_swimming'])

# Save each DataFrame as CSV
mens_volleyball_df.to_csv('mens_volleyball.csv', index=False)
mens_swimming_df.to_csv('mens_swimming.csv', index=False)
womens_volleyball_df.to_csv('womens_volleyball.csv', index=False)
womens_swimming_df.to_csv('womens_swimming.csv', index=False)

# Print average heights
print("Average Heights:")
print("Men's Volleyball:", mv_avg)
print("Men's Swimming:", ms_avg)
print("Women's Volleyball:", wv_avg)
print("Women's Swimming:", ws_avg)

# Function to print tallest/shortest with ties
def print_extremes(df, label):
    tallest = df[df['Height'] >= df['Height'].nlargest(5).min()]
    shortest = df[df['Height'] <= df['Height'].nsmallest(5).max()]
    print(f"\nTallest {label}:")
    print(tallest)
    print(f"\nShortest {label}:")
    print(shortest)

# Print all tallest and shortest athlete lists
print_extremes(mens_swimming_df, "Men's Swimming")
print_extremes(mens_volleyball_df, "Men's Volleyball")
print_extremes(womens_swimming_df, "Women's Swimming")
print_extremes(womens_volleyball_df, "Women's Volleyball")

# Plot bar graph of all 4 averages
labels = ['Men\'s Swimming', 'Men\'s Volleyball', 'Women\'s Swimming', 'Women\'s Volleyball']
averages = [ms_avg, mv_avg, ws_avg, wv_avg]

plt.figure(figsize=(10, 6))
plt.bar(labels, averages)
plt.ylabel('Average Height (inches)')
plt.title('Average Athlete Height by Team Category')
plt.xticks(rotation=15)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('average_heights_bargraph.png')
plt.show()

conn = sqlite3.connect('athlete_heights.db')

# Save each DataFrame to its respective table
mens_volleyball_df.to_sql('mens_volleyball', conn, if_exists='replace', index=False)
mens_swimming_df.to_sql('mens_swimming', conn, if_exists='replace', index=False)
womens_volleyball_df.to_sql('womens_volleyball', conn, if_exists='replace', index=False)
womens_swimming_df.to_sql('womens_swimming', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
