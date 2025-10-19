import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

# Animation parameters
outer_size = 10

# Square parameters
square_size = 0.8
square_x = 2.0
square_y = 3.0
square_vx = 0.08
square_vy = 0.06

# Circle parameters
circle_radius = 0.5
circle_x = 7.0
circle_y = 6.0
circle_vx = -0.07
circle_vy = -0.05

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, outer_size)
ax.set_ylim(0, outer_size)
ax.set_aspect('equal')
ax.set_title('Bouncing Square and Circle with Collision Detection')

# Create outer boundary square (fixed)
outer_square = patches.Rectangle((0, 0), outer_size, outer_size,
                                 linewidth=3, edgecolor='blue',
                                 facecolor='none')
ax.add_patch(outer_square)

# Create moving square
moving_square = patches.Rectangle((square_x, square_y), square_size, square_size,
                                  linewidth=2, edgecolor='red',
                                  facecolor='orange')
ax.add_patch(moving_square)

# Create moving circle
moving_circle = patches.Circle((circle_x, circle_y), circle_radius,
                               linewidth=2, edgecolor='green',
                               facecolor='lightgreen')
ax.add_patch(moving_circle)

def check_square_boundary_collision():
    """Check and handle square collision with outer boundary."""
    global square_x, square_y, square_vx, square_vy

    # Right boundary
    if square_x + square_size >= outer_size:
        square_x = outer_size - square_size
        square_vx = -abs(square_vx)
    # Left boundary
    elif square_x <= 0:
        square_x = 0
        square_vx = abs(square_vx)

    # Top boundary
    if square_y + square_size >= outer_size:
        square_y = outer_size - square_size
        square_vy = -abs(square_vy)
    # Bottom boundary
    elif square_y <= 0:
        square_y = 0
        square_vy = abs(square_vy)

def check_circle_boundary_collision():
    """Check and handle circle collision with outer boundary."""
    global circle_x, circle_y, circle_vx, circle_vy

    # Right boundary
    if circle_x + circle_radius >= outer_size:
        circle_x = outer_size - circle_radius
        circle_vx = -abs(circle_vx)
    # Left boundary
    elif circle_x - circle_radius <= 0:
        circle_x = circle_radius
        circle_vx = abs(circle_vx)

    # Top boundary
    if circle_y + circle_radius >= outer_size:
        circle_y = outer_size - circle_radius
        circle_vy = -abs(circle_vy)
    # Bottom boundary
    elif circle_y - circle_radius <= 0:
        circle_y = circle_radius
        circle_vy = abs(circle_vy)

def check_square_circle_collision():
    """Check and handle collision between square and circle."""
    global square_x, square_y, square_vx, square_vy
    global circle_x, circle_y, circle_vx, circle_vy

    # Find the closest point on the square to the circle center
    closest_x = max(square_x, min(circle_x, square_x + square_size))
    closest_y = max(square_y, min(circle_y, square_y + square_size))

    # Calculate distance from circle center to closest point
    dist_x = circle_x - closest_x
    dist_y = circle_y - closest_y
    distance = np.sqrt(dist_x**2 + dist_y**2)

    # Check if collision occurred
    if distance < circle_radius:
        # Collision detected!

        # Calculate collision normal (from square to circle)
        if distance > 0:
            normal_x = dist_x / distance
            normal_y = dist_y / distance
        else:
            # Circle center is inside square, use velocity-based normal
            normal_x = circle_x - (square_x + square_size/2)
            normal_y = circle_y - (square_y + square_size/2)
            norm = np.sqrt(normal_x**2 + normal_y**2)
            if norm > 0:
                normal_x /= norm
                normal_y /= norm
            else:
                normal_x, normal_y = 1, 0

        # Separate the objects to prevent overlap
        overlap = circle_radius - distance
        circle_x += normal_x * overlap * 0.5
        circle_y += normal_y * overlap * 0.5
        square_x -= normal_x * overlap * 0.5
        square_y -= normal_y * overlap * 0.5

        # Calculate relative velocity
        rel_vx = square_vx - circle_vx
        rel_vy = square_vy - circle_vy

        # Calculate relative velocity along collision normal
        vel_along_normal = rel_vx * normal_x + rel_vy * normal_y

        # Only resolve if objects are moving towards each other
        if vel_along_normal < 0:
            return

        # Bounce with elastic collision (simple version - equal mass)
        # Exchange velocity components along the normal
        square_vx -= vel_along_normal * normal_x
        square_vy -= vel_along_normal * normal_y
        circle_vx += vel_along_normal * normal_x
        circle_vy += vel_along_normal * normal_y

def animate(frame):
    global square_x, square_y, square_vx, square_vy
    global circle_x, circle_y, circle_vx, circle_vy

    # Update positions
    square_x += square_vx
    square_y += square_vy
    circle_x += circle_vx
    circle_y += circle_vy

    # Check collisions
    check_square_boundary_collision()
    check_circle_boundary_collision()
    check_square_circle_collision()

    # Update patch positions
    moving_square.set_xy((square_x, square_y))
    moving_circle.center = (circle_x, circle_y)

    return moving_square, moving_circle

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=2000,
                              interval=20, blit=True, repeat=True)

plt.show()
