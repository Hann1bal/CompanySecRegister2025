from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class FinancialData(Base):
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    year = Column(Integer, nullable=False)
    
    # Revenue and profit
    revenue = Column(DECIMAL(15, 2))
    net_profit = Column(DECIMAL(15, 2))
    
    # Staff
    total_staff = Column(Integer)
    moscow_staff = Column(Integer)
    
    # Salary funds
    total_salary_fund = Column(DECIMAL(15, 2))
    moscow_salary_fund = Column(DECIMAL(15, 2))
    
    # Average salaries
    avg_salary = Column(DECIMAL(10, 2))
    avg_moscow_salary = Column(DECIMAL(10, 2))
    
    # Taxes
    moscow_taxes = Column(DECIMAL(15, 2))
    profit_tax = Column(DECIMAL(15, 2))
    property_tax = Column(DECIMAL(15, 2))
    land_tax = Column(DECIMAL(15, 2))
    personal_income_tax = Column(DECIMAL(15, 2))
    transport_tax = Column(DECIMAL(15, 2))
    other_taxes = Column(DECIMAL(15, 2))
    excise_tax = Column(DECIMAL(15, 2))
    
    # Investments and export
    investments = Column(DECIMAL(15, 2))
    export_volume = Column(DECIMAL(15, 2))
    
    # Relationship
    company = relationship("Company", back_populates="financial_data")
    
    __table_args__ = (
        UniqueConstraint('company_id', 'year', name='unique_company_year'),
    )