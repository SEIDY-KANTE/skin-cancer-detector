from MultiSiteSkinScraper.base_scraper import BaseSkinCancerScraper
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import time
import random
import os

class SkinCancerOrgScraper(BaseSkinCancerScraper):
    def __init__(self, save_dir):
        super().__init__(save_dir)

    def extract_data(self, url):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        image_items = soup.find_all("div", class_="image-item")
        data = []
        for item in image_items:
            img_tag = item.find("img")
            if img_tag:
                img_url = img_tag.get("src")
                if img_url and img_url not in self.seen_urls:
                    self.seen_urls.add(img_url)
                    alt_text = img_tag.get("alt", "Skin Cancer Image")
                    caption_tag = item.find("p", class_="image-caption")
                    caption = caption_tag.text.strip() if caption_tag else alt_text

                    condition_type = "Cancer" # All are cancer
                    # if "melanoma" in caption.lower():
                    #     condition_type = "Melanoma"
                    # elif "basal cell carcinoma" in caption.lower():
                    #     condition_type = "Basal Cell Carcinoma"
                    # elif "squamous cell carcinoma" in caption.lower():
                    #     condition_type = "Squamous Cell Carcinoma"
                    # elif "merkel cell carcinoma" in caption.lower():
                    #     condition_type = "Merkel Cell Carcinoma"


                    data.append({
                        "title": alt_text,
                        "image_url": img_url,
                        "condition_type": condition_type
                    })

        self.driver.quit() # Close the browser after scraping

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

