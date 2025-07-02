Get Closest Point on Scalp
==========================

This script provides functionality to find the point on the scale (provided as a VTK file) that is closest to a given query point.

Requirements
------------
- Python 3.9 or higher
- PyVista
- NumPy
- SciPy

Usage
-----
```bash
usage: main.py [-h] [--scalp_fn SCALP_FN] [--query_point QUERY_POINT QUERY_POINT QUERY_POINT] [--method METHOD] [--print_source_coord] [--print_closest_coord]
               [--print_distance] [--benchmark]

Find the point on the scalp closest to a given query point.

options:
  -h, --help            show this help message and exit
  --scalp_fn SCALP_FN, -s SCALP_FN
                        Path to the scalp VTK file.
  --query_point QUERY_POINT QUERY_POINT QUERY_POINT, -q QUERY_POINT QUERY_POINT QUERY_POINT
                        Query point coordinates.
  --method METHOD, -m METHOD
                        Method to use for finding the closest point. Options: 'closest_point_pv', 'kd_tree_scipy', 'reference'. Default is 'closest_point_pv'.
  --print_query_coord, -pq
                        Print the query coordinates. Default is True.
  --print_closest_coord, -pc
                        Print the closest coordinates. Default is True.
  --print_distance, -pd
                        Print the distance to the closest point. Default is True.
  --benchmark, -b       Run benchmark tests.
  --demo, -d            Run a demo with a predefined surface and query point.
```

For example, for a query point at coordinates `(-48.97, 11.73, 56.77)` and scalp surface saved in `whole_skull.vtk`, you can run:

```bash
python ./main.py -s whole_skull.vtk -q -48.97 11.73 56.77 -m closest_point_pv -pq -pc -pd
```

The result would look like this:
![demo.png](demo.png)

Should you wish to reproduce the demo, you can run:

```bash
python ./main.py -d
```

To compare the performance of different methods, you can run:

```bash
python ./main.py -b -s whole_skull.vtk -q -48.97 11.73 56.77
```

On a MacBook Pro M4 Max (2024), the results are as follows:

```
closest_point_pv: 15.03 (1.17) ms.
Index: 180331, Coordinates: [-59.7   18.3   69.82], Distance: 18.13 mm
kd_tree_scipy: 55.24 (0.91) ms.
Index: 180331, Coordinates: [-59.7   18.3   69.82], Distance: 18.13 mm
reference: 931.73 (7.87) ms.
Index: 180331, Coordinates: [-59.7   18.3   69.82], Distance: 18.13 mm
```
