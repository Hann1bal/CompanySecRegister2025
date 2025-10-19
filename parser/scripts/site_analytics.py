import torch
import requests
import re
import json
from typing import List, Dict, Any, Set
import easyocr
from PIL import Image
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time
from io import BytesIO


class EnhancedCompanySiteAnalyzer:
    def __init__(self, max_pages: int = 25, max_depth: int = 2):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.visited_urls: Set[str] = set()
        self.session = requests.Session()

        # Приоритетные пути для поиска руководства
        self.priority_paths = [
            '/about/', '/about', '/company/', '/company',
            '/team/', '/team', '/management/', '/management',
            '/ru/about/', '/ru/company/', '/ru/team/', '/ru/management/',
            '/o-nas/', '/o-kompanii/', '/komanda/', '/rukovodstvo/',
            '/directors/', '/executive/', '/leadership/',
            '/contacts/', '/contact/', '/kontakty/',
            '/partners/', '/clients/', '/customers/',
            '/dealer/', '/dealers/', '/dilers/', '/diler/'
        ]

        # Настройки сессии
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
        })
        self.russian_cities = [
            'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Нижний Новгород',
            'Казань', 'Челябинск', 'Омск', 'Самара', 'Ростов-на-Дону', 'Уфа', 'Красноярск',
            'Воронеж', 'Пермь', 'Волгоград', 'Краснодар', 'Саратов', 'Тюмень', 'Тольятти',
            'Ижевск', 'Барнаул', 'Ульяновск', 'Иркутск', 'Хабаровск', 'Ярославль', 'Владивосток',
            'Махачкала', 'Томск', 'Оренбург', 'Кемерово', 'Новокузнецк', 'Рязань', 'Астрахань',
            'Набережные Челны', 'Пенза', 'Липецк', 'Киров', 'Чебоксары', 'Тула', 'Калининград',
            'Балашиха', 'Курск', 'Севастополь', 'Сочи', 'Ставрополь', 'Улан-Удэ', 'Тверь',
            'Магнитогорск', 'Иваново', 'Брянск', 'Белгород', 'Сургут', 'Владимир', 'Нижний Тагил',
            'Архангельск', 'Чита', 'Калуга', 'Смоленск', 'Волжский', 'Якутск', 'Саранск',
            'Подольск', 'Грозный', 'Орёл', 'Череповец', 'Вологда', 'Владикавказ', 'Мурманск',
            'Тамбов', 'Петрозаводск', 'Нижневартовск', 'Кострома', 'Новороссийск', 'Йошкар-Ола',
            'Химки', 'Таганрог', 'Сыктывкар', 'Нальчик', 'Шахты', 'Дзержинск', 'Орск', 'Братск',
            'Энгельс', 'Ангарск', 'Королёв', 'Псков', 'Бийск', 'Прокопьевск', 'Рыбинск',
            'Балаково', 'Северодвинск', 'Армавир', 'Подольск', 'Южно-Сахалинск', 'Петропавловск-Камчатский',
            'Сызрань', 'Норильск', 'Златоуст', 'Каменск-Уральский', 'Мытищи', 'Люберцы', 'Волгодонск',
            'Новочеркасск', 'Абакан', 'Находка', 'Уссурийск', 'Березники', 'Салават', 'Электросталь',
            'Миасс', 'Первоуральск', 'Керчь', 'Новоуральск', 'Железнодорожный', 'Альметьевск',
            'Хасавюрт', 'Копейск', 'Пятигорск', 'Одинцово', 'Рубцовск', 'Благовещенск', 'Кисловодск',
            'Новошахтинск', 'Жуковский', 'Северск', 'Назрань', 'Домодедово', 'Каспийск', 'Новотроицк'
        ]

        self.belarus_cities = [
            'Минск', 'Гомель', 'Могилёв', 'Витебск', 'Гродно', 'Брест', 'Бобруйск', 'Барановичи',
            'Борисов', 'Пинск', 'Орша', 'Мозырь', 'Солигорск', 'Новополоцк', 'Лида', 'Молодечно',
            'Полоцк', 'Жлобин', 'Светлогорск', 'Речица', 'Жодино', 'Слуцк', 'Кобрин', 'Волковыск',
            'Калинковичи', 'Сморгонь', 'Осиповичи', 'Рогачёв', 'Новогрудок', 'Горки', 'Берёза',
            'Ивацевичи', 'Лунинец', 'Поставы', 'Чаусы', 'Дзержинск', 'Микашевичи', 'Белоозёрск'
        ]
        print(f"🎯 Инициализация улучшенного анализатора")

        # Инициализация OCR
        try:
            self.reader = easyocr.Reader(['ru', 'en'])
            print("✅ OCR инициализирован")
        except Exception as e:
            print(f"❌ Ошибка OCR: {e}")
            self.reader = None

    def extract_slider_clients(self, html: str, base_url: str) -> Dict[str, List[str]]:
        """Анализ слайдеров и каруселей с клиентами и дилерами"""
        results = {
            "клиенты": [],
            "дилеры": [],
            "партнеры": []
        }

        if not self.reader:
            return results

        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Селекторы для слайдеров и каруселей
            slider_selectors = [
                # Слайдеры клиентов
                '.clients-slider', '.customers-slider', '.partners-slider',
                '.client-carousel', '.partner-carousel', '.brands-slider',
                '.logo-slider', '.clients-carousel',
                # Слайдеры дилеров
                '.dealers-slider', '.dealer-carousel', '.dilers-slider',
                '.dealer-network', '.dealer-list',
                # Общие слайдеры
                '.slick-slider', '.owl-carousel', '.swiper-container',
                '[class*="slider"]', '[class*="carousel"]'
            ]

            for selector in slider_selectors:
                sliders = soup.select(selector)
                for slider in sliders[:5]:  # Ограничиваем количество слайдеров
                    print(f"🔍 Анализ слайдера: {selector}")

                    # Извлекаем все изображения из слайдера
                    images = slider.find_all('img')
                    for img in images[:50]:  # Ограничиваем количество изображений
                        img_src = img.get('src')
                        if img_src:
                            img_url = urljoin(base_url, img_src)
                            try:
                                # Скачиваем и обрабатываем изображение
                                response = self.session.get(img_url, timeout=10)
                                if response.status_code == 200:
                                    image = Image.open(BytesIO(response.content))

                                    # OCR для извлечения текста
                                    ocr_results = self.reader.readtext(image)
                                    for (bbox, text, confidence) in ocr_results:
                                        if confidence > 0.6 and len(text) > 2:
                                            cleaned_text = self._clean_company_name(text)
                                            if self._looks_like_company_name(cleaned_text):
                                                # Определяем тип слайдера по контексту
                                                slider_type = self._classify_slider_type(slider, selector, text)
                                                if slider_type == "клиенты":
                                                    results["клиенты"].append(cleaned_text)
                                                elif slider_type == "дилеры":
                                                    results["дилеры"].append(cleaned_text)
                                                else:
                                                    results["партнеры"].append(cleaned_text)
                            except Exception as e:
                                continue

                    # Также анализируем текстовое содержимое слайдера
                    slider_text = slider.get_text(strip=True)
                    if slider_text:
                        companies_from_text = self._extract_companies_from_slider_text(slider_text)
                        slider_type = self._classify_slider_type(slider, selector, slider_text)

                        if slider_type == "клиенты":
                            results["клиенты"].extend(companies_from_text)
                        elif slider_type == "дилеры":
                            results["дилеры"].extend(companies_from_text)
                        else:
                            results["партнеры"].extend(companies_from_text)

            # Убираем дубликаты
            for key in results:
                results[key] = list(set(results[key]))

            print(f"✅ Найдено в слайдерах: {sum(len(v) for v in results.values())} компаний")

        except Exception as e:
            print(f"❌ Ошибка анализа слайдеров: {e}")

        return results

    def extract_representatives_from_contacts_pages(self, text: str, html: str = "", url: str = "") -> List[
        Dict[str, Any]]:
        """Извлечение представительств на страницах контактов/дилеров по паттернам компаний"""
        representatives = []

        # Проверяем, является ли это страницей контактов/дилеров
        if not self._is_contacts_or_dealers_page(url, text):
            return representatives

        print("🔍 Анализ страницы контактов/дилеров на представительства...")

        # Паттерны для поиска компаний-представителей
        company_patterns = [
            # ООО "Название", ОАО "Название" и т.д.
            r'(ООО|ОАО|ИП|ЗАО|АО|ПАО)\s+[«"]([^»"]+?)[»"]',
            r'[«"]([^»"]+?)[»"]\s+(ООО|ОАО|ИП|ЗАО|АО|ПАО)',
            # Без кавычек
            r'(ООО|ОАО|ИП|ЗАО|АО|ПАО)\s+([А-Я][A-ZА-Яa-zа-я\s&]{3,50})',
            r'([А-Я][A-ZА-Яa-zа-я\s&]{3,50})\s+(ООО|ОАО|ИП|ЗАО|АО|ПАО)',
        ]

        # Поиск компаний в тексте
        found_companies = []
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    company_type, company_name = match
                    if self._looks_like_company_name(company_name):
                        found_companies.append({
                            "тип_компании": company_type.upper(),
                            "название": company_name.strip(),
                            "контекст": self._extract_company_context(text, company_name)
                        })

        # Поиск сайтов и адресов рядом с найденными компаниями
        for company in found_companies:
            company_info = self._extract_company_details(text, html, company["название"])
            if company_info["сайт"] or company_info["адрес"]:
                representatives.append({
                    "название_компании": f"{company['тип_компании']} {company['название']}",
                    "сайт": company_info["сайт"],
                    "адрес": company_info["адрес"],
                    "телефон": company_info["телефон"],
                    "тип": "компания-представитель",
                    "источник": "страница_контактов",
                    "контекст": company["контекст"]
                })

        return representatives

    def _is_contacts_or_dealers_page(self, url: str, text: str) -> bool:
        """Определяет, является ли страница страницей контактов или дилеров"""
        url_lower = url.lower()
        text_lower = text.lower()

        # Ключевые слова в URL
        url_keywords = [
            'contacts', 'contact', 'kontakty', 'kontakt',
            'dealers', 'dealer', 'dilers', 'diler',
            'partners', 'partner', 'offices', 'office',
            'where-to-buy', 'distributors', 'distributor'
        ]

        # Ключевые слова в тексте
        text_keywords = [
            'контакты', 'дилеры', 'диллеры', 'партнеры',
            'где купить', 'адреса', 'офисы', 'представительства',
            'дилерская сеть', 'сеть продаж', 'региональные партнеры'
        ]

        # Проверяем URL
        if any(keyword in url_lower for keyword in url_keywords):
            return True

        # Проверяем заголовки и текст
        if any(keyword in text_lower for keyword in text_keywords):
            return True

        return False

    def _extract_company_context(self, text: str, company_name: str, context_size: int = 200) -> str:
        """Извлекает контекст вокруг названия компании"""
        start_idx = text.find(company_name)
        if start_idx == -1:
            return ""

        end_idx = start_idx + len(company_name)
        context_start = max(0, start_idx - context_size)
        context_end = min(len(text), end_idx + context_size)

        context = text[context_start:context_end].strip()
        # Очищаем контекст от лишних пробелов
        context = re.sub(r'\s+', ' ', context)
        return context

    def _extract_company_details(self, text: str, html: str, company_name: str) -> Dict[str, str]:
        """Извлекает контактные данные компании (сайт, адрес, телефон)"""
        details = {
            "сайт": "",
            "адрес": "",
            "телефон": ""
        }

        # Поиск в тексте
        company_context = self._extract_company_context(text, company_name, 300)

        # Поиск сайта
        website_patterns = [
            r'(?:www\.|https?://)[^\s,]+',
            r'(?:сайт|website)[:\s]*([^\s,]+)',
            r'[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?'
        ]

        for pattern in website_patterns:
            websites = re.findall(pattern, company_context, re.IGNORECASE)
            for website in websites:
                if self._is_valid_website(website):
                    details["сайт"] = website
                    break
            if details["сайт"]:
                break

        # Поиск адреса
        address_patterns = [
            r'(?:адрес|address)[:\s]*([А-Яа-я0-9\s,.-]{10,100})',
            r'(?:юридический адрес|legal address)[:\s]*([А-Яа-я0-9\s,.-]{10,100})',
            r'[А-Яа-я0-9\s,.-]{10,100}?(?:ул|улица|пр|проспект|пер|переулок)[^,.]{5,50}'
        ]

        for pattern in address_patterns:
            addresses = re.findall(pattern, company_context, re.IGNORECASE)
            if addresses:
                details["адрес"] = addresses[0].strip()
                break

        # Поиск телефона
        phone_patterns = [
            r'[\+]?[7|8][\s(-]?\d{3}[\s)-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}',
            r'\(\d{3,4}\)\s?\d{2,3}[\s-]?\d{2}[\s-]?\d{2}',
        ]

        for pattern in phone_patterns:
            phones = re.findall(pattern, company_context)
            if phones:
                details["телефон"] = phones[0]
                break

        # Дополнительный поиск в HTML
        if html:
            html_details = self._extract_company_details_from_html(html, company_name)
            if not details["сайт"] and html_details["сайт"]:
                details["сайт"] = html_details["сайт"]
            if not details["адрес"] and html_details["адрес"]:
                details["адрес"] = html_details["адрес"]
            if not details["телефон"] and html_details["телефон"]:
                details["телефон"] = html_details["телефон"]

        return details

    def _extract_company_details_from_html(self, html: str, company_name: str) -> Dict[str, str]:
        """Извлекает контактные данные компании из HTML структуры"""
        details = {"сайт": "", "адрес": "", "телефон": ""}

        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Ищем элементы, содержащие название компании
            company_elements = soup.find_all(string=re.compile(re.escape(company_name), re.IGNORECASE))

            for element in company_elements:
                parent = element.parent
                if parent:
                    # Ищем контактные данные в родительском элементе и соседних
                    context_text = parent.get_text()

                    # Поиск сайта
                    websites = re.findall(r'(?:www\.|https?://)[^\s,]+', context_text)
                    for website in websites:
                        if self._is_valid_website(website) and not details["сайт"]:
                            details["сайт"] = website

                    # Поиск адреса
                    addresses = re.findall(r'(?:адрес|address)[:\s]*([А-Яа-я0-9\s,.-]{10,100})', context_text,
                                           re.IGNORECASE)
                    if addresses and not details["адрес"]:
                        details["адрес"] = addresses[0].strip()

                    # Поиск телефона
                    phones = re.findall(r'[\+]?[7|8][\s(-]?\d{3}[\s)-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}', context_text)
                    if phones and not details["телефон"]:
                        details["телефон"] = phones[0]

        except Exception as e:
            print(f"❌ Ошибка извлечения данных компании из HTML: {e}")

        return details

    def _is_valid_website(self, website: str) -> bool:
        """Проверяет валидность веб-сайта"""
        website = website.strip()

        # Проверяем домен
        domain_patterns = [
            r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$',
            r'^www\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$',
            r'^https?://[a-zA-Z0-9-]+\.[a-zA-Z]{2,}',
            r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\.[a-zA-Z]{2,}$'
        ]

        for pattern in domain_patterns:
            if re.match(pattern, website):
                return True

        return False

    def extract_representatives(self, text: str, html: str = "") -> List[Dict[str, Any]]:
        """Извлечение информации о представительствах и филиалах с улучшенным поиском городов"""
        representatives = []

        # Списки городов России и Белоруссии для точного поиска


        all_cities = self.russian_cities + self.belarus_cities
        cities_pattern = '|'.join(all_cities)

        # Паттерны для поиска представительств с учетом суффиксов и окончаний
        patterns = [
            # Представительство в городе (точное совпадение)
            r'(?:представительство|филиал|офис|отделение|дилерский центр|сервисный центр)\s+(?:в|г\.?|городе?)\s*[«"]?(' + cities_pattern + ')[»"]?',

            # Город с суффиксами и окончаниями
            r'(?:г\.|город)\s*(' + '|'.join([re.escape(city) for city in
                                             all_cities]) + ')(?:ский|ской|ный|ное|ская|ское|ово|ево|ино|но|ск|цк|ьк)?\b',

            # Адреса представительств с городами
            r'(?:представительство|филиал|офис)[^.!?]{0,200}?(?:г\.|город)\s*(' + cities_pattern + ')[^.!?]{0,200}?([А-Яа-я0-9\s,.-]{10,100}?)(?=[.!]|$)',

            # Названия компаний-представителей с указанием городов
            r'(?:ооо|зао|ао|пао)\s+[«"]?([^»"]+?)[»"]?(?:\s+[^.!?]{0,150}?(?:в|г\.|город)\s*(' + cities_pattern + '))',

            # Контакты представительств
            r'(?:контакты|адрес)[^.!?]{0,150}?(?:в|г\.|город)\s*(' + cities_pattern + ')[^.!?]{0,150}?([А-Яа-я0-9\s,.-]{10,80})',

            # Региональные представительства
            r'(?:региональн|областн|городск)(?:ое|ой|ая)\s+(?:представительство|филиал|офис)[^.!?]{0,100}?(?:в|г\.|город)\s*(' + cities_pattern + ')',
        ]

        # Дополнительные паттерны для городов с разными окончаниями
        city_variations = []
        for city in all_cities:
            # Убираем окончания для базовой формы
            base_city = re.sub(r'(?:ский|ской|ный|ное|ская|ское|ово|ево|ино|но|ск|цк|ьк)$', '', city)
            if base_city != city:
                city_variations.append(base_city)

        if city_variations:
            variations_pattern = '|'.join(city_variations)
            patterns.append(
                r'(?:представительство|филиал|офис)\s+(?:в|г\.?|городе?)\s*[«"]?(' + variations_pattern + ')[»"]?'
            )

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    if len(match) == 2:
                        city, address = match
                        # Находим точное название города
                        exact_city = self._find_exact_city(city, all_cities)
                        if exact_city:
                            representatives.append({
                                "город": exact_city,
                                "адрес": self._clean_address(address),
                                "тип": "представительство",
                                "источник": "текст",
                                "страна": "Россия" if exact_city in self.russian_cities else "Беларусь"
                            })
                    elif len(match) >= 1:
                        city_or_company = match[0]
                        # Проверяем, является ли это городом
                        exact_city = self._find_exact_city(city_or_company, all_cities)
                        if exact_city:
                            representatives.append({
                                "город": exact_city,
                                "адрес": "",
                                "тип": "представительство",
                                "источник": "текст",
                                "страна": "Россия" if exact_city in self.russian_cities else "Беларусь"
                            })
                        else:
                            # Это название компании
                            representatives.append({
                                "название_компании": city_or_company.strip(),
                                "тип": "компания-представитель",
                                "источник": "текст"
                            })
                else:
                    exact_city = self._find_exact_city(match, all_cities)
                    if exact_city:
                        representatives.append({
                            "город": exact_city,
                            "адрес": "",
                            "тип": "представительство",
                            "источник": "текст",
                            "страна": "Россия" if exact_city in self.russian_cities else "Беларусь"
                        })

        # Поиск в HTML структуре
        if html:
            html_representatives = self._extract_representatives_from_html(html, all_cities)
            representatives.extend(html_representatives)

        # Убираем дубликаты
        unique_repr = []
        seen = set()
        for repr in representatives:
            key = f"{repr.get('город', '')}_{repr.get('название_компании', '')}_{repr.get('адрес', '')}"
            if key not in seen and key != "__":
                unique_repr.append(repr)
                seen.add(key)

        print(f"✅ Найдено {len(unique_repr)} представительств")
        return unique_repr

    def _find_exact_city(self, city_variant: str, all_cities: List[str]) -> str:
        """Находит точное название города по варианту с окончаниями"""
        city_variant_clean = re.sub(r'[^\w\s]', '', city_variant).strip()

        # Прямое совпадение
        for city in all_cities:
            if city.lower() == city_variant_clean.lower():
                return city

        # Совпадение с учетом окончаний
        for city in all_cities:
            base_city = re.sub(r'(?:ский|ской|ный|ное|ская|ское|ово|ево|ино|но|ск|цк|ьк)$', '', city)
            if base_city.lower() == city_variant_clean.lower():
                return city

        # Частичное совпадение (для случаев типа "Москв" вместо "Москва")
        for city in all_cities:
            if city.lower().startswith(city_variant_clean.lower()) and len(city_variant_clean) >= 4:
                return city
            if city_variant_clean.lower().startswith(city.lower()) and len(city) >= 4:
                return city

        return ""

    def _clean_address(self, address: str) -> str:
        """Очищает и форматирует адрес"""
        if not address:
            return ""

        # Убираем лишние слова
        clean_address = re.sub(r'(?:тел|телефон|phone|email|@|www\.)[^,.]*', '', address, flags=re.IGNORECASE)
        # Убираем лишние пробелы
        clean_address = re.sub(r'\s+', ' ', clean_address)
        # Обрезаем до разумной длины
        clean_address = clean_address.strip()

        if len(clean_address) > 150:
            clean_address = clean_address[:147] + "..."

        return clean_address

    def _extract_representatives_from_html(self, html: str, all_cities: List[str]) -> List[Dict[str, Any]]:
        """Извлечение представительств из HTML структуры с учетом городов"""
        representatives = []

        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Селекторы для разделов представительств
            representative_selectors = [
                '.representatives', '.offices', '.contacts-list', '.branches',
                '.filials', '.regional-offices', '.dealer-centers', '.service-centers',
                '[class*="representative"]', '[class*="branch"]', '[class*="filial"]',
                '[class*="office"]', '[class*="dealer"]', '[class*="service"]',
                '.city-list', '.regional-contacts', '.offices-list'
            ]

            cities_pattern = '|'.join(all_cities)

            for selector in representative_selectors:
                sections = soup.select(selector)
                for section in sections:
                    section_text = section.get_text()

                    # Ищем города в тексте раздела
                    for city in all_cities:
                        # Поиск точного упоминания города
                        city_pattern = r'(?:г\.|город|в)\s*{}'.format(re.escape(city))
                        if re.search(city_pattern, section_text, re.IGNORECASE):
                            address = self._extract_address_from_element(section)
                            representatives.append({
                                "город": city,
                                "адрес": address,
                                "тип": "представительство",
                                "источник": "html",
                                "страна": "Россия" if city in self.russian_cities else "Беларусь"
                            })

                    # Ищем названия компаний с указанием городов
                    company_city_pattern = r'(?:ооо|зао|ао|пао)\s+[«"]?([^»"]+?)[»"]?(?:\s+[^.!]{0,100}?(?:в|г\.|город)\s*(' + cities_pattern + '))'
                    company_matches = re.findall(company_city_pattern, section_text, re.IGNORECASE)
                    for company, city in company_matches:
                        exact_city = self._find_exact_city(city, all_cities)
                        if exact_city:
                            representatives.append({
                                "название_компании": company.strip(),
                                "город": exact_city,
                                "тип": "компания-представитель",
                                "источник": "html",
                                "страна": "Россия" if exact_city in self.russian_cities else "Беларусь"
                            })

        except Exception as e:
            print(f"❌ Ошибка анализа HTML представительств: {e}")

        return representatives


    def _extract_address_from_element(self, element) -> str:
        """Извлечение адреса из HTML элемента"""
        try:
            # Ищем адресные элементы
            address_selectors = ['[class*="address"]', '[class*="adress"]', '.address', '.adress']

            for selector in address_selectors:
                address_elem = element.select_one(selector)
                if address_elem:
                    address_text = address_elem.get_text(strip=True)
                    # Очищаем адрес от лишнего
                    clean_address = re.sub(r'(?:тел|телефон|phone|email|@)[^,]*', '', address_text, flags=re.IGNORECASE)
                    clean_address = re.sub(r'\s+', ' ', clean_address).strip()
                    if len(clean_address) > 10:
                        return clean_address

            # Если не нашли по селекторам, ищем в тексте элемента
            full_text = element.get_text()
            address_patterns = [
                r'(?:адрес|address)[:\s]*([А-Яа-я0-9\s,.-]{10,100}?)(?=[,.]|$)',
                r'[А-Яа-я0-9\s,.-]{10,100}?(?:ул|улица|пр|проспект|пер|переулок)[^,.]{5,50}'
            ]

            for pattern in address_patterns:
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                if matches:
                    return matches[0].strip()

        except Exception as e:
            print(f"❌ Ошибка извлечения адреса: {e}")

        return ""

    def extract_contacts_enhanced(self, text: str, html: str = "") -> Dict[str, Any]:
        """Расширенное извлечение контактов включая представительства"""
        contacts = self._extract_contacts(text)

        # Дополнительно ищем контакты в HTML
        if html:
            html_contacts = self._extract_contacts_from_html(html)
            # Объединяем контакты
            contacts["emails"] = list(set(contacts["emails"] + html_contacts["emails"]))[:10]
            contacts["phones"] = list(set(contacts["phones"] + html_contacts["phones"]))[:15]
            contacts["addresses"] = list(set(contacts["addresses"] + html_contacts["addresses"]))[:10]

        return contacts

    def _extract_contacts_from_html(self, html: str) -> Dict[str, List[str]]:
        """Извлечение контактов из HTML"""
        contacts = {"emails": [], "phones": [], "addresses": []}

        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Ищем контакты в специальных элементах
            contact_selectors = [
                '[class*="contact"]', '[class*="phone"]', '[class*="email"]',
                '[class*="address"]', '.footer', '.contacts'
            ]

            for selector in contact_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text()

                    # Email
                    emails = re.findall(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text)
                    contacts["emails"].extend(emails)

                    # Телефоны
                    phones = re.findall(r'[\+]?[7|8][\s(-]?\d{3}[\s)-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}', text)
                    contacts["phones"].extend(phones)

                    # Адреса
                    addresses = re.findall(
                        r'(?:г\.|город)\s*[А-Я][а-я]+[^.!?]{0,100}?(?:ул|улица|пр|проспект)[^.!?]{10,80}', text)
                    contacts["addresses"].extend(addresses)

        except Exception as e:
            print(f"❌ Ошибка извлечения контактов из HTML: {e}")

        # Убираем дубликаты
        for key in contacts:
            contacts[key] = list(set(contacts[key]))

        return contacts

    def _classify_slider_type(self, slider_element, selector: str, text: str) -> str:
        """Определяет тип слайдера (клиенты, дилеры, партнеры)"""
        text_lower = text.lower()
        selector_lower = selector.lower()

        # Проверяем классы и текст на наличие ключевых слов
        slider_classes = str(slider_element.get('class', [])).lower()

        # Ключевые слова для дилеров
        dealer_keywords = ['dealer', 'diler', 'дилер', 'диллер', 'dealer-network']
        # Ключевые слова для клиентов
        client_keywords = ['client', 'customer', 'клиент', 'заказчик', 'customer']
        # Ключевые слова для партнеров
        partner_keywords = ['partner', 'partners', 'партнер']

        # Проверяем дилеров
        if any(keyword in slider_classes or keyword in selector_lower or keyword in text_lower
               for keyword in dealer_keywords):
            return "дилеры"

        # Проверяем клиентов
        if any(keyword in slider_classes or keyword in selector_lower or keyword in text_lower
               for keyword in client_keywords):
            return "клиенты"

        # По умолчанию считаем партнерами
        return "партнеры"

    def _extract_companies_from_slider_text(self, text: str) -> List[str]:
        """Извлекает названия компаний из текста слайдера"""
        companies = []

        # Паттерны для извлечения компаний из текста
        patterns = [
            r'[«"]([^»"]{3,50})[»"]',
            r'\b([А-Я][A-ZА-Яa-zа-я\s&]{3,30})\b',
            r'\b([A-Z][A-Za-z\s&]{3,30})\b'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                cleaned_name = self._clean_company_name(match)
                if self._looks_like_company_name(cleaned_name):
                    companies.append(cleaned_name)

        return companies

    def _clean_company_name(self, text: str) -> str:
        """Очищает название компании от мусора"""
        # Убираем лишние символы
        cleaned = re.sub(r'[^\w\s&]', ' ', text)
        # Убираем лишние пробелы
        cleaned = re.sub(r'\s+', ' ', cleaned)
        # Обрезаем пробелы по краям
        cleaned = cleaned.strip()
        return cleaned

    def extract_partners_from_images(self, html: str, base_url: str) -> List[str]:
        """Извлечение партнеров и клиентов с изображений через OCR"""
        partners = []

        if not self.reader:
            return partners

        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Ищем изображения в разделах партнеров/клиентов
            partner_selectors = [
                '.partners img', '.clients img', '.customers img',
                '.partners-list img', '.clients-list img',
                'div[class*="partner"] img', 'div[class*="client"] img',
                'section[class*="partner"] img', 'section[class*="client"] img',
                '.dealers img', '.dealer img', '.dilers img'
            ]

            for selector in partner_selectors:
                images = soup.select(selector)
                for img in images[:10]:  # Ограничиваем количество
                    img_src = img.get('src')
                    if img_src:
                        img_url = urljoin(base_url, img_src)
                        try:
                            # Скачиваем и обрабатываем изображение
                            response = self.session.get(img_url, timeout=10)
                            if response.status_code == 200:
                                image = Image.open(BytesIO(response.content))

                                # OCR для извлечения текста
                                results = self.reader.readtext(image)
                                for (bbox, text, confidence) in results:
                                    if confidence > 0.6 and len(text) > 2:
                                        # Фильтруем названия компаний
                                        cleaned_text = self._clean_company_name(text)
                                        if self._looks_like_company_name(cleaned_text):
                                            partners.append(cleaned_text)
                        except Exception as e:
                            continue

        except Exception as e:
            print(f"❌ Ошибка OCR партнеров: {e}")

        return list(set(partners))

    def _looks_like_company_name(self, text: str) -> bool:
        """Проверяет, похож ли текст на название компании"""
        if len(text) < 3 or len(text) > 50:
            return False

        # Проверяем паттерны названий компаний
        company_patterns = [
            r'.*[Оо][Оо][Оо].*', r'.*[Зз][Аа][Оо].*', r'.*[Аа][Оо].*',
            r'.*[Пп][Аа][Оо].*', r'.*Inc.*', r'.*Ltd.*', r'.*GmbH.*',
            r'^[А-Я][A-ZА-Яa-zа-я\s&]+$', r'^[A-Z][A-Za-z\s&]+$'
        ]

        return any(re.match(pattern, text, re.IGNORECASE) for pattern in company_patterns)

    def extract_partners_from_text(self, text: str) -> Dict[str, List[str]]:
        """Извлечение партнеров, клиентов и дилеров из текста с разделением"""
        results = {
            "партнеры": [],
            "клиенты": [],
            "дилеры": []
        }

        # Паттерны для партнеров
        partner_patterns = [
            r'(?:партнеры?|сотрудничаем)(?:\s*[:—]\s*)([^.!?]+)',
            r'наши\s+партнеры(?:\s*[.:]?\s*)([^.!?]+)',
            r'партнерская\s+сеть[^.!?]*?([^.!?]+)',
        ]

        # Паттерны для клиентов
        client_patterns = [
            r'(?:клиенты?|заказчики?)(?:\s*[:—]\s*)([^.!?]+)',
            r'наши\s+клиенты(?:\s*[.:]?\s*)([^.!?]+)',
            r'работаем\s+с[^.!?]*?([^.!?]+)',
        ]

        # Паттерны для дилеров
        dealer_patterns = [
            r'(?:дилеры?|дилерская\s+сеть)(?:\s*[:—]\s*)([^.!?]+)',
            r'официальные\s+дилеры(?:\s*[.:]?\s*)([^.!?]+)',
            r'сеть\s+дилеров[^.!?]*?([^.!?]+)',
        ]

        # Обрабатываем партнеров
        for pattern in partner_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                companies = self._extract_companies_from_context(match)
                results["партнеры"].extend(companies)

        # Обрабатываем клиентов
        for pattern in client_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                companies = self._extract_companies_from_context(match)
                results["клиенты"].extend(companies)

        # Обрабатываем дилеров
        for pattern in dealer_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                companies = self._extract_companies_from_context(match)
                results["дилеры"].extend(companies)

        # Фильтрация и очистка
        for category in results:
            cleaned_companies = []
            for company in set(results[category]):
                company = company.strip()
                if (len(company) >= 4 and
                        not any(word in company.lower() for word in ['компания', 'организация', 'фирма']) and
                        self._looks_like_company_name(company)):
                    cleaned_companies.append(company)
            results[category] = cleaned_companies[:20]  # Ограничиваем количество

        return results

    def _extract_companies_from_context(self, context: str) -> List[str]:
        """Извлечение названий компаний из контекста"""
        companies = []

        # Паттерны для названий компаний
        company_patterns = [
            r'[«"]([^»"]+?)[»"]',  # В кавычках
            r'(?:ООО|ЗАО|АО|ПАО|ИП)\s+[«"]?([^»".!?,]+)',  # С указанием формы
            r'([А-Я][A-ZА-Яa-zа-я\s&]+?(?:ООО|ЗАО|АО|ПАО|Inc|Ltd))',  # С аббревиатурой
            r'([А-Я][A-ZА-Яa-zа-я\s&]{3,})'  # Любое название с заглавной буквы
        ]

        for pattern in company_patterns:
            matches = re.findall(pattern, context)
            companies.extend(matches)

        return companies

    def extract_management_reliable(self, text: str, url: str = "") -> List[Dict[str, Any]]:
        """Надежное извлечение руководства с помощью статистических паттернов"""
        management = []

        # Статистически частые сочетания для генерального директора
        director_patterns = [
            r'(генеральный\s+директор|гендиректор|директор|председатель)(?:\s+[—:-]\s*)?([А-Я][а-я]+\s+[А-Я][а-я]+(?:\s+[А-Я][а-я]+)?)',
            r'([А-Я][а-я]+\s+[А-Я][а-я]+(?:\s+[А-Я][а-я]+)?)(?:\s+[—:-]\s*)?(генеральный\s+директор|гендиректор|директор)',
            r'(директор|руководитель|председатель)(?:\s+[—:-]\s*)?([А-Я][а-я]+\s+[А-Я][а-я]+)',
            r'([А-Я][а-я]+\s+[А-Я][а-я]+)(?:\s+[—:-]\s*)?(директор|руководитель|председатель)'
        ]

        # Дополнительные контекстные паттерны
        context_patterns = [
            r'(?:во\s+главе\s+[^.!?]+?\s+стоит\s+)([А-Я][а-я]+\s+[А-Я][а-я]+)',
            r'(?:руководство\s+[^.!?]+?\s+осуществляет\s+)([А-Я][а-я]+\s+[А-Я][а-я]+)',
            r'(?:директором\s+[^.!?]+?\s+является\s+)([А-Я][а-я]+\s+[А-Я][а-я]+)'
        ]

        # Поиск по основным паттернам
        for pattern in director_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) == 2:
                    position, name = match
                    if self._is_valid_russian_name(name):
                        management.append({
                            "должность": position.strip().title(),
                            "имя": name.strip(),
                            "источник": "паттерн",
                            "контекст": self._extract_context(text, name)
                        })
                    elif self._is_valid_russian_name(position):
                        management.append({
                            "должность": name.strip().title(),
                            "имя": position.strip(),
                            "источник": "паттерн",
                            "контекст": self._extract_context(text, position)
                        })

        # Поиск по контекстным паттернам
        for pattern in context_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for name in matches:
                if self._is_valid_russian_name(name):
                    management.append({
                        "должность": "Генеральный директор",
                        "имя": name.strip(),
                        "источник": "контекст",
                        "контекст": self._extract_context(text, name)
                    })

        # Удаляем дубликаты
        unique_management = []
        seen_names = set()
        for person in management:
            if person['имя'] not in seen_names:
                unique_management.append(person)
                seen_names.add(person['имя'])

        print(f"✅ Найдено {len(unique_management)} руководителей")
        return unique_management

    def _is_valid_russian_name(self, name: str) -> bool:
        """Проверяет валидность русского имени"""
        name_parts = name.split()
        if len(name_parts) not in [2, 3]:
            return False

        # Проверяем русские символы и заглавные буквы
        russian_chars = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        for part in name_parts:
            if not part.istitle() or len(part) < 2:
                return False
            # Проверяем наличие русских символов
            if not any(char.lower() in russian_chars for char in part):
                return False

        return True

    def _extract_context(self, text: str, target: str, context_size: int = 100) -> str:
        """Извлекает контекст вокруг целевой фразы"""
        start_idx = text.find(target)
        if start_idx == -1:
            return ""

        end_idx = start_idx + len(target)
        context_start = max(0, start_idx - context_size)
        context_end = min(len(text), end_idx + context_size)

        return text[context_start:context_end].strip()

    def crawl_priority_pages(self, base_url: str) -> Dict[str, str]:
        """Приоритетный обход ключевых страниц"""
        print(f"🔍 Приоритетный поиск ключевых страниц: {base_url}")

        all_pages_text = {}
        priority_urls = self._generate_priority_urls(base_url)

        # Проверяем доступность приоритетных страниц
        valid_urls = []
        for url in priority_urls:
            if self._check_url_access(url):
                valid_urls.append(url)
                print(f"✅ Найдена: {url}")

        # Обрабатываем найденные страницы
        print(f"🚀 Обработка {len(valid_urls)} приоритетных страниц...")
        for url in valid_urls[:10]:  # Ограничиваем количество
            try:
                page_text = self._process_single_page(url)
                if page_text:
                    all_pages_text[url] = page_text
            except Exception as e:
                print(f"❌ Ошибка {url}: {e}")

        return all_pages_text

    def _generate_priority_urls(self, base_url: str) -> List[str]:
        """Генерация приоритетных URL"""
        priority_urls = []
        base_domain = urlparse(base_url).netloc
        base_scheme = urlparse(base_url).scheme

        for path in self.priority_paths:
            # Без www
            priority_urls.append(f"{base_scheme}://{base_domain}{path}")
            # С www
            priority_urls.append(f"{base_scheme}://www.{base_domain}{path}")

        return priority_urls

    def _check_url_access(self, url: str) -> bool:
        """Проверка доступности URL"""
        try:
            response = self.session.head(url, timeout=5, allow_redirects=True)
            return response.status_code == 200
        except:
            return False

    def _process_single_page(self, url: str) -> str:
        """Обработка одной страницы"""
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                return self._extract_text_from_html(response.text, url)
        except Exception as e:
            print(f"❌ Ошибка загрузки {url}: {e}")

        return ""

    def _extract_text_from_html(self, html: str, url: str = "") -> str:
        """Извлечение чистого текста из HTML"""
        soup = BeautifulSoup(html, 'html.parser')

        # Удаляем ненужные элементы
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'meta', 'link']):
            element.decompose()

        # Приоритетные селекторы для about/team страниц
        content_selectors = [
            'main', 'article', 'section',
            '.content', '.main-content', '.page-content',
            '.about-content', '.company-info', '.team-section',
            '.management-list', '.executive-team', '.directors',
            '.contact-info', '.contacts-list',
            '.partners', '.clients', '.dealers'
        ]

        text_parts = []

        # Ищем по специфическим селекторам
        for selector in content_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if len(text) > 50:
                    text_parts.append(text)

        # Если не нашли по селекторам, берем основной контент
        if not text_parts:
            content_elements = soup.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for element in content_elements:
                text = element.get_text(strip=True)
                if len(text) > 30:
                    text_parts.append(text)

        full_text = ' '.join(text_parts)
        full_text = re.sub(r'\s+', ' ', full_text)

        return full_text[:100000]  # Увеличиваем лимит для about-страниц

    def comprehensive_analysis(self, base_url: str) -> Dict[str, Any]:
        """Комплексный анализ компании"""
        print(f"\n🎯 КОМПЛЕКСНЫЙ АНАЛИЗ: {base_url}")

        # Приоритетный обход ключевых страниц
        priority_pages = self.crawl_priority_pages(base_url)

        if not priority_pages:
            return {"error": "Не найдены ключевые страницы для анализа"}

        print(f"📊 Обработано {len(priority_pages)} приоритетных страниц")

        # Анализ каждой страницы отдельно
        all_partners_data = {
            "текст_партнеры": [],
            "текст_клиенты": [],
            "текст_дилеры": [],
            "изображения_партнеры": [],
            "слайдер_клиенты": [],
            "слайдер_дилеры": [],
            "слайдер_партнеры": []
        }
        all_management = []
        all_contacts = []
        all_representatives = []

        for url, text in priority_pages.items():
            print(f"\n📄 Анализ страницы: {url}")

            try:
                # Получаем HTML для анализа слайдеров
                response = self.session.get(url, timeout=10)
                html_content = response.text

                # Анализ слайдеров
                slider_data = self.extract_slider_clients(html_content, base_url)
                all_partners_data["слайдер_клиенты"].extend(slider_data["клиенты"])
                all_partners_data["слайдер_дилеры"].extend(slider_data["дилеры"])
                all_partners_data["слайдер_партнеры"].extend(slider_data["партнеры"])

                # Партнеры из изображений
                image_partners = self.extract_partners_from_images(html_content, base_url)
                all_partners_data["изображения_партнеры"].extend(image_partners)

                # Анализ представительств (основной метод)
                page_representatives = self.extract_representatives(text, html_content)
                all_representatives.extend(page_representatives)

                # НОВОЕ: Анализ представительств на страницах контактов/дилеров
                contacts_representatives = self.extract_representatives_from_contacts_pages(text, html_content, url)
                all_representatives.extend(contacts_representatives)

            except Exception as e:
                print(f"❌ Ошибка анализа HTML: {e}")

            # Партнеры из текста
            text_partners_data = self.extract_partners_from_text(text)
            all_partners_data["текст_партнеры"].extend(text_partners_data["партнеры"])
            all_partners_data["текст_клиенты"].extend(text_partners_data["клиенты"])
            all_partners_data["текст_дилеры"].extend(text_partners_data["дилеры"])

            # Руководство
            page_management = self.extract_management_reliable(text, url)
            all_management.extend(page_management)

            # Контакты
            contacts = self._extract_contacts(text)
            if contacts["emails"] or contacts["phones"]:
                all_contacts.append({
                    "url": url,
                    "contacts": contacts
                })

        # Убираем дубликаты и формируем итоговые результаты
        final_partners_data = {}
        for key, companies in all_partners_data.items():
            final_partners_data[key] = list(set(companies))

        unique_management = self._remove_duplicate_management(all_management)

        # Обработка представительств
        unique_representatives = []
        seen_repr = set()
        for repr in all_representatives:
            key = f"{repr.get('город', '')}_{repr.get('название_компании', '')}_{repr.get('адрес', '')}"
            if key not in seen_repr and key != "__":
                unique_representatives.append(repr)
                seen_repr.add(key)

        # ОБЪЕДИНЕНИЕ ВСЕХ ДАННЫХ В ЕДИНЫЕ КАТЕГОРИИ
        consolidated_partners = {
            "все_партнеры": list(set(
                final_partners_data["текст_партнеры"] +
                final_partners_data["изображения_партнеры"] +
                final_partners_data["слайдер_партнеры"]
            )),
            "все_клиенты": list(set(
                final_partners_data["текст_клиенты"] +
                final_partners_data["слайдер_клиенты"]
            )),
            "все_дилеры": list(set(
                final_partners_data["текст_дилеры"] +
                final_partners_data["слайдер_дилеры"]
            ))
        }

        # Формируем результат
        result = {
            "url": base_url,
            "статус": "успешно",
            "руководство": unique_management,
            "бизнес_партнеры": {
                "детализированные_данные": final_partners_data,
                "объединенные_данные": consolidated_partners
            },
            "контакты": all_contacts,
            "представительства": unique_representatives,
            "проанализированные_страницы": list(priority_pages.keys()),
            "метаданные": {
                "найдено_руководителей": len(unique_management),
                # Детальная статистика
                "найдено_партнеров_текст": len(final_partners_data["текст_партнеры"]),
                "найдено_клиентов_текст": len(final_partners_data["текст_клиенты"]),
                "найдено_дилеров_текст": len(final_partners_data["текст_дилеры"]),
                "найдено_партнеров_изображения": len(final_partners_data["изображения_партнеры"]),
                "найдено_клиентов_слайдер": len(final_partners_data["слайдер_клиенты"]),
                "найдено_дилеров_слайдер": len(final_partners_data["слайдер_дилеры"]),
                "найдено_партнеров_слайдер": len(final_partners_data["слайдер_партнеры"]),
                # Общая статистика
                "всего_партнеров": len(consolidated_partners["все_партнеры"]),
                "всего_клиентов": len(consolidated_partners["все_клиенты"]),
                "всего_дилеров": len(consolidated_partners["все_дилеры"]),
                "найдено_страниц_с_контактами": len(all_contacts),
                "найдено_представительств": len(unique_representatives)
            }
        }

        return result

    def _remove_duplicate_management(self, management: List[Dict]) -> List[Dict]:
        """Удаляет дубликаты в руководстве"""
        unique = []
        seen_names = set()

        for person in management:
            if person['имя'] not in seen_names:
                unique.append(person)
                seen_names.add(person['имя'])

        return unique

    def _extract_contacts(self, text: str) -> Dict[str, List[str]]:
        """Извлечение контактной информации"""
        contacts = {"emails": [], "phones": [], "addresses": []}

        # Email
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        emails = re.findall(email_pattern, text)
        contacts["emails"] = list(set(emails))[:5]

        # Телефоны
        phone_patterns = [
            r'[\+]?[7|8][\s(-]?\d{3}[\s)-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}',
            r'\(\d{3,4}\)\s?\d{2,3}[\s-]?\d{2}[\s-]?\d{2}',
        ]

        all_phones = []
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            all_phones.extend(phones)

        contacts["phones"] = list(set(all_phones))[:10]

        return contacts


def main():
    """Демонстрация работы улучшенного анализатора"""

    print("🔄 Инициализация EnhancedCompanySiteAnalyzer...")
    analyzer = EnhancedCompanySiteAnalyzer(max_pages=15, max_depth=1)

    # Тестовые сайты
    test_urls = [
        "https://privod.ru/",
        "https://www.prst.ru/",
        "https://optimusdrive.ru/"
    ]

    for site in test_urls:
        print(f"\n{'=' * 80}")
        print(f"🔍 АНАЛИЗ: {site}")
        print(f"{'=' * 80}")

        try:
            result = analyzer.comprehensive_analysis(site)

            if "error" in result:
                print(f"❌ Ошибка: {result['error']}")
            else:
                print("✅ Анализ завершен успешно!")

                # Вывод результатов
                management = result.get("руководство", [])
                partners_data = result.get("бизнес_партнеры", {})
                consolidated_data = partners_data.get("объединенные_данные", {})
                representatives = result.get("представительства", [])  # НОВОЕ: представительства
                meta = result.get("метаданные", {})

                print(f"\n👑 РУКОВОДСТВО:")
                if management:
                    for i, person in enumerate(management, 1):
                        print(f"   {i}. {person['должность']}: {person['имя']}")
                else:
                    print("   ❌ Не найдено")

                # ВЫВОД ОБЪЕДИНЕННЫХ ДАННЫХ
                print(f"\n🤝 ВСЕ ПАРТНЕРЫ ({len(consolidated_data.get('все_партнеры', []))}):")
                all_partners = consolidated_data.get("все_партнеры", [])
                if all_partners:
                    for i, partner in enumerate(all_partners[:15], 1):
                        print(f"   {i}. {partner}")
                    if len(all_partners) > 15:
                        print(f"   ... и еще {len(all_partners) - 15}")
                else:
                    print("   ❌ Не найдено")

                print(f"\n💼 ВСЕ КЛИЕНТЫ ({len(consolidated_data.get('все_клиенты', []))}):")
                all_clients = consolidated_data.get("все_клиенты", [])
                if all_clients:
                    for i, client in enumerate(all_clients[:15], 1):
                        print(f"   {i}. {client}")
                    if len(all_clients) > 15:
                        print(f"   ... и еще {len(all_clients) - 15}")
                else:
                    print("   ❌ Не найдено")

                print(f"\n🚗 ВСЕ ДИЛЕРЫ ({len(consolidated_data.get('все_дилеры', []))}):")
                all_dealers = consolidated_data.get("все_дилеры", [])
                if all_dealers:
                    for i, dealer in enumerate(all_dealers[:15], 1):
                        print(f"   {i}. {dealer}")
                    if len(all_dealers) > 15:
                        print(f"   ... и еще {len(all_dealers) - 15}")
                else:
                    print("   ❌ Не найдено")

                # НОВОЕ: ВЫВОД ПРЕДСТАВИТЕЛЬСТВ
                print(f"\n🏢 ПРЕДСТАВИТЕЛЬСТВА ({len(representatives)}):")
                if representatives:
                    for i, repr in enumerate(representatives, 1):
                        if repr.get('город'):
                            country_flag = "🇷🇺" if repr.get('страна') == 'Россия' else "🇧🇾" if repr.get('страна') == 'Беларусь' else "🏢"
                            print(f"   {i}. {country_flag} {repr['город']}", end="")
                            if repr.get('адрес'):
                                print(f" - {repr['адрес']}")
                            else:
                                print()
                        elif repr.get('название_компании'):
                            print(f"   {i}. 🏢 {repr['название_компании']}", end="")
                            if repr.get('сайт'):
                                print(f" | 🌐 {repr['сайт']}", end="")
                            if repr.get('адрес'):
                                print(f" | 📍 {repr['адрес']}", end="")
                            if repr.get('телефон'):
                                print(f" | 📞 {repr['телефон']}", end="")
                            print()
                else:
                    print("   ❌ Не найдено")

                print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
                print(f"   👑 Руководителей: {meta.get('найдено_руководителей', 0)}")
                print(f"   🤝 Всего партнеров: {meta.get('всего_партнеров', 0)}")
                print(f"   💼 Всего клиентов: {meta.get('всего_клиентов', 0)}")
                print(f"   🚗 Всего дилеров: {meta.get('всего_дилеров', 0)}")
                print(f"   🏢 Представительств: {meta.get('найдено_представительств', 0)}")  # НОВОЕ
                print(f"   📞 Страниц с контактами: {meta.get('найдено_страниц_с_контактами', 0)}")

                # Сохранение результатов
                filename = f"enhanced_analysis_{urlparse(site).netloc}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"\n💾 Результаты сохранены в: {filename}")

        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    main()