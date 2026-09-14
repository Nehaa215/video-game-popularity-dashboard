
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("final_dataset.csv")

app = dash.Dash(__name__)

server = app.server

# PUT YOUR app.layout CODE HERE

# PUT YOUR @app.callback CODE HERE

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False
    )
