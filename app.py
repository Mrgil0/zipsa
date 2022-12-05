from flask import Flask, render_template, request, jsonify, session
import pymysql

app = Flask(__name__)


def read_pet_image(user_id):
    db = pymysql.connect(host='localhost', user='root', db='zipsa', password='test', charset='utf8')
    curs = db.cursor()

    sql = "select pet_image from pet where user_id = (%s)"
    record = user_id
    curs.execute(sql, record)
    rows = curs.fetchall()
    try:
        json_str = list(list(rows)[0])
    except IndexError:
        print('인덱스 에러')
        return 'no image'
    db.commit()
    db.close()
    return json_str


def read_posts():
    db = pymysql.connect(host='localhost', user='root', db='zipsa', password='test', charset='utf8')
    curs = db.cursor()

    sql = "select * from post"
    curs.execute(sql)
    result = curs.fetchall()
    if len(result) is 0 :
        return 'empty'
    db.commit()
    db.close()
    return result


def insert_user(user_id, password, email):
    db = pymysql.connect(host='localhost', user='root', db='zipsa', password='test', charset='utf8')
    curs = db.cursor()

    sql = "insert into user values (%s, %s, %s)"
    record = (user_id, password, email)
    curs.execute(sql, record)
    db.commit()
    db.close()


def insert_pet(user_id, pet_type, pet_name, pet_introduce, pet_image):
    db = pymysql.connect(host='localhost', user='root', db='zipsa', password='test', charset='utf8')
    curs = db.cursor()

    sql = "insert into pet values (%s, %s, %s, %s, %s)"
    record = (user_id, pet_type, pet_name, pet_introduce, pet_image)
    curs.execute(sql, record)
    db.commit()
    db.close()


def find_user(user_id):
    db = pymysql.connect(host='localhost', user='root', db='zipsa', password='test', charset='utf8')
    curs = db.cursor()

    sql = "select user_id from user where user_id = (%s)"
    record = user_id
    curs.execute(sql, record)
    try:
        result = list(list(curs.fetchone()))[0]
    except TypeError:
        print('타입 에러')
        return 'fail'
    db.commit()
    db.close()
    return result


def login_user(user_id, password):
    db = pymysql.connect(host='localhost', user='root', db='zipsa', password='test', charset='utf8')
    curs = db.cursor()

    sql = "select * from user where user_id = (%s) and password = (%s)"
    record = (user_id, password)
    curs.execute(sql, record)
    try:
        result = list(list(curs.fetchone()))[0]
    except TypeError:
        return
    session['user_id'] = result
    session['logged_in'] = True
    db.commit()
    db.close()
    return 'success'


# route
@app.route('/')
def index():
    if session.get('logged_in'):
        profile_image = read_pet_image(session['user_id'])
        post = read_posts()
        return render_template('index.html', component_name='login', pet_image=profile_image, posts=post, len=len(post))
    else:
        return render_template('index.html', component_name='logout')


@app.route('/page/login', methods=["GET"])
def get_login():
    return render_template('/components/modal.html', component_name='logout')


@app.route('/page/logout', methods=["GET"])
def logout():
    session['logged_in'] = False
    return render_template('index.html', component_name='logout')


@app.route('/page/singup', methods=["GET"])
def get_signup():
    return render_template('/components/modal.html', component_name='singup')


@app.route('/page/profile', methods=["GET"])
def read_my_profile():
    return render_template('/components/profile.html')


@app.route('/api/login', methods=["POST"])
def read_user():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]
    result = login_user(id_receive, pw_receive)
    if result == 'success':
        return jsonify({'msg': 'success'})
    else:
        return jsonify({'msg': 'fail'})


@app.route('/api/singup', methods=["POST"])
def login_post():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    em_receive = request.form['em_give']
    pet_type_receive = request.form['pet_type_give']
    pet_name_receive = request.form['pet_name_give']
    pet_introduce_receive = request.form['pet_introduce_give']
    pet_image_receive = request.form['pet_image_src']
    insert_user(id_receive, pw_receive, em_receive)
    insert_pet(id_receive, pet_type_receive, pet_name_receive, pet_introduce_receive, pet_image_receive)
    return jsonify({'msg': 'success'})


@app.route('/api/checkid', methods=["POST"])
def get_id():
    id_receive = request.form['id_give']
    result = find_user(id_receive)
    return jsonify({'msg': result})


# 서버실행
if __name__ == '__main__':
    app.secret_key = "15481245"
    app.run(host='127.0.0.1', port=8000)
