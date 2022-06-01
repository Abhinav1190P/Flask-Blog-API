import requests
import json

def giveOutPosts():
    x = requests.get('https://jsonplaceholder.typicode.com/posts')
    l = x.json()
    for i in l:
        newObj = (i['userId'], i['id'], i['title'], i['body']) 
        print(',')
        print(newObj)


def giveOutUsers():
    j = 0
    x = requests.get('https://jsonplaceholder.typicode.com/users')
    l = x.json()
    for i in l:
        j = j+1
        newObj = (j,
        
        i['name'], i['username'], i['email'], i['phone'], i['website'], i['address']['street'],
        i['address']['suite'], i['address']['city'], i['address']['zipcode'], i['company']['name'],
        i['company']['catchPhrase'],i['company']['bs'],i['address']['geo']['lat'],i['address']['geo']['lng']
        
        ) 
        print(',')
        print(newObj)

def giveOutComments():

    x = requests.get('https://jsonplaceholder.typicode.com/comments')
    l = x.json()
    for i in l:
        newObj = (i['postId'], i['id'], i['name'], i['email'], i['body'])
        print(',')
        print(newObj)



  

#giveOutComments()
#giveOutUsers()
#giveOutPosts()
