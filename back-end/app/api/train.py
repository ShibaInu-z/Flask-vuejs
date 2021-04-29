""" 暂不管返回的进度，先实现开启训练"""
import json
import re
from flask import request, jsonify, url_for,g
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request

import os
import logging
# from app.dl_and_ml_engine import dl_train_mode 获取数据的函数，暂不需
from app.models import TrainRecord
#from app.utils.data_utils import  write_to_args, read_args_from_ini, get_spark_logs#spark大数据端的内容，暂不会

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""开启训练"""
@bp.route("/train/", methods=["POST"])
@token_auth.login_required
def train_mode():
    """开启训练，返回开启训练信号"""
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    model_type = data.get('model_type')
    name = data.get('name')
    if model_type=='dl':
        return jsonify('开启训练!')
    
"""暂不需要"""
@bp.route("//mldl/inference/", methods=["POST"])
@token_auth.login_required
def inference_mode():
    return jsonify('Pong!')

"""训练进度"""
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
    logs,log_url = get_spark_logs(app_name,utc_str) #问题

    train_record.user_id = g.current_user.id
    train_record.logs = log_url
    record_search = TrainRecord.query.filter_by(utc_str=utc_str).first()
    if not record_search and train_record.logs!='':
        db.session.add(train_record)#首次的话，便创建训练记录表
        db.session.commit()  # 更新表格
    return logs
