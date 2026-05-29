#!/usr/bin/env python3
import argparse
import sys
import pandas as pd
import numpy as np

try:
    from plotnine import ggplot, aes, geom_point, geom_line, geom_bar
    from plotnine.data import penguins
except ImportError:
    print("Error: plotnine is not installed. Run: pip install plotnine pandas")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Plotnine Quick Plot Script')
    parser.add_argument('--x', required=True, help='X column name')
    parser.add_argument('--y', required=True, help='Y column name')
    parser.add_argument('--data', default='penguins', help='Data source (penguins or csv path)')
    parser.add_argument('--geom', default='point', choices=['point', 'line', 'bar'],
                        help='Geometry type')
    parser.add_argument('--color', help='Color mapping column')
    parser.add_argument('--output', default='plot.png', help='Output file')
    parser.add_argument('--width', type=float, default=6, help='Plot width')
    parser.add_argument('--height', type=float, default=4, help='Plot height')
    parser.add_argument('--dpi', type=int, default=100, help='DPI')

    args = parser.parse_args()

    try:
        if args.data == 'penguins':
            df = penguins.dropna()
        else:
            df = pd.read_csv(args.data)

        mapping = aes(args.x, args.y)
        if args.color:
            mapping = aes(args.x, args.y, color=args.color)

        p = ggplot(df, mapping)

        if args.geom == 'point':
            p = p + geom_point()
        elif args.geom == 'line':
            p = p + geom_line()
        elif args.geom == 'bar':
            p = p + geom_bar()

        p.save(args.output, width=args.width, height=args.height, dpi=args.dpi)
        print(f"Plot saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
