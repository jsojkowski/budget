from common.consts import VIS_DATA_DIR
import plotly.express as px
import plotly.io as pio

def pie_chart(categories: list[str], values: list[float], title: str) -> None:

    # Create the figure with plotly.express
    fig = px.pie(values=values, names=categories, title='Pie Chart with Plotly Express (No explicit DF)')

    # Display the chart
    fig.show()
        # Save the plot as a PNG file
    pio.write_image(fig, VIS_DATA_DIR / f'{title.replace(" ", "-")}.png')
