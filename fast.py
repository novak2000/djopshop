from djop import db
from djop.models import Product,User,Category

c1 = Category(name='voce', parentCategory=0)
c2 = Category(name='povrce', parentCategory=0)
c3 = Category(name='slatkisi', parentCategory=0)
c4 = Category(name='meso', parentCategory=0)

db.session.add(c1)
db.session.add(c2)
db.session.add(c3)
db.session.add(c4)
db.session.commit()

c1 = Category(name='cokolada', parentCategory=3)
c2 = Category(name='sladoled', parentCategory=3)
c3 = Category(name='bombone', parentCategory=3)
c4 = Category(name='keks', parentCategory=3)

db.session.add(c1)
db.session.add(c2)
db.session.add(c3)
db.session.add(c4)
db.session.commit()

p1 = Product(name='pile',price=8, description='sveze pile',category=4)
p2 = Product(name='jagnje',price=84, description='sveze jagnje',category=4)
p3 = Product(name='prase',price=85, description='sveze prase',category=4)
p4 = Product(name='sunka',price=88, description='sveza sunka',category=4)
p5 = Product(name='curetina',price=800, description='sveza curetina',category=4)

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.commit()

p1 = Product(name='milka noisete 100g',price=90, description='milka cokolada ukusno mnjam mnjam',category=5)
p2 = Product(name='sladoled cokolada frikom',price=84, description='svez sladoled liz liz',category=6)
p3 = Product(name='banane',price=85, description='sveze banane',category=1)
p4 = Product(name='jabuke',price=88, description='sveze jabuke',category=1)
p5 = Product(name='kruske',price=800, description='sveze kruske',category=1)

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.commit()