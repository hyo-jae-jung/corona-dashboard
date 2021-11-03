import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import countries_df
from builders import make_table


stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(countries_df, 
                     size="Confirmed",
                     locations="Country_Region",
                     locationmode="country names",
                    color="Confirmed",
                     hover_name="Country_Region",
                     size_max=40,
                     template="plotly_dark",
                     projection="natural earth",
                     hover_data={
                         "Confirmed":":,.0f",
                         "Deaths":":,.0f",
                         "Recovered":":,.0f",
                         "Country_Region":False
                     }
                    )

app.layout = html.Div(
    style={
        "textAlign": "center",
        "minHeight": "100vh",
        "backgroundColor": "black",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif"
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})]
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(figure=bubble_map)
                    ]
                ),
                html.Div(
                    children=[
                        make_table(countries_df)
                    ]
                )
            ]
        )
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True)
