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
from selenium.webdriver.common.action_chains import ActionChains




###
# 1. Run this file
# 2. Four .csv files will be saved to the ./csvs/ folder: remoteok_jobs.csv, greenhouse_jobs.csv, indeed_jobs.csv and linkedin_jobs.csv
# 3. View and run pandas operations in dataframe_notes.ipynb on your dataframes
# 4. Come back and modify the URL variables to conduct your own scrapes
# 5. CHANGE your filenames in ./csvs/ if you don't want to overwrite your .csvs everytime you run this

# "I only get one .csv when I run this script"

# Scroll down to the bottom and comment out one of the function calls
# Run one at a time if webdriver only delivers one csv
# Optional tools are commented out in some functions that gave me trouble
# You may have to run in AWS if you can't manage it locally
###



# RemoteOK job search URL (modify as needed)
REMOTEOK_URL = "https://remoteok.com/remote-dev-jobs"

# LinkedIn job search URL (modify as needed)
LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?keywords=Web%20Developer&location=United%20States&geoId=103644278"


# Indeed URL
INDEED_URL = "https://www.indeed.com/jobs?q=data+engineer&l=remote"

# List of Greenhouse company job boards to target
COMPANY_BOARDS = [
    "https://careers.airbnb.com/",
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

        driver.quit()
        df = pd.DataFrame(job_list)
        df.to_csv("./csvs/greenhouse_jobs.csv", index=False)
        print("Scraping complete! Data saved to greenhouse_jobs.csv")
        return df




def scroll_jobs_sidebar(driver, scroll_times=10):
    try:
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__list-container"))
        )
        for _ in range(scroll_times):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", container)
            time.sleep(1.5)
    except:
        print("⚠️ Sidebar not found — falling back to full page scroll.")
        for _ in range(scroll_times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)



def wait_for_modal_to_disappear(driver, timeout=10):
    """ Wait for the modal overlay to disappear (or become invisible) """
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'modal__overlay'))
        )
        print("✅ Modal overlay disappeared.")
    except:
        print("⚠️ Modal overlay still visible, continuing...")


def scrape_linkedin_jobs(driver, url, scrolls=8, max_jobs=None, csv_path="linkedin_jobs.csv"):

    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "base-search-card"))
    )

    scroll_jobs_sidebar(driver, scrolls)

    job_data = []
    job_cards = driver.find_elements(By.CLASS_NAME, 'base-search-card')

    for index, card in enumerate(job_cards):
        if max_jobs and index >= max_jobs:
            break

        try:
            # Wait for modal to disappear before clicking
            wait_for_modal_to_disappear(driver)

            # Scroll to ensure the job card is visible
            driver.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(1)

            # Ensure the job card is clickable (sometimes just waiting helps)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(card)
            )

            # Click the job card
            ActionChains(driver).move_to_element(card).click().perform()
            time.sleep(2)

            # Wait for the job details to load (top card with description)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup"))
            )

            # Extract job details
            title = card.find_element(By.CLASS_NAME, 'base-search-card__title').text.strip()
            company = card.find_element(By.CLASS_NAME, 'base-search-card__subtitle').text.strip()
            location = card.find_element(By.CLASS_NAME, 'job-search-card__location').text.strip()
            job_url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Extract job description
            desc_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup"))
            )
            description = desc_element.text.strip()

            job_data.append({
                'Title': title,
                'Company': company,
                'Location': location,
                'URL': job_url,
                'Job Description': description
            })

            print(f"✅ Scraped job {index+1}: {title} @ {company}")

        except Exception as e:
            print(f"❌ Failed on job {index+1}: {e}")
            continue

    # Export to CSV
    df = pd.DataFrame(job_data)
    df.to_csv(csv_path, index=False)
    print(f"\n📁 Saved {len(df)} jobs to {csv_path}")

    return df

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


search_url = "https://www.linkedin.com/jobs/search/?keywords=Web%20Developer&location=United%20States"

df = scrape_linkedin_jobs(
    driver,
    url=search_url,
    scrolls=10,
    max_jobs=5,
    csv_path="./csvs/linkedin_ds_jobs.csv"
)

driver.quit()


# Run and saves remoteok_jobs.csv
scrape_remoteok_jobs()

# Run and saves greenhouse_jobs.csv
scrape_greenhouse_jobs()