import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import Dash
from Data import *
from components import *



class AppCallback:
    def __init__(self):
        pass
    
    @staticmethod
    def _register_callbacks(app: Dash):
        @app.callback([Output('cost_reduction_txt', 'children'),
        Output('revenue_txt', 'children'),
        Output('total_impact_txt', 'children')],
        [Input('time_per_touch', 'value'),
        Input('dollar_per_min', 'value'),
        Input('visit_conversation', 'value'),
        Input('relative_value_unit', 'value'),
        Input('dollar_per_rvu', 'value'),
        Input('gross_margin', 'value')]
        )
        def calculation_variables(min_per_touch, usd_per_min, urg_conversion, rvu, usd_per_rvu, gross_margin):
            try:
                card5_data, card6_data, card7_data =  get_row2_data(float(min_per_touch), float(usd_per_min),
                    float(urg_conversion), float(rvu), float(usd_per_rvu), float(gross_margin))
                return [card5_data, card6_data, card7_data]
            except:
                raise PreventUpdate
    
    
        @app.callback(
        [Output('time_per_touch', 'value'),
        Output('dollar_per_min', 'value'),
        Output('visit_conversation', 'value'),
        Output('relative_value_unit', 'value'),
        Output('dollar_per_rvu', 'value'),
        Output('gross_margin', 'value')],
        [Input('variables_reset', 'n_clicks')]
        )
        def reset_values(n_clicks):
            min_per_touch = 3
            usd_per_min = 1.16
            urg_conversion = 0.5
            rvu = 1.3
            usd_per_rvu = 110
            gross_margin = 0.6
            return [min_per_touch, usd_per_min, urg_conversion, rvu, usd_per_rvu, gross_margin]
        
        

        @app.callback(
            Output('widget1_figure', 'figure'),
            [Input('memory', 'data'),
            Input('radiogroup-resample', 'value')]
        )
        def generate_widget1(df, resample_period):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                w1 = df.copy()
                w1 = w1.loc[(w1['touch_order'] == 1)][['conversation_id', 'touch_id', 'touch_dt_tm', 'state']]

                # Set index to datetime for resampling 
                w1.set_index('touch_dt_tm', inplace=True)
                # Group by filterable columns and resample to 1Hour
                w1 = w1.groupby('state').resample(resample_period)['touch_id'].count().reset_index().sort_values('touch_dt_tm', ignore_index=True)
                fig = px.bar(w1, x='touch_dt_tm', y='touch_id', color='state', barmode='group',
                        color_discrete_sequence=colors_discrete, labels={'touch_dt_tm':'Date','touch_id': 'Number of Messages'})
                fig.update_layout(showlegend=False)
                return fig
        
        @app.callback(
            Output('widget_2', 'children'),
            [Input('memory', 'data')]
        )
        def generate_widget2(df):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                w2 = df.copy()
                w2 = w2.loc[(w2['touch_order'] == 1)][['conversation_id', 'touch_id', 'touch_dt_tm', 'prediction', 'state']]
                w2 = w2.groupby(['prediction', 'state'])['touch_id'].agg(np.size).reset_index()

                fig = px.bar(w2, x='prediction', y='touch_id', color='state', barmode = 'stack', color_discrete_sequence=colors_discrete, labels={'prediction':'Label', 'touch_id':'Number of Conversations'})
                fig.update_layout(showlegend=False)
                return dmc.Card(
                    children=[
                        dmc.Text("Widget 2", size=20, weight=400),
                        dmc.Text("Text"),
                        dcc.Graph(figure=fig)
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                    style={"height": "100%"},
                )

        @app.callback(
            Output('widget_3', 'children'),
            [Input('memory', 'data')]
        )
        def generate_widget3(df):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                w3 = df.copy()
                w3 = w3.loc[(w3['interactor'] != 'bot')] 
                # Group by interactor for this entire time period
                w3 = w3.groupby('interactor').count().reset_index()
                fig = px.histogram(w3, x='touch_id', color='interactor', nbins=max(w3['touch_id']), color_discrete_sequence=colors_discrete, labels={'touch_id':'Number of touches total'})

                return dmc.Card(
                    children=[
                        dmc.Text("Widget 3", size=20, weight=400),
                        dmc.Text("Text"),
                        dcc.Graph(figure=fig)
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                )

        @app.callback(
            Output('widget_4', 'children'),
            [Input('memory', 'data')]
        )
        def generate_widget4(df):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                w4 = df.copy()
                w4 = w4.loc[(w4['interactor'] != 'bot')]
                w4 = w4.groupby(['conversation_id', 'prediction', 'state']).count()['touch_id'].reset_index()
                fig = px.box(w4, x='prediction', y='touch_id', color='state', color_discrete_sequence=colors_discrete, labels={'prediction':'Label', 'touch_id': 'Number of Touches'})
                return dmc.Card(
                    children=[
                        dmc.Text("Widget 4", size=20, weight=400),
                        dmc.Text("Text"),
                        dcc.Graph(figure=fig)
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                )

        @app.callback(
            Output('widget_5', 'children'),
            [Input('memory', 'data')]
        )
        def generate_widget5(df):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                LayoutType = "cose" #@param ["random", "grid", "cose", "concentric", "breadthfirst"]
                edges_number = 200 #@param {type:"integer"}
                conversation_size = 5 #@param {type:"integer"}

                class Neo4jConnection:
                    def __init__(self, uri, user, pwd):
                        self.__uri = uri
                        self.__user = user
                        self.__pwd = pwd
                        self.__driver = None
                        try:
                            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
                        except Exception as e:
                            print("Failed to create the driver:", e)
                        
                    def close(self):
                        if self.__driver is not None:
                            self.__driver.close()
                        
                    def query(self, query, parameters=None, db=None):
                        assert self.__driver is not None, "Driver not initialized!"
                        session = None
                        response = None
                        try: 
                            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
                            response = list(session.run(query, parameters))
                        except Exception as e:
                            print("Query failed:", e)
                        finally: 
                            if session is not None:
                                session.close()
                        return response
                        

                conn = Neo4jConnection(uri="neo4j+s://b4a3ea40.databases.neo4j.io", user="user", pwd="pass")
                query_string = '''MATCH p=(m)-[r:MessageSent]-(n) where n.numMessages>'''+str(conversation_size)+''' RETURN p LIMIT '''+str(edges_number)
                nodes=[]
                simple_elements=[]

                for _ in conn.query(query_string):
                    for node in dict(_)['p'].nodes:
                        if node.element_id not in nodes:
                            nodes.append(node.element_id)
                            if 'P' in dict(node.items())['name']:
                                simple_elements.append({'data':{'id':str(node.element_id),'label':'Patient'},'classes':'red'})
                            else:
                                simple_elements.append({'data':{'id':str(node.element_id),'label':'Staff'}})
                for _ in conn.query(query_string):
                    for relation in dict(_)['p'].relationships:
                        simple_elements.append({'data': {'source': str(relation.nodes[0].element_id), 'target': str(relation.nodes[1].element_id),'id':str(relation.element_id)}})


                fig = cyto.Cytoscape(
                    layout={'name': LayoutType},
                    style={'width': '100%', 'height': '400px'},
                    elements=simple_elements,
                    stylesheet=[
                        # Group selectors
                        {'selector': 'edge',
                        'style': {
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier'
                        }},
                        {
                            'selector': 'node',
                            'style': {
                                'content': 'data(label)'
                            }
                        },

                        # Class selectors
                        {
                            'selector': '.red',
                            'style': {
                                'background-color': 'red',
                                'line-color': 'red'
                            }
                        },
                        {
                            'selector': '.triangle',
                            'style': {
                                'shape': 'triangle'
                            }
                        }
                    ]
                )
                # fig.show()
                return dmc.Card(
                    children=[
                        dmc.Text("Widget 5", size=20, weight=400),
                        dmc.Text("Text"),
                        dmc.Grid(
                            children=[
                                dmc.Col(html.Div(fig), span=5),
                                dmc.Col(html.Div("Empty Space"), span=2),
                                dmc.Col(html.Div(fig), span=5)
                            ]
                        )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                )

        @app.callback(
            Output('widget_6', 'children'),
            [Input('memory', 'data')]
        )
        def generate_widget6(df):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                w6 = df.copy()
                # bar graph of location with count of first messages
                w6bar = w6[w6['touch_order'] == 1].groupby('location').size().sort_values(ascending=False).to_frame().reset_index()
                w6bar.columns = ['location', 'count']
                # line graph of location with time to open
                w6line = w6[w6['touch_status'] == 'opened'][['conversation_id', 'touch_dt_tm', 'message_create_dt_tm', 'location']].groupby(['conversation_id']).first().reset_index()
                w6line['time_to_open'] = (w6line['touch_dt_tm'] - w6line['message_create_dt_tm']) / pd.Timedelta(hours=1)
                w6line = w6line[['location', 'time_to_open']].groupby('location').mean().reset_index()
                # w6line.head()
                w6 = w6bar.merge(w6line, on='location')
                # w6.head()
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(
                    go.Bar(x=w6['location'], y=w6['count'], name="Count of Messages"),
                    secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=w6['location'], y=w6['time_to_open'], name="Average Time to Open (hours)"),
                    secondary_y=True,
                )
                fig.update_layout(
                    title_text="PC Statistics"
                )
                # Set x-axis title
                fig.update_xaxes(title_text="Location")
                # Set y-axes titles
                fig.update_yaxes(title_text="Message Count", secondary_y=False)
                fig.update_yaxes(title_text="Average Time to Open (hours)", secondary_y=True)
                return dmc.Card(
                    children=[
                        dmc.Text("Widget 6", size=20, weight=400),
                        dmc.Text("Text"),
                        dcc.Graph(figure=fig)
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                )

        @app.callback(
            Output('widget_7', 'children'),
            [Input('memory', 'data')]
        )
        def generate_widget7(df):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                w7 = df.copy()
                w7['touch_tm'] = w7['touch_dt_tm'].dt.time
                w7 = w7.groupby('touch_tm').size().to_frame('Number in Category').reset_index()
                # w7.head()
                fig = px.bar(w7, x='touch_tm', y='Number in Category', color='Number in Category', color_continuous_scale=colors_discrete, \
                labels={'touch_dt_tm':'Time Message Touched', 'Number in Category':'Number of Unique Messages'})
                fig.update_traces(width=2)

                return dmc.Card(
                    children=[
                        dmc.Text("Widget 7", size=20, weight=400),
                        dmc.Text("Text"),
                        dcc.Graph(figure=fig)
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                )

        @app.callback(
            Output('widget_8', 'children'),
            [Input('memory', 'data')]
        )
        def generate_widget8(df):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                w8 = df.copy()
                w8 = w8[['conversation_id', 'touch_dt_tm', 'prediction', 'state']].groupby(['conversation_id']).agg(['first', 'last']).droplevel(axis=1, level=0).reset_index()
                w8.columns = ['conversation_id', 'first', 'last', 'prediction', 'drop1', 'state', 'drop2']
                w8 = w8.drop(['drop1', 'drop2'], axis=1)
                w8['resolution_time'] = ((w8['last'] - w8['first'])) / pd.Timedelta(hours=1)
                w8 = w8[w8['resolution_time'] > 0]
                # w8.head()
                fig = px.scatter(w8, y='prediction', x='resolution_time', color='state', color_discrete_sequence=colors_discrete, labels={'prediction':'Label', 'resolution_time':'Conversation Resolution in Hours'})
                # fig.show()
                return dmc.Card(
                    children=[
                        dmc.Text("Widget 8", size=20, weight=400),
                        dmc.Text("Text"),
                        dcc.Graph(figure=fig)
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                )


        @app.callback(
            Output('widget_9', 'children'),
            [Input('memory', 'data')]
        )
        def generate_widget9(df):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                w9 = df.copy()
                w9['message_create_dt'] = w9['message_create_dt_tm'].dt.date
                w9 = w9.groupby(['message_create_dt', 'message_type']).count().reset_index()
                fig=px.area(pd.crosstab(w9['message_create_dt'], w9['message_type'], values=w9['message_id'],aggfunc='max'), facet_col="message_type", title='Messages by Type', facet_col_wrap=4)
                return dmc.Card(
                    children=[
                        dmc.Text("Widget 9", size=20, weight=400),
                        dmc.Text("Text"),
                        dcc.Graph(figure=fig)
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                )

        @app.callback(
            Output('widget_10', 'children'),
            [Input('memory', 'data')]
        )
        def generate_widget10(df):
            df = pd.DataFrame(df)
            if df.empty:
                raise PreventUpdate
            else:
                df['touch_dt_tm']= pd.to_datetime(df['touch_dt_tm'])
                df['message_create_dt_tm']= pd.to_datetime(df['message_create_dt_tm'])
                df['message_delete_dt_tm']= pd.to_datetime(df['message_delete_dt_tm'])
                w10 = df.copy()
                w10['message_create_dt'] = pd.to_datetime(w10['message_create_dt_tm']).dt.date
                fig = px.bar(w10.groupby(['message_create_dt','prediction']).size().to_frame('Number in Category').reset_index(), x='message_create_dt', y='Number in Category',
                    color='prediction', color_discrete_sequence=colors_discrete, labels={'message_create_dt':'Day Message Created', 'Number in Category':'Number of Unique Messages'}, barmode='group')

                return dmc.Card(
                    children=[
                        dmc.Text("Widget 10", size=20, weight=400),
                        dmc.Text("Text"),
                        dcc.Graph(figure=fig)
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                )
    
        

        @app.callback(
        [Output('memory', 'data')],
        [Input('date-range-picker', 'value'),
        Input('emr_select', 'value'),
        Input('interactor_select', 'value'),
        Input('inbasket_select', 'value'),
        Input('msg_label_select', 'value'),
        Input('patient_initiated_select', 'value'),
        Input('location_select', 'value'),
        Input('entity_select', 'value'),
        Input('state_select', 'value')]
        )
        def filter_data(date_range, emr_select, interactor_select, inbasket_select, 
        msg_label_select, patient_initiated_select, location_select, entity_select, state_select):
            data = return_filtered_data(date_range, emr_select, interactor_select, inbasket_select, 
                msg_label_select, patient_initiated_select, location_select, entity_select, state_select)
            if df.empty:
                return pd.DataFrame()
            else:
                return [data.to_dict('records')]


