import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse


# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------
a = 4.0
b = 2.0
phi = np.deg2rad(35.0)

theta_values = np.linspace(0, np.pi, 180)


# ------------------------------------------------------------
# Geometry
# ------------------------------------------------------------
def support(phi, theta, a, b, side):
    if side == 1:
        alpha = theta - phi
    else:
        alpha = theta + phi

    return np.sqrt(
        a**2 * np.sin(alpha)**2 +
        b**2 * np.cos(alpha)**2
    )


def ellipse_matrix(theta, a, b):
    c = np.cos(theta)
    s = np.sin(theta)

    R = np.array([
        [c, -s],
        [s,  c]
    ])

    return R @ np.diag([a**2, b**2]) @ R.T


def geometry(theta):
    # Unit ray directions
    d1 = np.array([np.cos(phi), np.sin(phi)])
    d2 = np.array([-np.cos(phi), np.sin(phi)])

    # Inward normals
    n1 = np.array([-np.sin(phi), np.cos(phi)])
    n2 = np.array([ np.sin(phi), np.cos(phi)])

    # Support distances
    h1 = support(phi, theta, a, b, 1)
    h2 = support(phi, theta, a, b, 2)

    # Center
    x0 = (h2 - h1) / (2 * np.sin(phi))
    y0 = (h1 + h2) / (2 * np.cos(phi))

    C = np.array([x0, y0])

    # Ellipse matrix
    Q = ellipse_matrix(theta, a, b)

    # Tangency points
    P1 = C - Q @ n1 / h1
    P2 = C - Q @ n2 / h2

    # Ray parameters
    t1 = np.dot(P1, d1)
    t2 = np.dot(P2, d2)

    return C, P1, P2, t1, t2


# ------------------------------------------------------------
# Numerical verification
# ------------------------------------------------------------
for theta in [0, 0.3, 0.8, 1.2, 2.0]:

    C, P1, P2, t1, t2 = geometry(theta)

    print(f"\ntheta = {np.rad2deg(theta):.2f} degrees")
    print("center =", C)
    print("P1 =", P1, "   t1 =", t1)
    print("P2 =", P2, "   t2 =", t2)

    # Check that the points lie on the corresponding lines
    line1_error = np.dot(
        np.array([-np.sin(phi), np.cos(phi)]), P1
    )

    line2_error = np.dot(
        np.array([np.sin(phi), np.cos(phi)]), P2
    )

    print("line 1 error =", line1_error)
    print("line 2 error =", line2_error)


# ------------------------------------------------------------
# Figure
# ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 8))

L = 10

# Rays
d1 = np.array([np.cos(phi), np.sin(phi)])
d2 = np.array([-np.cos(phi), np.sin(phi)])

t = np.linspace(0, L, 300)

ax.plot(
    t * d1[0],
    t * d1[1],
    'k--',
    lw=2,
    label=r"$p_1(t)$"
)

ax.plot(
    t * d2[0],
    t * d2[1],
    'k--',
    lw=2,
    label=r"$p_2(t)$"
)

# Origin
ax.plot(0, 0, 'ko', ms=5)

# Ellipse
ellipse_patch = Ellipse(
    xy=(0, 0),
    width=2*a,
    height=2*b,
    angle=0,
    fill=False,
    lw=2
)

ax.add_patch(ellipse_patch)

# Center
center_point, = ax.plot([], [], 'o', ms=7)

# Tangency points
contact1, = ax.plot([], [], 'o', ms=6)
contact2, = ax.plot([], [], 'o', ms=6)

# Major axis
major_axis, = ax.plot([], [], '-', lw=1.5)

# Text
info = ax.text(
    0.03, 0.97, '',
    transform=ax.transAxes,
    verticalalignment='top',
    fontsize=11
)


# ------------------------------------------------------------
# Animation
# ------------------------------------------------------------
def update(frame):

    theta = theta_values[frame]

    C, P1, P2, t1, t2 = geometry(theta)

    # Move ellipse
    ellipse_patch.center = C
    ellipse_patch.angle = np.rad2deg(theta)

    # Center
    center_point.set_data([C[0]], [C[1]])

    # Contact points
    contact1.set_data([P1[0]], [P1[1]])
    contact2.set_data([P2[0]], [P2[1]])

    # Major axis
    u = np.array([np.cos(theta), np.sin(theta)])

    A1 = C - a*u
    A2 = C + a*u

    major_axis.set_data(
        [A1[0], A2[0]],
        [A1[1], A2[1]]
    )

    info.set_text(
        rf"$\theta={np.rad2deg(theta):.1f}^\circ$" + "\n"
        rf"$C=({C[0]:.3f},{C[1]:.3f})$" + "\n"
        rf"$t_1={t1:.3f},\quad t_2={t2:.3f}$"
    )

    return (
        ellipse_patch,
        center_point,
        contact1,
        contact2,
        major_axis,
        info
    )


# ------------------------------------------------------------
# Formatting
# ------------------------------------------------------------
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(-8, 8)
ax.set_ylim(-1, 9)
ax.grid(True, alpha=0.25)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(
    "Ellipse tangent to two rays: center determined by orientation"
)

ax.legend()

ani = FuncAnimation(
    fig,
    update,
    frames=len(theta_values),
    interval=40,
    blit=False
)

plt.show()

# To save:
# ani.save("ellipse_two_rays.mp4", writer="ffmpeg", dpi=150)
# or
# ani.save("ellipse_two_rays.gif", writer="pillow", dpi=120)