from wtforms import BooleanField, Form, HiddenField, SelectField, StringField, TimeField, validators

from ..shared.form_validators import Gt, Lt


class RestaurantForm(Form):
    id = HiddenField("id")
    h = HiddenField("h")
    name = StringField("Name", [validators.DataRequired(), validators.Length(max=255)])
    street = StringField("Street", [validators.DataRequired(), validators.Length(max=255)])
    city = StringField("City", [validators.DataRequired(), validators.Length(max=255)])
    zip = StringField("Zip", [validators.DataRequired(), validators.Length(max=25)])
    country = SelectField(
        "Country",
        [validators.DataRequired(), validators.Length(max=2)],
        choices=[("AT", "Austria"), ("DE", "Germany")],
    )
    open_from = TimeField(
        "Open from",
        [validators.DataRequired(), Lt("open_until", message="'Open from' needs to be before 'Open until'")],
    )
    open_until = TimeField(
        "Open until",
        [validators.DataRequired(), Gt("open_from", message="'Open until' needs to be after 'Open from'")],
    )
    open_monday = BooleanField("Monday")
    open_tuesday = BooleanField("Tuesday")
    open_wednesday = BooleanField("Wednesday")
    open_thursday = BooleanField("Thursday")
    open_friday = BooleanField("Friday")
    open_saturday = BooleanField("Saturday")
    open_sunday = BooleanField("Sunday")
