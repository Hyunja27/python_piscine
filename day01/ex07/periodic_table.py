#!/usr/bin/python3

import sys

def html_make(info:list):
    basic_line = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>
            periodic table! | by spark
        </title>
        <style>
            table{{
                border-collapse: collapse;
            }}
            ul {{
                list-style:none;
                padding-left:0px;
            }}
            h4{{
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <table>
            {nodes}
        </table>
    </body>
    </html>
    """

    node = """
    <td style="border: 1px solid black; padding:10px">
        <h4>{name}</h4>
        <ul>
          <li>No {number}</li>
          <li>{small}</li>
          <li>{molar}</li>
          <li>{electron} electron</li>
        </ul>
"""
    nodes = "<tr>"
    old_sett= 0
    for i in info:
        sett = int(i["position"]) 
        if (int(sett) - int(old_sett) > 0):
            for _ in range(1, sett - old_sett):
                nodes += "    </td>\n    <td>"
        nodes += node.format(
            name=i["name"],
            number=i["number"],
            small=i["small"],
            molar=i["molar"],
            electron=i["electron"],
            )
        if (int(i["number"]) == 118):
            nodes += "  </tr>"
        elif (sett == 17):
            nodes += "    </tr>\n    <tr>"
        old_sett = sett
    return basic_line.format(nodes=nodes)

def parse_line(line:str):
    cut = line.split("= ")
    pos = cut[1].split(", ")
    dic = dict(a.split(':') for a in pos)
    dic["name"] = line.split('=')[0].strip()
    return dic

def main():
    fd = open("periodic_table.txt", "r")
    info = [parse_line(line) for line in fd.readlines()]
    fd.close()
    html_line = html_make(info)
    fd = open("periodic_table.html", "w")
    fd.write(html_line)
    fd.close()

if __name__=='__main__':
    main()
