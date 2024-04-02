from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import feedparser
import csv
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


# chrome drive path
driver_path = "/usr/local/bin/chromedriver"
s = Service(driver_path)
driver = webdriver.Chrome(service=s)

# categories and their corresponding URLs
categories = {
    "business": "https://www.bbc.co.uk/news/business",
    "tech": "https://www.bbc.co.uk/news/technology",
    "science": "https://www.bbc.co.uk/news/science_and_environment"
}

# open the CSV file for writing
with open('articles2.csv', 'w', newline='') as csvfile:
    fieldnames = ['title', 'content', 'class']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for category, url in categories.items():
        # Load the initial page
        driver.get(url)

        # loop through all pages, for each page:
        for _ in range(50):
            
    
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Find the articles on the page and loop over them
            article_divs_1 = soup.find_all('div', class_='gs-c-promo-body gs-u-mt@xxs gs-u-mt@m gs-c-promo-body--primary gs-u-mt@xs gs-u-mt@s gs-u-mt@m gs-u-mt@xl gel-1/3@m gel-1/2@xl gel-1/1@xxl')
            article_divs_2 = soup.find_all('div', class_='gel-layout__item gs-u-pb+@m gel-1/3@m gel-1/4@xl gel-1/3@xxl nw-o-keyline nw-o-no-keyline@m')
            article_divs = article_divs_1 + article_divs_2

            for div in article_divs:
                try:
                    # get the title and content of the article
                    title = div.find('h3', class_='gs-c-promo-heading__title gel-paragon-bold gs-u-mt+ nw-o-link-split__text')
                    content = div.find('p', class_='gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary')
                    
                    # if the title and content are not found in the first set of classes, look in the second set
                    if not title:
                        title = div.find('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')
                    if not content:
                        content = div.find('p', class_='gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary gs-u-display-none gs-u-display-block@m')

                    # write the data into the CSV file
                    writer.writerow({'title': title.text, 
                                     'content': content.text, 
                                     'class': category})
                    
                except AttributeError:
                    continue

            # click the next page button
            try:
                next_page_button = driver.find_element("css selector", "a.qa-pagination-next-page.lx-pagination__btn--active")
                next_page_button.click()

                time.sleep(5)  # time delay
            except Exception as e:
                print(f" page not found{e}")
                break  

    driver.quit()  
