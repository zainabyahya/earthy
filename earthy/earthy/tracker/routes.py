
from earthy import db
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify
from flask_login import current_user, login_required
from earthy.models import Plastic
from earthy.tracker.forms import plasticForm
from earthy.tracker.util import getItemWeight, getMax, getNewTrackingSession, getSuggestions, getTotalWeight, item, getItemTotalGrams, getItemWeight, lowerAverageNationally, lowerAverageLocally
import pygal

tracker = Blueprint('tracker', __name__)



@tracker.route('/tracker', methods=['GET', 'POST'])
@login_required
def track():
    items=[]
    form = plasticForm()
    if form.validate_on_submit():
        for field in form:
            frequency = request.form.get(f'frequency {field.name}')
            weight = getItemTotalGrams(getItemWeight(
                field.name), field.data, frequency)
            items.append(item(field.name, round(weight, 3)/1000))
        result = getTotalWeight(items)
        current_user.score = result
        trackingSession = getNewTrackingSession(items)
        db.session.add(trackingSession)
        db.session.commit()
    else:
        result = 0
    return render_template("tracker.html", user=current_user, form=form, result=result, title='Tracker', items=items)


@tracker.route('/getInsight')
@login_required
def getInsight():
    if current_user.score!=0:
        plastic = Plastic.query.filter_by(user_id=current_user.id)
        
        items, dates = [], []
        # get all dates where a session was created
        for row in plastic:
            dates.append(row.creation_datetime)
        # create a dictionary with lists for all items
        dictionary = {itemWeights: [] for itemWeights in range(14)}
        # insert the data into the lists
        for row in plastic:
            x = 0
            itemDict = dict((col, getattr(row, col))
                            for col in row.__table__.columns.keys())

            for key, value in itemDict.items():
                x += 1
                if key != "id" and key != "user_id" and key != "creation_datetime" and x < 14:
                    dictionary[x].append(value)

        line_chart = pygal.Line()
        # naming the title
        line_chart.title = 'The variation of your plastic consumption in kg over time'
        # set  the range of plot
        line_chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), dates)
        # adding lines
        itemsName = ['Plastic Bottle', 'Plastic Bag', 'Plastic Wrap', 'Yoghurt Box',
                    'Cotton Swab', 'Detergent Bottle', 'Shampoo Bottle', 'Toothbrush', 'Toothpaste', 'Takeaway Box', 'Takeaway Wrap', 'Straw', 'Disposable Cutlery', 'Plastic Plate']
        for x in range(14):
            line_chart.add(itemsName[x], dictionary[x])

        graph_data = line_chart.render_data_uri()
        members = current_user.members
        score = current_user.score
        locally = lowerAverageLocally(score/members)
        nationally = lowerAverageNationally(score/members)
        
        # evaluate the last record
        latestPlastic = Plastic.query.filter_by(user_id=current_user.id)[-1]
        latestDict = dict((col, getattr(latestPlastic, col))
                            for col in latestPlastic.__table__.columns.keys())
        count=0
        for key, value in latestDict.items():
            if key != "id" and key != "user_id" and key != "creation_datetime":
                items.append(item(itemsName[count], value))
                count+=1
        max = getMax(items)
        maxItems = ''
        if max:
            maxItems = max[0].name+', ' + max[1].name + ' and ' + max[2].name+'.'

        suggestions = getSuggestions(max)

        return render_template("insight.html", title='Insight', graph_data=graph_data, locally=locally, nationally=nationally,
                            score=score, members=members, maxItems=maxItems, suggestions=suggestions, items=items)
    else: 
        flash("You haven't logged any data to be analyzed, please enter your data first.", 'danger')
        return redirect(url_for(tracker.track))
