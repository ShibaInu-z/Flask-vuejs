from flask import jsonify
from app.api import bp


@bp.route('/train', methods=['GET'])
def train():
    '''前端Vue.js用来测试与后端Flask API的连通性'''
    return jsonify('Pong!')
