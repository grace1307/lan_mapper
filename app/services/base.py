from app.db import db


# Ignore it if db can't find the row when updating/deleting
# Todo: not ignore it, raise some error, remove checkers in view
class BaseService:
    __abstract__ = True
    model = None

    # Create
    def add_one(self, **kwargs):
        new_row = self.model(**kwargs)
        db.session.add(new_row)
        db.session.commit()  # sqlalchemy auto flushes so maybe this just need commit ?

        return new_row

    # Read
    def select_one(self, id):
        return self.model.query.filter(self.model.id == id).one_or_none()

    def select_all(self, conditions: list = None, sort_by=None, is_asc=None):
        query = db.session.query(self.model)

        if conditions is not None:
            for condition in conditions:
                query = query.filter(condition)

        if sort_by is not None and is_asc is not None:
            sort_column = self.model.__table__._columns[sort_by]
            is_asc = is_asc == 'true'

            if sort_column is not None:
                query = query.order_by(sort_column.asc() if is_asc else sort_column.desc())

        return query.all()

    # Update
    def update_one(self, id, updated):
        row = self.model.query.filter(self.model.id == id)
        row_result = row.one_or_none()

        if row_result is not None:
            row.update(updated)
            db.session.commit()

            return row.one_or_none()

    # Delete
    def delete_one(self, id):
        row = self.select_one(id)

        if row is not None:
            db.session.delete(row)
            db.session.commit()
