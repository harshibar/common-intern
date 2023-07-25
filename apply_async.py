import os # to get the resume file
import time

import asyncio
from caqui.easy import AsyncDriver
from caqui.exceptions import WebDriverError
from caqui.by import By

RETURN = "\ue006"
MAX_CONCURRENCY = 3  # number of webdriver instances running
sem = asyncio.Semaphore(MAX_CONCURRENCY)

# sample application links if we don't want to run get_links.py
URL_l2 = 'https://jobs.lever.co/scratch/2f09a461-f01d-4041-a369-c64c1887ed97/apply?lever-source=Glassdoor'
URL_l3 = 'https://jobs.lever.co/fleetsmith/eb6648a6-7ad9-4f4a-9918-8b124e10c525/apply?lever-source=Glassdoor'
URL_l4 = 'https://jobs.lever.co/stellar/0e5a506b-1964-40b4-93ab-31a1ee4e4f90/apply?lever-source=Glassdoor'
URL_l6 = 'https://jobs.lever.co/verkada/29c66147-82ef-4293-9a6a-aeed7e6d619e/apply?lever-source=Glassdoor'
URL_l8 = 'https://jobs.lever.co/rimeto/bdca896f-e7e7-4f27-a894-41b47c729c63/apply?lever-source=Glassdoor'
URL_l9 = 'https://jobs.lever.co/color/20ea56b8-fed2-413c-982d-6173e336d51c/apply?lever-source=Glassdoor'
URL_g1 = 'https://boards.greenhouse.io/gleanwork/jobs/4006898005'

URLS = [URL_g1, URL_l4, URL_l3, URL_l6, URL_l8, URL_l9]

# Fill in this dictionary with your personal details!
JOB_APP = {
    "first_name": "Foo",
    "last_name": "Bar",
    "email": "test@test.com",
    "phone": "123-456-7890",
    "org": "Self-Employed",
    "resume": "resume.pdf",
    "resume_textfile": "resume_short.txt",
    "linkedin": "https://www.linkedin.com/",
    "website": "www.youtube.com",
    "github": "https://github.com",
    "twitter": "www.twitter.com",
    "location": "San Francisco, California, United States",
    "grad_month": '06',
    "grad_year": '2021',
    "university": "MIT" # if only o.O
}

# Greenhouse has a different application form structure than Lever, and thus must be parsed differently
async def greenhouse(driver):
    # basic info
    await (await driver.find_element('id','first_name')).send_keys(JOB_APP['first_name'])
    await (await driver.find_element('id','last_name')).send_keys(JOB_APP['last_name'])
    await (await driver.find_element('id','email')).send_keys(JOB_APP['email'])
    await (await driver.find_element(By.ID,'phone')).send_keys(JOB_APP['phone'])

    # # This doesn't exactly work, so a pause was added for the user to complete the action
    # try:
    #     loc = driver.find_element_by_id('job_application_location')
    #     loc.send_keys(JOB_APP['location'])
    #     loc.send_keys(Keys.DOWN) # manipulate a dropdown menu
    #     loc.send_keys(Keys.DOWN)
    #     loc.send_keys(Keys.RETURN)
    #     time.sleep(2) # give user time to manually input if this fails

    # except WebDriverError:
    #     pass

    # Upload Resume as a Text File
    await (await driver.find_element(By.XPATH, "//*[contains(text(), 'or enter manually')]")).click()
    resume_zone = await driver.find_element('id','resume_text')
    with open(JOB_APP['resume_textfile']) as f:
        lines = f.readlines() # add each line of resume to the text area
        for line in lines:
            await resume_zone.send_keys(line)

    # add linkedin
    try:
        await (await driver.find_element(By.XPATH, "//label[contains(.,'LinkedIn')]")).send_keys(JOB_APP['linkedin'])

    except WebDriverError:
        pass
    
    # add linkedin
    try:
        await (await driver.find_element(By.XPATH, "//label[contains(.,'Do you know anyone')]")).send_keys('No')
    except WebDriverError:
        pass

    # add linkedin
    try:
        await (await driver.find_element(By.XPATH, "//label[contains(.,'Why are you interested')]")).send_keys('I am interested')
    except WebDriverError:
        pass

    # # add graduation year
    # try:
    #     driver.find_element_by_xpath("//select/option[text()='2021']").click()
    # except WebDriverError:
    #     pass

    # # add university
    # try:
    #     driver.find_element_by_xpath("//select/option[contains(.,'Harvard')]").click()
    # except WebDriverError:
    #     pass

    # # add degree
    # try:
    #     driver.find_element_by_xpath("//select/option[contains(.,'Bachelor')]").click()
    # except WebDriverError:
    #     pass

    # # add major
    # try:
    #     driver.find_element_by_xpath("//select/option[contains(.,'Computer Science')]").click()
    # except WebDriverError:
    #     pass

    # # add website
    # try:
    #     driver.find_element_by_xpath("//label[contains(.,'Website')]").send_keys(JOB_APP['website'])
    # except WebDriverError:
    #     pass

    # # add work authorization
    # try:
    #     driver.find_element_by_xpath("//select/option[contains(.,'any employer')]").click()
    # except WebDriverError:
    #     pass

    await (await driver.find_element("id","submit_app")).click()
async def lever(driver):
    # navigate to the application page
    await (await driver.find_element('class name', 'template-btn-submit')).click()

    # basic info
    first_name = JOB_APP['first_name']
    last_name = JOB_APP['last_name']
    full_name = first_name + ' ' + last_name  # f string didn't work here, but that's the ideal thing to do
    await (await driver.find_element('name', 'name')).send_keys(full_name)
    await (await driver.find_element('name', 'email')).send_keys(JOB_APP['email'])
    await (await driver.find_element('name', 'phone')).send_keys(JOB_APP['phone'])
    await (await driver.find_element('name', 'org')).send_keys(JOB_APP['org'])

    # socials
    await (await driver.find_element('name', 'urls[LinkedIn]')).send_keys(JOB_APP['linkedin'])
    await (await driver.find_element('name', 'urls[Twitter]')).send_keys(JOB_APP['twitter'])
    try: # try both versions
        await (await driver.find_element('name', 'urls[Github]')).send_keys(JOB_APP['github'])
    except WebDriverError:
        try:
            await (await driver.find_element('name', 'urls[GitHub]')).send_keys(JOB_APP['github'])
        except WebDriverError:
            pass
    await (await driver.find_element('name', 'urls[Portfolio]')).send_keys(JOB_APP['website'])

    # add university
    try:
        await (await driver.find_element('class name', 'application-university')).click()
        search = await driver.find_element('xpath', "//*[@type='search']")
        await search.send_keys(JOB_APP['university']) # find university in dropdown
        await search.send_keys(RETURN)
    except WebDriverError:
        pass

    # add how you found out about the company
    try:
        await (await driver.find_element('class name', 'application-dropdown')).click()
        search = await (await driver.find_element('xpath', "//select/option[text()='Glassdoor']")).click()
    except WebDriverError:
        pass

    # submit resume last so it doesn't auto-fill the rest of the form
    # since Lever has a clickable file-upload, it's easier to pass it into the webpage
    await (await driver.find_element('name', 'resume')).send_keys(os.getcwd()+"/resume.pdf")
    await (await driver.find_element('class name', 'template-btn-submit')).click()


if __name__ == '__main__':

    async def crawler(url):
        async with sem:
            remote = "http://127.0.0.1:9999"
            capabilities = {
                "desiredCapabilities": {
                    "name": "webdriver",
                    "browserName": "chrome",
                    "acceptInsecureCerts": True,
                    # "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
                }
            }    
            driver = AsyncDriver(remote, capabilities)

            if 'greenhouse' in url:
                await driver.get(url)
                try:
                    await greenhouse(driver)
                    print(f'SUCCESS FOR: {url}')
                except Exception:
                    print(f"FAILED FOR {url}")
                    driver.quit()

            elif 'lever' in url:
                try:
                    await driver.get(url)
                    await lever(driver)
                    print(f'SUCCESS FOR: {url}')
                except Exception:
                    print(f"FAILED FOR {url}")
                    driver.quit()
            # i dont think this else is needed
            else:
                print(f"NOT A VALID APP LINK FOR {url}")
                driver.quit()

            await asyncio.sleep(10) # can lengthen this as necessary (for captcha, for example)

            driver.quit()

    async def main():
        # call get_links to automatically scrape job listings from glassdoor
        # aggregatedURLs = get_links.getURLs()
        # print(f'Job Listings: {aggregatedURLs}')
        # print('\n')
        aggregatedURLs = URLS

        tasks = [asyncio.ensure_future(crawler(url)) for url in aggregatedURLs]
        await asyncio.gather(*tasks)

    start = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        end = time.time()
        print(f"Time: {end-start:.2f} sec")
