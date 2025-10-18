"""increase field lengths

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Увеличиваем длины полей в таблице companies
    op.alter_column('companies', 'full_name', type_=sa.String(1000))
    op.alter_column('companies', 'status', type_=sa.String(500))
    op.alter_column('companies', 'legal_address', type_=sa.String(1000))
    op.alter_column('companies', 'production_address', type_=sa.String(1000))
    op.alter_column('companies', 'additional_site_address', type_=sa.String(1000))
    op.alter_column('companies', 'main_industry', type_=sa.String(500))
    op.alter_column('companies', 'sub_industry', type_=sa.String(500))
    op.alter_column('companies', 'main_okved', type_=sa.String(200))
    op.alter_column('companies', 'okved_description', type_=sa.String(1000))
    op.alter_column('companies', 'production_okved', type_=sa.String(200))
    op.alter_column('companies', 'director', type_=sa.String(500))
    op.alter_column('companies', 'head_organization', type_=sa.String(1000))
    op.alter_column('companies', 'special_status', type_=sa.String(500))
    op.alter_column('companies', 'msp_status', type_=sa.String(200))
    # Убираем создание constraint - он уже существует

def downgrade():
    # Возвращаем обратно
    op.alter_column('companies', 'full_name', type_=sa.Text())
    op.alter_column('companies', 'status', type_=sa.String(100))
    op.alter_column('companies', 'legal_address', type_=sa.Text())
    op.alter_column('companies', 'production_address', type_=sa.Text())
    op.alter_column('companies', 'additional_site_address', type_=sa.Text())
    op.alter_column('companies', 'main_industry', type_=sa.String(300))
    op.alter_column('companies', 'sub_industry', type_=sa.String(300))
    op.alter_column('companies', 'main_okved', type_=sa.String(100))
    op.alter_column('companies', 'okved_description', type_=sa.Text())
    op.alter_column('companies', 'production_okved', type_=sa.String(100))
    op.alter_column('companies', 'director', type_=sa.String(300))
    op.alter_column('companies', 'head_organization', type_=sa.String(500))
    op.alter_column('companies', 'special_status', type_=sa.String(200))
    op.alter_column('companies', 'msp_status', type_=sa.String(100))