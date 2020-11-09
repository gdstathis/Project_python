from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, ValidationError

"""
Create a form for the application
Use validators from wtforms and create extra custom validators
When custom validators are enabled, a message will be displayed under input fields"""
class AppForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    def validate_name(form, name):
        if not len(name.data) in range(4, 50):
            raise ValidationError('Name must be more than 4 and less than 50 characters')

    lat = FloatField('Latitude', validators=[DataRequired()])
    def validate_lat(form, lat):
        if abs(lat.data) > 90:
            raise ValidationError('Latitude must be between -90 and 90')

    lon = FloatField('Longitude', validators=[DataRequired()])
    def validate_lon(form, lon):
        if abs(lon.data) > 180:
            raise ValidationError('Longitude must be between -180 and 180')

    submit = SubmitField('Submit')
