# %%
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# %%
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# %%
####################### NASA Mars News ##########################

# %%
# Mars news URL of page to be scraped
news_url = 'https://redplanetscience.com'

browser.visit(news_url)

html = browser.html

news_soup = BeautifulSoup(html, 'html.parser')

# %%
# Retrieve the latest news title and paragraph
news_title = news_soup.find_all('div', class_='content_title')[0].text
news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

print(news_title)
print("--------------------------------------------------------------------")
print(news_p)

# %%
######################## JPL Mars Space Images - Featured Image ##########################

# %%
# Mars Image to be scraped
spaceimages_mars_url = 'https://spaceimages-mars.com'
images_url = 'https://spaceimages-mars.com/image/featured/mars2.jpg'

browser.visit(images_url)

html = browser.html

images_soup = BeautifulSoup(html, 'html.parser')

# %%
# Retrieve featured image link
relative_image_path = images_soup.find_all('img')[0]["src"]
featured_image_url = spaceimages_mars_url + relative_image_path
print(featured_image_url)

# %%
#######################  Mars Facts ##########################
url_facts='https://galaxyfacts-mars.com/'
tables = pd.read_html(url_facts)
df=tables[0]
df.columns=['Mars - Earth Comparison','Mars','Earth']
df

# %%

Mars_only_df=df[["Mars - Earth Comparison","Mars"]]
Mars_only_df=Mars_only_df[1:]
Mars_only_df=Mars_only_df.rename(columns={"Mars - Earth Comparison":"Info","Mars":"Data"})
Mars_only_df.head()

# %%
html_table = Mars_only_df.to_html()
fact_table=Mars_only_df.to_html('table.html')
print(fact_table)

# %%
######################## Mars Hemispheres ##########################

# %%
hemis_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemis_url)
soup = BeautifulSoup(browser.html, 'html.parser')

hemisphere_image_urls = []

results_hemis = soup.find_all('div', class_='item')

for item in results_hemis:
    title_hemis = item.h3.text
    first_url = hemis_url[:30] + item.find('a', class_='itemLink')['href']
    browser.visit(first_url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    #time.sleep(1)
    final_url = hemis_url[:30] + soup.find('img', class_='wide-image')['src']
    hemisphere_image_urls .append({'title': title_hemis, 'img_url':final_url})
    
hemisphere_image_urls

# %%
# Create dictionary for all info scraped from sources above
mars_dict={
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "fact_table":fact_table,
    "hemisphere_images":hemisphere_image_urls
}

# %%
browser.quit()


