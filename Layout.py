from dash import dcc, html, Dash
import dash_mantine_components as dmc
from components import *
from Data import *
from datetime import date
import pandas as pd





class AppLayout:
    def __init__(self):
        pass
    
    
    # this method generates content Page Layout
    def generateContentLayout(self):
        c1_data, c2_data, c3_data, c4_data = card_row1_data()
        msg_label = df['prediction'].unique()
        entity = df['entity'].unique()
        location = [str(item) for item in df['location'].unique()]
        state = df['state'].unique()
        patient_initiated = [str(item) for item in df['patient_initiated'].unique()]
        emr = df['emr'].unique()
        interactor_type = [str(item) for item in df['interactor'].unique()]
        inbasket_assignment = [str(item) for item in df['predicted_id'].unique()]

        state1_df = df[df['state'] == 'state1']
        state2_df = df[df['state'] == 'state2']
        starting_state1_date = state1_df['message_create_dt_tm'].min()
        ending_state1_date = state1_df['message_create_dt_tm'].max()
        starting_state2_date = state2_df['message_create_dt_tm'].min()
        ending_state2_date = state2_df['message_create_dt_tm'].max()


        if pd.isnull(starting_state1_date):
            state1_period = "no time period"
        else:
            state1_period = f"""{starting_state1_date.strftime("%d-%m-%Y")} to {ending_state1_date.strftime("%d-%m-%Y")}"""
            
        if pd.isnull(starting_state2_date):
            state2_period = "no time period"
        else:
            state2_period = f"""{starting_state2_date.strftime("%d-%m-%Y")} to {ending_state2_date.strftime("%d-%m-%Y")}"""

        
        return dmc.MantineProvider(
            theme={
                "colorScheme": "light",
            },
            children=[
                html.Div([
                    dmc.Text("LIJC - Overview", weight=500, size=30),
                    dmc.Text("Welcome to your Dashboard for the LIJC model.", weight=100, size=16),
                    dmc.Text(f"Your state2 period is set to {state2_period}. The state1 period is set to LIJC model {state1_period}.", weight=100, size=16),
                    html.Br(),
                    dmc.SimpleGrid(
                        cols=4,
                        spacing="lg",
                        children=[
                            get_card("UPIM", c1_data),
                            get_card("ATPM", c2_data),
                            get_card("RREM", c3_data),
                            get_card("URG", c4_data),
                        ]
                    ),
                    dmc.SimpleGrid(
                        cols=4,
                        spacing="lg",
                        children=[
                            get_calculation_variables(),
                            get_card_second("Cost Reduction", "", "cost_reduction_txt"),
                            get_card_second("Revenue", "", "revenue_txt"),
                            get_card_second("Total Impact", "", "total_impact_txt"),
                        ]
                    ),
                ], className='lijc_overview_section'),

                html.Div([
                    dmc.Text("LIJC - Analytics", weight=500, size=30),
                    dmc.Grid(
                        children=[
                            dmc.Col([
                                dmc.Group(
                                    [
                                        dmc.Text("Filters", weight=400, size=20),
                                        dmc.DateRangePicker(
                                            id="date-range-picker",
                                            label="Date Range",
                                            inputFormat="D/M/YYYY",
                                            value=[date(2022, 9, 16), date(2022, 9, 30)],
                                            style={"width": 330},
                                        ),
                                        dmc.Select(
                                            label="EMR",
                                            id="emr_select",
                                            value=emr[0],
                                            data=emr,
                                            style={"width": "100%"},
                                        ),
                                        dmc.Select(
                                            label="Interactor Type",
                                            id="interactor_select",
                                            value=interactor_type[0],
                                            data=interactor_type,
                                            style={"width": "100%"},
                                        ),
                                        dmc.Select(
                                            label="Inbasket Assignment",
                                            id="inbasket_select",
                                            value=inbasket_assignment[0],
                                            data=inbasket_assignment,
                                            style={"width": "100%"},
                                        ),
                                        dmc.Select(
                                            label="Message Label",
                                            id="msg_label_select",
                                            value=msg_label[0],
                                            data=msg_label,
                                            style={"width": "100%"},
                                        ),
                                        dmc.Select(
                                            label="Patient-Initiated",
                                            id="patient_initiated_select",
                                            value=patient_initiated[0],
                                            data=patient_initiated,
                                            style={"width": "100%"},
                                        ),
                                        dmc.Select(
                                            label="Location",
                                            id="location_select",
                                            value=location[0],
                                            data=location,
                                            style={"width": "100%"},
                                        ),
                                        dmc.Select(
                                            label="Entity",
                                            id="entity_select",
                                            value=entity[0],
                                            data=entity,
                                            style={"width": "100%"},
                                        ),
                                        dmc.Select(
                                            label="State",
                                            id="state_select",
                                            value=state[0],
                                            data=state,
                                            style={"width": "100%"},
                                        ),
                                    ],
                                    position="center",
                                    mt="md",
                                    mb="xs",
                                ),
                            ], span=2),
                            dcc.Store(id='memory'),
                            dmc.Col([
                                dmc.Grid(
                                    children=[
                                        dmc.Col(id="widget_1", children=generate_widget1_card(), span=8),
                                        dmc.Col(id= 'widget_2', span=4),
                                        dmc.Col(id= 'widget_3', span=8),
                                        dmc.Col(id= 'widget_4', span=4),
                                        dmc.Col(id= 'widget_5', span=12),
                                        dmc.Col(id= 'widget_6', span=12),
                                        dmc.Col(id= 'widget_7', span=12),
                                        dmc.Col(id= 'widget_8', span=12),
                                        dmc.Col(id= 'widget_9', span=12),
                                        dmc.Col(id= 'widget_10', span=12),
                                    ],
                                    gutter="xl",
                                )
                            ], span=10),
                        ],
                        gutter="xl",
                        style={'margin-top' : '2%'}
                    ),

                ], className='lijc_analytics_section'),
        ])
    
    # ------This method generates Overall App's Layout ---------
    def getAppLayout(self, app : Dash):
        layout = html.Div(children=[
            html.Div(
                children=[
                        html.A(
                            html.Img(
                                src=app.get_asset_url("logo.png"),
                                className="logo_img",
                            ),
                        ),
                        dmc.Avatar(
                            src="https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes"
                            "-computer-wallpaper-thumbnail.png",
                            size="lg",
                            radius="xl",
                            style={'float' : 'right'}
                        ),
                ], className='header'
            ),
            self.generateContentLayout()
            ])
        return layout

    # ------------------ Layout Settings End --------------------