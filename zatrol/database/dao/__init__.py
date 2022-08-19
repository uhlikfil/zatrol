from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection

from zatrol.database.connection import get_connection


class BaseDAO:
    def __init__(self, connection: AsyncConnection = Depends(get_connection)):
        self.connection = connection
