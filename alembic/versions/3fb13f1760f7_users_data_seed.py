"""users_data_seed

Revision ID: 3fb13f1760f7
Revises: 2f9313691360
Create Date: 2025-03-25 20:05:35.203353

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, DateTime


# revision identifiers, used by Alembic.
revision: str = '3fb13f1760f7'
down_revision: Union[str, None] = '2f9313691360'#'d9834ff44a24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#указываем таблицу, в которую будет добавлять начальные данные
users_table = table('users',
                    column('id', Integer),
                    column('username', String),
                    column('password', String),
                    column('register_date', DateTime),
                    column('role', String))



def upgrade() -> None:
    #начальные данные
    init_data = [{'username': 'user', 'password': '$2b$12$yuGOqzGv7fxSUIVZk.Il/.b6GGsOri9rHjT3mQjyDA/8X/UarvKNe', 'register_date': datetime.datetime(2025, 3, 26, 12, 30, 35), "role": "user"},
                 {'username': 'moderator', 'password': '$2b$12$37i8GzOYNP8IwK8V8uUv6OmcMLS7dIWkrAHahBQbshF./PbSJEjQm', 'register_date': datetime.datetime(2025, 3, 26, 12, 35, 35), "role": "moderator"},
                 {'username': 'admin', 'password': '$2b$12$we0s3PMhTsRmHbcTypTtseRGk9eIphUH0l157lMAluUYPOCzvAgsW', 'register_date': datetime.datetime(2025, 3, 26, 12, 40, 35), "role": "admin"}]
    #вставляем начальные данные
    op.bulk_insert(users_table, init_data)

def downgrade() -> None:
    #удаляем все данные
    op.execute('DELETE FROM users;')
