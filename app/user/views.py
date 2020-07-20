from flask import jsonify, request, session
# from flask_login import login_user
from flask_jwt_extended import create_access_token
from app import db
from app.models import User
from . import user


@user.route('/register', methods=["POST"])
def register():
    """注册功能"""
    data = request.get_json()

    username = data['username']
    email = data['email']
    password = data['password']

    # 通过邮箱去数据库查询是否存在
    db_email = User.query.filter_by(email=email).first()
    if db_email:
        return jsonify({
            "code": 400,
            "msg": "该邮箱已经注册"
        })

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)

    try:
        db.session.commit()
        return jsonify({"code": 200, "msg": "注册成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "msg": e})
    finally:
        db.session.close()


@user.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email', '')
    password = data.get('password', '')
    # remember_password = data['remember_password']

    if not email or not password:
        return jsonify({"code": 400, "msg": "参数错误"})

    # 通过邮箱查询数据库是否存在
    db_user = User.query.filter_by(email=email).first()
    if db_user:
        if db_user.password == password:
            # login_user(db_user)
            session['userId'] = db_user.userId
            access_token = create_access_token(identity=db_user.userId, expires_delta=False)

            return jsonify({
                "code": 200,
                "msg": "",
                "data": {**db_user.to_dict(), "access_token": access_token}
            })
        else:
            return jsonify({"code": 400, "msg": "密码错误"})

    return jsonify({"code": 404, "msg": "该邮箱未注册"})
