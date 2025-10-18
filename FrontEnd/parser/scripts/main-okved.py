import requests
from bs4 import BeautifulSoup
import re
import time
import urllib3
from urllib.parse import urljoin

# Отключаем предупреждения SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SimpleCompanyParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.base_url = "https://www.list-org.com"
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })

    def get_search_page(self, page: int = 1):
        """Получение страницы поиска"""
        try:
            url = f"{self.base_url}/search"
            params = {'type': 'all', 'val': 'москва', 'page': page}
            time.sleep(1)
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.text
        except:
            return None

    def extract_inn(self, label_text: str):
        """Извлечение ИНН"""
        match = re.search(r'ИНН/КПП\s*:\s*(\d{10})', label_text, re.IGNORECASE)
        return match.group(1) if match else None

    def extract_okved(self, url: str):
        """Извлечение ОКВЭД"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            full_text = soup.get_text()
            
            # Поиск основного ОКВЭД
            patterns = [
                r'Основной\s*\(по\s*коду\s*ОКВЭД\)[^:]*:\s*(\d{2}\.\d{2}(?:\.\d{2})?)\s*[—\-]\s*([^\.\n]+)',
                r'Основной\s*вид\s*деятельности[^:]*:\s*(\d{2}\.\d{2}(?:\.\d{2})?)\s*[—\-]\s*([^\.\n]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    code, description = match.groups()
                    return f"{code.strip()} - {description.strip()}"
            
            # Поиск в таблицах
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        code_cell = cells[0].get_text(strip=True)
                        desc_cell = cells[1].get_text(strip=True)
                        if re.match(r'^\d{2}\.\d{2}(?:\.\d{2})?$', code_cell) and desc_cell:
                            return f"{code_cell} - {desc_cell}"
            
            return "ОКВЭД не указан"
            
        except:
            return "Ошибка загрузки"

    def get_20_companies(self):
        """Получение 20 компаний"""
        companies = []
        page = 1
        
        print("🔄 Загрузка данных...")
        
        while len(companies) < 20:
            html = self.get_search_page(page)
            if not html:
                page += 1
                continue
            
            soup = BeautifulSoup(html, 'html.parser')
            company_links = soup.find_all('a', href=re.compile(r'^/company/\d+'))
            
            for link in company_links:
                if len(companies) >= 20:
                    break
                    
                try:
                    company_name = link.get_text(strip=True)
                    company_url = urljoin(self.base_url, link.get('href', ''))
                    
                    parent = link.find_parent('label')
                    if not parent:
                        continue
                        
                    label_text = parent.get_text()
                    inn = self.extract_inn(label_text)
                    
                    if not inn:
                        continue
                    
                    okved = self.extract_okved(company_url)
                    
                    companies.append({
                        'name': company_name,
                        'inn': inn,
                        'okved': okved
                    })
                    
                    print(f"✅ {len(companies)}. {company_name}")
                    
                    time.sleep(0.5)
                    
                except Exception:
                    continue
            
            page += 1
            time.sleep(1)
        
        return companies

    def print_results(self, companies):
        """Вывод результатов"""
        print("\n" + "="*100)
        print(f"{'№':<3} {'Название компании':<40} {'ИНН':<12} {'ОКВЭД':<40}")
        print("="*100)
        
        for i, company in enumerate(companies, 1):
            name = company['name'][:38] + ".." if len(company['name']) > 40 else company['name']
            inn = company['inn']
            okved = company['okved'][:38] + ".." if len(company['okved']) > 40 else company['okved']
            
            print(f"{i:<3} {name:<40} {inn:<12} {okved:<40}")
        
        print("="*100)

def main():
    """Основная функция"""
    parser = SimpleCompanyParser()
    companies = parser.get_20_companies()
    parser.print_results(companies)

if __name__ == "__main__":
    main()