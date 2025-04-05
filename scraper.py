import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
# import undetected_chromedriver as uc
# uc.TARGET_VERSION = 85
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

###
# 1. Run this file
# 2. Three .csv files will be saved to the ./csvs/ folder: greenhouse_jobs.csv, indeed_jobs.csv and linkedin_jobs.csv
# 3. View and run pandas operations in dataframe_notes.ipynb on your dataframes
# 4. Come back and modify the URL variables to conduct your own scrapes
# 5. CHANGE your filenames in ./csvs/ if you don't want to overwrite your .csvs everytime you run this

# "I only get one .csv when I run this script"

# Scroll down to the bottom and comment out one of the function calls
# Run one at a time if webdriver only delivers one csv
# Optional tools are commented out some functions that gave me trouble
# You may have to run in AWS if you can't manage it locally
###


# Indeed URL (modify based on the job board you're targeting)
INDEED_URL = "https://www.indeed.com/jobs?q=data+engineer&l=remote"

# LinkedIn job search URL (modify as needed)
REMOTEOK_URL = "https://remoteok.com/remote-dev-jobs"

# LinkedIn job search URL (modify as needed)
LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?keywords=data%20engineer&location=Remote"

# List of Greenhouse company job boards to target
COMPANY_BOARDS = [
    "https://boards.greenhouse.io/airbnb",
    "https://boards.greenhouse.io/robinhood",
    "https://boards.greenhouse.io/stripe"
]


def scrape_remoteok_jobs():


    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(REMOTEOK_URL)
    time.sleep(3)  # Let content load

    job_list = []
    job_rows = driver.find_elements(By.CSS_SELECTOR, "tr.job")

    for job in job_rows:
        try:
            title = job.find_element(By.CSS_SELECTOR, "h2").text.strip()
            company = job.find_element(By.CSS_SELECTOR, "h3").text.strip()
            location_el = job.find_elements(By.CLASS_NAME, "location")
            location = location_el[0].text.strip() if location_el else "Remote"
            link = "https://remoteok.com" + job.get_attribute("data-href")

            job_list.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Job Link": link
            })
        except Exception as e:
            print(f"Error parsing job row: {e}")

    driver.quit()

    df = pd.DataFrame(job_list)
    df.to_csv("./csvs/remoteok_jobs.csv", index=False)
    print("Done! Saved to remoteok_jobs.csv")
    return df


def scrape_greenhouse_jobs():
    job_list = []

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for board_url in COMPANY_BOARDS:
        print(f"Scraping: {board_url}")
        driver.get(board_url)

        try:
            # Scroll down & load more jobs
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(2)
            postings = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "opening"))
            )

            for post in postings:
                try:
                    title_el = post.find_element(By.TAG_NAME, "a")
                    title = title_el.text.strip()
                    job_link = title_el.get_attribute("href")
                    location_el = post.find_element(By.CLASS_NAME, "location")
                    location = location_el.text.strip() if location_el else "N/A"

                    job_list.append({
                        "Title": title,
                        "Company": board_url.split("/")[-1].capitalize(),
                        "Location": location,
                        "Job Link": job_link
                    })
                except Exception as e:
                    print(f"Error extracting post data: {e}")
        except Exception as e:
            print(f"Error loading job board: {board_url} — {e.with_traceback}")
    driver.quit()
    df = pd.DataFrame(job_list)
    df.to_csv("./csvs/greenhouse_jobs.csv", index=False)
    print("Scraping complete! Data saved to greenhouse_jobs.csv")
    return df


def scrape_linkedin_jobs(num_pages=5):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(LINKEDIN_URL)
    time.sleep(3)

    job_list = []

    for _ in range(num_pages):
        jobs = driver.find_elements(By.CLASS_NAME, "base-card")

        for job in jobs:
            try:
                title = job.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
                company = job.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
                location = job.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()
                job_link = job.find_element(By.TAG_NAME, "a").get_attribute("href")

                job_list.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Job Link": job_link
                })
            except Exception as e:
                print(f"Error extracting job: {e}")

        # Scroll down & load more jobs
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

    # Save results
    df = pd.DataFrame(job_list)
    df.to_csv("./csvs/linkedin_jobs.csv", index=False)
    print("Scraping complete! Data saved to linkedin_jobs.csv")

    driver.quit()


def scrape_indeed_jobs(num_pages=5):
    job_list = []

    # Setup headless Chrome
    options = webdriver.ChromeOptions()

    # Use undetected Chrome driver if blocked by cloudflare
    # options = uc.ChromeOptions()
    options.add_argument("--headless")  # Remove this line if you're debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for page in range(num_pages):
        print(f"Scraping page {page + 1}...")
        url = f"{INDEED_URL}&start={page * 10}"
        # driver = uc.Chrome(options=options) # undetected driver

        driver.get(url)
        # Scroll down & load more jobs
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)  # optional
        print(f"Fetching URL: {url}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "job_seen_beacon"))
        )
        job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for job in job_cards:
            try:
                title = job.find_element(By.CLASS_NAME, "jobTitle").text.strip()
            except:
                title = "N/A"

            try:
                company = job.find_element(By.CLASS_NAME, "companyName").text.strip()
            except:
                company = "N/A"

            try:
                location = job.find_element(By.CLASS_NAME, "companyLocation").text.strip()
            except:
                location = "N/A"

            try:
                salary = job.find_element(By.CLASS_NAME, "salary-snippet").text.strip()
            except:
                salary = "Not Provided"

            try:
                job_link = job.find_element(By.CLASS_NAME, "jcs-JobTitle").get_attribute("href")
            except:
                job_link = "N/A"

            job_list.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Salary": salary,
                "Job Link": job_link
            })
    df = pd.DataFrame(job_list)
    df.to_csv("./csvs/indeed_jobs.csv", index=False)
    print("Scraping complete! Data saved to indeed_jobs.csv")
    driver.quit()


# Run and saves remoteok_jobs.csv
scrape_remoteok_jobs()

# Run and saves greenhouse_jobs.csv
scrape_greenhouse_jobs()

# Run and saves indeed_jobs.csv
scrape_indeed_jobs()

# Run and saves linkedin_jobs.csv
scrape_linkedin_jobs()

