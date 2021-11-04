import dash
from dash import dcc, html
import plotly.express as px
from data import countries_df,totals_df,dropdown_options,make_global_and_country_df
from builders import make_table
from dash.dependencies import Input, Output


stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

app.title = "Corona Dashboard"

server = app.server

bubble_map = px.scatter_geo(countries_df, 
                     size="Confirmed",
                     locations="Country_Region",
                     locationmode="country names",
                    color="Confirmed",
                     hover_name="Country_Region",
                     size_max=40,
                     title="Confirmed By Country",
                     template="plotly_dark",
                     projection="natural earth",
                     color_continuous_scale =px.colors.sequential.Oryel,
                     hover_data={
                         "Confirmed":":,.0f",
                         "Deaths":":,.0f",
                         "Recovered":":,.0f",
                         "Country_Region":False
                     }
                    )
bubble_map.update_layout(
    margin=dict(l=0,r=0,t=50,b=0),
    coloraxis_colorbar=dict(xanchor="left", x=0)
)

bars_graph =px.bar(
            totals_df,
            x="condition",
            y="count",
            hover_data={'count':":,"},
            template="plotly_dark",
            title="Total Global Cases",
            labels={"condition":"Condition","count":"Count","color":"Condition"},
           )
bars_graph.update_traces(
               marker_color=["#e74c3c", "#8e44ad", "#27ae60"]
           )

app.layout = html.Div(
    style={
        "textAlign": "center",
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif"
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px", "marginBottom": 100},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})]
        ),
        html.Div(
            style={
                "display":"grid",
                "gap":50,
                "gridTemplateColumns":"repeat(4,1fr)"
            },
            children=[
                html.Div(
                    style={"grid-column":"span 3"},
                    children=[dcc.Graph(figure=bubble_map)]
                    ),
                html.Div(children=[make_table(countries_df)])
            ],
        ),
        html.Div(
            style={
                "display":"grid",
                "gap":50,
                "gridTemplateColumns":"repeat(4,1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111",
                                },
                                placeholder="Select a Country",
                                id="country",
                                options=[
                                    {"label":country, "value":country}
                                    for country in dropdown_options
                                    ]
                                ),
                        dcc.Graph(id="country-graph"),
                    ]
                )
            ]
        ),

    ],
)

@app.callback(
    Output("country-graph","figure"),
    [
        Input("country","value")
    ]
)
def update_hello(value):
    df =make_global_and_country_df(value)
    fig = px.line(df, x="date", y=["confirmed","deaths","recovered"],
              template="plotly_dark",
              labels={
                    'value':'Cases',
                    'variable':'Condition',
                    'date':'Date'
                    },
                hover_data={
                    'value':':,',
                    'variable':False,
                    'date':False
                }
             )
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#8e44ad"
    fig["data"][2]["line"]["color"] = "#27ae60"
    return fig