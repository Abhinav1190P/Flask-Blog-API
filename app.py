from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
Bootstrap(app)

SWAGGER_URL ='/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Abhinav's Swagger UI REST Boilerplate"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


db = yaml.load(open('db.yaml'))

# Configure db
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_user',methods=['POST'])
def CREATE_USER():
    obj = request.get_json()

    name = obj['name']
    username = obj['username']
    email = obj['email']
    street = obj['address']['street']
    suite = obj['address']['suite']
    city = obj['address']['city']
    zipcode = obj['address']['zipcode']
    lat = obj['address']['geo']['lat']
    lng = obj['address']['geo']['lng']
    phone = obj['phone']
    website = obj['website']
    companyName = obj['company']['name']
    catchPhrase = obj['company']['catchPhrase']
    bs = obj['company']['bs']

    cur1 = mysql.connection.cursor()

    cur1.execute(
        'INSERT INTO users(name, username, email, phone, website, street, suite, city, zipcode, companyname, catchPhrase, bs, lat, lng) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        (name,username,email,phone,website,street,suite,city,zipcode,companyName,catchPhrase,bs,lat,lng))
    mysql.connection.commit()
    
    return request.data, 200



@app.route('/edit_user_info/<int:id>',methods=['POST'])
def EDIT_USER(id):

    obj = request.get_json()
    cur1 = mysql.connection.cursor()
    
    for key,value in obj.items():
        cur1.execute(
            'UPDATE users SET name = %s WHERE id=%s',(value,id)
        )
        mysql.connection.commit()
   

    return obj,200

@app.route('/delete_user/<int:id>',methods=['DELETE'])
def DEL_USER(id):
    cur1 = mysql.connection.cursor()

    cur1.execute(
        'DELETE FROM users WHERE id = %s',[id]
    )
    mysql.connection.commit()
    return 'done',200


@app.route('/create_post/<int:id>',methods=['POST'])
def CREATE_POST(id):
    obj = request.get_json()
    title = obj['title']
    body = obj['body']

    cur1 = mysql.connection.cursor()

    cur1.execute(
        'INSERT INTO posts(userId, title, body) VALUES (%s,%s,%s)',(id,title,body)
    )
    mysql.connection.commit()
    return 'done',200

@app.route('/edit_post/<int:postid>',methods=['POST'])
def EDIT_POST(postid):
    obj = request.get_json()
    title = obj['title']
    body = obj['body']
    cur1 = mysql.connection.cursor()

    if title != '' and body != '':

        cur1.execute(
        'UPDATE posts SET title = %s, body = %s WHERE id = %s',(title,body,postid)
        )
        mysql.connection.commit()
    elif title == '':
        cur1.execute(
        'UPDATE posts SET body = %s WHERE id = %s',(body,postid)
        )
        mysql.connection.commit()
    elif body == '':
        cur1.execute(
        'UPDATE posts SET title = %s WHERE id = %s',(title,postid)
        )
        mysql.connection.commit()

    return 'done',200

@app.route('/delete_post/<int:postid>',methods=['DELETE'])
def DEL_POST(postid):
    cur1 = mysql.connection.cursor()

    cur1.execute(
        'DELETE FROM posts WHERE id = %s',[postid]
    )
    mysql.connection.commit()
    return 'done',200


@app.route('/create_comment/<int:postid>',methods=['POST'])
def CREATE_COMMENT(postid):
    obj = request.get_json()

    name = obj['name']
    email = obj['email']
    body = obj['body']

    cur1 = mysql.connection.cursor()

    cur1.execute(
        'INSERT INTO comments(postId, name, email, body) VALUES (%s,%s,%s,%s)',(postid,name,email,body)
    )
    mysql.connection.commit()
    return 'done',200

@app.route('/edit_comment/<int:commentid>',methods=['POST'])
def EDIT_COMMENT(commentid):
    obj = request.get_json()
    name = obj['name']
    email = obj['email']
    body = obj['body']

    cur1 = mysql.connection.cursor()

    if name != '' and email != '' and body != '':

        cur1.execute(
        'UPDATE comments SET name = %s, email = %s, body = %s WHERE id = %s',(name,email,body,commentid)
        )
        mysql.connection.commit()

    elif name == '':
        cur1.execute(
        'UPDATE comments SET email = %s, body = "%s" WHERE id = %s',(email,body,commentid)
        )
        mysql.connection.commit()

    elif email == '':
        cur1.execute(
        'UPDATE comments SET name = %s, body = "%s" WHERE id = %s',(name,body,commentid)
        )
        mysql.connection.commit()

    elif body == '':
        cur1.execute(
        'UPDATE comments SET name = %s, email = "%s" WHERE id = %s',(name,email,commentid)
        )
        mysql.connection.commit()

    return 'done',200

@app.route('/delete_comment/<int:commentid>',methods=['DELETE'])
def DEL_COM(commentid):
    cur1 = mysql.connection.cursor()

    cur1.execute(
        'DELETE FROM comments WHERE id = %s',[commentid]
    )
    mysql.connection.commit()
    return 'done',200



if __name__ == '__main__':
    app.run(debug=True)
