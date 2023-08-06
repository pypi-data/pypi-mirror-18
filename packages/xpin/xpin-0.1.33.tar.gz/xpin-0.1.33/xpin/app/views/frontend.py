#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import datetime
import json

from flask import Blueprint
from flask import jsonify
from flask import request, current_app, g

from ... import constants
from ...log import logger
from ..models import Pin, User, PinLog
from ..extensions import db

bp = Blueprint('frontend', __name__)


@bp.before_request
def unpack_input():
    for key in ('data', 'sign'):
        if key not in request.values:
            return jsonify(
                ret=constants.RET_PARAMS_INVALID
            )

    client_secret = current_app.config['CLIENT_SECRET']

    my_sign = hashlib.md5('|'.join(
        [client_secret, request.values['data']]
    )).hexdigest()

    if my_sign != request.values['sign']:
        return jsonify(
            ret=constants.RET_SIGN_INVALID
        )

    try:
        g.input = json.loads(request.values['data'])
    except:
        logger.error('json loads fail. request: %s', request)
        return jsonify(
            ret=constants.RET_PARAMS_INVALID
        )


@bp.route(constants.URL_PIN_CREATE)
def create_pin():

    for key in ('username', 'source'):
        if key not in g.input:
            return jsonify(
                ret=constants.RET_PARAMS_INVALID
            )

    username = g.input['username']
    source = g.input['source']

    user = User.query.filter(User.username == username).first()

    if not user or not user.valid:
        logger.error('invalid user. request: %s', request)
        return jsonify(
            ret=constants.RET_USER_INVALID,
        )

    # 判断是否是合法的企业内部用户
    if not g.ding.get_user(user.ding_id):
        logger.error('invalid ding user. request: %s', request)
        return jsonify(
            ret=constants.RET_USER_INVALID,
        )

    # 删掉旧的
    Pin.query.filter(
        Pin.user_id == user.id,
        Pin.source == source,
    ).delete()

    db.session.commit()

    pin = Pin()
    pin.user_id = user.id
    pin.source = source
    pin.code = Pin.create_code(current_app.config['PIN_LENGTH'])

    if current_app.config['PIN_MAX_AGE']:
        pin.expire_time = datetime.datetime.now() + datetime.timedelta(seconds=current_app.config['PIN_MAX_AGE'])

    db.session.add(pin)
    db.session.commit()

    pin_log = PinLog()
    pin_log.username = username
    pin_log.source = source
    pin_log.pin = pin.code
    pin_log.address = request.remote_addr
    pin_log.expire_time = pin.expire_time

    db.session.add(pin_log)
    db.session.commit()

    msg_title = current_app.config['MSG_TITLE']
    msg_content = current_app.config['MSG_CONTENT_TPL'].format(
        username=username,
        source=source,
        address=request.remote_addr,
        pin=pin.code,
    )

    g.ding.emit(msg_title, msg_content, user_list=[user.ding_id])

    if g.send_cloud and user.mail:
        g.send_cloud.emit(msg_title, msg_content, [user.mail])

    return jsonify(
        ret=0,
        pin=pin.code,
    )


@bp.route(constants.URL_PIN_VERIFY)
def verify_pin():
    """
    验证pin
    :return:
    """

    for key in ('username', 'source', 'pin'):
        if key not in g.input:
            return jsonify(
                ret=constants.RET_PARAMS_INVALID
            )

    username = g.input['username']
    source = g.input['source']
    pin = g.input['pin']

    user = User.query.filter(User.username == username).first()

    if not user or not user.valid:
        logger.error('invalid user. request: %s', request)
        return jsonify(
            ret=constants.RET_USER_INVALID,
        )

    pin = Pin.query.filter(
        Pin.user_id == user.id,
        Pin.source == source,
        Pin.code == pin,
        ).first()

    if not pin:
        return jsonify(
            ret=constants.RET_PIN_VALID
        )

    if pin.expire_time and pin.expire_time < datetime.datetime.now():
        return jsonify(
            ret=constants.RET_PIN_EXPIRED,
        )

    # 删掉旧的
    Pin.query.filter(
        Pin.user_id == user.id,
        Pin.source == source,
        ).delete()

    db.session.commit()

    return jsonify(
        ret=0
    )
