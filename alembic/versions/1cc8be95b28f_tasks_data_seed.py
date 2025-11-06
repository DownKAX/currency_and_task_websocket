"""tasks_data_seed

Revision ID: 1cc8be95b28f
Revises: d9834ff44a24
Create Date: 2025-03-25 20:05:14.747635

"""

import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, DateTime
from datetime import datetime, timedelta

# revision identifiers, used by Alembic.
revision: str = '1cc8be95b28f'
down_revision: Union[str, None] = '3fb13f1760f7'#'2f9313691360'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tasks_table = (table(
    'tasks',
    column('id', Integer),
    column('title', String),
    column('description', String),
    column('created_by', String),
    column('finished_by', String),
    column('date_of_start', DateTime),
    column('date_of_finish', DateTime)
))


def upgrade() -> None:
    init_data = [{"title": "Task 1", "description": "Task1 description", "created_by": "user", "finished_by": None, "date_of_start": datetime.utcnow() - timedelta(days=4), "date_of_finish": None},
                 {"title": "Task 2", "description": "Task2 description", "created_by": "moderator", "finished_by": None, "date_of_start": datetime.utcnow() - timedelta(days=3), "date_of_finish": None},
                 {"title": "Task 3", "description": "Task3 description", "created_by": "admin", "finished_by": None, "date_of_start": datetime.utcnow() - timedelta(days=2), "date_of_finish": None},
                 {"title": "Task 4", "description": "Task4 description", "created_by": "moderator", "finished_by": None, "date_of_start": datetime.utcnow() - timedelta(days=1), "date_of_finish": datetime.utcnow()}]
    op.bulk_insert(tasks_table, init_data)

def downgrade() -> None:
    op.execute('DELETE FROM tasks;')