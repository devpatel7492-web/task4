import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("Pasted text.txt")

# Fix columns
df.columns = ["Sales", "Date", "Region"]

# Convert types
df["Date"] = pd.to_datetime(df["Date"])
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

# Sort
df = df.sort_values(by="Date")

# Convert Date to string (stable plotting)
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

# Create Dash app
app = dash.Dash(__name__)

# 🎨 Layout with styling
app.layout = html.Div(style={
    "backgroundColor": "#f4f6f9",
    "padding": "20px",
    "fontFamily": "Arial"
}, children=[

    html.H1(
        "🍬 Soul Foods Sales Dashboard",
        style={
            "textAlign": "center",
            "color": "#2c3e50"
        }
    ),

    html.P(
        "Analyze Pink Morsel sales before and after the price increase.",
        style={"textAlign": "center"}
    ),

    # ✅ RADIO BUTTON FILTER
    html.Div([
        html.Label("Select Region:", style={"fontWeight": "bold"}),

        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            inline=True,
            style={"marginTop": "10px"}
        )
    ], style={
        "textAlign": "center",
        "marginBottom": "20px"
    }),

    # GRAPH
    dcc.Graph(id="sales-graph")

])


# ✅ CALLBACK (IMPORTANT)
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):

    # Filter data
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["Region"].str.lower() == selected_region]

    # Create figure
    fig = px.line(
        filtered_df,
        x="Date",
        y="Sales",
        color="Region",
        title="Pink Morsel Sales Over Time"
    )

    # ✅ Vertical line (SAFE method)
    fig.add_shape(
        type="line",
        x0="2021-01-15",
        x1="2021-01-15",
        y0=0,
        y1=filtered_df["Sales"].max(),
        line=dict(color="red", dash="dash"),
    )

    fig.add_annotation(
        x="2021-01-15",
        y=filtered_df["Sales"].max(),
        text="Price Increase",
        showarrow=True
    )

    return fig


# Run app
if __name__ == '__main__':
    app.run(debug=True)