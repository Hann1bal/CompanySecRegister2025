from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    inn = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(500))
    full_name = Column(String(1000))
    status = Column(String(500))
    legal_address = Column(String(1000))
    production_address = Column(String(1000))
    additional_site_address = Column(String(1000))
    main_industry = Column(String(500))
    sub_industry = Column(String(500))
    main_okved = Column(String(200), index=True)
    okved_description = Column(String(1000))
    production_okved = Column(String(200))
    registration_date = Column(Date)
    director = Column(String(500))
    head_organization = Column(String(1000))
    head_inn = Column(String(20))
    management_contacts = Column(Text)
    employee_contacts = Column(Text)
    emergency_contacts = Column(Text)
    website = Column(String(500))
    email = Column(String(300))
    support_measures = Column(Text)
    special_status = Column(String(500))
    msp_status = Column(String(200))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    financial_data = relationship("FinancialData", back_populates="company", cascade="all, delete-orphan")
    geo_data = relationship("CompanyGeo", back_populates="company", uselist=False, cascade="all, delete-orphan")
    production_data = relationship("ProductionData", back_populates="company", uselist=False, cascade="all, delete-orphan")