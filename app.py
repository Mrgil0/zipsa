from flask import Flask, render_template, request, jsonify, session
import pymysql

app = Flask(__name__)


#  튜플에서 딕셔너리로 cursor= db.cursor(pymysql.cursors.DictCursor)

# db 연결
# 참고 - https://problem-solving.tistory.com/10
# 참고 - https://shanepark.tistory.com/64

def get_user():
    db = pymysql.connect(host='localhost', user='root', db='zipsa', password='test', charset='utf8')
    curs = db.cursor()

    sql = "select * from user"
    curs.execute(sql)
    rows = curs.fetchall()
    json_str = list(list(rows)[0])
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
        list(list(curs.fetchone()))[0]
    except TypeError:
        return
    session['logged_in'] = True
    db.commit()
    db.close()
    return 'success'


# route
@app.route('/')
def index():
    if session.get('logged_in'):
        return render_template('index.html', component_name='login', posts=get_user())
    else:
        return render_template('index.html', component_name='logout', posts=get_user())


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
    insert_user(id_receive, pw_receive, em_receive)
    return jsonify({'msg': 'join_ok'})


@app.route('/mypage', methods=["GET"])
def mypage():
    return render_template('/components/mypage.html')


@app.route('/check_id', methods=["POST"])
def get_id():
    id_receive = request.form['id_give']
    result = find_user(id_receive)
    return jsonify({'msg': result})


@app.route('/getName', methods=["GET"])
def getName():
    return get_user(), 200


# 서버실행
if __name__ == '__main__':
    app.secret_key = "15481245"
    app.run(host='127.0.0.1', port=8000)
