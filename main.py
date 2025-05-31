from meuPoema import app, database as db
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from meuPoema.models import User, Messages
from flask_socketio import SocketIO, emit, join_room
from datetime import datetime

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/<int:sender>/message/<int:recever>/", methods=['GET', 'POST'])
@login_required
def message(sender, recever):
    sender_user = User.query.get(sender)
    recever_user = User.query.get(recever)

    # Validações
    if sender_user.id == recever_user.id:
        flash('Você não pode enviar mensagens para si mesmo', 'alert-danger')
        return redirect(url_for('home'))

    if sender_user.id != current_user.id:
        flash('Ação não autorizada', 'alert-danger')
        return redirect(url_for('home'))

    if not sender_user or not recever_user:
        flash('Usuário não encontrado', 'alert-danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        message_content = request.form.get('message')
        if message_content:
            new_message = Messages(
                sender_id=sender,
                recever_id=recever,
                message=message_content
            )
            db.session.add(new_message)
            db.session.commit()

            # Envia via WebSocket
            room = f'chat_{min(sender, recever)}_{max(sender, recever)}'
            socketio.emit('new_message', {
                'sender_id': sender,
                'recever_id': recever,
                'message': message_content,
                'date_created': datetime.utcnow().strftime('%H:%M'),
                'sender_username': sender_user.username
            }, room=room)

            return '', 204  # Resposta vazia para requisições AJAX

    messages = Messages.query.filter(
        ((Messages.sender_id == sender) & (Messages.recever_id == recever)) |
        ((Messages.sender_id == recever) & (Messages.recever_id == sender))
    ).order_by(Messages.date_created.asc()).all()

    return render_template('message.html',
                         sender=sender_user,
                         recever=recever_user,
                         messages=messages)

# WebSocket Handlers
@socketio.on('join_chat')
def handle_join_chat(data):
    user_id = data['user_id']
    room = data['room']
    join_room(room)
    emit('user_connected', {'user_id': user_id}, room=room)


if __name__ == "__main__":
    app.run(debug=True)
    socketio.run(app, debug=True)
