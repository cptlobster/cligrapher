
class Raster:
    def __init__(self, width: int, height: int, colors_enabled: bool = True):
        self.width = width
        self.height = height
        self.display = [[{"char": ' '} for _ in range(width)] for _ in range(height)]
        self.overlays = []
        self.colors = colors_enabled

    def _flatten_esc_codes(self):
        disp = self.display
        ndisp = [[" " for i in range(self.width)] for i in range(self.height)]
        color = 0
        # iterate through and apply ANSI color codes
        # TODO: figure out if there's a cleaner way to set this up
        for i in range(len(disp)):
            for j in range(len(disp[i])):
                if self.colors:
                    if disp[i][j]["color"] != color:
                        color = disp[i][j]["color"]
                        ndisp[i][j] = "\u001b" + f"[38;5;{disp[i][j]['color']}m" + disp[i][j]["char"]
                    else:
                        ndisp[i][j] = disp[i][j]["char"]
                else:
                    ndisp[i][j] = disp[i][j]["char"]
        return ndisp

    def __str__(self):
        for i in self.overlays:
            # TODO: apply overlays to graph surface
            pass
        output = "\n".join(["".join(i) for i in self._flatten_esc_codes()])
        return output + "\u001b[0m"
