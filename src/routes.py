from flask import request, redirect, render_template, make_response, jsonify, abort
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import desc
from datetime import datetime

from .models import Todo, User
from .core import app, db

from .models import add_user, user_login
from .jwt import jwt_encode, jwt_verify


@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        user_id = jwt_verify(request.cookies.get("token"))
    except:
        return redirect("/logout")


    if request.method == 'POST':
        task_content = request.form['content']

        try:
            if not 3 <= len(task_content) <= 200:
                raise ValueError("Incorrect content length!")
            
            new_task = Todo(content=task_content, user_id=user_id)
            db.session.add(new_task)
            db.session.commit()
        except ValueError:
            return abort("Incorrect task content lengts!",422)
        except IntegrityError:
            return redirect("/logout")
        return redirect("/")
    else:
        current_page = request.args.get("page", default=1, type=int)
        if current_page < 1:
            current_page = 1

        
        tasks = Todo.query.order_by(desc(Todo.date_created), Todo.id).where(Todo.user_id == user_id).limit(10).offset((current_page - 1) * 10).all()
        return render_template('index.html', tasks=tasks, page=current_page)

@app.route('/delete/<int:id>')
def delete(id):
    try:
        user_id = jwt_verify(request.cookies.get("token"))
    except:
        return redirect("/logout")


    task_to_delete = Todo.query.get_or_404(id)

    if task_to_delete.user_id != user_id:
        return abort(403, "This task isn't yours!")
    

    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    try:
        user_id = jwt_verify(request.cookies.get("token"))
    except:
        return redirect("/logout")


    task = Todo.query.get_or_404(id)

    if task.user_id != user_id:
        return abort(403, "This task isn't yours!")
    
    if request.method== 'POST':
        task_content = request.form['content']
        
    
        if not 3 <= len(task_content) <= 200:
            return abort("Incorrect task content lengts!",422)
            
        task.content = task_content
        task.date_created = datetime.utcnow()
        db.session.commit()
        return redirect("/")
    
    return render_template('update.html',task=task)



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            new_user = add_user(username, password)
        except ValueError:
            return jsonify({"msg": "incorrect fields length"}), 422
        except IntegrityError:
            return jsonify({"msg": "this user already exists"}), 409

        jwt_token = jwt_encode(new_user.id)

        responce = make_response(jsonify({"msg": "success"}))
        responce.set_cookie("token", jwt_token, httponly=True, samesite="lax")
        return responce, 201
        
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            user = user_login(username, password)
        except ValueError:
            return jsonify({"msg": "incorrect fields length"}), 422
        except NoResultFound, IndentationError:
            return jsonify({"msg": "incorrect user or password"}), 401

        jwt_token = jwt_encode(user.id)
        
        responce = make_response(jsonify({"msg": "success"}))
        responce.set_cookie("token", jwt_token, httponly=True, samesite="lax")
        return responce, 200

    return render_template('login.html')

@app.route('/logout', methods=["GET"])
def logout():
    responce = make_response(redirect("/login"))
    responce.delete_cookie("token")
    return responce