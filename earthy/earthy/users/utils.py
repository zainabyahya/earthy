import os
import re
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from earthy import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
    
# Password validation in Python
# using naive method

# Function to validate the password
def password_check(passwd):
	
	SpecialSym =['$', '@', '#', '%']
	val = True
	
	if len(passwd) < 6:
		val = False
		
	if len(passwd) > 20:
		val = False
		
	if not any(char.isdigit() for char in passwd):
		val = False
		
	if not any(char.isupper() for char in passwd):
		val = False
		
	if not any(char.islower() for char in passwd):
		val = False
		
	if not any(char in SpecialSym for char in passwd):
		val = False
  
	if val:
		return val

