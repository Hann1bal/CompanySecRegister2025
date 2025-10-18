from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal

class FinancialDataBase(BaseModel):
    year: int
    revenue: Optional[Decimal] = None
    net_profit: Optional[Decimal] = None
    total_staff: Optional[int] = None
    moscow_staff: Optional[int] = None
    total_salary_fund: Optional[Decimal] = None
    moscow_salary_fund: Optional[Decimal] = None
    avg_salary: Optional[Decimal] = None
    avg_moscow_salary: Optional[Decimal] = None

class CompanyBase(BaseModel):
    inn: str
    name: Optional[str] = None
    full_name: Optional[str] = None
    status: Optional[str] = None
    legal_address: Optional[str] = None
    main_okved: Optional[str] = None
    okved_description: Optional[str] = None
    
    @validator('inn')
    def validate_inn(cls, v):
        if not v.isdigit() or len(v) not in (10, 12):
            raise ValueError('INN must be 10 or 12 digits')
        return v

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    legal_address: Optional[str] = None
    # ... другие поля для обновления

class CompanyResponse(CompanyBase):
    id: int
    registration_date: Optional[date] = None
    director: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CompanyDetailResponse(CompanyResponse):
    financial_data: List[FinancialDataBase] = []
    geo_data: Optional[Dict[str, Any]] = None
    production_data: Optional[Dict[str, Any]] = None

class CompanyListResponse(BaseModel):
    companies: List[CompanyResponse]
    total: int
    page: int
    size: int
    pages: int

class PaginatedResponse(BaseModel):
    page: int = 1
    size: int = 50