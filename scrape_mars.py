from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

mars_dictionary = {}
def scrape_info():
    
   
    browser = init_browser()

    #NASA 
    nasa_url = 'https://mars.nasa.gov/news'
    browser.visit(nasa_url)

    nasa_html = browser.html
    soup = bs(nasa_html, 'html.parser')

    title_results = soup.find_all('div', class_='content_title')
    news_title = title_results[1].text
    paragraph_results = soup.find_all('div', class_= 'article_teaser_body')
    news_paragraph = paragraph_results[0].text

    # Dictionary entry from MARS NEWS
    mars_dictionary['news_title'] = news_title
    mars_dictionary['news_paragraph'] = news_paragraph

    # return mars_dictionary

    #JPL - Featured Image

    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)


    jpl_html = browser.html
    soup = bs(jpl_html, 'html.parser')


    featured_image_url = soup.find('img', class_='fancybox-image').get("src")
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{featured_image_url}'
    mars_dictionary['featured_image_url'] = featured_image_url


    #Mars_Facts

    mars_fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_fact_url)
    df = tables[0]
    df.columns = ['Description', 'Value']
    html_table = df.to_html(header=False, index=False)
    mars_dictionary['mars_facts'] = html_table


    #Hemispheres
    try:
        hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        shorten_url = 'https://astrogeology.usgs.gov/'

        browser.visit(hemisphere_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        results_list = soup.find_all('div', class_='collapsible results')
        results = results_list[0]
        hemisphere_tags = results.find_all('img')

        hemisphere_list = []
        for tag in hemisphere_tags:
            title = tag['alt']
            image_source = tag['src']
            image_url = shorten_url + image_source
    
            hemisphere_dictionary = {"title": title, "image_url": image_url}
            hemisphere_list.append(hemisphere_dictionary)
            mars_dictionary['hemisphere_list'] = hemisphere_list
            
    except:
        print("hemisphere error") 
        mars_dictionary["hemisphere_list"] = [
            {"title": "not found", "image_url": 'https://cdn5.vectorstock.com/i/1000x1000/73/49/404-error-page-not-found-miss-paper-with-white-vector-20577349.jpg'},
            {"title": "not found", "image_url": 'https://cdn5.vectorstock.com/i/1000x1000/73/49/404-error-page-not-found-miss-paper-with-white-vector-20577349.jpg'},
            {"title": "not found", "image_url": 'https://cdn5.vectorstock.com/i/1000x1000/73/49/404-error-page-not-found-miss-paper-with-white-vector-20577349.jpg'},
            {"title": "not found", "image_url": 'https://cdn5.vectorstock.com/i/1000x1000/73/49/404-error-page-not-found-miss-paper-with-white-vector-20577349.jpg'}
        ]

    # Close the browser after scraping
    browser.quit()
    return mars_dictionary