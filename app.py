import os
import pandas as pd
import plotly.express as px

from dash import Dash, dcc, html, Input, Output


# =========================================================
# 1. LOAD DATA
# =========================================================

DATA_FILE = "final_dataset.csv"

df = pd.read_csv(DATA_FILE)


# =========================================================
# 2. BASIC DATA PREPARATION
# =========================================================

# Convert year to numeric
df["Year_of_Release"] = pd.to_numeric(
    df["Year_of_Release"],
    errors="coerce"
)

# Convert sales columns to numeric
sales_columns = [
    "NA_Sales",
    "EU_Sales",
    "JP_Sales",
    "Other_Sales",
    "Global_Sales"
]

for col in sales_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows where important values are missing
df = df.dropna(
    subset=["Name", "Platform", "Genre", "Global_Sales", "Popularity_Level"]
)

# Make popularity a string
df["Popularity_Level"] = df["Popularity_Level"].astype(str)


# =========================================================
# 3. CREATE DASH APP
# =========================================================

app = Dash(__name__)

server = app.server


# =========================================================
# 4. DROPDOWN VALUES
# =========================================================

genre_options = [
    {"label": genre, "value": genre}
    for genre in sorted(df["Genre"].dropna().unique())
]

platform_options = [
    {"label": platform, "value": platform}
    for platform in sorted(df["Platform"].dropna().unique())
]

popularity_options = [
    {"label": level, "value": level}
    for level in sorted(df["Popularity_Level"].dropna().unique())
]


# =========================================================
# 5. DASHBOARD LAYOUT
# =========================================================

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "padding": "20px",
        "backgroundColor": "#f5f6fa"
    },

    children=[

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        html.H1(
            "Video Game Popularity Dashboard",
            style={
                "textAlign": "center",
                "marginBottom": "5px"
            }
        ),

        html.P(
            "Predicting the Popularity of Video Games through Data Analytics",
            style={
                "textAlign": "center",
                "fontSize": "18px"
            }
        ),

        html.Hr(),


        # -------------------------------------------------
        # FILTERS
        # -------------------------------------------------

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
                "marginBottom": "25px"
            },

            children=[

                html.Div(
                    style={"flex": "1", "minWidth": "220px"},
                    children=[
                        html.Label("Select Genre"),
                        dcc.Dropdown(
                            id="genre-filter",
                            options=genre_options,
                            placeholder="All Genres",
                            multi=True
                        )
                    ]
                ),

                html.Div(
                    style={"flex": "1", "minWidth": "220px"},
                    children=[
                        html.Label("Select Platform"),
                        dcc.Dropdown(
                            id="platform-filter",
                            options=platform_options,
                            placeholder="All Platforms",
                            multi=True
                        )
                    ]
                ),

                html.Div(
                    style={"flex": "1", "minWidth": "220px"},
                    children=[
                        html.Label("Select Popularity Level"),
                        dcc.Dropdown(
                            id="popularity-filter",
                            options=popularity_options,
                            placeholder="All Popularity Levels",
                            multi=True
                        )
                    ]
                )
            ]
        ),


        # -------------------------------------------------
        # KPI CARDS
        # -------------------------------------------------

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": "15px",
                "marginBottom": "30px"
            },

            children=[

                html.Div(
                    id="total-games",
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"
                    }
                ),

                html.Div(
                    id="global-sales",
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"
                    }
                ),

                html.Div(
                    id="average-sales",
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"
                    }
                ),

                html.Div(
                    id="high-popularity",
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "boxShadow": "0 2px 5px rgba(0,0,0,0.1)"
                    }
                )
            ]
        ),


        # -------------------------------------------------
        # ROW 1
        # -------------------------------------------------

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px"
            },

            children=[

                dcc.Graph(id="popularity-chart"),

                dcc.Graph(id="genre-chart")
            ]
        ),


        # -------------------------------------------------
        # ROW 2
        # -------------------------------------------------

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px"
            },

            children=[

                dcc.Graph(id="platform-chart"),

                dcc.Graph(id="publisher-chart")
            ]
        ),


        # -------------------------------------------------
        # ROW 3
        # -------------------------------------------------

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px"
            },

            children=[

                dcc.Graph(id="year-chart"),

                dcc.Graph(id="regional-sales-chart")
            ]
        ),


        # -------------------------------------------------
        # ROW 4
        # -------------------------------------------------

        html.Div(
            style={
                "marginTop": "20px"
            },

            children=[

                dcc.Graph(id="critic-user-chart")
            ]
        ),

        html.Hr(),

        html.P(
            "Research Project: Predicting the Popularity of Video Games through Data Analytics",
            style={
                "textAlign": "center",
                "fontSize": "14px"
            }
        )
    ]
)


# =========================================================
# 6. CALLBACK
# =========================================================

@app.callback(

    Output("total-games", "children"),
    Output("global-sales", "children"),
    Output("average-sales", "children"),
    Output("high-popularity", "children"),

    Output("popularity-chart", "figure"),
    Output("genre-chart", "figure"),
    Output("platform-chart", "figure"),
    Output("publisher-chart", "figure"),
    Output("year-chart", "figure"),
    Output("regional-sales-chart", "figure"),
    Output("critic-user-chart", "figure"),

    Input("genre-filter", "value"),
    Input("platform-filter", "value"),
    Input("popularity-filter", "value")
)

def update_dashboard(
    selected_genres,
    selected_platforms,
    selected_popularity
):

    # -----------------------------------------------------
    # FILTER DATA
    # -----------------------------------------------------

    filtered_df = df.copy()

    if selected_genres:
        filtered_df = filtered_df[
            filtered_df["Genre"].isin(selected_genres)
        ]

    if selected_platforms:
        filtered_df = filtered_df[
            filtered_df["Platform"].isin(selected_platforms)
        ]

    if selected_popularity:
        filtered_df = filtered_df[
            filtered_df["Popularity_Level"].isin(
                selected_popularity
            )
        ]


    # -----------------------------------------------------
    # KPI VALUES
    # -----------------------------------------------------

    total_games = len(filtered_df)

    total_global_sales = filtered_df["Global_Sales"].sum()

    average_global_sales = filtered_df["Global_Sales"].mean()

    high_popularity_count = (
        filtered_df["Popularity_Level"]
        .astype(str)
        .str.lower()
        .eq("high")
        .sum()
    )


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    total_games_card = [

        html.H3("Total Games"),

        html.H2(
            f"{total_games:,}"
        )
    ]

    global_sales_card = [

        html.H3("Total Global Sales"),

        html.H2(
            f"{total_global_sales:.2f} M"
        )
    ]

    average_sales_card = [

        html.H3("Average Global Sales"),

        html.H2(
            f"{average_global_sales:.2f} M"
        )
    ]

    high_popularity_card = [

        html.H3("High Popularity Games"),

        html.H2(
            f"{high_popularity_count:,}"
        )
    ]


    # -----------------------------------------------------
    # POPULARITY DISTRIBUTION
    # -----------------------------------------------------

    popularity_data = (
        filtered_df["Popularity_Level"]
        .value_counts()
        .reset_index()
    )

    popularity_data.columns = [
        "Popularity_Level",
        "Count"
    ]

    popularity_fig = px.bar(
        popularity_data,
        x="Popularity_Level",
        y="Count",
        title="Popularity Level Distribution",
        labels={
            "Popularity_Level": "Popularity Level",
            "Count": "Number of Games"
        }
    )


    # -----------------------------------------------------
    # GENRE ANALYSIS
    # -----------------------------------------------------

    genre_data = (
        filtered_df
        .groupby("Genre", as_index=False)["Global_Sales"]
        .sum()
        .sort_values(
            "Global_Sales",
            ascending=False
        )
    )

    genre_fig = px.bar(
        genre_data,
        x="Genre",
        y="Global_Sales",
        title="Genre vs Global Sales",
        labels={
            "Global_Sales": "Global Sales (Millions)"
        }
    )


    # -----------------------------------------------------
    # PLATFORM ANALYSIS
    # -----------------------------------------------------

    platform_data = (
        filtered_df
        .groupby("Platform", as_index=False)["Global_Sales"]
        .sum()
        .sort_values(
            "Global_Sales",
            ascending=False
        )
        .head(15)
    )

    platform_fig = px.bar(
        platform_data,
        x="Platform",
        y="Global_Sales",
        title="Top Platforms by Global Sales",
        labels={
            "Global_Sales": "Global Sales (Millions)"
        }
    )


    # -----------------------------------------------------
    # PUBLISHER ANALYSIS
    # -----------------------------------------------------

    publisher_data = (
        filtered_df
        .groupby("Publisher", as_index=False)["Global_Sales"]
        .sum()
        .sort_values(
            "Global_Sales",
            ascending=False
        )
        .head(10)
    )

    publisher_fig = px.bar(
        publisher_data,
        x="Publisher",
        y="Global_Sales",
        title="Top 10 Publishers by Global Sales",
        labels={
            "Global_Sales": "Global Sales (Millions)"
        }
    )


    # -----------------------------------------------------
    # YEAR-WISE TREND
    # -----------------------------------------------------

    year_data = (
        filtered_df
        .dropna(subset=["Year_of_Release"])
        .groupby(
            "Year_of_Release",
            as_index=False
        )["Global_Sales"]
        .sum()
        .sort_values("Year_of_Release")
    )

    year_fig = px.line(
        year_data,
        x="Year_of_Release",
        y="Global_Sales",
        markers=True,
        title="Year-wise Global Sales Trend",
        labels={
            "Year_of_Release": "Release Year",
            "Global_Sales": "Global Sales (Millions)"
        }
    )


    # -----------------------------------------------------
    # REGIONAL SALES
    # -----------------------------------------------------

    regional_sales = pd.DataFrame({

        "Region": [
            "North America",
            "Europe",
            "Japan",
            "Other"
        ],

        "Sales": [

            filtered_df["NA_Sales"].sum(),

            filtered_df["EU_Sales"].sum(),

            filtered_df["JP_Sales"].sum(),

            filtered_df["Other_Sales"].sum()
        ]
    })

    regional_fig = px.bar(
        regional_sales,
        x="Region",
        y="Sales",
        title="Regional Sales Distribution",
        labels={
            "Sales": "Sales (Millions)"
        }
    )


    # -----------------------------------------------------
    # CRITIC SCORE VS GLOBAL SALES
    # -----------------------------------------------------

    score_data = filtered_df.dropna(
        subset=["Critic_Score", "Global_Sales"]
    )

    critic_fig = px.scatter(
        score_data,
        x="Critic_Score",
        y="Global_Sales",
        hover_data=["Name", "Genre", "Platform"],
        title="Critic Score vs Global Sales",
        labels={
            "Critic_Score": "Critic Score",
            "Global_Sales": "Global Sales (Millions)"
        }
    )


    # -----------------------------------------------------
    # RETURN EVERYTHING
    # -----------------------------------------------------

    return (

        total_games_card,

        global_sales_card,

        average_sales_card,

        high_popularity_card,

        popularity_fig,

        genre_fig,

        platform_fig,

        publisher_fig,

        year_fig,

        regional_fig,

        critic_fig
    )


# =========================================================
# 7. RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050)),
        debug=False
    )
