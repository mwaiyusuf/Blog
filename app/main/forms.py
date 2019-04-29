from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class PitchForm(FlaskForm):

    title = StringField('Post title')
    category = SelectField('Post Category', choices=[('Music', 'music-blog'),
                                                      ('Sports', 'sports-blog'),
                                                      ('Events', 'events-blogs'),
                                                      ('Travel', 'travel-blog'),
                                                      ('Food', 'food-blog'),
                                                      ('random', 'random')])
    content = TextAreaField('Type Here')
    submit = SubmitField('Create Post')


class CommentForm(FlaskForm):

    title = StringField('Comment Title')
    comment = TextAreaField('Post Of The Comment')
    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
