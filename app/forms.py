from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class IssueServiceForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    type = SelectField('Type', choices=[('Garbage Collection', 'Garbage Collection'), ('Public Transportation', 'Public Transportation'), ('Emergency Services', 'Emergency Services')], validators=[DataRequired()])
    submit = SubmitField('Submit')
