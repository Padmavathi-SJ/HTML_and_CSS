from models import User, Post

# Create tables
User.create_table()
Post.create_table()

# Insert user
u1 = User(name = "Alia", email="alia@gmail.com", age=30)
u1.save()

u2 = User(name = "Balia", email="Balia@gmail.com", age=20)
u2.save()

u3 = User(name = "Calia", email="Calia@gmail.com", age=25)
u3.save()


# Insert Port
p1 = Post(title="First Post", author = u2.id)
p1.save()

p2 = Post(title="Second Post", author = u2.id)
p2.save()

p3 = Post(title="Third Post", author = u3.id)
p3.save()

# Query
users = User.filter(age__gte=25).order_by("-name").all()
print(users)

# Lazy loading (reverse relation)
print(u2.posts) # fetch posts of Alia
print(u3.posts) # fetch posts of Calia
