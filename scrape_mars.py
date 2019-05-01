
# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import time




# Set the chromedriver path
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Create a data dictionary for all the scraped data
    mars_data = {}

    #Write URL to HTML
    url_news = "https://mars.nasa.gov/news/"
    browser.visit(url_news)
    time.sleep(2)
    html = browser.html
    soup = bs(html,"html.parser")
    #Print out News Titles and Paragraphs
    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    mars_data['news_title'] = news_title
    mars_data['news_summary'] = news_p


    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)
    # Design an XPATH selector to grab the Featured Image on the page
    xpath = '//*[@id="full_image"]'

    # Use splinter to Click the Mars Featured image 
    # to bring up the full resolution image
    results = browser.find_by_xpath(xpath)
    results.click()
    #Capture image url and save as featured_image_url
    time.sleep(2)
    html = browser.html
    soup = bs(html, 'html.parser')
    img_url = soup.find("img", class_="fancybox-image")["src"]
    img_url
    #Capture Base URL
    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
    base_url
    #Combine Base_Url and img_url
    featured_image_url = base_url+img_url
    mars_data["featured_image_url"] = featured_image_url

    #Vist the Mars Weather Twitter account for latests weather tweets
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    #Scrape Twitter and print out current weather on Mars
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_data["mars_weather"] = mars_weather
    
    #Import Facts table to Pandas
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    mars_facts = table[0]
    mars_facts = mars_facts.set_index(0).rename(columns={1: "Value"})
    del mars_facts.index.name

    #Write Table to HTML
    facts_html_table = mars_facts.to_html()

    #Take out "\n"
    facts_html_table = facts_html_table.replace("\n", "")
    mars_data['mars_table'] = facts_html_table

    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    #Get Base URL
    hbase_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
    hbase_url
    # Define Data Dictionary
    mars_hemispheres=[]
# loop through Each of the Four Pages
    for i in range (4):
        time.sleep(1)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        p_url = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = hbase_url + p_url
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemispheres.append(dictionary)
        browser.back()
    mars_data['mars_hemispheres'] = mars_hemispheres
    # Close the browser after scraping
    browser.quit()
    #Return the Dictionary
    return mars_data








