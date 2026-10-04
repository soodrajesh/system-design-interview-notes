"""Lane-based architecture diagrams: each flow is a horizontal lane of service tiles joined left to right.

lanes = [{"name": "WRITE PATH", "color": "#1a73e8", "nodes": [(label, glyph, category, sub), ...],
          "edges": [(i, label, legend_text), ...]}]     # edge i joins node i -> node i+1
Edge numbers run across lanes in order; the legend is generated from legend_text.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from archlib import Diagram

LANE_H, TOP, X0, STEP = 200, 110, 130, 200


def build(out, title, subtitle, lanes, notes=None, boundary=None):
    n_lanes = len(lanes)
    maxn = max(len(l["nodes"]) for l in lanes)
    W = max(1400, X0 * 2 + (maxn - 1) * STEP)
    notes = notes or []
    legend_rows = sum(len(l["edges"]) for l in lanes)
    leg_h = 34 + legend_rows * 22
    H = TOP + n_lanes * LANE_H + 30 + leg_h + (30 + 18 * len(notes) if notes else 0) + 110
    d = Diagram(W, H, title, subtitle)
    if boundary:
        d.group(30, TOP - 20, W - 60, n_lanes * LANE_H + 10, boundary, "#1a73e8", dash=False, fill="#fbfcff", label_w=len(boundary) * 7 + 30)
    rows, num = [], 0
    for k, lane in enumerate(lanes):
        top = TOP + k * LANE_H
        col = lane.get("color", "#5f6368")
        d.band(50, top + 10, W - 100, LANE_H - 30, lane["name"], col, "#ffffff")
        cy = top + 85
        for i, (label, glyph, cat, sub) in enumerate(lane["nodes"]):
            d.node(f"{k}_{i}", X0 + i * STEP, cy, label, glyph, cat, sub)
        for (i, lab, text) in lane["edges"]:
            num += 1
            d.edge(f"{k}_{i}", f"{k}_{i+1}", "h", num=num, label=lab, color=col)
            rows.append((str(num), text))
    y = TOP + n_lanes * LANE_H + 30
    d.legend(34, y, "Flow", rows, w=W - 68)
    y += leg_h + 30
    if notes:
        d.text(34, y, "Key design decisions", 13, "#202124", "700")
        for j, t in enumerate(notes):
            d.text(34, y + 20 + 18 * j, "•  " + t, 12, "#3c4043")
        y += 30 + 18 * len(notes)
    d.key(34, y + 20)
    d.save(out)
