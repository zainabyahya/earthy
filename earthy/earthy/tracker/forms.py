from flask_wtf import FlaskForm
from wtforms import  SubmitField, IntegerField
from wtforms.validators import InputRequired, ValidationError, NumberRange


class plasticForm(FlaskForm):
    plasticBottle=IntegerField('Plastic Bottle', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    plasticBag=IntegerField('Plastic Bag', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    plasticWrap=IntegerField('Plastic Wrap', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    yoghurtBox=IntegerField('Yoghurt Box', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    cottonSwab=IntegerField('Cotton Swab', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    detergentBottle=IntegerField('Detergent Bottle', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    shampooBottle=IntegerField('Shampoo Bottle', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    toothbrush=IntegerField('Tooth Brush', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    toothpaste=IntegerField('Tooth Paste', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    takeawayBox=IntegerField('Takeaway Box', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    takeawayWrap=IntegerField('Takeaway Wrap', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    straw=IntegerField('Straw', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    disposableCutlery=IntegerField('Disposable Cutlery', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    plasticPlate=IntegerField('Plastic Plate', validators=[
        InputRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Submit')
    
    class Meta:
        # No need for csrf token in this child form
        csrf = False

    
    