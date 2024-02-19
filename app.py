import flask
import pymysql
from flask import *


app = Flask(__name__)


def getDB():
    #连接数据库
    db = pymysql.connect(user='root',password='root',host='localhost',database='db')
    return db

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/movies')
@app.route('/movies/<int:page>')
def movies(page = 1):
    db = getDB()
    cursor = db.cursor()
    #查询当前电影列表
    sql = "select numberrank,link,first_name,fo_movename,score,num,sumary,first_director from movies limit {},{}".format((page-1)*25,page*25)
    cursor.execute(sql)
    data = cursor.fetchall()
    datalist = []
    for item in data:
        datalist.append(item)

    #查询电影总数
    sql1 = "select count(*) from movies"
    cursor.execute(sql1)
    total = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template('movies.html',page = page,movies=datalist,countnum=int(int(total[0]))/25)

@app.route('/tj')
def tj():
    return render_template('tj.html')

if __name__ == '__main__':
    app.run()