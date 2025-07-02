import argparse
import sys
import time

import numpy as np
import pyvista as pv
from scipy.spatial import KDTree


def main(
    scalp_fn: str, 
    query_point: tuple | list | np.ndarray, 
    method = 'closest_point_pv',
    print_query_coord: bool = True,
    print_closest_coord: bool = True,
    print_distance: bool = True,
    demo: bool = False,
) -> None:
    if demo:
        scalp = pv.Sphere(radius=100, theta_resolution=1000, phi_resolution=1000)
        query_point = np.array([20.29, 83.58, 26.50])
    else:
        scalp = pv.read(scalp_fn)
        if isinstance(query_point, (tuple, list)):
            query_point = np.array(query_point)
    print(f"Using method: {method}.")
    t0 = time.time() * 1000
    _, closest_point, d = get_closest_point(scalp, query_point, method)
    t1 = time.time() * 1000
    print(f"Elapsed time: {t1 - t0:.2f} ms.")
    print(f"Query Point: {np.round(query_point, 2)}, Closest Point: {np.round(closest_point, 2)}, Distance: {d:.2f} mm.")
    p = pv.Plotter()
    p.add_mesh(scalp, color='white', opacity=0.5)
    p.add_points(query_point, color='red', point_size=20, render_points_as_spheres=True, label='Query Point')
    p.add_points(closest_point, color='blue', point_size=20, render_points_as_spheres=True, label='Closest Point')
    text = ""
    if print_query_coord:
        text += f"Query Coordinates: {np.round(query_point, 2)}\n"
    if print_closest_coord:
        text += f"Closest Coordinates: {np.round(closest_point, 2)}\n"
    if print_distance:
        text += f"Distance: {d:.2f} mm\n"
    p.add_text(text, position='lower_edge', font_size=10, color='black')
    p.add_legend()
    p.show()

def get_closest_point(scalp: pv.PolyData, query_point: np.ndarray, method: str = 'closest_point_pv') -> tuple[int, np.ndarray, float]:
    if method == 'closest_point_pv':
        closest_point_id = scalp.find_closest_point(query_point)
        closest_point = scalp.points[closest_point_id]
        d = np.linalg.norm(closest_point - query_point)
        return int(closest_point_id), closest_point, d
    elif method == 'kd_tree_scipy':
        d, closest_point_id = KDTree(scalp.points).query(query_point, workers=-1)
        closest_point = scalp.points[closest_point_id]
        return int(closest_point_id), closest_point, d
    elif method == 'reference':
        d = 1_000_000
        closest_point_id = -1
        for i, point in enumerate(scalp.points):
            dist = np.linalg.norm(point - query_point)
            if dist < d:
                d = dist
                closest_point_id = i
        closest_point = scalp.points[closest_point_id]
        return int(closest_point_id), closest_point, d
    else:
        raise NotImplementedError(f"Method '{method}' is not implemented.")
    
def benchmark():
    # closest_point_pv
    t_lst = []
    for _ in range(10):
        t0 = time.time() * 1000
        scalp = pv.read("whole_skull.vtk")
        query_point = np.array([-48.97, 11.73, 56.77]) 
        closest_point_id, closest_point, d = get_closest_point(scalp, query_point, method='closest_point_pv')
        t1 = time.time() * 1000
        t_lst.append(t1 - t0)
    print(f"closest_point_pv: {np.mean(t_lst):.2f} ({np.std(t_lst):.2f}) ms.")
    print(f"Index: {closest_point_id}, Coordinates: {np.round(closest_point, 2)}, Distance: {d:.2f} mm")

    # kd_tree_scipy
    t_lst = []
    for _ in range(10):
        t0 = time.time() * 1000
        scalp = pv.read("whole_skull.vtk")
        query_point = np.array([-48.97, 11.73, 56.77]) 
        closest_point_id, closest_point, d = get_closest_point(scalp, query_point, method='kd_tree_scipy')
        t1 = time.time() * 1000
        t_lst.append(t1 - t0)
    print(f"kd_tree_scipy: {np.mean(t_lst):.2f} ({np.std(t_lst):.2f}) ms.")
    print(f"Index: {closest_point_id}, Coordinates: {np.round(closest_point, 2)}, Distance: {d:.2f} mm")

    # reference
    t_lst = []
    for _ in range(10):
        t0 = time.time() * 1000
        scalp = pv.read("whole_skull.vtk")
        query_point = np.array([-48.97, 11.73, 56.77]) 
        closest_point_id, closest_point, d = get_closest_point(scalp, query_point, method='reference')
        t1 = time.time() * 1000
        t_lst.append(t1 - t0)
    print(f"reference: {np.mean(t_lst):.2f} ({np.std(t_lst):.2f}) ms.")
    print(f"Index: {closest_point_id}, Coordinates: {np.round(closest_point, 2)}, Distance: {d:.2f} mm")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find the point on the scalp closest to a given query point.")
    parser.add_argument("--scalp_fn", "-s", type=str, help="Path to the scalp VTK file.")
    parser.add_argument("--query_point", "-q", type=float, nargs=3, help="Query point coordinates.")
    parser.add_argument("--method", "-m", type=str, default="closest_point_pv", help="Method to use for finding the closest point. Options: 'closest_point_pv', 'kd_tree_scipy', 'reference'. Default is 'closest_point_pv'.")
    parser.add_argument("--print_query_coord", "-pq", action='store_true', default=True, help="Print the query coordinates. Default is True.")
    parser.add_argument("--print_closest_coord", "-pc", action='store_true', default=True, help="Print the closest coordinates. Default is True.")
    parser.add_argument("--print_distance", "-pd", action='store_true', default=True, help="Print the distance to the closest point. Default is True.")
    parser.add_argument("--benchmark", "-b", action='store_true', help="Run benchmark tests.")
    parser.add_argument("--demo", "-d", action='store_true', help="Run a demo with a predefined surface and query point.")
    args = parser.parse_args()
    
    if args.benchmark:
        benchmark()
        sys.exit(0)
    elif args.demo:
        main(scalp_fn='', query_point=(0, 0, 0), demo=True)
        sys.exit(0) 
    else:
        main(
            scalp_fn=args.scalp_fn, 
            query_point=args.query_point, 
            method=args.method, 
            print_query_coord=args.print_query_coord, 
            print_closest_coord=args.print_closest_coord, 
            print_distance=args.print_distance, 
        )
        sys.exit(0)
