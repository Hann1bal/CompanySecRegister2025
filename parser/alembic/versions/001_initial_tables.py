"""Initial tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create companies table
    op.create_table('companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('inn', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=500), nullable=True),
        sa.Column('full_name', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=100), nullable=True),
        sa.Column('legal_address', sa.Text(), nullable=True),
        sa.Column('production_address', sa.Text(), nullable=True),
        sa.Column('additional_site_address', sa.Text(), nullable=True),
        sa.Column('main_industry', sa.String(length=300), nullable=True),
        sa.Column('sub_industry', sa.String(length=300), nullable=True),
        sa.Column('main_okved', sa.String(length=100), nullable=True),
        sa.Column('okved_description', sa.Text(), nullable=True),
        sa.Column('production_okved', sa.String(length=100), nullable=True),
        sa.Column('registration_date', sa.Date(), nullable=True),
        sa.Column('director', sa.String(length=300), nullable=True),
        sa.Column('head_organization', sa.String(length=500), nullable=True),
        sa.Column('head_inn', sa.String(length=20), nullable=True),
        sa.Column('management_contacts', sa.Text(), nullable=True),
        sa.Column('employee_contacts', sa.Text(), nullable=True),
        sa.Column('emergency_contacts', sa.Text(), nullable=True),
        sa.Column('website', sa.String(length=500), nullable=True),
        sa.Column('email', sa.String(length=300), nullable=True),
        sa.Column('support_measures', sa.Text(), nullable=True),
        sa.Column('special_status', sa.String(length=200), nullable=True),
        sa.Column('msp_status', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('inn')
    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=False)
    op.create_index(op.f('ix_companies_inn'), 'companies', ['inn'], unique=False)
    op.create_index(op.f('ix_companies_main_okved'), 'companies', ['main_okved'], unique=False)

    # Create financial_data table
    op.create_table('financial_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('revenue', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('net_profit', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('total_staff', sa.Integer(), nullable=True),
        sa.Column('moscow_staff', sa.Integer(), nullable=True),
        sa.Column('total_salary_fund', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('moscow_salary_fund', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('avg_salary', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('avg_moscow_salary', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('moscow_taxes', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('profit_tax', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('property_tax', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('land_tax', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('personal_income_tax', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('transport_tax', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('other_taxes', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('excise_tax', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('investments', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('export_volume', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('company_id', 'year', name='unique_company_year'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_financial_data_id'), 'financial_data', ['id'], unique=False)

    # Create company_geo table
    op.create_table('company_geo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('legal_lat', sa.DECIMAL(precision=10, scale=6), nullable=True),
        sa.Column('legal_lon', sa.DECIMAL(precision=10, scale=6), nullable=True),
        sa.Column('production_lat', sa.DECIMAL(precision=10, scale=6), nullable=True),
        sa.Column('production_lon', sa.DECIMAL(precision=10, scale=6), nullable=True),
        sa.Column('additional_lat', sa.DECIMAL(precision=10, scale=6), nullable=True),
        sa.Column('additional_lon', sa.DECIMAL(precision=10, scale=6), nullable=True),
        sa.Column('district', sa.String(length=100), nullable=True),
        sa.Column('area', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_company_geo_id'), 'company_geo', ['id'], unique=False)

    # Create production_data table
    op.create_table('production_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('land_cadastral_number', sa.String(length=100), nullable=True),
        sa.Column('land_area', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('land_usage_type', sa.String(length=300), nullable=True),
        sa.Column('land_ownership_type', sa.String(length=100), nullable=True),
        sa.Column('land_owner', sa.String(length=500), nullable=True),
        sa.Column('property_cadastral_number', sa.String(length=100), nullable=True),
        sa.Column('property_area', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('property_usage_type', sa.String(length=300), nullable=True),
        sa.Column('property_building_type', sa.String(length=200), nullable=True),
        sa.Column('property_ownership_type', sa.String(length=100), nullable=True),
        sa.Column('property_owner', sa.String(length=500), nullable=True),
        sa.Column('production_area', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('standardized_products', sa.Boolean(), nullable=True),
        sa.Column('product_names', sa.String(length=1000), nullable=True),
        sa.Column('product_okpd_codes', sa.String(length=1000), nullable=True),
        sa.Column('product_segments', sa.String(length=1000), nullable=True),
        sa.Column('product_catalog', sa.String(length=1000), nullable=True),
        sa.Column('has_state_order', sa.Boolean(), nullable=True),
        sa.Column('capacity_utilization', sa.DECIMAL(precision=5, scale=2), nullable=True),
        sa.Column('has_export', sa.Boolean(), nullable=True),
        sa.Column('export_volume_previous_year', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('import_countries', sa.String(length=1000), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_production_data_id'), 'production_data', ['id'], unique=False)

def downgrade():
    op.drop_table('production_data')
    op.drop_table('company_geo')
    op.drop_table('financial_data')
    op.drop_table('companies')