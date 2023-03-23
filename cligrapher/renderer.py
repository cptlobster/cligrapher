def map_pt(x, y, old, new):
    opx = old[0]
    opy = old[1]
    ow = old[2]
    oh = old[3]
    npx = new[0]
    npy = new[1]
    nw = new[2]
    nh = new[3]


class Renderer:
    def __init__(self, rows: int = 40, cols: int = 120):
        self.rows = rows
        self.cols = cols
        self.textfield = [[{"char": " ", "color": ""} for i in range(cols)] for i in range(rows)]
        self.graphs = []

    def push_string(self, s: str, x: int = 0, y: int = 0, color: str = "", align: str = "left"):
        """add a string to the text field

        :param s: the string
        :param x: string's x-position on the textfield
        :param y: string's y-position on the textfield
        :param color: the ANSI 256-color code that you want to use for the specified string
        :param align: left, center, or right; aligns text relative to specified coordinates
        """
        arrs = s.split("\n")
        for i in range(0, len(arrs)):
            match align:
                case "left":
                    tx = x
                case "right":
                    tx = x - len(arrs[i])
                case "center":
                    tx = x - (len(arrs[i]) // 2)
                case _:
                    tx = x
            for j in range(0, len(arrs[i])):
                self.textfield[(y + i) % self.rows][(tx + j) % self.cols]["char"] = arrs[i][j]
                self.textfield[(y + i) % self.rows][(tx + j) % self.cols]["color"] = color

    def push_graph_axes(self, x: int = 4, y: int = 4, w: int = None, h: int = None, xmin=0, ymin=0, xstep=1, ystep=None,
                        xmax=None, ymax=1):
        """Add graph axes to the text field and register the graph region

        :param x: graph's x-position on the textfield
        :param y: graph's y-position on the textfield
        :param w: graph's width
        :param h: graph's height
        :param xmin: minimum value of x-axis
        :param xmax: maximum value of x-axis
        :param xstep: x-axis step
        :param ymin: minimum value of y-axis
        :param ymax: maximum value of y-axis
        :param ystep: y-axis step"""
        if w is None:
            w = self.cols - x * 2
        if h is None:
            h = self.rows - y * 2

        x_offset = max(len(str(xmin)), len(str(xmax))) + 1
        y_offset = 1
        col_inc = 0
        if xmax is None and xstep is not None:
            xmax = xstep * (w - x_offset)
        elif xmax is None and xstep is None:
            raise Exception("either xmax or xstep must be defined")

        if ymax is None and ystep is not None:
            ymax = ystep * (h - y_offset)
        elif ymax is None and ystep is None:
            raise Exception("either ymax or ystep must be defined")

        # vertical lines
        for i in range(y, y + h - y_offset):
            self.textfield[i][x + x_offset]["char"] = "┃"
            self.textfield[i][x + x_offset]["color"] = "246"
            col_inc += 1
        # horizontal lines
        for i in range(x + x_offset, x + w):
            self.textfield[y + h - y_offset][i]["char"] = "━"
            self.textfield[y + h - y_offset][i]["color"] = "246"
            col_inc += 1
        # corner
        self.textfield[y + h - y_offset][x + x_offset]["char"] = "┗"
        self.push_string(str(ymax), x + x_offset - 1, y, "255", "right")
        self.push_string(str(ymin), x + x_offset - 1, y + h - y_offset, "255", "right")
        self.push_string(str(xmin), x + x_offset + 2, y + h, "255", "right")
        self.push_string(str(xmax), x + w, y + h, "255", "right")
        self.graphs.append(
            {
                "x": x + (x_offset + 1),
                "y": y,
                "w": w - (x_offset + 1),
                "h": h - (y_offset + 1),
                "xmin": xmin,
                "xmax": xmax,
                "ymin": ymin,
                "ymax": ymax,
                "lines": []
            }
        )

    def register(self, xs, ys, graph: int, name: str = None):
        """Register data to the graph"""
        px = self.graphs[graph]['x']
        py = self.graphs[graph]['y']
        pw = self.graphs[graph]['w']
        ph = self.graphs[graph]['h']
        xmin = self.graphs[graph]['xmin']
        xmax = self.graphs[graph]['xmax']
        ymin = self.graphs[graph]['ymin']
        ymax = self.graphs[graph]['ymax']
        lv = len(self.graphs[graph]['lines']) + 1
        if name is None:
            name = str(lv)
        self.graphs[graph]['lines'].append({"name": name, "color": (lv % 6) + 1, "x": xs, "y": ys})

    def draw_line(self, graph: int, idx: int = None):
        """Draw a line on a specified graph region.

        :param xs: List of x parameters (sorted)
        :param ys: List of y parameters corresponding to each x parameter
        :param graph: Numeric ID of the graph to draw on"""
        xs = self.graphs[graph]['lines'][idx]["x"]
        ys = self.graphs[graph]['lines'][idx]["y"]
        px = self.graphs[graph]['x']
        py = self.graphs[graph]['y']
        pw = self.graphs[graph]['w']
        ph = self.graphs[graph]['h']
        xmin = self.graphs[graph]['xmin']
        xmax = self.graphs[graph]['xmax']
        ymin = self.graphs[graph]['ymin']
        ymax = self.graphs[graph]['ymax']
        lv = self.graphs[graph]['lines'][idx]["color"]
        for i in range(0, min(len(xs), len(ys)) - 1):
            x = xs[i]
            y = ys[i]
            # map the value to relative decimal position in coord plane
            mx = (x - xmin) / (xmax - xmin)
            my = 1 - (y - ymin) / (ymax - ymin)
            # then multiply to graph plane size
            cpx = round(mx * pw)
            cpy = round(my * ph)
            # now we do the line to the next point
            nx = xs[i + 1]
            ny = ys[i + 1]
            # map the value to relative decimal position in coord plane
            nmx = (nx - xmin) / (xmax - xmin)
            nmy = 1 - (ny - ymin) / (ymax - ymin)
            # then multiply to graph plane size
            ncpx = round(nmx * pw)
            ncpy = round(nmy * ph)
            cprange = ncpx - cpx
            cpslope = ncpy - cpy
            for j in range(cpx, ncpx):
                pos = (j - cpx)
                slp = round((pos / cprange) * cpslope)
                self.textfield[py + cpy + slp][px + cpx + pos]["char"] = "#"
                self.textfield[py + cpy + slp][px + cpx + pos]["color"] = str((lv % 6) + 1)
            self.textfield[py + cpy][px + cpx]["char"] = "#"
            self.textfield[py + cpy][px + cpx]["color"] = str(((lv % 6) + 1))

    def draw_pts(self, graph: int, idx: int = None):
        """Draw points on a specified graph region.

        :param xs: List of x parameters (sorted)
        :param ys: List of y parameters corresponding to each x parameter
        :param graph: Numeric ID of the graph to draw on"""
        xs = self.graphs[graph]['lines'][idx]["x"]
        ys = self.graphs[graph]['lines'][idx]["y"]
        px = self.graphs[graph]['x']
        py = self.graphs[graph]['y']
        pw = self.graphs[graph]['w']
        ph = self.graphs[graph]['h']
        xmin = self.graphs[graph]['xmin']
        xmax = self.graphs[graph]['xmax']
        ymin = self.graphs[graph]['ymin']
        ymax = self.graphs[graph]['ymax']
        lv = self.graphs[graph]['lines'][idx]["color"]
        for i in range(0, min(len(xs), len(ys))):
            x = xs[i]
            y = ys[i]
            # map the value to relative decimal position in coord plane
            mx = (x - xmin) / (xmax - xmin)
            my = 1 - (y - ymin) / (ymax - ymin)
            # then multiply to graph plane size
            cpx = round(mx * pw)
            cpy = round(my * ph)
            self.textfield[py + cpy][px + cpx]["char"] = "#"
            self.textfield[py + cpy][px + cpx]["color"] = str(((lv % 6) + 1))

    def draw_flame(self, graph: int, idx: int = None):
        """draw flamegraph of a region"""
        xs = self.graphs[graph]['lines'][idx]["x"]
        ys = self.graphs[graph]['lines'][idx]["y"]
        px = self.graphs[graph]['x']
        py = self.graphs[graph]['y']
        pw = self.graphs[graph]['w']
        ph = self.graphs[graph]['h']
        xmin = self.graphs[graph]['xmin']
        xmax = self.graphs[graph]['xmax']
        ymin = self.graphs[graph]['ymin']
        ymax = self.graphs[graph]['ymax']
        lv = self.graphs[graph]['lines'][idx]["color"]
        colors = ["226", "220", "214", "208", "202", "196"]
        for i in range(0, min(len(xs), len(ys))):
            x = xs[i]
            y = ys[i]
            # map the value to relative decimal position in coord plane
            mx = (x - xmin) / (xmax - xmin)
            my = 1 - (y - ymin) / (ymax - ymin)
            # then multiply to graph plane size
            cpx = round(mx * pw)
            cpy = round(my * ph)
            ys = [round((k * ((ph - cpy - 1) / (len(colors) - 1))) + cpy) for k in range(0, len(colors))]
            print(ys)
            ci = 0
            cy = ys[0]
            for j in range(cpy, ph):
                if cy < j + py:
                    ci = (ci + 1) % len(ys)
                    cy = ys[ci]

                col = colors[ci]
                self.textfield[j][px + cpx]["char"] = "█"
                self.textfield[j][px + cpx]["color"] = col

    def draw_legend(self, x: int, y: int, graph: int):
        lines = self.graphs[graph]["lines"]
        xoffset = 0
        yoffset = 0
        for i in lines:
            length = 4 + len(i["name"])
            if x + xoffset + length >= self.cols - 1:
                xoffset = 0
                yoffset += 1
            self.push_string("┗━━ ", x + xoffset, y + yoffset, i["color"], "left")
            self.push_string(i["name"], x + xoffset + 4, y + yoffset, "255", "left")
            xoffset += length + 1

    def render(self):
        """fully builds graph output and returns as string"""
        rstr = ""
        currcol = ""
        for i in self.textfield:
            for j in i:
                if j["color"] != "" and currcol != j["color"]:
                    rstr += "\u001b" + f"[38;5;{j['color']}m"
                    currcol = j['color']
                rstr += j["char"]
            rstr += "\r\n"
        return rstr
