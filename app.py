from flask import Flask, render_template, request, jsonify, session
import pymysql, os

app = Flask(__name__)
app.secret_key = os.urandom(24)


def set_db_password():
    db = pymysql.connect(host='localhost', user='lsi', db='zipsa', password='0000', charset='utf8') # password를 각자 db의 비밀번호에 맞게 변경
    return db


def read_pet_image(user_id):
    db = set_db_password()
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
    db = set_db_password()
    curs = db.cursor()

    sql = "select * from post"
    curs.execute(sql)
    result = curs.fetchall()
    if len(result) == 0:
        return 'empty'
    print(result)
    db.commit()
    db.close()
    return result


def update_post(post_content, post_date, post_id):
    db = set_db_password()
    curs = db.cursor()

    sql = "update post set post_content=%s, post_date=%s where post_id=%s"
    record = (post_content, post_date, post_id)
    curs.execute(sql, record)
    db.commit()
    db.close()


def insert_user(user_id, password,email):
    db = set_db_password()
    curs = db.cursor()

    sql = "insert into user values (%s, %s, %s)"
    record = (user_id, password, email)
    curs.execute(sql, record)
    db.commit()
    db.close()


def insert_pet(user_id, pet_type, pet_name, pet_introduce, pet_image):
    db = set_db_password()
    curs = db.cursor()

    sql = "insert into pet values (%s, %s, %s, %s, %s)"
    record = (user_id, pet_type, pet_name, pet_introduce, pet_image)
    curs.execute(sql, record)
    db.commit()
    db.close()


def find_user(user_id):
    db = set_db_password()
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


def find_posts(text):
    db = set_db_password()
    curs = db.cursor()

    sql = "select * from post where user_id like %s or post_content like %s"
    record = ('%' + text + '%', '%' + text + '%')
    curs.execute(sql, record)
    try:
        result = curs.fetchall()
    except TypeError:
        print('타입 에러')
        return 'fail'
    db.commit()
    db.close()
    return result


def login_user(user_id, password):
    db = set_db_password()
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


def insert_post(user_id, post_content, post_date):
    db = set_db_password()
    curs = db.cursor()
    print(post_date)
    sql = "insert into post values (null, %s, %s,%s)"
    record = (user_id, post_content, post_date)
    curs.execute(sql, record)
    db.commit()
    db.close()


# route
@app.route('/')
def index():
    post = read_posts()
    if session.get('logged_in'):
        profile_image = read_pet_image(session['user_id'])
        return render_template('/components/modal.html', status='login', pet_image=profile_image,
                               posts=post, len=len(post), page="home", user_id=session['user_id'])
    else:
        return render_template('/components/modal.html', status='logout', posts=post, len=len(post), page="home", user_id='')


@app.route('/page/login', methods=["GET"])
def get_login():
    return render_template('/components/modal.html', status='logout')


@app.route('/page/logout', methods=["GET"])
def logout():
    session['logged_in'] = False
    return render_template('/components/modal.html', status='logout', page="home")


@app.route('/page/signup', methods=["GET"])
def get_signup():
    return render_template('/components/modal.html', status='signup')


@app.route('/page/profile', methods=["GET"])
def read_my_profile():
    return render_template('/components/modal.html', page='profile')


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


@app.route('/api/posts', methods=["POST"])
def insert_posts():
    content_receive = request.form['post_give']
    date_receive = request.form['date_give']
    user_id = session['user_id']
    insert_post(user_id, content_receive, date_receive)
    return jsonify({'msg': 'success'})


@app.route('/api/posts', methods=["PUT"])
def modify_posts():
    content_receive = request.form['post_give']
    date_receive = request.form['date_give']
    id_receive = request.form['id_give']
    update_post(content_receive, date_receive, id_receive)
    return jsonify({'msg': 'success'})


@app.route('/posts/search', methods=["GET"])
def search_posts():
    search_receive = request.args.get('search_input')
    post = find_posts(search_receive)
    print(post)
    if session.get('logged_in'):
        profile_image = read_pet_image(session['user_id'])
        return render_template('/components/modal.html', status='login', pet_image=profile_image,
                               posts=post, len=len(post), page="home", user_id=session['user_id'])
    else:
        return render_template('/components/modal.html', status='logout', posts=post, len=len(post), page="home", user_id='')


# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
