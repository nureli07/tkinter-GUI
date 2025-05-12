import requests
from bs4 import BeautifulSoup
import csv
import time
import random

class TapAzScraper:
    def __init__(self):
        self.base_url = "https://tap.az"
        self.search_url = "https://tap.az/elanlar?keywords=iphone"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        self.iphone_data = []
    
    def get_page_content(self, url):
        """GET request ilə saytdan HTML məzmununu alır"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Xəta üçün yoxlama
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Xəta baş verdi: {e}")
            return None
    
    def parse_iphone_listings(self, html_content):
        """HTML-dən iPhone elanlarını parse edir"""
        soup = BeautifulSoup(html_content, 'html.parser')
        product_cards = soup.select('div.products-i')
        
        for card in product_cards:
            try:
                # Məhsul adını yoxla (iPhone olduğuna əmin ol)
                title_element = card.select_one('div.products-name')
                if not title_element or 'iphone' not in title_element.text.lower():
                    continue
                
                title = title_element.text.strip()
                price_element = card.select_one('span.price-val')
                price = price_element.text.strip() if price_element else "Qiymət göstərilməyib"
                currency_element = card.select_one('span.price-cur')
                currency = currency_element.text.strip() if currency_element else ""
                
                link_element = card.select_one('a.products-link')
                link = self.base_url + link_element['href'] if link_element else ""
                
                location_element = card.select_one('div.products-location')
                location = location_element.text.strip() if location_element else "Məkan göstərilməyib"
                
                timestamp_element = card.select_one('div.products-created')
                timestamp = timestamp_element.text.strip() if timestamp_element else "Vaxt göstərilməyib"
                
                image_element = card.select_one('img.thumbnail-img')
                image_url = image_element['src'] if image_element and 'src' in image_element.attrs else ""
                
                iphone_info = {
                    'title': title,
                    'price': price,
                    'currency': currency,
                    'location': location,
                    'timestamp': timestamp,
                    'link': link,
                    'image_url': image_url
                }
                
                self.iphone_data.append(iphone_info)
                print(f"Tapıldı: {title} - {price} {currency}")
            
            except Exception as e:
                print(f"Elan məlumatı alınarkən xəta baş verdi: {e}")
    
    def get_next_page_url(self, html_content):
        """Növbəti səhifənin URL-ni qaytar"""
        soup = BeautifulSoup(html_content, 'html.parser')
        next_page = soup.select_one('a.next')
        if next_page and 'href' in next_page.attrs:
            return self.base_url + next_page['href']
        return None
    
    def export_to_csv(self, filename='iphone_elanlar.csv'):
        """Nəticələri CSV faylına ixrac edir"""
        if not self.iphone_data:
            print("İxrac etmək üçün məlumat yoxdur.")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'price', 'currency', 'location', 'timestamp', 'link', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in self.iphone_data:
                writer.writerow(item)
            
        print(f"Məlumatlar {filename} faylına ixrac edildi. Cəmi {len(self.iphone_data)} elan tapıldı.")
    
    def scrape_iphones(self, max_pages=5):
        """Saytdan iPhone elanlarını yığır"""
        current_url = self.search_url
        page_count = 0
        
        while current_url and page_count < max_pages:
            page_count += 1
            print(f"\nSəhifə {page_count} yoxlanılır: {current_url}")
            
            html_content = self.get_page_content(current_url)
            if not html_content:
                break
            
            self.parse_iphone_listings(html_content)
            
            # Növbəti səhifəyə keçmədən əvvəl serveri yükləməmək üçün
            # kiçik təsadüfi gecikmə əlavə edin
            sleep_time = random.uniform(1.5, 3.0)
            print(f"Növbəti səhifəyə keçməzdən əvvəl {sleep_time:.2f} saniyə gözlənilir...")
            time.sleep(sleep_time)
            
            current_url = self.get_next_page_url(html_content)
        
        print(f"\nÜmumilikdə {len(self.iphone_data)} iPhone elanı tapıldı.")
        return self.iphone_data

# Skripti icra et
if __name__ == "__main__":
    scraper = TapAzScraper()
    
    try:
        # 3 səhifə yoxla (istəyinizə görə dəyişdirə bilərsiniz)
        scraper.scrape_iphones(max_pages=3)
        
        # Nəticələri CSV faylına ixrac et
        scraper.export_to_csv()
    except KeyboardInterrupt:
        print("\nSkript dayandırıldı.")
        # Yarımçıq qalsa belə topladığımız məlumatları ixrac et
        scraper.export_to_csv()
    except Exception as e:
        print(f"Gözlənilməz xəta baş verdi: {e}")
