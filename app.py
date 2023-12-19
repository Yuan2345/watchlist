import os
import sys

from flask import Flask, render_template,request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        date = request.form.get('date')
        country= request.form.get('country')
        type = request.form.get('type')

        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, date=date,country=country,type=type)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页


    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html',  movies=movies)

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    date = db.Column(db.String(15))  # 电影年份
    country = db.Column(db.String(20)) #电影国家
    type = db.Column(db.String(20))#类型
    year = db.Column(db.String(4))

import click


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Yuan2345'
    movies = [
        {'title': '战狼2', 'date': '2017/7/27','country':'中国','type':'战争','year':'2017'},
        {'title': '哪吒之魔童降世', 'date': '2019/7/26','country':'中国','type':'动画','year':'2019'},
        {'title': '流浪地球', 'date': '2019/2/5', 'country': '中国', 'type': '科幻', 'year': '2019'},
        {'title': '复仇者联盟4', 'date': '2019/4/24', 'country': '美国', 'type': '科幻', 'year': '2019'},
        {'title': '红海行动', 'date': '2018/2/16', 'country': '中国', 'type': '战争', 'year': '2018'},
        {'title': '唐人街探案2', 'date': '2018/2/16', 'country': '中国', 'type': '喜剧', 'year': '2018'},
        {'title': '我不是药神', 'date': '2018/7/5', 'country': '中国', 'type': '喜剧', 'year': '2018'},
        {'title': '中国机长', 'date': '2019/9/30', 'country': '中国', 'type': '剧情', 'year': '2019'},
        {'title': '速度与激情8', 'date': '2017/4/14', 'country': '美国', 'type': '动作', 'year': '2017'},
        {'title': '西虹市首富', 'date': '2018/7/27', 'country': '中国', 'type': '喜剧', 'year': '2018'},
        {'title': '复仇者联盟3', 'date': '2018/5/11', 'country': '美国', 'type': '科幻', 'year': '2018'},
        {'title': '捉妖记', 'date': '2018/2/16', 'country': '中国', 'type': '喜剧', 'year': '2018'},
        {'title': '八佰', 'date': '2020/8/21', 'country': '中国', 'type': '战争', 'year': '2020'},
        {'title': '姜子牙', 'date': '2020/10/01', 'country': '中国', 'type': '动画', 'year': '2020'},
        {'title': '我和我的家乡', 'date': '2020/10/01', 'country': '中国', 'type': '剧情', 'year': '2020'},
        {'title': '你好，李焕英', 'date': '2021/2/12', 'country': '中国', 'type': '喜剧', 'year': '2021'},
        {'title': '长津湖', 'date': '2021/9/20', 'country': '中国', 'type': '战争', 'year': '2021'},
        {'title': '速度与激情9', 'date': '2021/5/21', 'country': '美国', 'type': '动作', 'year': '2021'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], date=m['date'],country=m['country'],type=m['type'],year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页

