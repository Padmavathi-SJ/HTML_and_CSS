from orm import Model, CharField, IntegerField, ForeignKey

class User(Model):
    name = CharField(100)
    email = CharField(255)
    age = IntegerField()

class Post(Model):
    title = CharField(200)
    author = ForeignKey(User, related_name="posts")
    