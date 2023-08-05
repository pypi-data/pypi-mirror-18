#!/usr/bin/env python
# crate_anon/anonymise/dbholder.py

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

from crate_anon.common.sqla import get_table_names

log = logging.getLogger(__name__)


# =============================================================================
# Convenience object
# =============================================================================

DB_SAFE_CONFIG_FWD_REF = "DatabaseSafeConfig"


class DatabaseHolder(object):
    def __init__(self,
                 name: str,
                 url: str,
                 srccfg: DB_SAFE_CONFIG_FWD_REF = None,
                 with_session: bool = False,
                 with_conn: bool = True,
                 reflect: bool = True,
                 encoding: str = 'utf-8') -> None:
        self.name = name
        self.srccfg = srccfg
        self.engine = create_engine(url, encoding=encoding)
        self.conn = None
        self.session = None
        self.table_names = []
        self.metadata = MetaData(bind=self.engine)
        log.debug(self.engine)  # obscures password

        if with_conn:  # for raw connections
            self.conn = self.engine.connect()
        if reflect:
            self.table_names = get_table_names(self.engine)
            self.metadata.reflect(views=True)  # include views
            self.table_names = [t.name
                                for t in self.metadata.sorted_tables]
        if with_session:  # for ORM
            self.session = sessionmaker(bind=self.engine)()  # for ORM

