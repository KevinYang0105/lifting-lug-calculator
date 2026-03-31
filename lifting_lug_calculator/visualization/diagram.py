"""Matplotlib-based lug diagram rendering."""

import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_lug_diagram(W, R, H, d, t, t_p, theta):
    """Draw the standard front and side view diagram."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6), gridspec_kw={"width_ratios": [2.2, 1]})
    bg_color = "#1e2235"
    fig.patch.set_facecolor(bg_color)

    edge_color = "#63b3ed"
    fill_color = "#2d3748"
    reinf_edge = "#7b93db"
    text_color = "#e2e8f0"
    dim_color = "#a0aec0"
    hole_fill = bg_color
    centerline = "#718096"

    hole_r = d / 2
    top_y = H
    head_radius = R
    min_width = 2 * head_radius
    effective_w = max(W, min_width)
    total_height = top_y + head_radius
    reinforcement_radius = min(R * 0.7, R - 2) if t_p > 0 else 0

    ax1.set_aspect("equal")
    ax1.axis("off")
    ax1.set_facecolor(bg_color)

    def get_upper_tangent_point(px, py, cx, cy, radius):
        vx = px - cx
        vy = py - cy
        dist_sq = vx * vx + vy * vy
        if dist_sq <= radius * radius:
            return None

        scale = (radius * radius) / dist_sq
        offset = radius * math.sqrt(dist_sq - radius * radius) / dist_sq
        cand1 = (cx + scale * vx - offset * vy, cy + scale * vy + offset * vx)
        cand2 = (cx + scale * vx + offset * vy, cy + scale * vy - offset * vx)
        return cand1 if cand1[1] >= cand2[1] else cand2

    if math.isclose(effective_w, min_width, rel_tol=1e-9, abs_tol=1e-9):
        ax1.add_patch(patches.Rectangle((-effective_w / 2, 0), effective_w, top_y, linewidth=2, edgecolor=edge_color, facecolor=fill_color, alpha=0.8))
        ax1.add_patch(patches.Arc((0, top_y), 2 * head_radius, 2 * head_radius, theta1=0, theta2=180, linewidth=2, edgecolor=edge_color))
    else:
        left_base = (-effective_w / 2, 0)
        right_base = (effective_w / 2, 0)
        left_tangent = get_upper_tangent_point(left_base[0], left_base[1], 0, top_y, head_radius)
        right_tangent = get_upper_tangent_point(right_base[0], right_base[1], 0, top_y, head_radius)
        arc_angles = [
            math.atan2(right_tangent[1] - top_y, right_tangent[0])
            + (math.atan2(left_tangent[1] - top_y, left_tangent[0]) - math.atan2(right_tangent[1] - top_y, right_tangent[0])) * i / 120
            for i in range(121)
        ]
        arc_points = [(head_radius * math.cos(angle), top_y + head_radius * math.sin(angle)) for angle in arc_angles]
        profile_points = [left_base, right_base, right_tangent] + arc_points[1:-1] + [left_tangent]
        ax1.add_patch(
            patches.Polygon(profile_points, closed=True, linewidth=2, edgecolor=edge_color, facecolor=fill_color, alpha=0.8, joinstyle="round")
        )

    if t_p > 0:
        ax1.add_patch(patches.Circle((0, top_y), reinforcement_radius, linewidth=1.5, edgecolor=reinf_edge, linestyle="--", facecolor="none"))

    ax1.add_patch(patches.Circle((0, top_y), hole_r, linewidth=2, edgecolor=edge_color, facecolor=hole_fill))

    half_span = max(effective_w / 2, head_radius)
    ax1.plot([-half_span - 12, half_span + 12], [top_y, top_y], color=centerline, linestyle="-.", lw=0.8)
    ax1.plot([0, 0], [-10, top_y + head_radius + 12], color=centerline, linestyle="-.", lw=0.8)

    ax1.annotate("", xy=(-hole_r, top_y), xytext=(hole_r, top_y), arrowprops=dict(arrowstyle="<->", color=edge_color, lw=1.2))
    ax1.text(0, top_y + hole_r + 4, f"d={d:.0f}", ha="center", color=edge_color, fontsize=8, fontweight="bold")

    angle_45 = math.radians(45)
    ax1.annotate("", xy=(0, top_y), xytext=(head_radius * math.cos(angle_45), top_y + head_radius * math.sin(angle_45)), arrowprops=dict(arrowstyle="<-", color=dim_color, lw=1))
    ax1.text(head_radius / 2 * math.cos(angle_45) + 3, top_y + head_radius / 2 * math.sin(angle_45) + 3, f"R={R:.0f}", color=text_color, fontsize=8)

    ax1.annotate("", xy=(-effective_w / 2, -12), xytext=(effective_w / 2, -12), arrowprops=dict(arrowstyle="<->", color=dim_color, lw=1))
    ax1.text(0, -22, f"W={effective_w:.0f}", ha="center", color=text_color, fontsize=8)

    h_dim_x = -half_span - 10
    ax1.annotate("", xy=(h_dim_x, 0), xytext=(h_dim_x, top_y), arrowprops=dict(arrowstyle="<->", color=dim_color, lw=1))
    ax1.text(h_dim_x - 4, top_y / 2, f"H={H:.0f}", ha="right", va="center", color=text_color, fontsize=8, rotation=90)

    force_len = 35
    dx = force_len * math.cos(math.radians(theta))
    dy = force_len * math.sin(math.radians(theta))
    ax1.annotate("", xy=(0, top_y), xytext=(dx, top_y + dy), arrowprops=dict(arrowstyle="<-", color="#fc8181", lw=2))
    ax1.text(dx + 2, top_y + dy + 4, "P", color="#fc8181", fontsize=10, fontweight="bold")
    ax1.plot([0, force_len * 1.1], [top_y, top_y], color=centerline, linestyle=":", lw=0.8)
    theta_arc = patches.Arc((0, top_y), force_len * 0.8, force_len * 0.8, theta1=0, theta2=theta, linewidth=1, edgecolor="#fc8181", linestyle="-")
    ax1.add_patch(theta_arc)
    ax1.text(force_len * 0.24, top_y + force_len * 0.12, f"θ={theta}°", color="#fc8181", fontsize=7)
    ax1.text(0, -35, "Front View", ha="center", color=text_color, fontsize=9, fontstyle="italic")
    ax1.set_xlim(-half_span - 35, half_span + 45)
    ax1.set_ylim(-42, total_height + 20)

    ax2.set_aspect("equal")
    ax2.axis("off")
    ax2.set_facecolor(bg_color)
    ax2.add_patch(patches.Rectangle((-t / 2, 0), t, total_height, linewidth=2, edgecolor=edge_color, facecolor=fill_color, alpha=0.8))

    if t_p > 0:
        reinf_h = 2 * reinforcement_radius
        reinf_y = top_y - reinforcement_radius
        ax2.add_patch(patches.Rectangle((-t / 2 - t_p, reinf_y), t_p, reinf_h, linewidth=1.5, edgecolor=reinf_edge, facecolor="#2a2f50", alpha=0.7))
        ax2.add_patch(patches.Rectangle((t / 2, reinf_y), t_p, reinf_h, linewidth=1.5, edgecolor=reinf_edge, facecolor="#2a2f50", alpha=0.7))
        label_y = reinf_y + reinf_h + 6
        ax2.annotate("", xy=(t / 2, label_y), xytext=(t / 2 + t_p, label_y), arrowprops=dict(arrowstyle="<->", color=reinf_edge, lw=1))
        ax2.text(t / 2 + t_p / 2, label_y + 4, f"tp={t_p:.0f}", ha="center", color=reinf_edge, fontsize=7, fontweight="bold")

    side_extent = t / 2 + (t_p if t_p > 0 else 0)
    ax2.plot([-side_extent - 5, side_extent + 5], [top_y + hole_r, top_y + hole_r], color=centerline, linestyle="--", lw=0.8)
    ax2.plot([-side_extent - 5, side_extent + 5], [top_y - hole_r, top_y - hole_r], color=centerline, linestyle="--", lw=0.8)
    ax2.plot([0, 0], [-10, total_height + 12], color=centerline, linestyle="-.", lw=0.8)
    ax2.plot([-side_extent - 15, side_extent + 15], [top_y, top_y], color=centerline, linestyle="-.", lw=0.8)

    t_label_y = 25
    ax2.annotate("", xy=(-t / 2, t_label_y), xytext=(t / 2, t_label_y), arrowprops=dict(arrowstyle="<->", color=dim_color, lw=1))
    ax2.text(0, t_label_y + 4, f"t={t:.0f}", ha="center", color=text_color, fontsize=8)

    h_side_x = side_extent + 10
    ax2.annotate("", xy=(h_side_x, 0), xytext=(h_side_x, top_y), arrowprops=dict(arrowstyle="<->", color=dim_color, lw=1))
    ax2.text(h_side_x + 3, top_y / 2, f"H={H:.0f}", ha="left", va="center", color=text_color, fontsize=8, rotation=90)

    ax2.text(0, -35, "Side View", ha="center", color=text_color, fontsize=9, fontstyle="italic")
    ax2.set_xlim(-side_extent - 25, side_extent + 25)
    ax2.set_ylim(-42, total_height + 20)

    plt.tight_layout(pad=1.0)
    return fig
