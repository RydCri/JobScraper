import requests # if the page uses javascript, use selenium instead
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



# Indeed URL (modify based on the job board you're targeting)
INDEED_URL = "https://www.indeed.com/jobs?q=data+engineer&l=remote"

# Headers to mimic a browser visit (using Bsoup and requests - if this doesn't work, use selenium & webdriver)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# LinkedIn job search URL (modify as needed)
LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?keywords=data%20engineer&location=Remote"


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


def scrape_indeed_jobs(url, num_pages):
    job_list = []

    for page in range(num_pages):
        print(f"Scraping page {page + 1}...")
        url = f"{url}&start={page * 10}"  # Indeed paginates every 10 jobs
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print("Failed to fetch data:", response.status_code)
            break

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="job_seen_beacon")

        for job in job_cards:
            title = job.find("h2", class_="jobTitle").text.strip() if job.find("h2", class_="jobTitle") else "N/A"
            company = job.find("span", class_="companyName").text.strip() if job.find("span",
                                                                                      class_="companyName") else "N/A"
            location = job.find("div", class_="companyLocation").text.strip() if job.find("div",
                                                                                          class_="companyLocation") else "N/A"
            salary = job.find("div", class_="metadata salary-snippet-container")
            salary = salary.text.strip() if salary else "Not Provided"
            job_link = "https://www.indeed.com" + job.find("a", class_="jcs-JobTitle")["href"]

            job_list.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Salary": salary,
                "Job Link": job_link
            })

        time.sleep(2)  # Be polite & avoid getting blocked

    return pd.DataFrame(job_list)


# Run the scraper and save results
df = scrape_indeed_jobs(INDEED_URL,5)

df.to_csv("./csvs/indeed_jobs.csv", index=False)
print("Scraping complete! Data saved to indeed_jobs.csv")
# Run the scraper
scrape_linkedin_jobs()