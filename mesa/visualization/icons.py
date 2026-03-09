"""Procedural icon generation utilities for Mesa visualizations.

This module provides a small library of simple, procedurally generated
icons that can be used in agent portrayals. Icons are generated at
runtime using Pillow so no binary assets need to be shipped with Mesa.

Icons are intentionally minimalist so that they remain legible at small
sizes and across backends.
"""

from __future__ import annotations

import base64
import io
from functools import lru_cache

from PIL import Image, ImageDraw


@lru_cache(maxsize=None)
def _make_base_canvas(size: int) -> Image.Image:
    """Create a transparent square canvas."""
    return Image.new("RGBA", (size, size), (0, 0, 0, 0))


def _draw_person(size: int) -> Image.Image:
    img = _make_base_canvas(size).copy()
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r_head = size * 0.18
    head_box = [
        cx - r_head,
        cy - size * 0.35 - r_head,
        cx + r_head,
        cy - size * 0.35 + r_head,
    ]
    draw.ellipse(head_box, fill=(0, 0, 0, 255))

    body_top = (cx, cy - size * 0.15)
    body_bottom = (cx, cy + size * 0.3)
    draw.line([body_top, body_bottom], fill=(0, 0, 0, 255), width=max(1, size // 12))

    arm_span = size * 0.3
    arm_y = cy - size * 0.02
    draw.line(
        [(cx - arm_span, arm_y), (cx + arm_span, arm_y)],
        fill=(0, 0, 0, 255),
        width=max(1, size // 14),
    )

    leg_y = cy + size * 0.3
    leg_span = size * 0.2
    draw.line(
        [(cx, leg_y), (cx - leg_span, size * 0.95)],
        fill=(0, 0, 0, 255),
        width=max(1, size // 14),
    )
    draw.line(
        [(cx, leg_y), (cx + leg_span, size * 0.95)],
        fill=(0, 0, 0, 255),
        width=max(1, size // 14),
    )
    return img


def _draw_house(size: int) -> Image.Image:
    img = _make_base_canvas(size).copy()
    draw = ImageDraw.Draw(img)

    margin = size * 0.15
    base_top = size * 0.45
    base_box = [margin, base_top, size - margin, size - margin]
    draw.rectangle(base_box, outline=(0, 0, 0, 255), width=max(1, size // 14))

    roof_peak = (size * 0.5, size * 0.12)
    roof_left = (margin, base_top)
    roof_right = (size - margin, base_top)
    draw.polygon([roof_left, roof_peak, roof_right], outline=(0, 0, 0, 255))

    door_width = size * 0.18
    door_height = size * 0.28
    door_left = size * 0.5 - door_width / 2
    door_right = size * 0.5 + door_width / 2
    door_top = size - margin - door_height
    door_bottom = size - margin
    draw.rectangle(
        [door_left, door_top, door_right, door_bottom],
        outline=(0, 0, 0, 255),
        width=max(1, size // 18),
    )
    return img


def _draw_tree(size: int) -> Image.Image:
    img = _make_base_canvas(size).copy()
    draw = ImageDraw.Draw(img)

    trunk_width = size * 0.16
    trunk_height = size * 0.3
    trunk_left = size * 0.5 - trunk_width / 2
    trunk_right = size * 0.5 + trunk_width / 2
    trunk_bottom = size * 0.92
    trunk_top = trunk_bottom - trunk_height
    draw.rectangle(
        [trunk_left, trunk_top, trunk_right, trunk_bottom],
        fill=(0, 0, 0, 255),
    )

    canopy_radius = size * 0.32
    canopy_center = (size * 0.5, size * 0.32)
    canopy_box = [
        canopy_center[0] - canopy_radius,
        canopy_center[1] - canopy_radius,
        canopy_center[0] + canopy_radius,
        canopy_center[1] + canopy_radius,
    ]
    draw.ellipse(canopy_box, outline=(0, 0, 0, 255), width=max(1, size // 18))
    return img


def _draw_factory(size: int) -> Image.Image:
    img = _make_base_canvas(size).copy()
    draw = ImageDraw.Draw(img)

    margin = size * 0.12
    base_top = size * 0.5
    base_box = [margin, base_top, size - margin, size - margin]
    draw.rectangle(base_box, outline=(0, 0, 0, 255), width=max(1, size // 16))

    step_width = (size - 2 * margin) / 3
    for i in range(3):
        left = margin + i * step_width
        right = left + step_width
        height = base_top - size * (0.12 + 0.08 * i)
        draw.polygon(
            [(left, base_top), (left, height), (right, base_top)],
            outline=(0, 0, 0, 255),
        )

    chimney_width = size * 0.12
    chimney_left = size - margin - chimney_width
    chimney_right = size - margin
    chimney_bottom = base_top
    chimney_top = size * 0.16
    draw.rectangle(
        [chimney_left, chimney_top, chimney_right, chimney_bottom],
        outline=(0, 0, 0, 255),
        width=max(1, size // 18),
    )
    return img


def _draw_robot(size: int) -> Image.Image:
    img = _make_base_canvas(size).copy()
    draw = ImageDraw.Draw(img)
    margin = size * 0.18

    head_top = size * 0.15
    head_bottom = size * 0.35
    draw.rectangle(
        [margin, head_top, size - margin, head_bottom],
        outline=(0, 0, 0, 255),
        width=max(1, size // 18),
    )

    eye_r = size * 0.04
    eye_y = (head_top + head_bottom) / 2
    eye_dx = size * 0.09
    for sign in (-1, 1):
        cx = size * 0.5 + sign * eye_dx
        draw.ellipse(
            [cx - eye_r, eye_y - eye_r, cx + eye_r, eye_y + eye_r],
            fill=(0, 0, 0, 255),
        )

    body_top = head_bottom + size * 0.04
    body_bottom = size * 0.75
    body_left = margin * 0.9
    body_right = size - margin * 0.9
    draw.rectangle(
        [body_left, body_top, body_right, body_bottom],
        outline=(0, 0, 0, 255),
        width=max(1, size // 18),
    )

    dial_center = (size * 0.5, (body_top + body_bottom) / 2)
    dial_r = size * 0.07
    draw.ellipse(
        [
            dial_center[0] - dial_r,
            dial_center[1] - dial_r,
            dial_center[0] + dial_r,
            dial_center[1] + dial_r,
        ],
        outline=(0, 0, 0, 255),
        width=max(1, size // 22),
    )
    draw.line(
        [
            dial_center,
            (dial_center[0] + dial_r * 0.8, dial_center[1] - dial_r * 0.2),
        ],
        fill=(0, 0, 0, 255),
        width=max(1, size // 24),
    )
    return img


def _draw_hazard(size: int) -> Image.Image:
    img = _make_base_canvas(size).copy()
    draw = ImageDraw.Draw(img)

    margin = size * 0.15
    top = margin
    bottom = size - margin
    left = margin
    right = size - margin

    triangle = [(size * 0.5, top), (right, bottom), (left, bottom)]
    draw.polygon(triangle, outline=(0, 0, 0, 255), width=max(1, size // 18))

    ex_top = size * 0.38
    ex_bottom = size * 0.7
    cx = size * 0.5
    draw.line(
        [(cx, ex_top), (cx, ex_bottom)],
        fill=(0, 0, 0, 255),
        width=max(1, size // 16),
    )
    dot_r = size * 0.04
    draw.ellipse(
        [cx - dot_r, bottom - dot_r * 3, cx + dot_r, bottom - dot_r],
        fill=(0, 0, 0, 255),
    )
    return img


ICON_BUILDERS = {
    "person": _draw_person,
    "house": _draw_house,
    "tree": _draw_tree,
    "factory": _draw_factory,
    "robot": _draw_robot,
    "hazard": _draw_hazard,
}


def builtin_icons() -> list[str]:
    """Return the list of built-in icon names."""
    return sorted(ICON_BUILDERS.keys())


@lru_cache(maxsize=None)
def get_icon_image(name: str, size: int = 32) -> Image.Image:
    """Return a Pillow image for the given icon name."""
    if name not in ICON_BUILDERS:
        raise KeyError(f"Unknown icon '{name}'. Available: {', '.join(builtin_icons())}")
    size = max(8, int(size))
    return ICON_BUILDERS[name](size)


@lru_cache(maxsize=None)
def get_icon_png_bytes(name: str, size: int = 32) -> bytes:
    """Return PNG-encoded bytes for the given icon."""
    img = get_icon_image(name, size)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@lru_cache(maxsize=None)
def get_icon_data_url(name: str, size: int = 32) -> str:
    """Return a data URL suitable for use in image-based backends."""
    raw = get_icon_png_bytes(name, size)
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{b64}"

