from datetime import datetime

from sqlalchemy import BOOLEAN, JSON, TEXT, TIMESTAMP, Column, Index, String
from sqlalchemy.ext.declarative import declarative_base

"""
A base class is required to define models:

https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html

We build three models in the module:

 ------                     ---------                     ------------
| app  | --- has many ---> | version | --- has many ---> | iteraction |
 ------                     ---------                     ------------

App is the container of versions. But only one version can be active.
Each version (except the first one of every app) contains a parent version, which
means the versions construct a tree instead of a list. The version has a configuration
which stores the DAG. The DAG defines how to interact with LLM and how to deal with
input data. Each time the DAG is executed, a new iteraction is produced. The iteraction
stores all data the DAG nodes produced.
"""
Base = declarative_base()


class Application(Base):
    """
    Application models app. An app has many versions but only one of them are active.
    Each time the app is called, the active_version's configration is used to build
    the DAG, and then produce the interaction record.
    """

    __tablename__ = "app