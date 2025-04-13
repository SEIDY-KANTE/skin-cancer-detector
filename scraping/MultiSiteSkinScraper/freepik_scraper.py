
from MultiSiteSkinScraper.base_scraper import BaseSkinCancerScraper
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import urllib.parse
import urllib.request
import time
import random
import os

class FreepikScraper(BaseSkinCancerScraper):
    def __init__(self, save_dir):
        super().__init__(save_dir)

    def extract_data(self, url):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        figure_tags = soup.find_all("figure", class_="$relative")
        data = []
        for figure in figure_tags:
            img_tag = figure.find("img")
            if img_tag and img_tag.has_attr("src"):
                img_url = img_tag["src"]
                if img_url and img_url not in self.seen_urls:
                    self.seen_urls.add(img_url)
                    alt_text = img_tag.get("alt", "Skin Image")
                    data.append({
                        "title": alt_text,
                        "image_url": img_url,
                        "condition_type": "Non_Cancer" # All images are Non-Cancer from this site
                    })
        return data

    def download_images(self, data):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        ]
        for i, item in enumerate(data):
            folder_name = self.sanitize_filename(item["condition_type"])
            folder_path = os.path.join(self.save_dir, folder_name)
            self.create_directory(folder_path)

            filename = f"{self.sanitize_filename(item['title'])}_{i}.jpg"
            save_path = os.path.join(folder_path, filename)
            try:
                req = urllib.request.Request(item["image_url"], headers={'User-Agent': random.choice(user_agents)})
                with urllib.request.urlopen(req) as response:
                    image_data = response.read()
                    with open(save_path, 'wb') as f:
                        f.write(image_data)

                print(f"Downloaded: {save_path}")
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f"Error downloading {item['image_url']}: {e}")

    def scrape_website(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        all_data = []
        page_num = 1
        max_pages = 100

        while page_num <= max_pages:
            print(f"Scraping page {page_num}")
            data = self.extract_data(url)
            all_data.extend(data)

            # Find the "Next Page" button and click it
            try:
                next_button = self.driver.find_element(By.XPATH, "//a[@data-cy='pagination-next']")
                next_button.click()
                time.sleep(5)  # Wait for the next page to load
                page_num += 1
            except Exception as e:
                print(f"Error navigating to next page: {e}")
                break # break the loop if there is no next page.

        self.driver.quit() # Close the browser after scraping

        # Download all images after scraping
        self.download_images(all_data)
