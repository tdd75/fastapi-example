from typing import Type

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.properties import ColumnProperty, RelationshipProperty


def is_scalar_field(model: Type[DeclarativeMeta], field_name: str) -> bool:
    mapper = inspect(model)
    prop = mapper.attrs.get(field_name)
    return isinstance(prop, ColumnProperty)


def is_relationship_field(model: Type[DeclarativeMeta], field_name: str):
    mapper = inspect(model)
    prop = mapper.attrs.get(field_name)
    return isinstance(prop, RelationshipProperty)
