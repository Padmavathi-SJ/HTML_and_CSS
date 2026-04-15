import sqlite3

# DB connection
conn = sqlite3.connect("orm.db");
cursor = conn.cursor()

# FIELD (Descriptor)
class Field:
    def __init__(self, column_type):
        self.column_type = column_type
        self.name = None # will be set by ModelMeta

    def __set_name__(self, owner, name):
        self.name = name # field name inside class
    
    def __get__(self, instance, owner):
        if instance is None:
            return self 
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


# FIELD TYPES

class CharField(Field):
    def __init__(self, max_length, **kwargs):
        super().__init__(f"VARCHAR({max_length})", **kwargs)

class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)

class ForeignKey(Field):
    def __init__(self, to, related_name=None):
        super().__init__("INTEGER")
        self.to = to
        self.related_name = related_name

# METACLASS
class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return super().__new__(cls, name, bases, attrs)
        
        fields = {}

        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
        
        attrs["_fields"] = fields
        attrs["_table"] = name.lower()

        new_class = super().__new__(cls, name, bases, attrs)

        # Setup reverse relation (lazy loading)
        for field_name, field in fields.items():
            if isinstance(field, ForeignKey) and field.related_name:
                setattr(field.to, field.related_name,
                        property(lambda obj, fn=field_name, cls=new_class:
                                 cls.filter(**{fn: obj.id}).all()))
                
        return new_class
    

# QUERYSET (Method Chaining)
class QuerySet:
    def __init__(self, model):
        self.model = model
        self.query = f"SELECT * FROM {model._table}"
        self.conditions = []
        self.values = []
        self.order = ""

    def filter(self, **kwargs):
        for key, value in kwargs.items():
            if "__gte" in key:
                field = key.split("__")[0]
                self.conditions.append(f"{field} >= ?")
            else:
                self.conditions.append(f"{key} = ?")

            self.values.append(value)

        return self
    

    def order_by(self, field):
        if field.startswith("-"):
            self.order = f" ORDER BY {field[1:]} DESC"
        else:
            self.order = f" ORDER BY {field} ASC"
        
        return self
    

    def all(self):
        sql = self.query

        if self.conditions:
            sql += " WHERE " + " AND ".join(self.conditions)

        sql += self.order

        print("SQL: ", sql)

        cursor.execute(sql, self.values)
        rows = cursor.fetchall()

        # Convert rows -> objects
        result = []
        for row in rows:
            obj = self.model(**dict(zip(self.model._fields.keys(), row[1:])))
            obj.id = row[0]
            result.append(obj)

        return result
    

# BASE MODEL
class Model(metaclass=ModelMeta):
    
    def __init__(self, **kwargs):
        for field in self._fields:
            setattr(self, field, kwargs.get(field))
        self.id = kwargs.get("id")

    # CREATE TABLE
    @classmethod
    def create_table(cls):
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        for name, field in cls._fields.items():
            col = f"{name} {field.column_type}"

            columns.append(col)

        sql = f" CREATE TABLE IF NOT EXISTS {cls._table} ({', '.join(columns)})"
        print("SQL: ", sql)

        cursor.execute(sql)
        conn.commit()


    # SAVE (INSERT)
    def save(self):
        fields = ", ".join(self._fields.keys())
        values = [getattr(self, f) for f in self._fields]
        placeholders = ", ".join(["?"] * len(values))

        sql = f"INSERT INTO {self._table} ({fields}) VALUES ({placeholders})"
        print("SQL: ", sql)

        cursor.execute(sql, values)
        conn.commit()

        self.id = cursor.lastrowid
        print(f"Saved: {self.__class__.__name__}(id={self.id})")

    
    # DELETE
    def delete(self):
        sql = f"DELETE FROM {self._table} WHERE id=?"
        print("SQL: ", sql)

        cursor.execute(sql, (self.id,))
        conn.commit()


    # QUERY START
    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)
    
    @classmethod
    def all(cls):
        return QuerySet(cls).all()
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

  



    

