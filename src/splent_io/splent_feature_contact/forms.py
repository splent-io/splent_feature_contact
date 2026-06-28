from flask_wtf import FlaskForm
from wtforms import SubmitField


class SplentFeatureContactForm(FlaskForm):
    submit = SubmitField("Save splent_feature_contact")
