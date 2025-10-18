from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean  # Добавили Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class CompanyGeo(Base):
    __tablename__ = "company_geo"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    
    # Coordinates
    legal_lat = Column(DECIMAL(10, 6))
    legal_lon = Column(DECIMAL(10, 6))
    production_lat = Column(DECIMAL(10, 6))
    production_lon = Column(DECIMAL(10, 6))
    additional_lat = Column(DECIMAL(10, 6))
    additional_lon = Column(DECIMAL(10, 6))
    
    # Location info
    district = Column(String(100))
    area = Column(String(100))
    
    company = relationship("Company", back_populates="geo_data")

class ProductionData(Base):
    __tablename__ = "production_data"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    
    # Land plots
    land_cadastral_number = Column(String(100))
    land_area = Column(DECIMAL(10, 2))
    land_usage_type = Column(String(300))
    land_ownership_type = Column(String(100))
    land_owner = Column(String(500))
    
    # Property
    property_cadastral_number = Column(String(100))
    property_area = Column(DECIMAL(10, 2))
    property_usage_type = Column(String(300))
    property_building_type = Column(String(200))
    property_ownership_type = Column(String(100))
    property_owner = Column(String(500))
    
    # Production capacity
    production_area = Column(DECIMAL(10, 2))
    standardized_products = Column(Boolean)
    product_names = Column(String(1000))
    product_okpd_codes = Column(String(1000))
    product_segments = Column(String(1000))
    product_catalog = Column(String(1000))
    has_state_order = Column(Boolean)
    capacity_utilization = Column(DECIMAL(5, 2))
    has_export = Column(Boolean)
    export_volume_previous_year = Column(DECIMAL(15, 2))
    import_countries = Column(String(1000))
    
    company = relationship("Company", back_populates="production_data")