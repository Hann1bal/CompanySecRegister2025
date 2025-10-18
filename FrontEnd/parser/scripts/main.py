import requests
from bs4 import BeautifulSoup
import time
import json
import re
from typing import List, Dict, Optional
import urllib3
from urllib.parse import urljoin
import logging

# Отключаем предупреждения SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FinalMoscowCompaniesParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.base_url = "https://www.list-org.com"
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })

    def get_search_page(self, page: int = 1) -> Optional[str]:
        """Получение страницы с поисковыми результатами"""
        try:
            url = f"{self.base_url}/search"
            params = {'type': 'all', 'val': 'москва', 'page': page}
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Ошибка загрузки страницы {page}: {e}")
            return None

    def parse_companies(self, html: str) -> List[Dict]:
        """Парсинг компаний из HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        companies = []
        
        # Находим все label элементы с компаниями
        labels_with_companies = []
        for label in soup.find_all('label'):
            if label.find('a', href=re.compile(r'^/company/\d+')):
                labels_with_companies.append(label)
        
        logger.info(f"Найдено элементов с компаниями: {len(labels_with_companies)}")
        
        for label in labels_with_companies:
            company_data = self.parse_company_label(label)
            if company_data and company_data.get('inn'):
                companies.append(company_data)
        
        return companies

    def parse_company_label(self, label) -> Optional[Dict]:
        """Парсинг данных компании из label элемента"""
        try:
            # Извлекаем название и ссылку
            company_link = label.find('a', href=re.compile(r'^/company/\d+'))
            if not company_link:
                return None
                
            company_name = company_link.get_text(strip=True)
            company_url = urljoin(self.base_url, company_link.get('href', ''))
            
            # Получаем весь текст label
            full_text = label.get_text()
            
            # Извлекаем ИНН (формат: инн/кпп: 7707294277/770701001)
            inn_match = re.search(r'инн/кпп:\s*(\d{10})/\d{9}', full_text, re.IGNORECASE)
            inn = inn_match.group(1) if inn_match else None
            
            if not inn:
                return None
            
            # Извлекаем ОГРН (может быть в другом формате)
            ogrn_match = re.search(r'ОГРН\s*(\d{13})', full_text, re.IGNORECASE)
            ogrn = ogrn_match.group(1) if ogrn_match else None
            
            # Извлекаем адрес (формат: юр.адрес: 103159, Г.Москва, УЛ. ОХОТНЫЙ РЯД, Д.2)
            address_match = re.search(r'юр\.адрес:\s*([^\n]+)', full_text, re.IGNORECASE)
            address = address_match.group(1).strip() if address_match else None
            
            # Извлекаем статус
            status = 'не действующее' if 'не действующее' in full_text else 'действующее'
            
            # Извлекаем полное наименование (идет после статуса)
            full_name_match = re.search(r'не действующее([^руководитель]+)', full_text)
            if not full_name_match:
                full_name_match = re.search(r'действующее([^руководитель]+)', full_text)
            
            full_name = full_name_match.group(1).strip() if full_name_match else None
            
            # Извлекаем руководителя
            director_match = re.search(r'руководитель:\s*([^\n]+?)(?=инн|юр\.адрес|$)', full_text, re.IGNORECASE)
            director = director_match.group(1).strip() if director_match else None
            
            return {
                'name': company_name,
                'full_name': full_name,
                'inn': inn,
                'ogrn': ogrn,
                'address': address,
                'director': director,
                'status': status,
                'url': company_url,
                'parsed_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.warning(f"Ошибка парсинга компании {company_name if 'company_name' in locals() else 'N/A'}: {e}")
            return None

    def has_next_page(self, html: str, current_page: int) -> bool:
        """Проверка наличия следующей страницы"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Ищем ссылки с номером следующей страницы
        next_links = soup.find_all('a', href=re.compile(r'page=\d+'))
        for link in next_links:
            href = link.get('href', '')
            page_match = re.search(r'page=(\d+)', href)
            if page_match:
                page_num = int(page_match.group(1))
                if page_num == current_page + 1:
                    return True
                    
        return False

    def collect_companies(self, max_pages: int = 5) -> List[Dict]:
        """Сбор компаний с нескольких страниц"""
        all_companies = []
        
        for page in range(1, max_pages + 1):
            logger.info(f"📄 Обрабатываю страницу {page}...")
            
            html = self.get_search_page(page)
            if not html:
                logger.error(f"Не удалось загрузить страницу {page}")
                break
                
            companies = self.parse_companies(html)
            all_companies.extend(companies)
            
            logger.info(f"✅ На странице {page} найдено {len(companies)} компаний")
            logger.info(f"📊 Всего собрано: {len(all_companies)} компаний")
            
            # Проверяем есть ли следующая страница
            if page < max_pages and self.has_next_page(html, page):
                time.sleep(2)  # Пауза между запросами
            else:
                logger.info("🏁 Достигнута последняя страница")
                break
                
        return all_companies

    def save_results(self, companies: List[Dict]):
        """Сохранение результатов в файлы"""
        if not companies:
            logger.warning("❌ Нет данных для сохранения")
            return
            
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Сохраняем полные данные в JSON
        json_filename = f"moscow_companies_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(companies, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Полные данные сохранены в {json_filename}")
        
        # Сохраняем только ИНН в текстовый файл
        inns = [company['inn'] for company in companies if company.get('inn')]
        inns_filename = f"moscow_inns_{timestamp}.txt"
        with open(inns_filename, 'w', encoding='utf-8') as f:
            for inn in inns:
                f.write(f"{inn}\n")
        logger.info(f"📝 Список ИНН сохранен в {inns_filename} ({len(inns)} записей)")

    def print_statistics(self, companies: List[Dict]):
        """Вывод подробной статистики"""
        print("\n" + "="*70)
        print("СТАТИСТИКА СБОРА КОМПАНИЙ МОСКВЫ")
        print("="*70)
        
        total = len(companies)
        if total == 0:
            print("❌ Не найдено ни одной компании")
            return
            
        with_inn = len([c for c in companies if c.get('inn')])
        with_ogrn = len([c for c in companies if c.get('ogrn')])
        with_address = len([c for c in companies if c.get('address')])
        with_director = len([c for c in companies if c.get('director')])
        active_companies = len([c for c in companies if c.get('status') == 'действующее'])
        inactive_companies = len([c for c in companies if c.get('status') == 'не действующее'])
        
        print(f"📈 Всего компаний: {total}")
        print(f"🔢 С ИНН: {with_inn} ({with_inn/total*100:.1f}%)")
        print(f"📋 С ОГРН: {with_ogrn} ({with_ogrn/total*100:.1f}%)")
        print(f"🏠 С адресом: {with_address} ({with_address/total*100:.1f}%)")
        print(f"👤 С руководителем: {with_director} ({with_director/total*100:.1f}%)")
        print(f"✅ Действующие: {active_companies} ({active_companies/total*100:.1f}%)")
        print(f"❌ Не действующие: {inactive_companies} ({inactive_companies/total*100:.1f}%)")
        
        print(f"\n📋 Первые 5 компаний:")
        print("-" * 70)
        for i, company in enumerate(companies[:5], 1):
            print(f"{i}. {company['name']}")
            print(f"   🆔 ИНН: {company.get('inn', 'не указан')}")
            if company.get('full_name'):
                print(f"   📛 Полное название: {company['full_name']}")
            if company.get('address'):
                print(f"   📍 Адрес: {company['address']}")
            if company.get('director'):
                print(f"   👤 Руководитель: {company['director']}")
            if company.get('status'):
                print(f"   📊 Статус: {company['status']}")
            if company.get('url'):
                print(f"   🔗 Ссылка: {company['url']}")
            print()
            
        print("="*70)


def main():
    """Основная функция"""
    parser = FinalMoscowCompaniesParser()
    
    try:
        logger.info("🚀 Запуск сбора компаний Москвы...")
        
        # Собираем компании
        companies = parser.collect_companies(max_pages=5)
        
        # Сохраняем результаты
        parser.save_results(companies)
        
        # Выводим статистику
        parser.print_statistics(companies)
        
        return companies
        
    except KeyboardInterrupt:
        logger.info("⏹ Сбор данных прерван пользователем")
        return []
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        return []


if __name__ == "__main__":
    main()