from splinter import Browser
from bs4 import BeautifulSoup
from splinter.exceptions import ElementDoesNotExist
import time
from pymongo import MongoClient
import pymongo
import requests

executable_path = {'executable_path' :  'C:/Users/renzh/CU-NYC-DATA-PT-10-2019-U-C_master/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape_mars_img_fun():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find('ul', class_="articles")
    categories = articles.find_all('li')

    url_list = []

    def split(word): 
        return [char for char in word][30:38] 
      
    def splitnjoin(word):
        return''.join(split(word)) 

    for category in categories:
        image_overall = category.find('div',class_="img")
        image_url = image_overall.find('img')['src']
        featured_image_url = splitnjoin(image_url)
        Accessible_imgae_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/"+featured_image_url+"_hires.jpg"
        url_list.append(Accessible_imgae_url)
        url_dict = {}
        url_dict['Image_url'] = url_list

    browser.quit()

    return url_dict


def scrape_mars_hemi_fun():
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div',class_="item")
    links = []
    name_list = []
    for item in items:
        link = item.find('a')['href']
        featured_link = ['https://astrogeology.usgs.gov'+link]
        name = item.find('h3')
        links.append(featured_link)
        name_list.append(name.text)
    res =[]

    for link in links:
        for i in link:
            res.append(i)
    
    featured_img_list=[]
    for item in res:
        browser.visit(item)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find('img', class_= "wide-image")['src']
        featured_img = "https://astrogeology.usgs.gov" + img
        featured_img_list.append(featured_img)
    
    dic = {}

    title_list = []

    for item in name_list:
        dic = {}
        dic.update({"title":item})
        title_list.append(dic)
    
    url_list = []

    for item in featured_img_list:
        dic = {}
        dic.update({"img_url":item})
        url_list.append(dic)
    
    def countList(title_list, url_list): 
        return [sub[item] for item in range(len(url_list)) 
                        for sub in [title_list, url_list]] 

    hemisphere_image_urls  = countList(title_list,url_list)
    
    browser.quit()

    return hemisphere_image_urls 

def scrape_mars_news_fun():
    executable_path = {'executable_path' :  'C:/Users/renzh/CU-NYC-DATA-PT-10-2019-U-C_master/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    all_news = soup.find_all('li',class_='slide')
    news_list=[]

    for each in all_news:
        news_dict = {}
        news_title = each.find('div',class_='content_title').find('a')
        news_teaser = each.find('div',class_='article_teaser_body')
        news_dict["news_title"] = news_title.text
        news_dict["news_teaser"] = news_teaser.text
        news_list.append(news_dict)

    browser.quit()

    return news_list

def scrape_mars_weather_fun():
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    mars_weather = soup.find('div',class_= 'tweet').find('p')
    weather_string = mars_weather.text
    data = []
    weather_dict = {"Latest_Weather" : weather_string}
    data.append(weather_dict)
    
    browser.quit()

    return data

