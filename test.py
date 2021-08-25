from web_blog import db,User
db.create_all()
user1 = User(username = "bob", email = "bob@gmail.com", password = "bob123")
user2 = User(username = "marty", email = "marty@gmail.com", password = "marty123")

db.session.add(user1)
db.session.add(user2)
db.session.commit()