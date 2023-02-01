from flask import Flask, render_template, request, flash, redirect, url_for

from config import Config
from game import Game
from project.forms import GameForm, ReviewForm

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    global counter

    Game(1)
    return render_template('index.html')


@app.route('/about/<string:letter>')  # динамический маршрут
@app.route('/about')  # статический маршрут
def about(letter="Игра круть просто жуть!"):
    return render_template('info.html', letter=letter)


@app.route('/game', methods=['get', 'post'])
def games():
    game = Game()
    form_game = GameForm()
    form_review = ReviewForm()

    if form_game.move.data:
        direction = int(form_game.direction.data)
        step = form_game.step.data

        string = game.move(direction, step)
        flash(*string)
        # return redirect(url_for('games'))

    if form_review.push.data:
        name = form_review.name.data or 'Anonymous'
        review = form_review.message.data

        with open('review.txt', 'a', encoding='utf-8') as file:
            print(f'Имя: {name}\nСообщение: {review}\n{"-" * 10}', end='\n', file=file)

        flash('Спасибо за отзыв')
        return redirect(url_for('index'))

    if request.method == 'GET' and game.current_room == 'Подземелье':
        flash('После бурной ночи вы оказались в подземельнье! Вам нужно срочно убегать. Найдите путь на балкон...',
              'start')
    return render_template('game.html', form_game=form_game, form_review=form_review,
                           current_room=game.getCurrentRoom())


if __name__ == '__main__':
    app.run(debug=True)
