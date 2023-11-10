from uniplot import plot

from chomp.data_manager import get_weight_diary
from chomp.utils import days_since_today

def stats():

    # TODO: expose as configurable option
    num_days_to_show = 30

    data = get_weight_diary()
    datapoints = sorted(data.items())

    x = 1
    xs = []
    ys = []
    for (x, y) in datapoints:
        days_ago = days_since_today(x)
        if days_ago > num_days_to_show:
            continue

        xs.append(num_days_to_show - days_ago)
        ys.append(y['weight'])

    plot(ys, xs, interactive=True)
