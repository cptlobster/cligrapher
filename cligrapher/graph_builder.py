from renderer import Renderer
import random


def simple_graph(data=None, rows: int=40, cols: int=120, title: str=None, subtitle: str=None):
    rend = Renderer()
    rend.push_string(title, cols // 2, 1, "255", "center")
    rend.push_string(subtitle, cols // 2, 2, "246", "center")
    rend.push_string("https://github.com/cptlobster/cligrapher", cols - 1, rows - 1, "240", "right")
    rend.push_graph_axes(xmax=1)
    for i in range(0, 6):
        rend.register([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                      [(random.randrange(0, 100) / 100) for _ in range(0, 11)], 0)
        rend.draw_line(0, i)
    rend.draw_legend(1, 38, 0)
    print(rend.render())
    print("\u001b[0m")


def simple_flamegraph(data=None, rows: int=40, cols: int=120, title: str=None, subtitle: str=None):
    rend = Renderer()
    rend.push_string(title, cols // 2, 1, "255", "center")
    rend.push_string(subtitle, cols // 2, 2, "246", "center")
    rend.push_string("https://github.com/cptlobster/cligrapher", cols - 1, rows - 1, "240", "right")
    rend.push_graph_axes()
    rend.register([*range(0, 107)],
                  [(random.randrange(0, 100) / 100) for _ in range(0, 107)], 0)
    rend.draw_flame(0, 0)
    # rend.draw_legend(1, 38, 0)
    print(rend.render())
    print("\u001b[0m")