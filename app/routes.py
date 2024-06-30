from flask import render_template, request, redirect, url_for, flash, current_app as app
from .forms import IssueServiceForm
from .models import Issue, Transaction, blockchain
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from . import db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report_service', methods=['GET', 'POST'])
def report_service():
    form = IssueServiceForm()
    if form.validate_on_submit():
        description = form.description.data
        location = form.location.data
        issue_type = form.type.data
        issue = Issue(description=description, location=location, type=issue_type)
        db.session.add(issue)
        db.session.commit()
        blockchain.add_transaction(sender=description, receiver=location, amount=0)
        flash(f'{issue_type} request submitted successfully', 'success')
        return redirect(url_for('report_service'))
    return render_template('report_service.html', form=form)

@app.route('/data')
def data():
    issues = Issue.query.all()
    transactions = Transaction.query.all()

    issue_data = [{'description': issue.description, 'location': issue.location, 'type': issue.type, 'timestamp': issue.timestamp} for issue in issues]

    # Example data for ML model
    data = pd.DataFrame({'feature': [1, 2, 3, 4, 5], 'value': [2, 4, 6, 8, 10]})
    X = data[['feature']]
    y = data['value']
    model = LinearRegression()
    model.fit(X, y)
    prediction = model.predict([[6]])[0]

    # Anomaly detection
    anomaly_data = np.random.rand(100, 2)
    clf = IsolationForest(random_state=0).fit(anomaly_data)
    anomaly_prediction = clf.predict([[0.5, 0.5]])[0]

    real_time_data = {
        'air_quality': 'Good',
        'traffic_flow': 'Moderate',
        'energy_consumption': '120 MW'
    }

    transaction_data = [{'sender': tx.sender, 'receiver': tx.receiver, 'amount': tx.amount, 'timestamp': tx.timestamp} for tx in transactions]

    # Generate graphs
    fig, ax = plt.subplots()
    ax.bar([i['location'] for i in issue_data], [1 for i in issue_data])
    ax.set_xlabel('Location')
    ax.set_ylabel('Number of Issues')
    ax.set_title('Reported Issues by Location')
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('data.html', prediction=prediction, real_time_data=real_time_data, issues=issue_data, anomaly_prediction=anomaly_prediction, transactions=transaction_data, plot_url=plot_url)

@app.route('/about')
def about():
    return render_template('about.html')