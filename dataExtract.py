"""
dataExtract.py

Author: Jack Miller
Date: 27-July-2025
Project: FatalBearAttacks_NA
Python version: 3.12.5

Description:
Extract data of fatal bear attacks from Wikipedia

Usage: Extract all fatal north american bear attacks and export to CSV

Dependencies:
-requests
-beautifulsoup4

Output:
BearAttackData.csv

Notes: Data not cleaned with this script
"""
import requests, csv
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_fatal_bear_attacks_in_North_America"

#Send GET request
response = requests.get(url)

#Load HTML for parsing
soup = BeautifulSoup(response.text, 'html.parser')

#Get tables from wiki page
tables = soup.find_all('table', {"class": "wikitable"})

heading_tags = ["h3"]
target_headings = ["Black bear", "Brown bear", "Polar bear"]

#Print how many tables
print(f"There are {len(tables)} tables.")

with open("BearAttackData.csv", mode='w', newline='', encoding="utf-8-sig") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')

    writer.writerow(["Heading", "Date", "Victim", "Captive/Wild", "Location/Circumstances"])

    for table in tables:
        #Get heading, ie black/brown/polar bear
        heading = None
        prev = table.find_previous()
        while prev:
            if prev.name == "h3":
                span = prev.find("span", {"class": "mw-headline"})
                if span:
                    heading = span.get_text(strip=True)
                else:
                    heading = prev.get_text(strip=True)

                break
            prev = prev.find_previous()


        #Loop through 1st row and keep header
        print(f"*{heading}*")
        for row in table.find_all('tr')[1:]:

          #find data in cells
          cells = row.find_all(['td', 'th'])

          #extract data
          data = [cell.get_text(strip=True) for cell in cells]

          #write data
          if data:
              writer.writerow([heading] + data)


