from wtforms import BooleanField, Form, HiddenField, SelectField, StringField, TimeField, ValidationError, validators


class Lt(object):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data >= other.data:
            d = {
                "other_label": hasattr(other, "label") and other.label.text or self.fieldname,
                "other_name": self.fieldname,
            }
            message = self.message
            if message is None:
                message = field.gettext("Field must be equal to %(other_name)s.")

            raise ValidationError(message % d)


class Gt(object):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data <= other.data:
            d = {
                "other_label": hasattr(other, "label") and other.label.text or self.fieldname,
                "other_name": self.fieldname,
            }
            message = self.message
            if message is None:
                message = field.gettext("Field must be equal to %(other_name)s.")

            raise ValidationError(message % d)


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
