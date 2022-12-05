from flask import Flask, render_template, request, jsonify, session
import pymysql

app = Flask(__name__)


#  튜플에서 딕셔너리로 cursor= db.cursor(pymysql.cursors.DictCursor)

# db 연결
# 참고 - https://problem-solving.tistory.com/10
# 참고 - https://shanepark.tistory.com/64

def get_pet_image(user_id):
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
        return 'none'
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
        profile_image = get_pet_image(session['user_id'])
        print(profile_image)
        return render_template('index.html', component_name='login', pet_image=profile_image)
    else:
        return render_template('index.html', component_name='logout')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('/components/modal.html', component_name='logout')
    else:
        id_receive = request.form["id_give"]
        pw_receive = request.form["pw_give"]
        result = login_user(id_receive, pw_receive)
        if result == 'success':
            return jsonify({'msg': 'success'})
        else:
            return jsonify({'msg': 'fail'})


@app.route('/logout', methods=["GET"])
def logout():
    session['logged_in'] = False
    return render_template('index.html', component_name='logout')


@app.route('/join', methods=["GET", "POST"])
def login_post():
    if request.method == 'GET':
        return render_template('/components/modal.html', component_name='join')
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    em_receive = request.form['em_give']
    pet_type_receive = request.form['pet_type_give']
    pet_name_receive = request.form['pet_name_give']
    pet_introduce_receive = request.form['pet_introduce_give']
    pet_image_receive = request.form['pet_image_src']
    insert_user(id_receive, pw_receive, em_receive)
    insert_pet(id_receive, pet_type_receive, pet_name_receive, pet_introduce_receive, pet_image_receive)
    return jsonify({'msg': 'join_ok'})


@app.route('/mypage', methods=["GET"])
def mypage():
    return render_template('/components/mypage.html')


@app.route('/check_id', methods=["POST"])
def get_id():
    id_receive = request.form['id_give']
    result = find_user(id_receive)
    return jsonify({'msg': result})


# 서버실행
if __name__ == '__main__':
    app.secret_key = "15481245"
    app.run(host='127.0.0.1', port=8000)
