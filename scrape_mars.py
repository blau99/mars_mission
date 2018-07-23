import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import pandas as pd


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_news():

    # Initialize browser
    browser = init_browser()

    url = url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find latest headline and blurb
    news_title = soup.find('div', class_='content_title').a.text
    news_p = soup.find('div', class_='article_teaser_body').text

    news = {
        "news_title": news_title,
        "news_p": news_p
    }

    return news

def scrape_featured():

    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = 'https://www.jpl.nasa.gov' + soup.find('article', class_='carousel_item')['style'].split("'")[1]

    featured = {
        "featured_image_url": featured_image_url
    }

    return featured

def scrape_weather():

    browser = init_browser()

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    weather = {
        "mars_weather": mars_weather
    }

    return weather

def scrape_table():
    browser = init_browser()

    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description','Values']
    df.set_index('Description', inplace=True)
    html_table = df.to_html()
    html_table.replace('\n', '')
    # mars_data['html_table'] = html_table

    table = {
        "mars_table": html_table
    }

    return table

def scrape_images():

    browser = init_browser()

    urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
            'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced',
           'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
           'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced']
    hemisphere_image_url = []

    for url in urls:
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)
        html = browser.html

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2',class_='title').text
        img_url = "https://astrogeology.usgs.gov/"+ soup.find('img',class_='wide-image')['src']
        hemisphere_image_url.append({"title":title,"img_url":img_url})

    # Store in dictionary
    images = {
        "hemisphere_image_url": hemisphere_image_url
    }

    # Return results
    return images
