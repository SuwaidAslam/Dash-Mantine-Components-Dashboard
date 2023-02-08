import pandas as pd 
import numpy as np
from dash import dcc, html

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def return_filtered_data(date_range, emr_select, interactor_select, inbasket_select, 
        msg_label_select, patient_initiated_select, location_select, entity_select, state_select):

    df = pd.read_csv('dash-fiverr.csv', parse_dates=['touch_dt_tm','message_create_dt_tm','message_delete_dt_tm'])
    # filter data on date range
    df = df[(df['touch_dt_tm'] > date_range[0]) & (df['touch_dt_tm'] <= date_range[1])]

    # #other filters
    # df = df[(df['state'] == state_select) & (df['source'] == entity_select) &
    #     (df['patient_initiated'] == patient_initiated_select) & (df['prediction'] == msg_label_select)
    #     & (df['emr'] == emr_select) & (df['interactor'] == interactor_select) 
    #     & (df['location'] == location_select) & (df['predicted_id'] == inbasket_select)]
    return df

df = pd.read_csv('dash-fiverr.csv', parse_dates=['touch_dt_tm','message_create_dt_tm','message_delete_dt_tm'])
states = ['state2', 'state1']
def card_row1_data():
    data1 = []
    # Card 1
    upim = {}
    for state in states:
        upim[state] = df[(df['sender_id'] == 'patient') & (df['state'] == state)].drop_duplicates(['message_id'])
        data1.append(str('%i' % len(upim[state])))
    
    data2 = []
    # Card 2
    atpm = {}
    for state in states:
        atpm[state] = df.loc[(df['interactor'] != 'bot') & (df['state'] == state)].drop_duplicates(['message_id', 'interactor']).groupby('message_id').count()['touch_id']
        # data2.append(str(state + ' atpm: %.2f' % atpm[state].mean()))
        data2.append(str('%.2f' % atpm[state].mean()))
    touches_saved = atpm['state2'].mean() - atpm['state1'].mean()
    if np.isnan(touches_saved):
        touches_saved = 0
    # print('difference: %.2f' % touches_saved)
    data3 = []
    # Card 3
    rrem = {}
    for state in states:
        try:
            rrem[state] = upim[state].loc[(upim[state]['touch_order'] == 1)]
            data3.append(str('%i (%.2f%%)' % (rrem[state].shape[0], rrem[state].shape[0]/upim[state].shape[0]*100)))
        except ZeroDivisionError:
            data3.append('0 of 0')
    data4 = []
    # Card 4
    urg = {}
    for state in states:
        try:
            urg[state] = upim[state][upim[state]['prediction'] == 'urgent'].drop_duplicates('message_id')
            data4.append(str('%i (%.2f%%)' % (urg[state].shape[0], urg[state].shape[0]/upim[state].shape[0]*100)))
        except ZeroDivisionError:
            data4.append(str('0 of 0'))

    return data1, data2, data3, data4


def get_row2_data(min_per_touch, usd_per_min, urg_conversion, rvu, usd_per_rvu, gross_margin):
    data1 = []
    # Card 1
    upim = {}
    for state in states:
        upim[state] = df[(df['sender_id'] == 'patient') & (df['state'] == state)].drop_duplicates(['message_id'])
        data1.append(str(state + ' upim: %i' % len(upim[state])))
    
    data2 = []
    # Card 2
    atpm = {}
    for state in states:
        atpm[state] = df.loc[(df['interactor'] != 'bot') & (df['state'] == state)].drop_duplicates(['message_id', 'interactor']).groupby('message_id').count()['touch_id']
        data2.append(str(state + ' atpm: %.2f' % atpm[state].mean()))
    touches_saved = atpm['state2'].mean() - atpm['state1'].mean()
    if np.isnan(touches_saved):
        touches_saved = 0
    # print('difference: %.2f' % touches_saved)
    data3 = []
    # Card 3
    rrem = {}
    for state in states:
        try:
            rrem[state] = upim[state].loc[(upim[state]['touch_order'] == 1)]
            data3.append(str(state + ' rrem: %i (%.2f%%)' % (rrem[state].shape[0], rrem[state].shape[0]/upim[state].shape[0]*100)))
        except ZeroDivisionError:
            data3.append(str(state + ' rrem: 0 of 0'))
    data4 = []
    # Card 4
    urg = {}
    for state in states:
        try:
            urg[state] = upim[state][upim[state]['prediction'] == 'urgent'].drop_duplicates('message_id')
            data4.append(str(state + ' urg: %i (%.2f%%)' % (urg[state].shape[0], urg[state].shape[0]/upim[state].shape[0]*100)))
        except ZeroDivisionError:
            data4.append(str(state + ' urg: 0 of 0'))
    
    # Card 5
    sb1k = rrem['state1'].shape[0] / len(upim['state1'])*1000
    cr = sb1k * touches_saved * min_per_touch * usd_per_min
    card5_data = html.Div([
        html.H3("%i Messages" % (sb1k)),
        html.H3("× %.2f touches saved" % (touches_saved)),
        html.H3("× %.1f minutes per touch" % (min_per_touch)),
        html.H3("× $%.2f per minute" % (usd_per_min)),
        html.H3("= $%i per 1K messages" % (cr)),
    ])

    # Card 6
    urg1k = urg['state1'].shape[0] / len(upim['state1'])*1000
    rev = urg1k * urg_conversion * rvu * usd_per_rvu * gross_margin
    card6_data = html.Div([
        html.H3("%i urgent visit needs" % (urg1k)),
        html.H3("× %.1f%% conversion rate" % (urg_conversion*100)),
        html.H3("× %.1f RVU" % (rvu)),
        html.H3("× $%i per RVU" % (usd_per_rvu)),
        html.H3("× %.1f%% gross margin" % (gross_margin*100)),
        html.H3(" = $%i per 1K messages" % (rev)),
    ])

    # Card 7
    impact = cr + rev
    card7_data = html.Div([
        html.H3("$%i combined" % (impact)),
        html.H3("= $%i at 75%% confidence" % (impact*.75)),
        html.H3("= $%i at 50%% confidence" % (impact*.5)),
        html.H3("= $%i at 25%% confidence" % (impact*.25)),
    ])
            
    return card5_data, card6_data, card7_data

