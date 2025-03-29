import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

world_cup_data = pd.DataFrame({
    "year" : [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
    "winner": ["URY", "ITA", "ITA", "URY", "DEU", "BRA", "BRA", "GBR", "BRA", "DEU", "ARG", "ITA", "ARG", "DEU", "BRA", "FRA", "BRA", "ITA", "ESP", "DEU", "FRA", "ARG"],
    "runner_up": ["ARG", "CSK", "HUN", "BRA", "HUN", "SWE", "CSK", "DEU", "ITA", "NLD", "NLD", "DEU", "DEU", "ARG", "ITA", "BRA", "DEU", "FRA", "NLD", "ARG", "CRO", "FRA"]
})

dropdown_data = []
for i, r in world_cup_data.iterrows():
    option = {
        "label" : r["year"],
        "value" : r["year"]
    }
    dropdown_data.append(option)


win_data = pd.DataFrame({
    "country" : ["URY", "ITA", "DEU", "BRA", "GBR", "ARG", "FRA", "ESP", "CSK", "HUN", "SWE", "NLD", "CRO"],
    "wins" : [2, 4, 4, 5, 1, 3, 2, 1 , 0, 0, 0, 0, 0],
    "runner_up" : [0, 2, 4, 2, 0, 3, 2, 0, 2, 2, 1, 3, 1]
})

win_data["shading_weight"] = win_data["wins"] * 2 + win_data["runner_up"]

app = dash.Dash()

app.layout = html.Div([
    html.H1("World Cup Tracker", style={"textAlign": "center", "margin-bottom": "10px"}),
    html.Fieldset([
        html.Legend("Data Choices"),

        html.Label("Data Choice : "),
        dcc.RadioItems(id="radio", options=[
            {"label" : "All Countries     ", "value" : "o1"},
            {"label" : "Country Select    ", "value" : "o2"},
            {"label" : "Year Select       ", "value" : "o3"}
        ], value="o1", inline=True),
        
        html.Label("Country Code if \"Country Select\" Selected: "),
        dcc.Input(id="country", type="text"),

        html.Br(),
        
        html.Label("Year if Option 3 Selected: "),
        dcc.Dropdown(id="year", options=dropdown_data)
       
    ], style={"margin" : "5px"}),

    html.Div([
        dcc.Graph(id="map_graph"),
    ]),   
])


@callback(
    Output("map_graph", "figure"),
    [Input("radio", "value"),
    Input("country", "value"),
    Input("year", "value")]
)

def update_graph(radio, country, year):
    
    fig = go.Figure()
    
    if radio == "o1":
        fig = px.choropleth(
            win_data,
            locations="country",
            locationmode="ISO-3",
            color="shading_weight",
            color_continuous_scale="Viridis",
            hover_name="country",
            hover_data={"wins" : True, "runner_up" : True, "country" : False, "shading_weight" : False}
        )
        return fig

    elif radio == "o2":

        country = country.upper()
        
        o2_data = win_data.copy()
        
        if country not in o2_data["country"].values:
            o2_data = pd.concat([o2_data, pd.DataFrame({"country": [country], "wins": [0], "runner_up": [0], "shading_weight": [0]})])

        cond = o2_data["country"] == country
        
        filter_data = o2_data[cond]
        
        fig = px.choropleth(
            filter_data,
            locations="country",
            locationmode="ISO-3",
            color="shading_weight",
            color_continuous_scale="Viridis",
            hover_name="country",
            hover_data={"wins" : True, "runner_up" : True, "country" : False, "shading_weight" : False}
        )
        
        return fig
        
    elif radio == "o3":
        if year is None:
            return fig
        
        o3_data = world_cup_data.copy()

        cond = o3_data["year"] == year

        filter_data = o3_data[cond].iloc[0]

        winner = filter_data["winner"]
        runner_up = filter_data["runner_up"]

        fig.add_trace(go.Choropleth(
            locations=[winner],
            z=[1],
            locationmode="ISO-3",
            colorscale=[[0,"green"], [1,"green"]],
            showscale=False,
            name="Winner",
        ))

        fig.add_trace(go.Choropleth(
            locations=[runner_up],
            z=[1],
            locationmode="ISO-3",
            colorscale=[[0,"red"], [1,"red"]],
            showscale=False,
            name="Runner Up",
        ))

        return fig



if __name__ == "__main__":
    app.run(debug=True)
    server = app.server
        
