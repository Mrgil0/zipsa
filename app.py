import os
from math import ceil

import pymysql
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = os.urandom(24)


def set_db_password():
    db = pymysql.connect(host='localhost', user='lsi', db='zipsa', password='0000',
                         charset='utf8')  # password를 각자 db의 비밀번호에 맞게 변경
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

    sql = "select * from post ORDER BY post_date desc"
    curs.execute(sql)
    result = curs.fetchall()
    if len(result) == 0:
        return ''
    db.commit()
    db.close()
    return result


def read_replies():
    db = set_db_password()
    curs = db.cursor()

    sql = "select * from reply"
    curs.execute(sql)
    result = list(curs.fetchall())
    if len(result) == 0:
        return ''
    print(result)
    db.commit()
    db.close()
    return result


def read_my_posts(user_id, cur_page):
    db = set_db_password()
    curs = db.cursor()

    sql = "select * from post where user_id=%s LIMIT %s, %s"
    try:
        min_num = (int(cur_page)-1) * 5
    except TypeError:
        min_num = 0
    record = (user_id, min_num, int(cur_page)*5)
    curs.execute(sql, record)
    result = curs.fetchall()
    if len(result) == 0:
        return ''
    db.commit()
    db.close()
    return result
    # 글의 총 갯수 13개
    # 한 페이지당 5개라면
    # 페이지의 총 갯수는 13/5 2.6 -> 3개 (아래의 get_page_num)
    # 클릭한 페이지가 1이면 LIMIT 0, 5 / 2라면 LIMIT 5, 10 (0을 곱하면 오류가 생겨서 예외처리함)
    # 페이지에 맞는 글 리스트가 return됨


def get_page_num(post):
    if len(post) == 0:
        return
    page_num = ceil(len(post) / 5)
    return page_num


def read_one_post(post_id):
    db = set_db_password()
    curs = db.cursor()

    sql = "select * from post where post_id=%s"
    curs.execute(sql, post_id)
    result = curs.fetchall()
    if len(result) == 0:
        return ''
    db.commit()
    db.close()
    return result


def read_my_all_posts(user_id):
    db = set_db_password()
    curs = db.cursor()

    sql = "select * from post where user_id=%s"
    curs.execute(sql, user_id)
    result = curs.fetchall()
    if len(result) == 0:
        return ''
    db.commit()
    db.close()
    return result


def read_user(user_id):
    db = set_db_password()
    curs = db.cursor()

    sql = "select u.user_id, pet_image FROM user u, pet p WHERE u.user_id = %s AND u.user_id = p.user_id"
    curs.execute(sql, user_id)
    result = curs.fetchall()
    db.commit()
    db.close()
    return result


def read_pet(user_id):
    db = set_db_password()
    curs = db.cursor()

    sql = "select * from pet where user_id = %s"
    curs.execute(sql, user_id)
    result = curs.fetchall()
    db.commit()
    db.close()
    return result


def update_user(user_id, password, email):
    db = set_db_password()
    curs = db.cursor()

    sql = "update user set password=%s, email=%s where user_id=%s"
    record = (password, email, user_id)
    curs.execute(sql, record)
    db.commit()
    db.close()


def update_pet(user_id, pet_type, pet_name, pet_introduce, pet_image):
    db = set_db_password()
    curs = db.cursor()

    sql = "update pet set pet_type=%s, pet_name=%s, pet_introduce=%s, pet_image=%s where user_id=%s"
    record = (pet_type, pet_name, pet_introduce, pet_image, user_id)
    curs.execute(sql, record)
    db.commit()
    db.close()


def update_post(post_content, post_date, post_id):
    db = set_db_password()
    curs = db.cursor()

    sql = "update post set post_content=%s, post_date=%s where post_id=%s"
    record = (post_content, post_date, post_id)
    curs.execute(sql, record)
    db.commit()
    db.close()


def insert_user(user_id, password, email):
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


def insert_post(user_id, post_content, post_date):
    db = set_db_password()
    curs = db.cursor()
    sql = "insert into post values (null, %s, %s,%s)"
    record = (user_id, post_content, post_date)
    curs.execute(sql, record)
    db.commit()
    db.close()


def insert_reply(post_id, user_id, reply_content, reply_date):
    db = set_db_password()
    curs = db.cursor()

    sql = "insert into reply values (null, %s, %s, %s,%s)"
    record = (post_id, user_id, reply_content, reply_date)
    curs.execute(sql, record)
    db.commit()
    db.close()


def find_user_id(user_id):
    db = set_db_password()
    curs = db.cursor()

    sql = "select user_id from user where user_id = (%s)"
    record = user_id
    curs.execute(sql, record)
    try:
        result = list(list(curs.fetchone()))[0]
    except TypeError:
        print('타입 에러')
        return 'success'
    db.commit()
    db.close()
    return result


def find_user_pw(user_id, password):
    db = set_db_password()
    curs = db.cursor()

    sql = "select password from user where user_id = %s and password = %s"
    record = (user_id, password)
    curs.execute(sql, record)
    try:
        result = list(list(curs.fetchone()))
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


def select_user(user_id, password):
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

def delete_post(post_id):
    db = set_db_password()
    curs = db.cursor()

    sql = "delete from post where post_id = (%s)"
    curs.execute(sql, post_id)
    db.commit()
    db.close()
    return 'success'

def get_session_id():
    user_id = session['user_id']
    return user_id
    # 로그인 시 담은 아이디 return


# ------------------------------------ 함수 구분 ---------------------------------------------#
@app.route('/')
def index():
    post = read_posts()
    reply = read_replies()
    if session.get('logged_in'):
        user_id = get_session_id()
        profile_image = read_pet_image(user_id)
        return render_template('/components/modal.html', status='login', pet_image=profile_image, posts=post, page="home", user_id=user_id, replies=reply)
    else:
        return render_template('/components/modal.html', status='logout', posts=post, page="home", user_id='', replies=reply)


@app.route('/page/login', methods=["GET"])
def get_login():
    return render_template('/components/modal.html', status='logout')


@app.route('/page/logout', methods=["GET"])
def logout():
    post = read_posts()
    session['logged_in'] = False
    return render_template('/components/modal.html', status='logout', page="home", posts=post)


@app.route('/page/signup', methods=["GET"])
def get_signup():
    return render_template('/components/modal.html', status='signup')


@app.route('/page/profile/user', methods=["GET"])
def read_my_profile_user():
    user_id = get_session_id()
    user = read_user(user_id)
    pet = read_pet(user_id)
    profile_image = read_pet_image(user_id)
    if request.args.get('result') == 'true':
        return render_template('/components/modal.html', page='profile/user', toggle='user', password_chk=True, users=user, pets=pet, status='login', pet_image=profile_image)
    else:
        return render_template('/components/modal.html', page='profile/user', toggle='user', password_chk=False, status='login', pet_image=profile_image)


@app.route('/page/profile/post', methods=["GET"])
def read_my_profile_post():
    cur_page = request.args.get('page')
    user_id = get_session_id()
    cur_post = read_my_posts(user_id, cur_page)
    posts = read_my_all_posts(user_id)
    max_page = get_page_num(posts)
    profile_image = read_pet_image(user_id)
    reply = read_replies()
    return render_template('/components/modal.html', page='profile/post', toggle='post', posts=cur_post, max_page=max_page, cur_page=cur_page, pet_image=profile_image, replies=reply)


@app.route('/posts/search', methods=["GET"])
def search_posts():
    search_receive = request.args.get('search_input')
    post = find_posts(search_receive)
    if session.get('logged_in'):
        profile_image = read_pet_image(session['user_id'])
        return render_template('/components/modal.html', status='login', pet_image=profile_image,
                               posts=post, page="home", user_id=session['user_id'])
    else:
        return render_template('/components/modal.html', status='logout', posts=post, page="home",
                               user_id='')


@app.route('/api/users/login', methods=["POST"])
def login_user():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]
    result = select_user(id_receive, pw_receive)
    if result == 'success':
        return jsonify({'msg': 'success'})
    else:
        return jsonify({'msg': 'fail'})


@app.route('/api/users/signup', methods=["POST"])
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


@app.route('/api/user/modify', methods=["PUT"])
def modify_user():
    user_id = get_session_id()
    pw_receive = request.form['pw_give']
    em_receive = request.form['em_give']
    pet_type_receive = request.form['pet_type_give']
    pet_name_receive = request.form['pet_name_give']
    pet_introduce_receive = request.form['pet_introduce_give']
    pet_image_receive = request.form['pet_image_src']
    update_user(user_id, pw_receive, em_receive)
    update_pet(user_id, pet_type_receive, pet_name_receive, pet_introduce_receive, pet_image_receive)
    return jsonify({'msg': 'success'})


@app.route('/api/checkid', methods=["POST"])
def get_id():
    id_receive = request.form['data_give']
    result = find_user_id(id_receive)
    return jsonify({'msg': result})


@app.route('/api/checkpw', methods=["POST"])
def get_password():
    password_receive = request.form['data_give']
    user_id = get_session_id()
    result = find_user_pw(user_id, password_receive)
    return jsonify({'msg': result})


@app.route('/api/posts', methods=["POST"])
def insert_posts():
    content_receive = request.form['post_give']
    date_receive = request.form['date_give']
    user_id = get_session_id()
    insert_post(user_id, content_receive, date_receive)

    return jsonify({'msg': 'success'})


@app.route('/api/replies', methods=["POST"])
def insert_replies():
    reply_receive = request.form['reply_give']
    date_receive = request.form['date_give']
    id_receive = request.form['id_give']
    user_id = get_session_id()
    insert_reply(id_receive, user_id, reply_receive, date_receive)
    return jsonify({'msg': 'success'})


@app.route('/api/posts', methods=["PUT"])
def modify_posts():
    content_receive = request.form['post_give']
    date_receive = request.form['date_give']
    id_receive = request.form['id_give']
    update_post(content_receive, date_receive, id_receive)
    return jsonify({'msg': 'success'})


@app.route('/api/posts', methods=["DELETE"])
def remove_post():
    post_receive = request.form['post_give']
    delete_post(post_receive)
    print("삭제되었습니다.")
    return jsonify({'msg': 'deleted'})


# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)


