from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    tags = StringField('Tags')
