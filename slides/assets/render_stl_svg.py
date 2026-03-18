#!/usr/bin/env python3

import math
import sys
from pathlib import Path


def parse_ascii_stl(path):
    triangles = []
    verts = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4 and parts[0] == "vertex":
                verts.append(tuple(float(v) for v in parts[1:4]))
                if len(verts) == 3:
                    triangles.append(tuple(verts))
                    verts = []
    return triangles


def rotate(v, yaw_deg, pitch_deg):
    x, y, z = v
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)

    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)

    x1 = cy * x + sy * z
    y1 = y
    z1 = -sy * x + cy * z

    x2 = x1
    y2 = cp * y1 - sp * z1
    z2 = sp * y1 + cp * z1
    return (x2, y2, z2)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def normalize(v):
    mag = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) or 1.0
    return (v[0] / mag, v[1] / mag, v[2] / mag)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def project(v, scale, width, height):
    x, y, _ = v
    return (width / 2 + x * scale, height / 2 - y * scale)


def render_svg(triangles, out_path, yaw_deg, pitch_deg, width=1800, height=1200):
    rotated = []
    all_pts = []
    for tri in triangles:
        rtri = tuple(rotate(v, yaw_deg, pitch_deg) for v in tri)
        rotated.append(rtri)
        all_pts.extend(rtri)

    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    span_x = (max(xs) - min(xs)) or 1.0
    span_y = (max(ys) - min(ys)) or 1.0
    scale = 0.82 * min(width / span_x, height / span_y)

    light = normalize((0.4, -0.7, 0.6))
    faces = []
    for tri in rotated:
        v1, v2, v3 = tri
        normal = normalize(cross(sub(v2, v1), sub(v3, v1)))
        intensity = max(0.15, dot(normal, light) * 0.5 + 0.5)
        shade = int(60 + 150 * intensity)
        points = [project(v, scale, width, height) for v in tri]
        depth = sum(v[2] for v in tri) / 3.0
        faces.append((depth, shade, points))

    faces.sort(key=lambda item: item[0])

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f6f3ec"/>',
    ]

    for _, shade, points in faces:
        pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        fill = f"rgb({shade},{shade},{shade})"
        svg.append(f'<polygon points="{pts}" fill="{fill}" stroke="none"/>')

    svg.append("</svg>")
    Path(out_path).write_text("\n".join(svg), encoding="utf-8")


def main():
    if len(sys.argv) != 5:
        raise SystemExit("usage: render_stl_svg.py input.stl output.svg yaw_deg pitch_deg")
    render_svg(parse_ascii_stl(sys.argv[1]), sys.argv[2], float(sys.argv[3]), float(sys.argv[4]))


if __name__ == "__main__":
    main()
