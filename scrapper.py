from selenium import webdriver 
from selenium.webdriver.common.by import By  
from bs4 import BeautifulSoup  
import time 
import pandas as pd 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC  

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"  # URL of the NASA Exoplanet Catalog

# Webdriver
browser = webdriver.Chrome()  # Initializing Chrome WebDriver
browser.get(START_URL)  # Opening the specified URL in the browser

time.sleep(2)  # Adding a delay to allow the page to fully load

planets_data = []  # List to store extracted planet data

# Define Exoplanet Data Scraping Method
def scrape():
    for i in range(0, 5):  # Looping through a range of 10 pages (adjust as needed)
        print(f'Scraping page {i+1} ...')

        # Creating a BeautifulSoup object for the current page
        soup = BeautifulSoup(browser.page_source,"html.parser")

        # Finding all planet elements on the page, find list od div with class hds-content-item and loop on each one as planet
        for planet in soup.find_all("div",class_='hds-content-item'):


            # Create planet_info list to store information about each planet
            planet_info = []
            # Find planet name in h3 tag with class heading-22 in planet and append it to planet_info
            planet_info.append(planet.find('h3',class_='heading-22').text.strip())
        
            # info to be extracted
            information_to_extract = ["Light-Years From Earth", "Planet Mass", 
                                      "Stellar Magnitude", "Discovery Date"]

            # Loop through each info_name
            for info_name in information_to_extract: 
                # Add try block
                try:
                    # Select span from planet which contains info_name as text and then extract text from next sibling span and append it to planet_info
                    planet_info.append(planet.select_one(f'span:-soup-contains("{info_name}")')
                    .find_next_sibling('span').text.strip())
                # Add except block
                except:
                    # Append unknown ro planet_info
                    planet_info.append("Unknown")
            # Add planet information to the list planet_data
            planets_data.append(planet_info)
        # Add try block
        try:
            # Sleep for 2 ms
            time.sleep(2)
            # Find next button
            next_button=WebDriverWait(browser,10).until(EC.element_to_clickable((
                By.XPATH,'/html/body/div[1]/div/div[2]/main/div/div[3]/div/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/a'
            )))

            # Scroll to next button on page
            browser.execute_script("arguments[0].scrollIntoView()",next_button)
            # Sleep for 2 ms
            time.sleep(2)
            # Click next button to go on next page
            next_button.click()
        # Except block
        except:
            # Print Error occurred while navigating to next page: and break the loop
            print(f"error occured while navigating to the nextg page:")
            break

# Calling the scraping method
scrape()

# Define Header for DataFrame
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Create pandas DataFrame from the extracted data
planet_df_1 = pd.DataFrame(planets_data,columns=headers)

# Convert DataFrame to CSV and save to file
planet_df_1.to_csv('scrapped_data.csv',index=True,index_label = "id")

