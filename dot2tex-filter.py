#!/usr/bin/env python3

from pandocfilters import toJSONFilter, Str, RawBlock
from subprocess import Popen, PIPE, STDOUT

def dot2tex(key, value, format, meta):
    if not format=="latex":
        # rise ValueError("This filter works only with latex/pdf output format")
        pass
    if key=="CodeBlock"and "dot" in value[0][1]:
        caption = ""
        label = ""
        for pair in value[0][2]:
            if pair[0] == "caption":
                caption = pair[1]
            if pair[0] == "label":
                label = pair[1]
        graph = value[1]
        p = Popen(['dot2tex', '--figonly', '--autosize'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        response = p.communicate(input=bytes(graph, "utf-8"))
        err = response[1].decode("utf-8")
        if len(err) != 0:
            raise ValueError(err)
        tikz_code = response[0].decode("utf-8")
        result = "\\begin{figure}\n\\centering\\begin{tikzpicture}" + tikz_code + "\\end{tikzpicture}\\caption{" + caption + "} \\label{" + label + "}\\end{figure}"
        return {
            "c": [
                "latex",
                result
            ],
            "t": "RawBlock"
        }

if __name__ == "__main__":
    toJSONFilter(dot2tex)
