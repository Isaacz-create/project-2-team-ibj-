This project is a simple web scraper built with Python that collects athlete names and heights from sports rosters on various school websites. The primary goal is to extract these two data points name and height—for each athlete, organized by sport and school, and then analyze the data to find the tallest and shortest athletes within each sport.

The script works by visiting each roster page URL (manually added to a list within the script or an external file), parsing the HTML to locate name and height information, and storing the results in a structured format such as a CSV file. After collecting the data, it performs basic analysis to identify the tallest and shortest players for each sport.

The project requires Python 3 and the following libraries: requests, beautifulsoup4, and pandas. These can be installed using pip. Once the URLs are set and the scraper is configured to match the structure of the target websites, the script can be run with a single Python command. The output includes a cleaned CSV of athlete data and printed summaries for the tallest and shortest athletes in each sport.

Author: Isaac Zhong

Fixed Errors/Bugs, Cleaned up script/data: Jahmar Lawrence, Brian Chum
