import uuid
from typing import Any, Dict, Type, List

from core.database import DBSession, Base

DataObject = Dict[str, Any]


class DBInterface:
    """
    DBInterface is an abstract class that defines the methods for interacting with a database.
    This class provides a blueprint for defining the methods for adding, updating and retrieving data from a database.
    The concrete implementations of this class should define the actual database operations.
    """

    def __init__(self, db_class: Type[Base]):
        self.db_class = db_class

    def to_dict(self, obj: Base) -> Dict[str, Any]:
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

    def read_by_id(self, id: str) -> DataObject:
        session = DBSession()
        item: Base = session.query(self.db_class).get(id)
        session.close()
        return item

    def read_all(self) -> List[DataObject]:
        session = DBSession()
        return session.query(self.db_class).all()

    def create(self, data: DataObject) -> DataObject:
        session = DBSession()
        item: Base = self.db_class(**data)
        session.add(item)
        session.commit()
        session.close()
        return self.to_dict(item)

    def update(self, id: str, data: DataObject) -> DataObject:
        session = DBSession()
        item: Base = session.query(self.db_class).get(id)
        for key, value in data.items():
            setattr(item, key, value)
        session.commit()
        session.close()
        return self.to_dict(item)

    def delete(self, id: str) -> DataObject:
        session = DBSession()
        item: Base = session.query(self.db_class).get(id)
        result = self.to_dict(item)
        session.delete(item)
        session.commit()
        session.close()
        return result

    def get_single_item_by_filters(self, fields: tuple) -> Any:
        session = DBSession()
        item: Base = session.query(self.db_class).filter(*fields)
        item: Any = item.first()
        session.close()
        return item

    def get_multiple_items_by_filters(self, fields: tuple) -> Any:
        session = DBSession()
        item: Base = session.query(self.db_class).filter(*fields)
        item: Any = item.all()
        session.close()
        return item

    def create_with_uuid(self, data: DataObject) -> DataObject:
        session = DBSession()
        data.update({"id": str(uuid.uuid4())})
        item: Base = self.db_class(**data)
        session.add(item)
        session.commit()
        session.close()
        return item

    def upsert(self, data: DataObject) -> DataObject:
        session = DBSession()
        item: Base = self.db_class(**data)
        session.merge(item)
        session.commit()
        result = self.to_dict(item)
        session.close()
        return result
