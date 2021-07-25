import os, glob
from datetime import datetime as dt
from datetime import timedelta

from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import pandas as pd

fs = glob.glob(os.path.join(os.getcwd(),'data','*_forecast.csv'))
dfs_forecast = {os.path.splitext(os.path.split(f)[1])[0].split('_')[0]:pd.read_csv(f).set_index('index') for f in fs}
fs = glob.glob(os.path.join(os.getcwd(),'data','*_historic.csv'))
dfs_historic = {os.path.splitext(os.path.split(f)[1])[0].split('_')[0]:pd.read_csv(f).set_index('Unnamed: 0') for f in fs}
for kk in dfs_forecast.keys():
    dfs_forecast[kk].index = pd.to_datetime(dfs_forecast[kk].index)
    dfs_historic[kk].index = pd.to_datetime(dfs_historic[kk].index)

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    os.environ['USERNAME']: generate_password_hash(os.environ['USERPASSWORD'])
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/api/')
@auth.login_required
def index():
    reservoir = request.args.get('reservoir')
    if reservoir is None or reservoir not in dfs_historic.keys():
        return jsonify({'error':f'specify a reservoir from {dfs_historic.keys()}'})
    date = request.args.get('date')
    try:
        date = dt.strptime(date,'%Y-%m-%d')
    except:
        return jsonify({'error':f'specify a date as YYYY-MM-DD'})

    try:
        data = {
            'historic':dfs_historic[reservoir].loc[(dfs_historic[reservoir].index>=(date-timedelta(days=90))) & (dfs_historic[reservoir].index<=(date)),'PRESENT_STORAGE_TMC'].to_json(),
            'predicted':dfs_forecast[reservoir].loc[date,:].to_json()
        }
        return jsonify(data)
        
    except Exception as e:
        print ('Error!',e)
        return jsonify({'Error':'bad request.'})

    

if __name__ == '__main__':
    app.run()