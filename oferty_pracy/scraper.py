import requests
from bs4 import BeautifulSoup

def get_offers():
    # Step 1: Fetch the HTML content
    url = "https://www.linkedin.com/jobs/search/?keywords=Python%20Developer"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    # Step 2: Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Extract job listings
    job_listings = soup.find_all("div", class_="base-card")

    offers = []
    for job in job_listings:
        try:
            title = job.find("h3", class_="base-search-card__title").text.strip()
            company = job.find("h4", class_="base-search-card__subtitle").text.strip()
            location = job.find("span", class_="job-search-card__location").text.strip()
            link = job.find("a", class_="base-card__full-link")["href"]

            offers.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link
            })
        except AttributeError:
            # Skip if a job listing is missing some information
            continue

    return offers

if __name__ == "__main__":
    job_offers = get_offers()
    for offer in job_offers:
        print(offer)
