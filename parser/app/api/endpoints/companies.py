from fastapi import APIRouter, Depends, HTTPException, Query, status
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