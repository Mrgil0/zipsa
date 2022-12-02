from flask import Flask, render_template, request
import pymysql
import json

app = Flask(__name__)


#  튜플에서 딕셔너리로 cursor= db.cursor(pymysql.cursors.DictCursor)

# db 연결
# 참고 - https://problem-solving.tistory.com/10
# 참고 - https://shanepark.tistory.com/64


# route
@app.route('/')
def root():
    return render_template('index.html')


@app.route('/getName', methods=["GET"])
def groupsLayout():
    db = pymysql.connect(host='localhost', user='root', db='zipsa', password='test', charset='utf8')
    curs = db.cursor()

    sql = """select * from user"""
    curs.execute(sql)
    rows = curs.fetchall()
    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    print(json_str)
    db.commit()
    db.close()
    return json_str, 200


# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
