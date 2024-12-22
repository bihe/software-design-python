from datetime import date

from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, IntegerField, StringField, TimeField, ValidationError, validators

from ..shared.form_validators import Gt, Lt


def validate_positive_number(form, field):
    if int(field.data) <= 0:
        raise ValidationError("Please enter a correct number of people!")


def validate_max_people(form, field):
    if int(field.data) > 6:
        raise ValidationError("A reservation for more than 6 people is not possible!")


def date_current_or_future(form, field):
    if field.data < date.today():
        raise ValidationError("Cannot make reservations in the past!")


class ReservationForm(FlaskForm):
    restaurant_id = HiddenField("restaurant_id")
    h = HiddenField("h")
    name = StringField("Reservation name", [validators.DataRequired(), validators.Length(max=255)])
    num_people = IntegerField(
        "Number of people", [validators.DataRequired(), validate_positive_number, validate_max_people]
    )
    time_from = TimeField(
        "Time from",
        [validators.DataRequired(), Lt("time_until", message="'Time from' needs to be before 'Time until'")],
    )
    time_until = TimeField(
        "Time until",
        [validators.DataRequired(), Gt("time_from", message="'Time until' needs to be after 'Time from'")],
    )
    reservation_date = DateField("Reservation date", [validators.DataRequired(), date_current_or_future])
