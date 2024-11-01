import panel as pn
import matplotlib as plt
from StockAPI import StockInfos 
import holoviews as hv
import pandas as pd

# Loads javascript dependencies and configures Panel (required)
pn.extension()
api = StockInfos()
api.loadstock("WYNN_stock_data.csv")


# WIDGET DECLARATIONS
# Search Widgets
time_period = pn.widgets.Select(name = "Time Frame", options = ['All', '1 Year', '6 Months', '3 Months', '1 Month'])
ma_length = pn.widgets.IntSlider(name="MA Length", start=1, end=200, step=10, value=10)
#checkbox for VWAP, MA on/off
show_ma = pn.widgets.Checkbox(name = "Show Moving Average (Green)", value = False)
show_vwap = pn.widgets.Checkbox(name = "Show Volume Weighted Average Price (Orange)", value = False)


# CALLBACK FUNCTIONS, 
def update_plot(time_period, show_ma, ma_length, show_vwap):
    """
    Creates a plot that takes values from the widgets we created. Will make a new StockInfos df of a sperified length and will add our studies on top of the plot if selected or not. 

        Args:
            time_period (pn.widgets.Select) = Select specified time frames. 
            show_ma (pn.widgets.Checkbox) = Returns a boolean wether moving averge is selected and shoule be showed.
            ma_length (pn.widgets.IntSlider) = Gives a value from the slider from 10 to 200 for the moving average length.
            show_vwap(pn.widgets.Checkbox) = Returns a boolean wether vwap is selected and should be showed.

        
        Returns:
            plot = a plot of our data with certain time frame, vwap, ma, and ma length selected
        """
    df_filtered = api.FinalStockInfo.copy()
    
    # Filter data based on time period
    if time_period != 'All':
        last_date = df_filtered['date'].max()
        if time_period == '1 Year':
            df_filtered = df_filtered[df_filtered['date'] >= f"{last_date.year - 1}-01-01"]
        elif time_period == '6 Months':
            df_filtered = df_filtered[df_filtered['date'] >= last_date - pd.DateOffset(months=6)]
        elif time_period == '3 Months':
            df_filtered = df_filtered[df_filtered['date'] >= last_date - pd.DateOffset(months=3)]
        elif time_period == '1 Month':
            df_filtered = df_filtered[df_filtered['date'] >= last_date - pd.DateOffset(months=1)]

    # Create initial plot
    plot = hv.Curve(df_filtered, 'date', 'close').opts(title='Stock Price', ylabel='Price', xlabel='Date', width=800, height=400)

    if show_ma:
        api.getMA(ma_length)  # Update moving average
        plot *= hv.Curve(df_filtered, 'date', 'Moving_Average').opts(color='green')

    if show_vwap:
        api.getVWAP()  # Update VWAP
        plot *= hv.Curve(df_filtered, 'date', 'VWAP').opts(color='orange')

    return plot

# CALLBACK BINDINGS (Connecting widgets to callback functions)
plot = pn.bind(update_plot, time_period, show_ma, ma_length, show_vwap)

# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 400

param_card = pn.Card(
    pn.Column(
        time_period,
        show_ma,
        ma_length,
        show_vwap
    ),

    title="Plot", width=card_width, collapsed=True
)


# LAYOUT

layout = pn.template.FastListTemplate(
    title="WYNN Stock Analysis",
    sidebar=[
        param_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Chart", plot),  # Replace None with callback binding
            active=1  # Which tab is active by default?
        )

    ],
    header_background='#a93226'

).servable()

layout.show()

"""

have origional data as df

make a widget that helps select a variable

make a graph, etc with a parameter

make an update graph function with bind from widget
that updates the paramater passed to the origional graph

"""