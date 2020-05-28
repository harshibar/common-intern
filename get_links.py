# selenium stup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# to find links
from bs4 import BeautifulSoup
import json
import urllib.request
import re

import time # to sleep

# fill this in with your job preferences!
PREFERENCES = {
    "position_title": "Software Engineer",
    "location": "San Francisco, CA"
}

# helper method to give user time to log into glassdoor
def login(driver):
    driver.get('https://www.glassdoor.com/index.htm')

    # keep waiting for user to log-in until the URL changes to user page
    while True:
        try:
            WebDriverWait(driver, 1).until(EC.url_contains("member"))
        except TimeoutException:
            break
    return True # return once this is complete

# navigate to appropriate job listing page
def go_to_listings(driver):

    # wait for the search bar to appear
    element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='scBar']"))
        )

    try:
        # look for search bar fields
        position_field = driver.find_element_by_xpath("//*[@id='sc.keyword']")
        location_field = driver.find_element_by_xpath("//*[@id='sc.location']")
        location_field.clear()

        # fill in with pre-defined data
        position_field.send_keys(PREFERENCES['position_title'])
        location_field.clear()
        location_field.send_keys(PREFERENCES['location'])

        # wait for a little so location gets set
        time.sleep(1)
        driver.find_element_by_xpath(" //*[@id='scBar']/div/button").click()

        # close a random popup if it shows up
        try:
            driver.find_element_by_xpath("//*[@id='JAModal']/div/div[2]/span").click()
        except NoSuchElementException:
            pass

        return True

    # note: please ignore all crappy error handling haha
    except NoSuchElementException:
        return False

# aggregate all url links in a set
def aggregate_links(driver):
    allLinks = [] # all hrefs that exist on the page

    # wait for page to fully load
    element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='MainCol']/div[1]/ul"))
        )

    time.sleep(5)

    # parse the page source using beautiful soup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source)

    # find all hrefs
    allJobLinks = soup.findAll("a", {"class": "jobLink"})
    allLinks = [jobLink['href'] for jobLink in allJobLinks]
    allFixedLinks = []

    # clean up the job links by opening, modifying, and 'unraveling' the URL
    for link in allLinks:
        # first, replace GD_JOB_AD with GD_JOB_VIEW
        # this will replace the Glassdoor hosted job page to the proper job page
        # hosted on most likely Greenhouse or Lever
        link = link.replace("GD_JOB_AD", "GD_JOB_VIEW")

        # if there is no glassdoor prefex, add that
        # for example, /partner/jobListing.htm?pos=121... needs the prefix

        if link[0] == '/':
            link = f"https://www.glassdoor.com{link}"

        # then, open up each url and save the result url
        # because we got a 403 error when opening this normally, we have to establish the user agent
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent,}
        request=urllib.request.Request(link,None,headers) #The assembled request

        try:
            # the url is on glassdoor itself, but once it's opened, it redirects - so let's store that
            response = urllib.request.urlopen(request)
            newLink = response.geturl()

            # if the result url is from glassdoor, it's an 'easy apply' one and worth not saving
            # however, this logic can be changed if you want to keep those
            if "glassdoor" not in newLink:
                print(newLink)
                print('\n')
                allFixedLinks.append(newLink)
        except Exception:
            # horrible way to catch errors but this doesnt happen regualrly (just 302 HTTP error)
            print(f'ERROR: failed for {link}')
            print('\n')

    # convert to a set to eliminate duplicates
    return set(allFixedLinks)

# 'main' method to iterate through all pages and aggregate URLs
def getURLs():
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    success = login(driver)
    if not success:
        # close the page if it gets stuck at some point - this logic can be improved
        driver.close()

    success = go_to_listings(driver)
    if not success:
        driver.close()

    allLinks = set()
    page = 1
    next_url = ''
    while page < 5: # pick an arbitrary number of pages so this doesn't run infinitely
        print(f'\nNEXT PAGE #: {page}\n')

        # on the first page, the URL is unique and doesn't have a field for the page number
        if page == 1:
            # aggregate links on first page
            allLinks.update(aggregate_links(driver))

            # find next page button and click it
            next_page = driver.find_element_by_xpath("//*[@id='FooterPageNav']/div/ul/li[3]/a")
            this_page = next_page.get_attribute('href')

            # use regex to parse out the page number
            m = re.search('(?P<url>[^;]*?)(?P<page>.htm\?p=)(?P<pagenum>.)', this_page)

            # for page 2 onwards, there's a different page structure that we need to convert from
            # (idk why it's like this tho)
            # from: .../jobs-SRCH_IL.0,13_IC1147401_KE14,33.htm?p=2
            # to: .../jobs-SRCH_IL.0,13_IC1147401_KE14,33_IP2.htm
            page += 1 # increment page count
            next_url = f"{m.group('url')}_IP{page}.htm" # update url with new page number
            time.sleep(1) # just to give things time

        # same patterns from page 2 onwards
        if page >=2 :
            # open page with new URL
            driver.get(next_url)
            # collect all the links
            allLinks.update(aggregate_links(driver))
            # run regex to get all reusable parts of URL
            m = re.search('(?P<url>[^;]*?)(?P<pagenum>.)(?P<html>.htm)', next_url)
            # increment page number for next time
            page += 1
            # update URL
            next_url = f"{m.group('url')}{page}.htm"

    driver.close()
    return allLinks

# for testing purpose
# getURLs()
