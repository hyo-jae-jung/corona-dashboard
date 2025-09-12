# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from data import countries_df, totals_df, dropdown_options, make_global_df, make_country_df
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.2/reset.min.css",# css 비우기. "css reset cdn"로 검색
    "https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap", # 폰트 적용. 구글 폰트 Open Sans
]

app = Dash(__name__, external_stylesheets=stylesheets)

server = app.server

bubble_map = px.scatter_geo(
    countries_df, 
    size="Confirmed",
    size_max=40,
    title="Confirmed By Country",
    hover_name="Country_Region", 
    color="Confirmed", 
    locations="Country_Region", 
    locationmode="country names", 
    template="plotly_dark",
    color_continuous_scale=px.colors.sequential.Oryel, 
    projection="natural earth",
    hover_data={
        "Confirmed": ":,d",
        "Deaths": ":,d",
        "Recovered": ":,d",
        "Country_Region": False
    })

bubble_map.update_layout(
    margin=dict(l=0,r=0,t=50,b=0), coloraxis_colorbar=dict(xanchor="left", x=0)
)

bars_graph = px.bar(
    totals_df, 
    hover_data={"count":":,"},
    x="condition",
    y="count", 
    template="plotly_dark", 
    title="Total Global Cases",
    labels={
        "condition":"Condition",
        "count":"Count",
        "color":"Condition",
        },
    )
bars_graph.update_traces(marker_color=["#e74c3c","#8e44ad","#1abc9c"])

app.layout = html.Div(
    style={
        "minHeight":"100vh",
        "backgroundColor":"#111111",
        "color":"white",
        "fontFamily":"Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign":"center","paddingTop":"50px", "marginBottom": 100},
            children=[html.H1('Corona Dashboard',style={"fontSize":40})],
        ),
        html.Div(
            style={"display":"grid", "gap":50, "gridTemplateColumns":"repeat(4, 1fr)"},
            children=[
                html.Div(
                    style={"grid-column":"span 3"}, 
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(children=[make_table(countries_df)]),
            ],
        ),
        html.Div(
            style={"display":"grid", "gap":50, "gridTemplateColumns":"repeat(4, 1fr)"},
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width":320,
                                "margin":"0 auto",
                                "color":"#111111",
                            },
                            placeholder="Select a Country",
                            id="country",
                            options=[
                                {"label":country, "value":country}
                                for country in dropdown_options
                            ],
                        ),
                        dcc.Graph(id="country_graph", style={"height":"600px"})
                    ],
                ),
            ],
        ),
    ],
)

@app.callback(
    Output("country_graph", "figure"),
    [
    Input("country", "value")
    ]
)
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()
    fig = px.line(
        df, 
        x="date", 
        y=["confirmed","deaths","recovered"],
        template="plotly_dark",
        labels={
            "value":"cases",
            "variable":"Condition",
            "date":"Date",
        },
        hover_data={
            "value":":,",
            "variable": False,
            "date":False,
            },
        )
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#8e44ad"
    fig["data"][2]["line"]["color"] = "#1abc9c"
    return fig

