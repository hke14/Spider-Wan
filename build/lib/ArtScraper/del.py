import pymongo

from pprint import pprint




connection = pymongo.MongoClient("ds040309.mlab.com", 40309)

db = connection["newsaggregartor"]

db.authenticate("gnr011", "Kalash1")



#category:middle east
category1= db.articles.find({'categorie':'middle-east'})
#category:world
category2= db.articles.find({'categorie':'world'})
#category:sport
category3= db.articles.find({'categorie':'sport'})
#category:arts and technology
category4= db.articles.find({'categorie':'tech'})
#category:business
category5= db.articles.find({'categorie':'business'})
#get five random documents
#random=db.articles.find({'categorie':'middle-east'})
#radom1= random.aggregate([{'$sample': {'size': 5 }}])

category1=db.articles.aggregate([{'$match':{'categorie':"middle-east"}},{'$sample': {'size': 5 }}])
category2=db.articles.aggregate([{'$match':{'categorie':"world"}},{'$sample': {'size': 5 }}])
category3=db.articles.aggregate([{'$match':{'categorie':"sport"}},{'$sample': {'size': 5 }}])
category4=db.articles.aggregate([{'$match':{'categorie':"tech"}},{'$sample': {'size': 5 }}])
category5=db.articles.aggregate([{'$match':{'categorie':"business"}},{'$sample': {'size': 5 }}])

users=db.articles.find({"keywords" : {'$regex' : ".*مانشستر يونايتد.*"}})
for user in users:
 print (user)

#for item in ran:
   # print (item)
