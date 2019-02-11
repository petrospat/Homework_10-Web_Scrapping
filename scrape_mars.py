# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import requests
import pymongo
import time

# Web page parsing function
def url_soup (url):
    executable_path = {'executable_path': './chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    # Retrieve page with the html module
    html = browser.html
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(html, 'html.parser')
    browser.quit()
    return soup

def scrape ():  
    #Webpages to be visited
    x = 'https://mars.nasa.gov/news/'
    y = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    z = 'https://twitter.com/marswxreport?lang=en'
    w = 'https://space-facts.com/mars/'
    q = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Webscrap Nasa news 
    soup = url_soup(x)
    results = soup.find_all('li', class_='slide')

    #initialize lists for use at python
    news_title = []
    news_description = []

    for result in results:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes    
        
        try:
            # Identify and return title of listing
            title = result.find('h3').text
            description = result.find('div', class_="article_teaser_body").text
            news_title.append(title)
            news_description.append(description)
            print(title)
            print(description)
            print('-----------')
            
        except SyntaxError as s:
            print(s)
    
    #Webscrap images

    soup = url_soup(y)

    #Extract featured image JPG id 
    featured_image = soup.find('div', class_='carousel_container')
    link = featured_image.a['data-fancybox-href']
    #Image link buid up
    jpg_id = link.split("/mediumsize/")[1].split("_ip")[0]
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/'+ jpg_id +'_hires.jpg'
    print(featured_image_url)
   
    #Webscrap tweeter

    soup = url_soup(z)

    # Get list of tweets with weather
    tlist = soup.find_all("li", class_="js-stream-item")
    wtext = None

    # Search through list for weather tweet/ skip retweets
    for t in tlist:
        if t.div["data-screen-name"] == "MarsWxReport":       
            wtext = t.find(class_="tweet-text").a.previousSibling 
    #             if "Sol" in str(wtext):
    #                 wtext
            break   
    print(wtext)
    

    # Webscrap MarsFacts
    #Scrap html table into a dataframe and back to html
    tables = pd.read_html(w)
    df = tables[0]
    df.columns = ['property','fact']
    html_table = df.to_html()
    print(html_table)
    

    #Webscrap Mars Hemispheres
    
    soup = url_soup(q)

    #Extract featured image JPG id 
    get_headers = soup.find_all('div', class_='item')

    header = []
    img_url = []
    hemisphere_image_urls = {}

    for g in get_headers:
        
        t = g.find('h3').text
        img_src = g.a['href']
        img_src_sp = img_src.split("/search/map/")[1]
        f_img = 'https://astropedia.astrogeology.usgs.gov/download/' + img_src_sp + '.tif/full.jpg'
        header.append(t)
        img_url.append(f_img)

    #Zip lists, Transpose them and convert them into a list of Dictionaries
    hemisphere_image_urls  = []

    z = pd.DataFrame(list(zip(header,img_url)),columns =['header','img_url']).T.to_dict()

    for x in range(len(header)):
        hemisphere_image_urls .append(z[x])
    
    print(hemisphere_image_urls)

    mars_data = {}

    mars_data["Title"] = news_title[0]
    mars_data["Description"] = news_description[0]
    mars_data["Mars_Img"] = featured_image_url
    mars_data["Weather"] = wtext
    mars_data["Facts"] = html_table
    mars_data["Hemispheres"] = hemisphere_image_urls


    return mars_data
