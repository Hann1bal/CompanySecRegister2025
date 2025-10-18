import aiohttp
import asyncio
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import datetime
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

from app.models.company import Company
from app.models.financial import FinancialData
from app.models.geo import CompanyGeo, ProductionData
from app.core.config import settings

logger = logging.getLogger(__name__)

class ListOrgParser:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.base_url = "https://www.list-org.com"
        self.session = None
        self.batch_size = settings.PARSER_BATCH_SIZE
        
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_search_page(self, page: int = 1) -> Optional[str]:
        try:
            url = f"{self.base_url}/search"
            params = {'type': 'all', 'val': 'москва', 'page': page}
            
            await asyncio.sleep(1)
            
            async with self.session.get(url, params=params, ssl=False) as response:
                response.raise_for_status()
                return await response.text()
                
        except Exception as e:
            logger.error(f"Error getting search page {page}: {str(e)}")
            return None

    def extract_inn(self, label_text: str) -> Optional[str]:
        match = re.search(r'ИНН/КПП\s*:\s*(\d{10})', label_text, re.IGNORECASE)
        return match.group(1) if match else None

    async def extract_company_details(self, url: str) -> Dict[str, Any]:
        try:
            async with self.session.get(url, ssl=False) as response:
                response.raise_for_status()
                html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            full_text = soup.get_text()
            
            company_data = await self._parse_basic_info(soup, full_text)
            company_data.update(await self._parse_financial_info(soup, full_text))
            company_data.update(await self._parse_address_info(soup, full_text))
            company_data.update(await self._parse_contacts_info(soup, full_text))
            
            return company_data
            
        except Exception as e:
            logger.error(f"Error extracting company details from {url}: {str(e)}")
            return {}

    async def _parse_basic_info(self, soup: BeautifulSoup, full_text: str) -> Dict[str, Any]:
        data = {}
        
        patterns = [
            r'Основной\s*\(по\s*коду\s*ОКВЭД\)[^:]*:\s*(\d{2}\.\d{2}(?:\.\d{2})?)\s*[—\-]\s*([^\.\n]+)',
            r'Основной\s*вид\s*деятельности[^:]*:\s*(\d{2}\.\d{2}(?:\.\d{2})?)\s*[—\-]\s*([^\.\n]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                code, description = match.groups()
                data['main_okved'] = code.strip()
                data['okved_description'] = description.strip()
                break
        
        status_patterns = [
            r'Статус[^:]*:\s*([^\n]+)',
            r'Состояние[^:]*:\s*([^\n]+)'
        ]
        for pattern in status_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                data['status'] = match.group(1).strip()
                break
        
        reg_pattern = r'Дата\s*регистрации[^:]*:\s*(\d{2}\.\d{2}\.\d{4})'
        match = re.search(reg_pattern, full_text, re.IGNORECASE)
        if match:
            try:
                date_str = match.group(1)
                day, month, year = map(int, date_str.split('.'))
                data['registration_date'] = datetime.date(year, month, day)
            except:
                pass
        
        director_pattern = r'Руководитель[^:]*:\s*([^\n]+)'
        match = re.search(director_pattern, full_text, re.IGNORECASE)
        if match:
            data['director'] = match.group(1).strip()
        
        return data

    async def _parse_financial_info(self, soup: BeautifulSoup, full_text: str) -> Dict[str, Any]:
        data = {}
        
        revenue_pattern = r'Выручка[^:]*:\s*([\d\s]+)'
        match = re.search(revenue_pattern, full_text)
        if match:
            try:
                revenue = int(match.group(1).replace(' ', ''))
                data['revenue'] = revenue
            except:
                pass
        
        return data

    async def _parse_address_info(self, soup: BeautifulSoup, full_text: str) -> Dict[str, Any]:
        data = {}
        
        legal_addr_pattern = r'Юридический\s*адрес[^:]*:\s*([^\n]+)'
        match = re.search(legal_addr_pattern, full_text, re.IGNORECASE)
        if match:
            data['legal_address'] = match.group(1).strip()
        
        production_addr_pattern = r'Адрес\s*производства[^:]*:\s*([^\n]+)'
        match = re.search(production_addr_pattern, full_text, re.IGNORECASE)
        if match:
            data['production_address'] = match.group(1).strip()
        
        return data

    async def _parse_contacts_info(self, soup: BeautifulSoup, full_text: str) -> Dict[str, Any]:
        data = {}
        
        website_pattern = r'Сайт[^:]*:\s*([^\n]+)'
        match = re.search(website_pattern, full_text, re.IGNORECASE)
        if match:
            data['website'] = match.group(1).strip()
        
        email_pattern = r'[Ee]-?mail[^:]*:\s*([^\n]+)'
        match = re.search(email_pattern, full_text)
        if match:
            data['email'] = match.group(1).strip()
        
        return data

    async def get_companies_batch(self, limit: int = 20) -> List[Dict[str, Any]]:
        companies = []
        page = 1
        
        logger.info(f"🔄 Starting to parse {limit} companies...")
        
        while len(companies) < limit:
            html = await self.get_search_page(page)
            if not html:
                page += 1
                continue
            
            soup = BeautifulSoup(html, 'html.parser')
            company_links = soup.find_all('a', href=re.compile(r'^/company/\d+'))
            
            for link in company_links:
                if len(companies) >= limit:
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
                    
                    details = await self.extract_company_details(company_url)
                    
                    company_data = {
                        'name': company_name,
                        'inn': inn,
                        'full_name': company_name,
                        **details
                    }
                    
                    companies.append(company_data)
                    
                    logger.info(f"✅ {len(companies)}. {company_name} (ИНН: {inn})")
                    
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error processing company: {str(e)}")
                    continue
            
            page += 1
            await asyncio.sleep(1)
        
        return companies

    async def save_company_data(self, data: Dict[str, Any]):
        try:
            query = select(Company).where(Company.inn == data['inn'])
            result = await self.db.execute(query)
            existing_company = result.scalar_one_or_none()
            
            if existing_company:
                for key, value in data.items():
                    if hasattr(existing_company, key) and value is not None:
                        setattr(existing_company, key, value)
                company = existing_company
            else:
                company = Company(**data)
                self.db.add(company)
            
            await self.db.flush()
            await self.db.commit()
            return company
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error saving company data for INN {data.get('inn')}: {str(e)}")
            raise

    async def process_companies_batch(self, companies_data: List[Dict[str, Any]]):
        saved_count = 0
        error_count = 0
        
        for company_data in companies_data:
            try:
                await self.save_company_data(company_data)
                saved_count += 1
            except Exception as e:
                logger.error(f"Failed to save company {company_data.get('inn')}: {str(e)}")
                error_count += 1
        
        logger.info(f"Batch processing complete: {saved_count} saved, {error_count} errors")
        return saved_count, error_count

class DataParser:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.parser = ListOrgParser(db)
    
    async def run_parsing(self, full_refresh: bool = False, limit: int = 100):
        logger.info(f"Starting data parsing (full_refresh: {full_refresh}, limit: {limit})")
        
        try:
            async with self.parser as parser:
                if full_refresh:
                    await self.full_parse(parser, limit)
                else:
                    await self.incremental_parse(parser, limit)
                    
            logger.info("Data parsing completed successfully")
            
        except Exception as e:
            logger.error(f"Data parsing failed: {str(e)}")
            raise
    
    async def full_parse(self, parser: ListOrgParser, limit: int):
        logger.info(f"Starting full data parse for {limit} companies")
        
        companies_data = await parser.get_companies_batch(limit)
        await parser.process_companies_batch(companies_data)
    
    async def incremental_parse(self, parser: ListOrgParser, limit: int):
        logger.info(f"Starting incremental data parse for {limit} companies")
        
        companies_data = await parser.get_companies_batch(limit)
        await parser.process_companies_batch(companies_data)