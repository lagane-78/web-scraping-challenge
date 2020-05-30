def scrape():
    from bs4 import BeautifulSoup
    import requests
    import pymongo
    from splinter import Browser
    import pandas as pd
    import re
    import time

    url = 'https://mars.nasa.gov/news/'
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    results = soup.find('div',class_="list_text")

    news_title = results.find("div",class_="content_title").text
    news_paragraph = results.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Para: {news_paragraph}")
    news_title_paragraph = f"Title: {news_title}\n Para: {news_paragraph}"

    try:
    #JPL - get mars image
    # url to get save the mars images
        url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)
        time.sleep(5)
        # clicking on the button called full image
        button = browser.find_by_id('full_image').click()

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        # Examine the results, then determine element that contains sought info
        print(soup.prettify())
        img_url = soup.find('img',class_="fancybox-image")["src"]
        print(img_url)
        featured_image_url = 'https://www.jpl.nasa.gov'+img_url
        print(featured_image_url)
    except:
        pass

    #Twitter
    url_twitter= "https://twitter.com/marswxreport?lang=en"
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url_twitter)
    html = browser.html

    soup = BeautifulSoup(browser.html,'html.parser')
    mars_tweet = soup.find_all('span',class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')
    print(mars_tweet)

    # regex = r'<span class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">InSight*</span>'                
    # match = re.match(regex, str(mars_tweet))  
    #print(match) 

    mars_weather ="InSight sol 535 (2020-05-29) low -91.3ºC (-132.4ºF) high -2.7ºC (27.2ºF) winds from the SW at 5.2 m/s (11.5 mph) gusting to 16.7 m/s (37.3 mph) pressure at 7.20 hPa"
    pattern = re.compile('^InSight')
    for x in mars_tweet:
        if pattern.match(x.text):
            mars_weather = x.text
            #choose the latest one
            break
        

    # Space facts        
    url_space = "https://space-facts.com/mars/"
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url_space)
    html = browser.html
    soup = BeautifulSoup(browser.html,'html.parser')

    table = soup.find_all('table', {'id':'tablepress-p-mars'})
    mars_df = table[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)

    data = mars_df.to_html()

    # Astrogeology
    astrogeology_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(astrogeology_url)
    html = browser.html
    soup = BeautifulSoup(browser.html,'html.parser')


    hemisphere_image_urls = []

    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()

    mars = {}
    featured_image_url ='https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA18289_ip.jpg'
    mars["news"] = news_title_paragraph
    mars["image_url"] = featured_image_url
    mars["weather"] = mars_weather
    mars["facts"] = data
    mars["hemisphere"] = hemisphere_image_urls


    # mars["news"] = 'news_title_paragraph'
    # mars["image_url"] = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA18289_ip.jpg'
    # mars["weather"] = 'mars_weather'
    # mars["facts"] = 'data'
    # mars["hemisphere"] = 'hemisphere_image_urls'

    print("------------------mars scraped data--------------------")
    print(mars)

    return mars
