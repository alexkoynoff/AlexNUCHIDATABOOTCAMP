from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    # Set the chromedriver path - for Windows Users
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():

    # Debug flag. Set it to "True" or "False"
    debug = False

    browser = init_browser()

    
    #                   NASA Mars News Site                  #
  
    
    # Visit the following URL using splinter.Browser module
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(10)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text #goes two levels deep
    news_p = soup.find('div', class_='article_teaser_body').text

    if debug:
        # Display scrapped data 
        print(news_title)
        print(news_p)

        
    #     JPL Mars Space Images - Featured Image        #
    

    # Visit the following URL using splinter.Browser module
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)
    
    time.sleep(5)

    # HTML Object 
    html_jpl = browser.html

    # Parse HTML with Beautiful Soup
    mars_image = BeautifulSoup(html_jpl, 'html.parser')

    # Scrape the image path from soup
    image_url = mars_image.find('a', class_='button fancybox')['data-fancybox-href']

    # JPL url 
    main_url_jpl = 'https://www.jpl.nasa.gov'

    # Concatenate jpl_url with scrapped image_path
    featured_image_url = main_url_jpl + image_url

    if debug:
        # Display url to featured image
        print(featured_image_url)
    

    
    #                   Mars Weather with Twitter                    #
    
    
    # Visit the following URL using splinter.Browser module
    url_mars_tweet = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_mars_tweet)

    time.sleep(5)

    # HTML Object 
    html_mars_tweet = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_mars_tweet, 'html.parser')

    #Set up temperature scrape
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    if debug:
        # Print mars weather
        print(mars_weather)

    
    #                   Mars Facts                      #
    

    #Set up url
    url_mars_facts = 'https://space-facts.com/mars/'

    # Use Panda's read_html to read the first table
    mars_facts_df = pd.read_html(url_mars_facts)[0]

    # Name the columns
    mars_facts_df.columns = ["description","value"]

    # Set the index to description
    mars_facts_df.set_index("description", inplace=True)

    # Save df as html
    mars_facts_html = mars_facts_df.to_html(classes='table1')

    #Clean HTML data for unwanted newlines
    mars_facts_html = mars_facts_html.replace("\n", "")

    if debug:
        # Display mars_df
        print(mars_facts_df)

    
    #                   Mars Hemispheres                #
    

    # Visit the following URL using splinter.Browser module
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemispheres)

    time.sleep(5)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, "html.parser")

    # Scrape information of all the hemispheres
    hemispheres = soup.find_all("div", class_="item")

    # Empty list 
    hemisphere_image_urls = []

    # Main url
    main_url = "https://astrogeology.usgs.gov"


    #Set up a loop through all the hemispheres info
    for hemisphere in hemispheres: 
    

        #Scrap titles
        title = hemisphere.find('h3').text

        #Get url for each image
        image_link = hemisphere.find('a', class_='itemLink product-item')["href"]
    
        #Combine image_url and main url
        image_url = main_url + image_link
    
        #Click into link for each image via Splinter function to get to jpg link
        browser.visit(image_url)
    
        # HTML Object
        html_full_image = browser.html
    
        #Parse a specific hemisphere information website 
        soup = BeautifulSoup(html_full_image, 'html.parser')
    
        #Get jpg link for each image
        image_jpg = soup.find('img', class_='wide-image')['src']
    
        #Combine main url with jpg link 
        image_url = main_url + image_jpg
        
        #Append the empty list 
        hemisphere_image_urls.append({"title" : title, "img_url" : image_url})
     

    
    # Store all the above scraped data in to a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_html": mars_facts_html,
        "hemisphere_image_urls": hemisphere_image_urls 
    }

    # Close the browser after scraping
    browser.quit()

    if debug:
        # Print hemispheree urls and mars data
        print(hemisphere_image_urls)
        print(mars_data)

    if (not debug):
        # Return results if debug is false
        return mars_data
        
    
    
if __name__ == "__main__":
    scrape()