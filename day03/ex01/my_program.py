#!/usr/bin/python3

from path import Path


def main():

    try:
        Path.mkdir("spark_dir")
    except FileExistsError as e:
        print(e)
    Path.touch("spark_dir/spark_note")
    f = Path("spark_dir/spark_note")
    f.write_lines(["Please Help me.....\nPlease Help me.....\n"
                   "Please Help me.....\nPlease Help me.....\n",
                   "Please Help me.....\nPlease Help me.....\n",
                   "Please Help me.....\nPlease Help me.....\n",
                   "Please Help me.....\nPlease Help me.....\n",
                   "Please Help me.....\nPlease Help me.....\n"])
    print(f.read_text())


if __name__ == '__main__':
    main()
