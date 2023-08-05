# !/usr/bin/env python
# -*- coding=UTF-8 -*-
# *************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: forms.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-10-29 07:09:54
# *************************************************************************
from flask import flash, session
from wtforms import (StringField, PasswordField, BooleanField)
from wtforms.validators import Length, DataRequired, Email
from flask_babelex import lazy_gettext as _
from .response import HTTPResponse

try:
    from flask_wtf import FlaskForm as Form
except ImportError:
    from flask_wtf import Form


def flash_errors(form):
    for field, errors in form.errors.items():
        flash(u"%s %s" % (getattr(form, field).label.text, errors[0]))
        break


def return_errors(form):
    for field, errors in form.errors.items():
        data = (u"%s %s" % (getattr(form, field).label.text, errors[0]))
        break
    return HTTPResponse(
        HTTPResponse.FORM_VALIDATE_ERROR, description=data).to_response()


class BaseForm(Form):
    username = StringField(
        _('Username:'), [DataRequired(), Length(
            min=4, max=20)])
    password = PasswordField(
        _('Password:'), [DataRequired(), Length(
            min=4, max=20)])
    captcha = StringField(
        _('Captcha:'), [DataRequired(), Length(
            min=4, max=4)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        captcha = session['captcha']
        captcha_data = self.captcha.data
        if captcha_data.lower() != captcha.lower():
            self.captcha.errors.append(_('The captcha is error'))
            return False

        return True


class RegisterForm(BaseForm):
    email = StringField(_('Email:'), [DataRequired(), Email()])


class LoginForm(BaseForm):
    remember = BooleanField(_('Remember me'), default=False)


class ForgetForm(Form):
    email = StringField(_('Register Email:'), [DataRequired(), Email()])

    captcha = StringField(
        _('Captcha:'), [DataRequired(), Length(
            min=4, max=4)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        captcha = session['captcha']
        captcha_data = self.captcha.data
        if captcha_data.lower() != captcha.lower():
            self.captcha.errors.append(_('The captcha is error'))
            return False

        return True
