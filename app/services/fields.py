from datetime import datetime
from typing import Annotated

from sqlalchemy import text, String
from sqlalchemy.orm import mapped_column

pk = Annotated[int, mapped_column(primary_key=True)]
str_255 = Annotated[str, mapped_column(String(255), nullable=False)]
auto_now_add = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
auto_now = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)]
