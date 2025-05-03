import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Dictionary of team URLs
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

def process_data(urls):
    names = []
    heights = []

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            name_tags = soup.find_all('td', class_='sidearm-table-player-name')
            height_tags = soup.find_all('td', class_='height')

            for name_tag, height_tag in zip(name_tags, height_tags):
                name = name_tag.get_text(strip=True)
                raw_height = height_tag.get_text(strip=True)

                if '-' in raw_height:
                    split_height = raw_height.split('-')

                    if len(split_height) == 2 and split_height[0].isdigit() and split_height[1].isdigit():
                        feet = int(split_height[0])
                        inches = int(split_height[1])
                        total_inches = feet * 12 + inches

                        names.append(name)
                        heights.append(total_inches)

    return pd.DataFrame({'name': names, 'height': heights})

# Process data
mens_volleyball_df = process_data(sports_teams['mens_volleyball'])
mens_swimming_df = process_data(sports_teams['mens_swimming'])
womens_volleyball_df = process_data(sports_teams['womens_volleyball'])
womens_swimming_df = process_data(sports_teams['womens_swimming'])

# Save to CSV
mens_volleyball_df.to_csv('mens_volleyball.csv', index=False)
mens_swimming_df.to_csv('mens_swimming.csv', index=False)
womens_volleyball_df.to_csv('womens_volleyball.csv', index=False)
womens_swimming_df.to_csv('womens_swimming.csv', index=False)

# Calculate averages
print("\nAverage Heights:")
print("Men's Volleyball:", mens_volleyball_df['height'].mean())
print("Men's Swimming:", mens_swimming_df['height'].mean())
print("Women's Volleyball:", womens_volleyball_df['height'].mean())
print("Women's Swimming:", womens_swimming_df['height'].mean())

# Tallest and Shortest
def extremes(df, label):
    tallest = df[df['height'] >= df['height'].nlargest(5).min()]
    shortest = df[df['height'] <= df['height'].nsmallest(5).max()]
    print(f"\nTallest {label}:")
    print(tallest)
    print(f"\nShortest {label}:")
    print(shortest)

extremes(mens_volleyball_df, "Men's Volleyball")
extremes(mens_swimming_df, "Men's Swimming")
extremes(womens_volleyball_df, "Women's Volleyball")
extremes(womens_swimming_df, "Women's Swimming")
