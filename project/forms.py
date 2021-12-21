from logging import PlaceHolder
from typing import Text
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, Length, NumberRange


class GameForm(FlaskForm):
    direction = SelectField('Выберите сторону света, в которую желаете отправиться', 
                            choices={
                                (0, 'Север'),
                                (1, 'Восток'),
                                (2, 'Юг'),
                                (3, 'Запад')
                            }, default='1')
    step = IntegerField('Как далеко планируется продвинуться?', validators=[NumberRange(min=1, max=2)], default=1)
    move = SubmitField('В путь!')


class ReviewForm(FlaskForm):
    name = StringField('Имя', validators=[Length(2, 100)])
    message = TextAreaField('Ваш отзыв', validators=[DataRequired()])
    push = SubmitField('Отправить!')