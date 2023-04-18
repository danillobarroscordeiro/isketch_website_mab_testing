from flask import Flask, render_template, redirect, url_for, request
import pandas as pd
import numpy as np 
app = Flask( __name__)


@app.route( '/home')
def index():
    # get data
    df = pd.read_csv('data_experiment.csv')

    df['no_click'] = df['visit'] - df['click']
    click_array = df.groupby('group').sum().reset_index()[['click', 'no_click']].T.to_numpy()

    # Thompson Agent
    prob_reward = np.random.beta( click_array[0], click_array[1])

    if np.argmax(prob_reward) == 0:
        return render_template( 'page01.html')
    else:
        return render_template( 'page02.html')


@app.route( '/yes', methods=['POST'] )
def yes_event():
    df = pd.read_csv('data_experiment.csv')
    
    if request.form['yescheckbox'] == 'red':
        click = 1
        visit = 1
        group = 'treatment'
    else:
        click = 1
        visit = 1
        group = 'control'

    df_raw = pd.DataFrame({'click': click, 'visit': visit, 'group':group}, index= [0])
    df = pd.concat([df,df_raw])
    df.to_csv('data_experiment.csv', index=False)

    return redirect( url_for ( 'index') )


@app.route( '/no', methods=['POST'] )
def no_event():
    df = pd.read_csv('data_experiment.csv')

    if request.form['nocheckbox'] == 'red':
        click = 0
        visit = 1
        group = 'treatment'
    else:
        click = 0
        visit = 1
        group = 'control'

    df_raw = pd.DataFrame({'click': click, 'visit': visit, 'group':group}, index = [0])
    df = pd.concat([df,df_raw])
    df.to_csv('data_experiment.csv', index=False)

    return redirect( url_for ( 'index') )


if __name__ == '__main__':
    app.run(port=5000)


