ORM = Object-Relational Mapping -> a technique to convert between SQL databases and Python objects.

The problem ORM Solves:
# Without ORM (Raw SQL):

cursor.execute("SELECT id, name, email, age from user where age >=25)
rows = cursor.fetchall()
users = []
for row in rows:
users.append({
    'id': row[0],
    'name': row[1],
    'email': row[2],
    'age': row[3]
})

# With ORM:
users = User.filter(age__gte=25).all() # much cleaner

--> What is a Descriptor? -> A python protocol that controls attribute access.

--> Descriptor Protocol Methods:
1. __set_name__ - Called when class if created (knows the feild name)
2. __get__ - called when reading attribute (user.name)
3. __set__ - Called when setting attribute (user.name = "Alice")

--> __set_name__ method:
def __set_name__ (self, owner, name):
  self.name = name # Store the feild name  (eg: "name", "email", "age")

When is this called?
 class User(Model):
   name = CharFiels(100) # when this line executes, Python calls:
   --> CharField.__set_name__(User, 'name')

Why needed? The field needs to know its name to store values properly.

--> __get__ method
def __get__(self, instance, owner):
return instance.__dict__.get(self.name)
 
What it does: Returns the value from the instance's dictionary.

When you write:
user.name

--> Python calls:
Field.__get__(user, User)  # Returns: user.__dict__['name']

--> __set__ method
def __set__(self, instance, value):
  instance.__dict__[self.name] = value

What it does: Stores the value in instance's dictionary

When you write:
user.name = "Alice"

--> Python calls:
Field.__set__(user, "Alice")  # Stores: user.__dict__['name'] = "Alice"

# Descriptor Flow:
Class Definition:
 class User(Model):
   name = CharField(100) <- Creates descriptor

Intance Creation:
  user = User(name = "Alice")

Attribute Access:
  user.name <- Triggers __get__  <- Returns "Alice"

Attribute Assignment:
  user.name = "Bob" <- Triggers __set__  <- Stores "Bob"

# MetaClass - Tha Class Factory
class ModelMeta(type):
  def __new__(cls, name, bases, attrs)

What is a Metaclass? A class that create classes.

--> Regular class:
class User:  # type() creates this class
  pass

--> Metaclass:
class ModelMeta(type):  # custom class creater
  pass

class user(Model):  # ModelMeta creates this class
  pass

--> Metaclass Flow:
1. Python sees: class User(Model):
2. Python calls: ModelMeta.__new__(metaclass, 'User', (Model,), {...})
3. Metaclass modifies the class before it's created
4. Returns the final class
   

What you write:
class User(Model):
  name = CharField(100)
  email = CharField(255)
  age = IntegerField()

What metaclass does:
1. Collects fields: {'name': CharField, 'email': CharField, 'age': IntegerField}
2. Adds __fields = {'name': CharField, 'emai': CharField, 'age': IntegerField}
3. Adds_table = 'user'
4. Creates class with these attributes

--> Resulting class internally:
class User:
  __fields = {'name': CharField, 'email': CharField, 'age': IntegerField}
  _table = 'user'
  name = CharField(100)
  email = CharField(255)
  age = IntegerField()

What **kwargs does:
--> When you create:
user = user(name = "Alice", email="alice@gmail.com", age=30)

--> kwargs becomes:
kwargs = {'name': 'Alice', 'email': 'alice@gmail.com', 'age': 30}

--> Loop sets:
setattr(self, 'name', 'Alice')
setattr(self, 'email', 'alice@gmail.com')
setattr(self, 'age', 30)

# SQL Generation Example:
--> For user class:
columns = [
    "id integer primary key autoincrement",
    "name varchar(100)",
    "email varchar(255)", 
    "age integer"
]

--> Generated SQL:
"""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    email VARCHAR(255),
    age INTEGER
)
"""

# Filter Examples:
--> Simple filter:
User.filter(age=25)
 --> SQL: SELECT * FROM user WHERE age = 25

--> GTE (Greater Than or Equal):
User.filter(age__gte=25)
 --> SQL: SELECT * FROM user where age >= 25

--> Multiple conditions:
User.filter(name="Alice", age_gte=25)
 --> SQL: SELECT * FROM user where name = 'Alice' AND age >= 25

# Complete Workflow 

### Phase Definition (when python starts)
1. Python reads: class user(Model):
2. Modelmeta.__new__ is called
3. collects all Field instances (name, email, age)
4. Adds _fields = {'name': CharField, 'email': CharField, 'age': IntegerField}
5. Adds _table = 'user'
6. Returns configures User class

### Phase 2: Table Creation
1. User.create_table() is called
2. Builds SQL: CREATE TABLE IF NOT EXISTS user (...)
3. Executes SQL via cursor.executes()
4. Table created in database.db


### Phase 3: Object Creation & Save
1. u1 = User(name = 'Padma', 'email = 'padma@gmail.com', age = 20)
2. Mode.__init__ receives kwargs
3. For each field in __fields: setattr(self, 'name', 'Padma')
4. Descriptor __set__ stores values in instance.__dict__
5. u1.save() called
6. Builds INSERT SQL qith placeholders
7. cursor.execute(sql, values) - SAFE from SQL injection
8. conn.commit() - Permanenetly saves to disk

### Phase 4: Querying
1. User.filter(age_gte=20) called
2. Detects __gte operator in key
3. Builds WHERE clause: age >= ?
4. Executes: SELECT * FROM user WHERE age >= 20
5. Returns raw rows as tuples

