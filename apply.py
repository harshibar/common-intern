from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os # to get the resume file
from time import sleep # to sleep

# sample applications
URL_g1 = 'https://boards.greenhouse.io/braintree/jobs/1316736?gh_jid=1316736&gh_src=1d1244401'
URL_g2 = 'https://boards.greenhouse.io/gusto/jobs/1862076'
URL_g4 = 'https://boards.greenhouse.io/thumbtack/jobs/1814883'
URL_g3 = 'https://boards.greenhouse.io/lyft/jobs/4358047002?gh_jid=4358047002'
URL_l1 = 'https://jobs.lever.co/figma/91da97b9-ff1d-4e08-a2f1-4867537e5eb2'
URL_l2 = 'https://jobs.lever.co/blendlabs/2a469512-a8c2-44fa-a260-ef3ae0c90db7'
URL_l3 = 'https://jobs.lever.co/affirm/5340f1d3-cd6d-44ef-a5c6-f9def8609d02'
URL_l4 = 'https://jobs.lever.co/grandrounds/cbf92d6f-83c2-41a3-b1a7-350e338c76a7'

# there's probably a prettier way to do all of this
URLS = [URL_g1, URL_g2, URL_g3, URL_g4, URL_l1, URL_l2, URL_l3, URL_l4] # to test all the URLS

# Fill in this dictionary with your personal details!
JOB_APP = {
    "first_name": "Harshi",
    "last_name": "Bar",
    "email": "info.harshibar@gmail.com",
    "phone": "123-456-7890",
    "org": "Self-Employed",
    "resume": "resume.pdf",
    "resume_textfile": "resume_short.txt",
    "linkedin": "https://www.linkedin.com/in/hyerramreddy/",
    "website": "www.harshi.me",
    "github": "https://github.com/harshibar",
    "twitter": "www.twitter.com",
    "location": "Austin, Texas, United States",
    "grad_month": '06',
    "grad_year": '2021',
    "university": "Harvard" # not tru
}

# Greenhouse has a different application form structure than Lever, and thus must be parsed differently
def greenhouse(driver):

    # basic info
    driver.find_element_by_id('first_name').send_keys(JOB_APP['first_name'])
    driver.find_element_by_id('last_name').send_keys(JOB_APP['last_name'])
    driver.find_element_by_id('email').send_keys(JOB_APP['email'])
    driver.find_element_by_id('phone').send_keys(JOB_APP['phone'])

    # This doesn't exactly work, so a pause was added for the user to complete the action
    try:
        loc = driver.find_element_by_id('job_application_location')
        loc.send_keys(JOB_APP['location'])
        loc.send_keys(Keys.DOWN) # manipulate a dropdown menu
        loc.send_keys(Keys.DOWN)
        loc.send_keys(Keys.RETURN)
        sleep(2) # give user time to manually input if this fails

    except NoSuchElementException:
        pass

    # Upload Resume as a Text File
    driver.find_element_by_css_selector("[data-source='paste']").click()
    resume_zone = driver.find_element_by_id('resume_text')
    resume_zone.click()
    with open(JOB_APP['resume_textfile']) as f:
        lines = f.readlines() # add each line of resume to the text area
        for line in lines:
            resume_zone.send_keys(line.decode('utf-8'))

    # add linkedin
    try:
        driver.find_element_by_xpath("//label[contains(.,'LinkedIn')]").send_keys(JOB_APP['linkedin'])
    except NoSuchElementException:
        try:
            driver.find_element_by_xpath("//label[contains(.,'Linkedin')]").send_keys(JOB_APP['linkedin'])
        except NoSuchElementException:
            pass

    # add graduation year
    try:
        driver.find_element_by_xpath("//select/option[text()='2021']").click()
    except NoSuchElementException:
        pass

    # add university
    try:
        driver.find_element_by_xpath("//select/option[contains(.,'Harvard')]").click()
    except NoSuchElementException:
        pass

    # add degree
    try:
        driver.find_element_by_xpath("//select/option[contains(.,'Bachelor')]").click()
    except NoSuchElementException:
        pass

    # add major
    try:
        driver.find_element_by_xpath("//select/option[contains(.,'Computer Science')]").click()
    except NoSuchElementException:
        pass

    # add website
    try:
        driver.find_element_by_xpath("//label[contains(.,'Website')]").send_keys(JOB_APP['website'])
    except NoSuchElementException:
        pass

    # add work authorization
    try:
        driver.find_element_by_xpath("//select/option[contains(.,'any employer')]").click()
    except NoSuchElementException:
        pass

    driver.find_element_by_id("submit_app").click()

# Handle a Lever form
def lever(driver):
    # navigate to the application page
    driver.find_element_by_class_name('template-btn-submit').click()

    # basic info
    first_name = JOB_APP['first_name']
    last_name = JOB_APP['last_name']
    full_name = first_name + ' ' + last_name  # f string didn't work here, but that's the ideal thing to do
    driver.find_element_by_name('name').send_keys(full_name)
    driver.find_element_by_name('email').send_keys(JOB_APP['email'])
    driver.find_element_by_name('phone').send_keys(JOB_APP['phone'])
    driver.find_element_by_name('org').send_keys(JOB_APP['org'])

    # socials
    driver.find_element_by_name('urls[LinkedIn]').send_keys(JOB_APP['linkedin'])
    driver.find_element_by_name('urls[Twitter]').send_keys(JOB_APP['twitter'])
    try: # try both versions
        driver.find_element_by_name('urls[Github]').send_keys(JOB_APP['github'])
    except NoSuchElementException:
        try:
            driver.find_element_by_name('urls[GitHub]').send_keys(JOB_APP['github'])
        except NoSuchElementException:
            pass
    driver.find_element_by_name('urls[Portfolio]').send_keys(JOB_APP['website'])

    # add university
    try:
        driver.find_element_by_class_name('application-university').click()
        search = driver.find_element_by_xpath("//*[@type='search']")
        search.send_keys(JOB_APP['university']) # find university in dropdown
        search.send_keys(Keys.RETURN)
    except NoSuchElementException:
        pass

    # add how you found out about the company
    try:
        driver.find_element_by_class_name('application-dropdown').click()
        search = driver.find_element_by_xpath("//select/option[text()='Glassdoor']").click()
    except NoSuchElementException:
        pass

    # submit resume last so it doesn't auto-fill the rest of the form
    # since Lever has a clickable file-upload, it's easier to pass it into the webpage
    driver.find_element_by_name('resume').send_keys(os.getcwd()+"/resume.pdf")
    driver.find_element_by_class_name('template-btn-submit').click()

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')

    for url in URLS:
        driver.get(url)

        if 'greenhouse' in url:
            greenhouse(driver)

        if 'lever' in url:
            lever(driver)

        sleep(1) # can lengthen this as necessary (for captcha, for example)
    driver.close()