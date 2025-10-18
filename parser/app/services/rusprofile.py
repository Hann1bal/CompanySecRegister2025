import sys
import time
import json
import re
from typing import Optional, Dict, Any
import requests
from bs4 import BeautifulSoup

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
})

# Настройки
RETRIES = 3
SLEEP_BETWEEN_RETRIES = 1.0  # секунды


def get_url_for_inn(inn: str) -> str:
    """
    Формируем URL поиска по ИНН.
    Rusprofile поддерживает поиск через /search?query=...
    """
    base = "https://www.rusprofile.ru/search"
    return f"{base}?query={inn}"


def safe_get(url: str, session: requests.Session = SESSION, timeout: int = 15) -> Optional[requests.Response]:
    """GET с простыми повторами."""
    for i in range(RETRIES):
        try:
            resp = session.get(url, timeout=timeout, allow_redirects=True)
            # Нормальные коды: 200, иногда 301/302 будут автоматически обработаны
            if resp.status_code == 200:
                return resp
            else:
                # Если сайт вернул 4xx/5xx — делаем паузу и повтор
                time.sleep(SLEEP_BETWEEN_RETRIES)
        except requests.RequestException:
            time.sleep(SLEEP_BETWEEN_RETRIES)
    return None


def extract_jsonld(soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    """Пытаемся найти application/ld+json и распарсить его."""
    scripts = soup.find_all("script", type="application/ld+json")
    for s in scripts:
        try:
            txt = s.string or s.get_text()
            data = json.loads(txt)
            # Иногда JSON-LD — массив
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type", "").lower() in ("organization", "legalentity", "localbusiness"):
                        return item
            elif isinstance(data, dict):
                t = data.get("@type", "").lower()
                if t in ("organization", "legalentity", "localbusiness") or "organization" in t:
                    return data
                # иногда данные глубже в ключах
                for v in data.values():
                    if isinstance(v, dict) and v.get("@type", "").lower() in ("organization", "legalentity", "localbusiness"):
                        return v
        except Exception:
            continue
    return None


def kv_from_text(text: str) -> Dict[str, str]:
    """Базовый поиск пар ключ:значение из текста страницы (регексы)."""
    out = {}
    # Убираем лишние пробелы
    t = re.sub(r"\s+", " ", text)

    # ИНН (10 или 12 цифр)
    m = re.search(r"ИНН[:\s]*([0-9]{10,12})", t, flags=re.IGNORECASE)
    if m:
        out["inn"] = m.group(1)

    # ОГРН (13 или 15 цифр)
    m = re.search(r"ОГРН[:\s]*([0-9]{13,15})", t, flags=re.IGNORECASE)
    if m:
        out["ogrn"] = m.group(1)

    # Генеральный директор / Руководитель
    m = re.search(r"(Генеральный директор|Руководитель)[:\s]*([A-ЯЁ][A-ЯЁа-яё\-\s]+)", t, flags=re.IGNORECASE)
    if m:
        out["director"] = m.group(2).strip()

    # Адрес
    m = re.search(r"Юридический адрес[:\s]*([0-9A-Za-zА-Яа-яЁё\.,\-\/\s]+?)(?:\s{2,}|Телефон|ИНН|ОГРН|$)", t)
    if m:
        out["address"] = m.group(1).strip()

    # Телефон(ы)
    phones = re.findall(r"Телефон(?:ы)?[:\s]*([\d\+\-\(\)\s,;/]+)", t, flags=re.IGNORECASE)
    if phones:
        out["phones"] = phones[0].strip()

    # Статус
    m = re.search(r"Статус[:\s]*([А-Яа-яЁё\s\-]+)", t)
    if m:
        out["status"] = m.group(1).strip()

    # Дата регистрации
    m = re.search(r"зарегистрирован[а|о]?\s*([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4})", t, flags=re.IGNORECASE)
    if m:
        out["registered"] = m.group(1).strip()

    # Основной вид деятельности
    m = re.search(r"Основной вид деятельности\s*([^(]+)\s*\(([^)]+)\)", t, flags=re.IGNORECASE)
    if m:
        out["main_activity"] = {
            "name": m.group(1).strip(),
            "code": m.group(2).strip()
        }

    return out


def parse_company_page(html: str, url: str) -> Dict[str, Any]:
    """Парсинг страницы компании: сначала JSON-LD, затем регулярки по тексту."""
    soup = BeautifulSoup(html, "html.parser")

    result: Dict[str, Any] = {"source_url": url}

    # 1) Попробуем извлечь JSON-LD
    j = extract_jsonld(soup)
    if j:
        # Берём часто встречающиеся поля
        if "name" in j:
            result["name"] = j.get("name")
        if "telephone" in j:
            result["phone"] = j.get("telephone")
        if "address" in j:
            # address может быть строкой или объектом
            if isinstance(j["address"], dict):
                addr = []
                for k in ("postalCode", "streetAddress", "addressLocality", "addressRegion"):
                    if j["address"].get(k):
                        addr.append(j["address"].get(k))
                result["address"] = ", ".join(addr).strip()
            else:
                result["address"] = j["address"]
        # возможны поля 'identifier' с ИНН/ОГРН
        ident = j.get("identifier")
        if isinstance(ident, dict):
            for k in ("inn", "ogrn"):
                if ident.get(k):
                    result[k] = ident.get(k)
        # Если есть дополнительные поля — добавим их целиком
        result["_jsonld_raw"] = j

    # 2) Базовый регекспарс по видимому тексту (фолбэк)
    text = soup.get_text(separator="\n", strip=True)
    kv = kv_from_text(text)
    result.update(kv)

    # 3) Попытка найти название (если не найдено)
    if "name" not in result:
        # Популярный селектор: заголовок компании — h1
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            result["name"] = h1.get_text(strip=True)

    # 4) Попытка найти блок с реквизитами (частые ключевые слова)
    # (ищем пары "ИНН" рядом)
    if "inn" not in result:
        m = re.search(r"ИНН[:\s]*([0-9]{10,12})", html)
        if m:
            result["inn"] = m.group(1)

    return result


def fetch_company_by_inn(inn: str, session: requests.Session = SESSION) -> Dict[str, Any]:
    """
    Основная функция:
    1) делает запрос в /search?query=INN
    2) если ответ — страница поиска с результатом, переходит на первую запись (редирект или парсинг ссылки)
    3) парсит страницу компании
    """
    url_search = get_url_for_inn(inn)
    resp = safe_get(url_search, session)
    if resp is None:
        return {"error": "Не удалось получить поисковую страницу (network/timeout)"}

    # Если запрос сразу вернул страницу компании (иногда сайт редиректит), используем её
    final_url = resp.url
    html = resp.text

    # Если это страница поиска, найдём первую ссылку на /id/
    if "/search" in final_url or "search?query" in final_url:
        soup = BeautifulSoup(html, "html.parser")
        # чаще всего результат содержит ссылку вида /id/<number>
        first_link = None
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if re.match(r"^/id/\d+", href):
                first_link = "https://www.rusprofile.ru" + href
                break
            # иногда ссылка ведёт напрямую на полное имя организации
            if "/profile/" in href and re.match(r".*\d+", href):
                first_link = "https://www.rusprofile.ru" + href
                break

        if first_link:
            resp = safe_get(first_link, session)
            if resp is None:
                return {"error": "Не удалось получить страницу компании (network/timeout)", "searched_url": url_search}
            final_url = resp.url
            html = resp.text
        else:
            # Если ссылки не нашли — попробуем найти на странице прямой текст/блок (редкий кейс)
            # и всё равно вернуть то, что смогли вытянуть
            parsed = parse_company_page(html, final_url)
            parsed["note"] = "Найдено через страницу поиска — прямая ссылка не обнаружена"
            return parsed

    # Наконец парсим страницу компании
    parsed = parse_company_page(html, final_url)
    return parsed


def main(argv):
    if len(argv) < 2:
        print("Usage: python fetch_rusprofile.py <INN>")
        sys.exit(1)
    inn = argv[1].strip()
    if not re.fullmatch(r"\d{10}|\d{12}", inn):
        print("ИНН должен быть 10 или 12 цифр.")
        sys.exit(1)

    data = fetch_company_by_inn(inn)
    print(json.dumps(data, ensure_ascii=False, indent=2))
