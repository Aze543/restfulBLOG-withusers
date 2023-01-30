from flask import Flask, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime as dt
from flask_gravatar import Gravatar
import smtplib

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


not_logged = None
user_state = None
msg = None
exist = None
out = True
in_reg = True
in_log = None
admin = False
admin_key = 'sha256$spnxIb3I$f8a0bd8e52b1679e3f7a4dc0b6b68bf8ea03b6a0b460b3ddd625844eb4cb9ba3'
user_in = None
first = None
user_name = ""
msg_sent = None


def arrange(data):
    db = sqlite3.connect("posts.db")
    cursor = db.cursor()
    ilist = []
    n = 1
    for num in range(1, len(data) * 2):
        for item in data:
            if item[0] == num:
                if not item[0] in ilist:
                    cursor.execute(f"""UPDATE blog_post SET id = '{n}' WHERE id = {item[0]}""")
                    db.commit()
                    ilist.append(n)
                    n += 1
##WTForm


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterBlogForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginBlogForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")


# db = sqlite3.connect("posts.db")
# cursor = db.cursor()
# cursor.execute("""DELETE FROM users WHERE id = 4""")
# cursor.execute("CREATE TABLE comments (id INTEGER PRIMARY KEY, "
#                "title varchar(250) NOT NULL, comment varchar(250) NOT NULL, name varchar(250) NOT NULL)")
# db.commit()

#routes
@app.route('/')
def get_all_posts():
    global user_state, not_logged, in_reg, out, exist, msg, admin, in_log, user_in, user_name, msg_sent
    if user_state:
        if admin:
            not_logged = True
            exist = False
            in_reg = False
            in_log = False
            out = False
            msg_sent = False
            db = sqlite3.connect("posts.db")
            cursor = db.cursor()
            data = cursor.execute("SELECT * from blog_post").fetchall()
            print(data)
            print(user_state)
            return render_template("index.html", all_posts=data, logged=not_logged, out=out, admin=admin, user=user_in)
        else:
            not_logged = True
            exist = False
            in_reg = False
            in_log = False
            out = False
            msg_sent = False
            db = sqlite3.connect("posts.db")
            cursor = db.cursor()
            data = cursor.execute("SELECT * from blog_post").fetchall()
            print(data)
            print(user_state)
            return render_template("index.html", all_posts=data, logged=not_logged, out=out, in_reg=in_reg,
                                   in_log=in_log,
                                   user=user_in)
    else:
        not_logged = False
        msg = None
        exist = None
        out = True
        in_reg = False
        msg_sent = False
        db = sqlite3.connect("posts.db")
        cursor = db.cursor()
        data = cursor.execute("SELECT * from blog_post").fetchall()
        print(data)
        print(user_state)
        return render_template("index.html", all_posts=data, logged=not_logged, out=out, in_reg=in_reg)


@app.route("/post/<int:index>", methods=["GET", "POST"])
def show_post(index):
    global user_state, not_logged, in_reg, out, exist, msg, admin, first, user_in, user_name, msg_sent
    comment_form = CommentForm()
    requested_post = None
    msg_sent = False
    db = sqlite3.connect("posts.db")
    cursor = db.cursor()
    if comment_form.validate_on_submit():
        if user_state:
            data = cursor.execute("SELECT * from blog_post").fetchall()
            for blog_post in data:
                if blog_post[0] == index:
                    requested_post = blog_post
            data = cursor.execute("SELECT * from comments").fetchall()
            if admin:
                img = 'https://i.pinimg.com/736x/ce/c9/0b/cec90bbe5ddf994043f722371879ce35.jpg'
                cursor.execute(
                    f"""INSERT INTO comments VALUES(
                                            '{len(data) + 1}', '{requested_post[1]}', '{comment_form.comment.data}', 
                                            '{user_name}', '{img}'
                                            )"""
                )
                db.commit()
                return redirect(url_for('show_post', index=index))
            cursor.execute(
                f"""INSERT INTO comments VALUES(
                            '{len(data) + 1}', '{requested_post[1]}', '{comment_form.comment.data}', 
                            '{user_name}', '{'https://picsum.photos/200'}'
                            )"""
            )
            db.commit()
            return redirect(url_for('show_post', index=index))
        else:
            first = True
            return redirect(url_for('register'))
    data = cursor.execute("SELECT * from blog_post").fetchall()
    for blog_post in data:
        if blog_post[0] == index:
            requested_post = blog_post
    clist = []
    comment_list = cursor.execute("SELECT * from comments").fetchall()
    for item in comment_list:
        if item[1] == requested_post[1]:
            clist.append(item)
    print(clist)
    return render_template("post.html", post=requested_post, admin=admin, in_reg=in_reg, logged=not_logged, out=out,
                           in_log=in_log, form=comment_form, user=user_in, comments=clist, num=len(clist))


@app.route('/new-post', methods=["GET", "POST"])
def add_post():
    global user_state, not_logged, in_reg, out, exist, msg, admin, msg_sent
    if admin:
        not_logged = True
        exist = False
        in_reg = False
        out = False
        msg_sent = False
        create_post_form = CreatePostForm()
        if create_post_form.validate_on_submit():
            now = dt.datetime.now()
            date_today = now.strftime("%B %d, %Y")
            db = sqlite3.connect("posts.db")
            cursor = db.cursor()
            data = cursor.execute("SELECT * from blog_post").fetchall()
            arrange(data)
            cursor.execute(
                f"""INSERT INTO blog_post VALUES(
                '{len(data) + 1}', '{create_post_form.title.data}', '{date_today}', '{create_post_form.body.data}', 
                '{create_post_form.author.data}', '{create_post_form.img_url.data}', '{create_post_form.subtitle.data}'
                )"""
            )
            db.commit()
            data = cursor.execute("SELECT * from blog_post").fetchall()
            return render_template("index.html", all_posts=data,  in_reg=in_reg, logged=not_logged,
                                   out=out, in_log=in_log, admin=admin)

        return render_template("make-post.html", form=create_post_form, in_reg=in_reg, logged=not_logged, out=out,
                               exist=exist, in_log=in_log, admin=admin)
    else:
        return "<p>You don't have access to this site.</p>"


@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    global user_state, not_logged, in_reg, out, exist, msg, admin, msg_sent
    requested_post = None
    msg_sent = False
    db = sqlite3.connect("posts.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * from blog_post").fetchall()
    if admin:
        for blog_post in data:
            if blog_post[0] == post_id:
                requested_post = blog_post
        create_post_form = CreatePostForm(
            title=requested_post[1],
            subtitle=requested_post[6],
            img_url=requested_post[5],
            author=requested_post[4],
            body=requested_post[3]
        )
        if create_post_form.validate_on_submit():
            requested_post = None
            data = cursor.execute("SELECT * from blog_post").fetchall()
            arrange(data)
            for blog_post in data:
                if blog_post[0] == post_id:
                    requested_post = blog_post
            cursor.execute(f"""UPDATE blog_post SET 
            title = '{create_post_form.title.data}',
            subtitle = '{create_post_form.subtitle.data}',
            img_url = '{create_post_form.img_url.data}',
            author = '{create_post_form.author.data}',
            body = '{create_post_form.body.data}'
            WHERE id = {requested_post[0]}"""
                           )
            db.commit()
            data = cursor.execute("SELECT * from blog_post").fetchall()
            return render_template("index.html", all_posts=data, in_reg=in_reg, logged=not_logged,
                                   out=out, in_log=in_log, admin=admin)
        return render_template("make-post.html", form=create_post_form, edit=True, logged=not_logged, admin=admin)
    else:
        return "<p>You don't have access to this site.</p>"


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    global msg_sent
    requested_post = None
    msg_sent = False
    db = sqlite3.connect("posts.db")
    cursor = db.cursor()
    data = cursor.execute("SELECT * from blog_post").fetchall()
    for blog_post in data:
        if blog_post[0] == post_id:
            requested_post = blog_post
    cursor.execute(f"""DELETE FROM blog_post WHERE id = {requested_post[0]}""")
    db.commit()
    data = cursor.execute("SELECT * from blog_post").fetchall()
    arrange(data)
    data = cursor.execute("SELECT * from blog_post").fetchall()
    return render_template("index.html", all_posts=data)


@app.route('/register', methods=["GET", "POST"])
def register():
    global user_state, msg, exist, in_reg, out, not_logged, in_log, first, user_in, msg_sent
    not_logged = True
    in_reg = True
    in_log = False
    msg_sent = False
    register_form = RegisterBlogForm()
    if register_form.validate_on_submit():
        first = False
        db = sqlite3.connect('posts.db')
        cursor = db.cursor()
        data = cursor.execute("SELECT * from users").fetchall()
        if len(data) > 0:
            arrange(data)
        phash = generate_password_hash(register_form.password.data, method='sha256', salt_length=8)
        for item in data:
            if register_form.email.data == item[1]:
                exist = True
                msg = False
                return redirect(url_for('login'))
        cursor.execute(f"""INSERT INTO users VALUES(
        '{len(data) + 1}', '{register_form.email.data}', '{phash}', '{register_form.name.data}')"""
                       )
        db.commit()
        user_id = len(data) + 1
        data = cursor.execute("SELECT * from users").fetchall()
        for item in data:
            if item[0] == user_id:
                user_state = True
                user_in = True
        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=register_form, in_reg=in_reg, logged=not_logged, out=out,
                           exist=exist, in_log=in_log, first=first)


@app.route('/login', methods=["GET", "POST"])
def login():
    global user_state, msg, exist, not_logged, admin, admin_key, user_in, first, user_name, in_reg, in_log, msg_sent
    not_logged = True
    in_reg = False
    in_log = True
    first = False
    msg_sent = False
    login_form = LoginBlogForm()
    if login_form.validate_on_submit():
        db = sqlite3.connect('posts.db')
        cursor = db.cursor()
        data = cursor.execute("SELECT * from users").fetchall()
        key = None
        name = ""
        for item in data:
            if login_form.email.data == item[1] and check_password_hash(item[2], login_form.password.data):
                key = True
                name = item[3]
                user_state = True
        if key:
            if login_form.email.data == "eizen.inopia@gmail.com" and check_password_hash(admin_key,
                                                                                         login_form.password.data):
                admin = True
                user_name = "Admin"
                return redirect(url_for('get_all_posts'))
            else:
                user_in = True
                user_name = name
                return redirect(url_for('get_all_posts'))
        else:
            msg = True
            exist = False
            login_form = LoginBlogForm()
            return render_template("login.html", msg=msg, form=login_form, exist=exist, in_reg=in_reg,
                                   logged=not_logged, out=out, in_log=in_log)

    return render_template("login.html", msg=msg, form=login_form, exist=exist, in_reg=in_reg, logged=not_logged,
                           out=out, in_log=in_log)


@app.route('/logout')
def logout():
    global user_state, msg, exist, admin, user_in, msg_sent
    user_state = False
    admin = False
    user_in = False
    msg_sent = False
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    global user_state, msg, exist, not_logged, admin, admin_key, user_in, first, user_name, admin, user_in, msg_sent
    return render_template("about.html", in_reg=in_reg, logged=not_logged,
                           out=out, in_log=in_log, admin=admin, user=user_in)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    global user_state, msg, exist, not_logged, admin, admin_key, user_in, first, user_name, admin, msg_sent, in_log,\
        out, \
        in_reg
    if user_in or admin:
        not_logged = True
        exist = False
        in_reg = False
        out = False
        create_post_form = CreatePostForm()
        if create_post_form.validate_on_submit():
            now = dt.datetime.now()
            title = create_post_form.title.data
            subtitle = create_post_form.subtitle.data
            name = create_post_form.author.data
            date_today = now.strftime("%B %d, %Y")
            img_url = create_post_form.img_url.data
            body = create_post_form.body.data
            my_gmail = "pythonaze543@gmail.com"
            pw_gmail = "dvpqoswxpgyyyznw"
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=my_gmail, password=pw_gmail)
                connection.sendmail(
                    from_addr=my_gmail,
                    to_addrs="eizen.inopia.9@gmail.com",
                    msg=f"Subject: Blog-Inquiry! \n\n"
                        f"title: {title}\n\n"
                        f"subtitle: {subtitle}\n\n"
                        f"name: {name}\n\n"
                        f"date: {date_today}\n\n,"
                        f"image_url: {img_url}\n\n,"
                        f"body(html): {body}\n\n"
                )
            msg_sent = True
            return redirect(url_for("contact", in_reg=in_reg, logged=not_logged, out=out,
                                    exist=exist, in_log=in_log, admin=admin, user=user_in,))

        return render_template("contact.html", form=create_post_form, in_reg=in_reg, logged=not_logged, out=out,
                               exist=exist, in_log=in_log, admin=admin, user=user_in)
    else:
        first = True
        return redirect(url_for('register'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
