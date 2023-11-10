from chomp.data_manager import get_weight_diary

from uniplot import plot

def stats():
    data = get_weight_diary()
    datapoints = sorted(data.items())

    x = 1
    xs = []
    ys = []
    for (_,y) in datapoints:
        xs.append(x)
        ys.append(y['weight'])
        x += 1

    plot(ys, interactive=True)
