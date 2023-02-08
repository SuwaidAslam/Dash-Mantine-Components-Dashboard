import dash_mantine_components as dmc
from dash import dcc, html
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import dash_cytoscape as cyto
from neo4j import GraphDatabase
import xml.etree.ElementTree as ET


# Define color palette
colors_discrete = ['#3DC5FC', '#009DF3', '#30FEC8', '#1985B0', '#FC5676', '#FCF123', '#B0A821']

def get_card(title, text_arr):
    return dmc.Card(
        children=[
            dmc.Group(
                [
                    dmc.Text(title, weight=500, color="dimmed"),
                ],
                position="center",
                mt="xs",
                mb="xs",
            ),
            dmc.Grid(
                children=[
                    dmc.Col(html.H3("State2"), span=4),
                    dmc.Col(span=4),
                    dmc.Col(html.H3(text_arr[0]), span=4),
                    dmc.Col(html.H3("State1"), span=4),
                    dmc.Col(span=4),
                    dmc.Col(html.H3(text_arr[1]), span=4),
                ],
                justify="center",
                align="center",
                gutter=0,
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={'margin-top' : '2%'},
    )

def get_card_second(title, div_elem, id):
    return dmc.Card(
        children=[
            dmc.Group(
                [
                    dmc.Text(title, weight=500, color="dimmed"),
                ],
                position="center",
                mt="md",
                mb="xs",
            ),
             dmc.Group(
                [
                    html.Div(div_elem, id=id),
                ],
                position="center",
                spacing='xl'
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={'margin-top' : '15%'},
    )


def get_calculation_variables():
    return  html.Div([
        dmc.Group(
                [
                    dmc.Text("Calculation Variables", weight=500),
                ],
                position="center",
                mt="md",
                mb="xs",
        ),
        dmc.Grid(
            children=[
                dmc.Col(html.P('Time per Touch'), span=6),
                dmc.Col(dmc.TextInput(value=3, id='time_per_touch'), span=6),
                dmc.Col(html.P('Dollar per Minute'), span=6),
                dmc.Col(dmc.TextInput(value=1.16, id='dollar_per_min'), span=6),
                dmc.Col(html.P('Urgent Visit Conversation Rate 50%'), span=6),
                dmc.Col(dmc.TextInput(value=0.5, id='visit_conversation'), span=6),
                dmc.Col(html.P('Relative Value Unit (RVU)'), span=6),
                dmc.Col(dmc.TextInput(value=1.3,id='relative_value_unit'), span=6),
                dmc.Col(html.P('Dollar per RVU'), span=6),
                dmc.Col(dmc.TextInput(value=110, id='dollar_per_rvu'), span=6),
                dmc.Col(html.P('Gross Margin'), span=6),
                dmc.Col(dmc.TextInput(value=0.6, id='gross_margin'), span=6),
            ],
            gutter=0,
        ),  
        dmc.Button(
            "Reset Values",
            variant="light",
            color="gray",
            fullWidth=True,
            mt="md",
            radius="md",
            id='variables_reset'
        ),
    ], style={'margin-top' : '15%'})


def generate_widget1_card():
    radio_data = [["M", "Month"], ["D", "Day"], ["H", "Hour"], ["T", "Minute"]]
    return dmc.Card(
                children=[
                    dmc.Text("Widget 1", size=20, weight=400),
                    dmc.Text("Text"),
                    dmc.RadioGroup(
                        [dmc.Radio(l, value=k) for k, l in radio_data],
                        id="radiogroup-resample",
                        value="H",
                        size="sm",
                        mt=10,
                    ),
                    dcc.Graph(id="widget1_figure")
                ],
                withBorder=True,
                shadow="sm",
                radius="lg",
                style={"height": "100%"},
            )