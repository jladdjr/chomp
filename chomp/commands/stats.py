from uniplot import plot

from chomp.data_manager import get_weight_diary
from chomp.utils import days_since_today

def stats(days=30, plotwidth=60, interactive=False):
    data = get_weight_diary()
    datapoints = sorted(data.items())

    xs = []
    ys = []
    for (x, y) in datapoints:
        days_ago = days_since_today(x)
        if days_ago > days:
            continue

        xs.append(days - days_ago)
        ys.append(y['weight'])

    # yes, y's come first (likely because x's are optional)
    # https://github.com/olavolav/uniplot/blob/814747125ee3be9ab87d2d932f6b310cc46ffad7/uniplot/uniplot.py#L14
    plot(ys, xs, interactive=interactive, title=f"Weight Over Past {days} Days", width=plotwidth)
