import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

# Animation parameters
outer_size = 10
inner_size = 1
speed_x = 0.1
speed_y = 0.08

# Initial position of inner square (center)
pos_x = outer_size / 2
pos_y = outer_size / 2

# Velocity
vel_x = speed_x
vel_y = speed_y

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, outer_size)
ax.set_ylim(0, outer_size)
ax.set_aspect('equal')
ax.set_title('Bouncing Square Animation')

# Create outer square (fixed)
outer_square = patches.Rectangle((0, 0), outer_size, outer_size,
                                 linewidth=3, edgecolor='blue',
                                 facecolor='none')
ax.add_patch(outer_square)

# Create inner square (moving)
inner_square = patches.Rectangle((pos_x, pos_y), inner_size, inner_size,
                                 linewidth=2, edgecolor='red',
                                 facecolor='orange')
ax.add_patch(inner_square)

def animate(frame):
    global pos_x, pos_y, vel_x, vel_y

    # Update position
    pos_x += vel_x
    pos_y += vel_y

    # Check for collision with boundaries and bounce
    # Right boundary
    if pos_x + inner_size >= outer_size:
        pos_x = outer_size - inner_size
        vel_x = -vel_x
    # Left boundary
    elif pos_x <= 0:
        pos_x = 0
        vel_x = -vel_x

    # Top boundary
    if pos_y + inner_size >= outer_size:
        pos_y = outer_size - inner_size
        vel_y = -vel_y
    # Bottom boundary
    elif pos_y <= 0:
        pos_y = 0
        vel_y = -vel_y

    # Update inner square position
    inner_square.set_xy((pos_x, pos_y))

    return inner_square,

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=1000,
                              interval=20, blit=True, repeat=True)

plt.show()
