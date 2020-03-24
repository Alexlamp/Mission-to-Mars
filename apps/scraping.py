# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


# Add a function that will
# #1) Initialize the browser 3)End the WebDriver and return the scraped data.
def scrape_all():
    import datetime as dt
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    return data

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path)


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page. Telling our browser to wait a second before searching for components:
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up the HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')

        # Search within the element for the title.And stripe the additional HTML attributes and tags with the use of .get_text().
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Next add the summary text. Use the unique class associated with the summary ie “article_teaser_body.”
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


# Define a function and add an argument "browser"
def featured_image(browser):

        # Set up the URL to visit the site
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        # Find and click the full image button, Use the id in our code
        full_image_elem = browser.find_by_id('full_image')      # the browser frinds an element with its id and hplds it in a var
        full_image_elem.click()                                 # splinter will "click" the image to view its full size


        # Use Splinter’s functionality ability to find elements using text.
        # Find the "more info" button using only text and "click" that
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info_elem = browser.find_link_by_partial_text('more info')
        more_info_elem.click()

        # Scrape the full-size image URL. Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        # Adding error handling try & except clause "AttributeError"
        try:
            # Tags used to find the most recent image :  <figure /> and <a /> tags have the image link nested within them.
            # Use (<figure />, <a />, and <img />) to build the URL to the full-size image.  Find the relative image url
            img_url_rel = img_soup.select_one('figure.lede a img').get("src")

        except AttributeError:
            return None

         # Add the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

        return img_url

# Add a function to the Mars Facts
def mars_facts():
    # Add try/except for "BaseException" to error handle
    try:
        # Scraping an entire table with Pandas’ .read_html() function.
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    # Assign columns and set index of DF
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # Adding the DataFrame to a web application
    # Using Pandas convert DataFrame back into HTML-ready code using the .to_html()
    return df.to_html()


# Deactivating/Turning Off the automated browser session
#browser.quit()

# Tells Flask our script is complete and ready to run/for action
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())