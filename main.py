from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired , URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField(label = 'location url', validators=[DataRequired(), URL()])
    open_time = StringField(label = "Open time", validators=[DataRequired()])
    close_time = StringField(label = "Close time", validators=[DataRequired()])
    coffee_rating = SelectField('Coffee rating ', choices=[('✘', '✘'), ('☕️', '☕️'), ('☕️☕️', '☕️☕️'),('☕️☕️☕️', '☕️☕️☕️'), ('☕️☕️☕️☕️', '☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')], validators=[DataRequired()])
    wifi_rating = SelectField('WiFi rating', choices=[('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'),('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')], validators=[DataRequired()])
    power_outlet = SelectField('Power Outlet ', choices=[('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'),( '🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    is_added=False
    if request.method =="POST":
        if form.validate_on_submit():
            print("True")
            with open ('cafe-data.csv','a+', encoding="utf-8", newline='') as file:
                new_row = [form.cafe.data, form.location_url.data,form.open_time.data, form.close_time.data, form.coffee_rating.data, form.wifi_rating.data, form.power_outlet.data]
                csv_data = csv.writer(file, delimiter=',')
                csv_data.writerow(new_row)
                is_added = True
        return render_template('add.html',form=form,add_completed = is_added)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form, add_completed = is_added)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
