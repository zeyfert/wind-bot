import io
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def create_graph(x, y):
    """Build a digram based on the data from OpenWeather API.

    Args:
        x (list): list of values for x axis
        y (list): list of values for y axis

    Returns:
        Diagram is like bytes object
    """
    figure, ax = plt.subplots(figsize=(20, 10))
    figure.patch.set_facecolor('#191919')
    ax.set_facecolor('#191919')
    ax.plot(
        x,
        y,
        color='#24d3ff',
        marker='o',
        ms='22',
        linewidth=3
    )
    ax.hlines(8, 0, (len(x) - 1), color='red', linestyle=':')
    ax.grid(color='#404040')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_ylabel('Speed m/s', color='white')
    ax.tick_params(
        axis='both',
        direction='inout',
        color='white',
        labelcolor='white'
    )
    for x, y in zip(x, y):
        plt.text(
            x,
            y,
            str(y),
            horizontalalignment='center',
            verticalalignment='center',
            fontweight='bold',
            color='#404040'
        )
    buf = io.BytesIO()
    figure.savefig(buf, format='png', facecolor='#191919', bbox_inches='tight')
    buf.seek(0)
    return buf
