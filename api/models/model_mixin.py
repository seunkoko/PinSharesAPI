from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from ..models import db


class ModelMixin(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Saves an instance of the model to the database."""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except SQLAlchemyError as error:
            db.session.rollback()
            return error

    def delete(self):
        """Delete an instance of the model from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            return False

    @classmethod
    def delete_all(cls, **kwargs):
        """Delete multiple instances of the model form the database."""
        try:
            is_deleted = cls.query.filter_by(**kwargs).delete()

            db.session.commit()
            return is_deleted
        except SQLAlchemyError as error:
            db.session.rollback()
            return False

    @classmethod
    def update(cls, instance, **kwargs):
        """Update an instance of the model."""
        try:
            if instance is None:
                return False

            for key, value in kwargs.items():
                setattr(instance, key, value)
            db.session.commit()
            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            return False

    @classmethod
    def get_by_id(cls, id):
        """Gets data by Id."""
        return cls.query.get(id)

    @classmethod
    def find_first(cls, **kwargs):
        """Filters the data and returns the first result."""
        try:
            return cls.query.filter_by(**kwargs).first()
        except SQLAlchemyError as error:
            return False

    @classmethod
    def order_by(cls, **kwargs):
        """Orders and returns all the ordered data."""
        try:
            return cls.query.order_by(**kwargs)
        except SQLAlchemyError as error:
            return False

    @classmethod
    def find_all(cls, **kwargs):
        """Filters and returns all the filtered data of the model."""
        try:
            query = cls.query.filter_by(**kwargs)

            return query.all()
        except SQLAlchemyError as error:
            return False

    @classmethod
    def filter(cls, **kwargs):
        """Filters and returns all the filtered data of the model."""
        try:
            query = cls.query.filter(**kwargs)

            return query.all()
        except SQLAlchemyError as error:
            return False

    @classmethod
    def count(cls, **kwargs):
        """Returns the count of a filtered result."""
        try:
            return cls.query.filter_by(**kwargs).count()
        except SQLAlchemyError as error:
            return False

    @classmethod
    def check_exists(cls, **kwargs):
        """Returns true/false if a filtered result exists or not"""
        try:
            result = cls.query.filter_by(**kwargs).count()

            if result > 0:
                return True
            else:
                return False
        except SQLAlchemyError as error:
            return False

    @classmethod
    def paginate(cls, offset, limit, **kwargs):
        """Filters and paginates data of a model"""
        try:
            return cls.query.filter_by(**kwargs).paginate(page=offset, per_page=limit, error_out=False)
        except SQLAlchemyError as error:
            return False

    @classmethod
    def get(cls, *args):
        """Gets data by the Id."""
        return cls.query.get(*args)

    @classmethod
    def save_all(cls, records_object):
        """Saves a list of model instances to the database."""
        try:
            db.session.bulk_save_objects(records_object)
            db.session.commit()
            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            return False

    @classmethod
    def query_sql(cls, query, args):
        """Executes a query directly in the db.

        Args:
            query: SQL query
            args: JSON object of query params

        Returns:
            result -- Returns a SQLAlchemy result proxy
        """
        try:
            return db.session.execute(query, args)
        except SQLAlchemyError as error:
            db.session.rollback()
            return False
