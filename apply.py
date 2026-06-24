from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import get_links


# sample application links as fallback when get_links returns nothing
URLS = [
    'https://jobs.lever.co/intrafi/b1639c0d-ae9d-4f28-921e-c75c5286794d',
    'https://jobs.lever.co/voxy-engen/b2c2b60f-ed12-4d23-92f5-a60969ace49f',
    'https://jobs.lever.co/integrate/041a9433-2b9b-4f0f-84d1-be42f011a504',
    'https://jobs.lever.co/everbridge/641816ba-51f9-43d5-b16d-448e2f830ac4',
    'https://jobs.lever.co/quantcast/4c579231-9b59-425b-a32f-68b31413e5f8',
    'https://jobs.lever.co/CordTechnologies/1ca5a094-cc96-4247-b638-942ae4179e1a',
]

# Fill in this dictionary with your personal details!
JOB_APP = {
    "first_name": "Harold",
    "last_name": "Pasion",
    "email": "pasionharold252002@gmail.com",
    "phone": "639924658229",
    "org": "Vaultech",
    "resume": "resume.pdf",
    "resume_textfile": "resume_short.txt",
    "linkedin": "https://www.linkedin.com/in/arownz/",
    "website": "https://harolddevfolio.netlify.app/",
    "github": "https://github.com/arownz",
    "location": "Bacoor, Cavite, Philippines",
    "grad_month": '08',
    "grad_year": '2026',
    "university": "National University Philippines"
}

# Greenhouse has a different application form structure than Lever, and thus must be parsed differently
def greenhouse(driver):

    # basic info
    driver.find_element(By.ID, 'first_name').send_keys(JOB_APP['first_name'])
    driver.find_element(By.ID, 'last_name').send_keys(JOB_APP['last_name'])
    driver.find_element(By.ID, 'email').send_keys(JOB_APP['email'])
    driver.find_element(By.ID, 'phone').send_keys(JOB_APP['phone'])

    try:
        loc = driver.find_element(By.ID, 'job_application_location')
        loc.send_keys(JOB_APP['location'])
        loc.send_keys(Keys.DOWN)
        loc.send_keys(Keys.DOWN)
        loc.send_keys(Keys.RETURN)
        time.sleep(2)
    except NoSuchElementException:
        pass

    driver.find_element(By.CSS_SELECTOR, "[data-source='paste']").click()
    resume_zone = driver.find_element(By.ID, 'resume_text')
    resume_zone.click()
    with open(JOB_APP['resume_textfile'], encoding='utf-8') as f:
        for line in f:
            resume_zone.send_keys(line)

    try:
        driver.find_element(By.XPATH, "//label[contains(.,'LinkedIn')]").send_keys(JOB_APP['linkedin'])
    except NoSuchElementException:
        try:
            driver.find_element(By.XPATH, "//label[contains(.,'Linkedin')]").send_keys(JOB_APP['linkedin'])
        except NoSuchElementException:
            pass

    try:
        driver.find_element(By.XPATH, "//select/option[text()='2021']").click()
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.XPATH, "//select/option[contains(.,'Harvard')]").click()
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.XPATH, "//select/option[contains(.,'Bachelor')]").click()
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.XPATH, "//select/option[contains(.,'Information Technology')]").click()
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.XPATH, "//label[contains(.,'Website')]").send_keys(JOB_APP['website'])
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.XPATH, "//select/option[contains(.,'any employer')]").click()
    except NoSuchElementException:
        pass

    driver.find_element(By.ID, "submit_app").click()

def lever(driver):
    driver.find_element(By.CLASS_NAME, 'template-btn-submit').click()

    first_name = JOB_APP['first_name']
    last_name = JOB_APP['last_name']
    full_name = f"{first_name} {last_name}"
    driver.find_element(By.NAME, 'name').send_keys(full_name)
    driver.find_element(By.NAME, 'email').send_keys(JOB_APP['email'])
    driver.find_element(By.NAME, 'phone').send_keys(JOB_APP['phone'])
    driver.find_element(By.NAME, 'org').send_keys(JOB_APP['org'])

    driver.find_element(By.NAME, 'urls[LinkedIn]').send_keys(JOB_APP['linkedin'])
    try:
        driver.find_element(By.NAME, 'urls[Github]').send_keys(JOB_APP['github'])
    except NoSuchElementException:
        try:
            driver.find_element(By.NAME, 'urls[GitHub]').send_keys(JOB_APP['github'])
        except NoSuchElementException:
            pass
    driver.find_element(By.NAME, 'urls[Portfolio]').send_keys(JOB_APP['website'])

    try:
        driver.find_element(By.CLASS_NAME, 'application-university').click()
        search = driver.find_element(By.XPATH, "//*[@type='search']")
        search.send_keys(JOB_APP['university'])
        search.send_keys(Keys.RETURN)
    except NoSuchElementException:
        pass

    try:
        driver.find_element(By.CLASS_NAME, 'application-dropdown').click()
        driver.find_element(By.XPATH, "//select/option[text()='Glassdoor']").click()
    except NoSuchElementException:
        pass

    resume_path = os.path.join(os.getcwd(), "resume.pdf")
    driver.find_element(By.NAME, 'resume').send_keys(resume_path)
    driver.find_element(By.CLASS_NAME, 'template-btn-submit').click()

if __name__ == '__main__':
    import sys as _sys

    if len(_sys.argv) > 1 and _sys.argv[1] == '-s':
        print('Skipping get_links (use -s flag), using sample URLs...')
        aggregatedURLs = URLS
    else:
        aggregatedURLs = get_links.getURLs()
        print(f'get_links returned: {len(aggregatedURLs)} ATS URLs')

        if not aggregatedURLs:
            print('No URLs from Adzuna, using sample Lever/Greenhouse URLs as fallback...')
            aggregatedURLs = URLS

    print(f'\nProcessing {len(aggregatedURLs)} job URLs...')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    for url in aggregatedURLs:
        print(f'\nOpening: {url}')

        if 'greenhouse' in url:
            driver.get(url)
            try:
                greenhouse(driver)
                print(f'SUCCESS: greenhouse')
            except Exception as e:
                print(f'FAILED: {e}')

        elif 'lever' in url:
            driver.get(url)
            try:
                lever(driver)
                print(f'SUCCESS: lever')
            except Exception as e:
                print(f'FAILED: {e}')
        else:
            print(f'SKIP: not a known ATS format')

        time.sleep(1)

    driver.close()
    print('\nDone.')
