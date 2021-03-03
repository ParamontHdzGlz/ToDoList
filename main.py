import unittest
from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user

from app import create_app
from app.forms import TodoForm
from app.firestore_service import get_users, get_to_dos, put_to_do

app = create_app()

to_dos = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video a productor ']


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET','POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    to_do_form = TodoForm()

    context = {
        'user_ip': user_ip,
        'to_dos': get_to_dos(user_id=username),
        'username': username,
        'to_do_form': TodoForm()
    }

    if to_do_form.validate_on_submit():
        put_to_do(user_id=username, description=to_do_form.description.data)
        flash('Tu tarea se creo con éxito.')
        return redirect(url_for('hello'))

    return render_template('hello.html', **context)


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
