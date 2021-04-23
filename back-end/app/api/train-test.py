import re
import json
from flask import request, jsonify, url_for,g, current_app
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
# from app.dl_and_ml_engine import dl_train_mode, inference, get_result_train_and_infer
import os
from app.models import User,TrainRecord
# from app.utils.tasks import async_train_mode
from app.dl_and_ml_engine import dl_train_mode
from app.models import TrainRecord

@bp.route("/train/", methods=["POST"])
@token_auth.login_required
def train_mode():
    if g.current_user.get_task_in_progress('train_mode'):  # 如果用户已经有同名的后台任务在运行中时
        return bad_request('您上一个训练的后台任务尚未结束')
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    data_paras = data.get('data_paras')
    model_paras = data.get('model_paras')
    if not data_paras or not model_paras:
        return bad_request('parameters wrong!')

    print(data)
    return jsonify('训练已经开始!')

@bp.route("/get_logs/", methods=["POST"])
@token_auth.login_required
def get_logs():
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    # data_name = data.get('data_name')
    # mode = data.get('mode')
    app_name = data.get('app_name')
    utc_str = data.get('utc_str')
    submit_paras = data.get('submit_paras')

    if not app_name or  not utc_str or not submit_paras:
        return bad_request('app_name,utc_str,submit_paras must be posted.')
    print(app_name,utc_str)
    train_record = TrainRecord()
    train_record.from_json(data)
    logs,log_url = get_spark_logs(app_name,utc_str)

    train_record.user_id = g.current_user.id
    train_record.logs = log_url
    record_search = TrainRecord.query.filter_by(utc_str=utc_str).first()
    if not record_search and train_record.logs!='':
        db.session.add(train_record)#首次的话，便创建训练记录表
        db.session.commit()  # 更新表格
    return logs


@bp.route("/get_results/", methods=["GET"])
@token_auth.login_required
def get_results():
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    data_name = data.get('data_name')
    mode = data.get('mode')
    app_name = data.get('app_name')
    logs = get_logs(app_name)
    return logs