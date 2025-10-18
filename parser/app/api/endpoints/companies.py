from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List

from app.database import get_db
from app.models.company import Company
from app.models.financial import FinancialData
from app.models.geo import CompanyGeo, ProductionData
from app.schemas.company import (
    CompanyResponse, 
    CompanyDetailResponse,
    CompanyListResponse,
    CompanyUpdate,
    PaginatedResponse
)

router = APIRouter()

@router.get("/companies/{inn}", response_model=CompanyDetailResponse)
async def get_company_by_inn(
    inn: str,
    db: AsyncSession = Depends(get_db)
):
    if not inn.isdigit() or len(inn) not in (10, 12):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="INN must be 10 or 12 digits"
        )
    
    company_query = select(Company).where(Company.inn == inn)
    result = await db.execute(company_query)
    company = result.scalar_one_or_none()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with INN {inn} not found"
        )
    
    financial_query = select(FinancialData).where(FinancialData.company_id == company.id)
    financial_result = await db.execute(financial_query)
    financial_data = financial_result.scalars().all()
    
    geo_query = select(CompanyGeo).where(CompanyGeo.company_id == company.id)
    geo_result = await db.execute(geo_query)
    geo_data = geo_result.scalar_one_or_none()
    
    production_query = select(ProductionData).where(ProductionData.company_id == company.id)
    production_result = await db.execute(production_query)
    production_data = production_result.scalar_one_or_none()
    
    return CompanyDetailResponse(
        **company.__dict__,
        financial_data=financial_data,
        geo_data=geo_data.__dict__ if geo_data else None,
        production_data=production_data.__dict__ if production_data else None
    )

@router.get("/companies", response_model=CompanyListResponse)
async def get_companies_list(
    okved: Optional[str] = Query(None, description="Filter by OKVED"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(50, ge=1, le=100, description="Page size"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Company)
    
    if okved:
        query = query.where(Company.main_okved.contains(okved))
    
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)
    
    result = await db.execute(query)
    companies = result.scalars().all()
    
    pages = (total + size - 1) // size
    
    return CompanyListResponse(
        companies=companies,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.put("/companies/{inn}", response_model=CompanyResponse)
async def update_company(
    inn: str,
    company_update: CompanyUpdate,
    db: AsyncSession = Depends(get_db)
):
    if not inn.isdigit() or len(inn) not in (10, 12):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="INN must be 10 or 12 digits"
        )
    
    query = select(Company).where(Company.inn == inn)
    result = await db.execute(query)
    company = result.scalar_one_or_none()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with INN {inn} not found"
        )
    
    update_data = company_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
    await db.commit()
    await db.refresh(company)
    
    return company

### Rusprofile

from app.services.rusprofile import fetch_company_by_inn
import asyncio
import concurrent.futures
import re
from typing import Dict, Any
from fastapi.responses import JSONResponse

# Rusprofile endpoints
@router.get("/rusprofile/{inn}", response_model=Dict[str, Any])
async def get_company_rusprofile(inn: str):
    """Возвращает данные о компании с Rusprofile по ИНН."""
    if not re.fullmatch(r"\d{10}|\d{12}", inn):
        raise HTTPException(status_code=400, detail="ИНН должен быть 10 или 12 цифр")

    # выполняем синхронную функцию в пуле потоков
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        data = await loop.run_in_executor(pool, fetch_company_by_inn, inn)

    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])

    return JSONResponse(content=data)

# Pdf parser
import PyPDF2
import io

@router.post("/parse-pdf/")
async def parse_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, "Требуется PDF файл")
    
    content = await file.read()
    pdf = PyPDF2.PdfReader(io.BytesIO(content))
    text = " ".join(p.extract_text() or "" for p in pdf.pages)
    text = re.sub(r"\s+", " ", text)
    
    data = {}
    patterns = {
        "inn": r"ИНН юридического лица [^\d]*([\d\s]{10,11})",
        "kpp": r"КПП\s+(?:юридического лица\s*)?(\d{9,12})",
        "orgFullName": r"Полное наименование на русском языке\s+([^0-9]+)",
        "registrationNalogDate": r"Дата постановки на учет в налоговом\s*органе\s*(\d{2}\.\d{2}\.\d{4})",
        "registerNumberInsurer": r"Регистрационный номер страхователя\s+(\d{5,15})",
        "registrationInsureDate": r"Дата постановки на учет в качестве\s*страхователя\s*(\d{2}\.\d{2}\.\d{4})",
        "main_okved": r"Код и наименование вида деятельности\s+([\d\.]+)",
        "okved_description": r"Код и наименование вида деятельности\s+[\d\.]+\s+([А-Яа-яЁё\s,\-\"\n\(\)]+)",
        "legalAddress": r"Адрес юридического лица\s+([0-9,А-ЯЁа-яё\.\-\s]+?)(?=\s\d{2,3}\s|\sE-mail|$)",
        "head": r"(?:Фамилия Имя Отчество|Руководитель|Генеральный директор)\s*([А-ЯЁA-Z\s\-]+)",
        "ogrn": r"ОГРН\s+(\d{13,15})",
        "email": r"E[-\s]*mail\s+([\w\.\-]+@[\w\.\-]+)",
        # "productionAddress": "",
        # "additionalSiteAddress": "",
        # "industry": "",
        # "subIndustry": "",
        # "mainOkved": "",
        # "mainOkvedActivity": "",
        # "productionOkved": "",
        # "registrationDate": "",
        # "parentOrgName": "",
        # "parentOrgInn": "",
        #...
    }

    for key, pattern in patterns.items():
        if m := re.search(pattern, text, re.IGNORECASE):
            data[key] = m.group(1).strip()
    
    return data
