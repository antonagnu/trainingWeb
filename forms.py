from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Length, InputRequired
from wtforms.fields.html5 import DateField
import db_management

class AddForm(FlaskForm):

    locations = db_management.getLocation()

    #actype = SelectField(label='Type', choices=[('Running', "Running"), ('Walking', "Walking")], validators=[InputRequired()])
    date =  DateField('Date', validators=[InputRequired()])
    race = SelectField(label='Race', choices=[('0', "No"), ('1', "Yes")], validators=[InputRequired()])
    location = TextField('Location', validators=[InputRequired(),Length(max=30)] )
    #location = SelectField(label='Location', choices=locations)
    distance = TextField('Distance', validators=[InputRequired(),Length(max=5)] )
    #calories =  TextField('Calories', validators=[InputRequired(),Length(max=15)] )
    time =  TextField('Time', validators=[InputRequired(),Length(max=15)] )
    avgHr =  TextField('Avg HR', validators=[InputRequired(),Length(max=15)] )
    maxHr=  TextField('Max HR', validators=[InputRequired(),Length(max=15)] )
    avgCadence=  TextField('Avg Cadence', validators=[InputRequired(),Length(max=15)] )
    maxCadence=  TextField('Max Cadence', validators=[InputRequired(),Length(max=15)] )
    avgPace =  TextField('Avg Pace', validators=[InputRequired(),Length(max=15)] )
    elevGain =  TextField('Elev. Gain', validators=[InputRequired(),Length(max=15)] )  
    elevLoss =  TextField('Elev. Loss', validators=[InputRequired(),Length(max=15)] )
    avgStrideLength = TextField('Stride Lenth', validators=[InputRequired(),Length(max=15)] )
    
    
    submit = SubmitField('Add Activity')
