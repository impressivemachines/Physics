import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np

# Simulation parameters
NUM_PARTICLES = 100
DOMAIN_SIZE = 100.0
PARTICLE_RADIUS = 0.5
MIN_MASS = 1.0
MAX_MASS = 5.0
G = 1.0  # Gravitational constant
DT = 0.05  # Time step
SOFTENING = 0.5  # Softening parameter to prevent singularities
RESTITUTION = 1.0  # Coefficient of restitution (1.0 = perfectly elastic)

# Particle arrays
positions = np.zeros((NUM_PARTICLES, 2))  # [x, y]
velocities = np.zeros((NUM_PARTICLES, 2))  # [vx, vy]
masses = np.zeros(NUM_PARTICLES)

def initialize_particles():
    """Initialize particles with random non-overlapping positions and random masses."""
    global positions, velocities, masses

    # Assign random masses
    masses[:] = np.random.uniform(MIN_MASS, MAX_MASS, NUM_PARTICLES)

    # Initialize first particle randomly
    positions[0] = np.random.uniform(PARTICLE_RADIUS, DOMAIN_SIZE - PARTICLE_RADIUS, 2)

    # Place remaining particles ensuring no overlap
    for i in range(1, NUM_PARTICLES):
        max_attempts = 1000
        for attempt in range(max_attempts):
            # Generate random position
            new_pos = np.random.uniform(PARTICLE_RADIUS, DOMAIN_SIZE - PARTICLE_RADIUS, 2)

            # Check if it overlaps with any existing particle
            distances = np.linalg.norm(positions[:i] - new_pos, axis=1)
            min_distance = 2 * PARTICLE_RADIUS

            if np.all(distances > min_distance):
                positions[i] = new_pos
                break
        else:
            # If we couldn't find a spot, just place it randomly
            # This can happen with many particles
            positions[i] = np.random.uniform(PARTICLE_RADIUS, DOMAIN_SIZE - PARTICLE_RADIUS, 2)

    # Initialize velocities to zero (or small random velocities)
    velocities[:] = np.random.uniform(-0.5, 0.5, (NUM_PARTICLES, 2))

def calculate_gravitational_forces():
    """Calculate gravitational forces on all particles using Newton's law of gravitation."""
    forces = np.zeros((NUM_PARTICLES, 2))

    for i in range(NUM_PARTICLES):
        for j in range(i + 1, NUM_PARTICLES):
            # Vector from particle i to particle j
            r_vec = positions[j] - positions[i]
            r_mag = np.linalg.norm(r_vec)

            # Apply softening to prevent singularities when particles get very close
            r_softened = np.sqrt(r_mag**2 + SOFTENING**2)

            # Calculate gravitational force magnitude: F = G * m1 * m2 / r^2
            if r_mag > 0:
                force_mag = G * masses[i] * masses[j] / (r_softened**2)
                force_vec = force_mag * (r_vec / r_mag)

                # Apply equal and opposite forces
                forces[i] += force_vec
                forces[j] -= force_vec

    return forces

def handle_collisions():
    """Detect and resolve elastic collisions between particles."""
    for i in range(NUM_PARTICLES):
        for j in range(i + 1, NUM_PARTICLES):
            # Vector between particle centers
            r_vec = positions[j] - positions[i]
            distance = np.linalg.norm(r_vec)

            # Check if particles are colliding
            min_distance = 2 * PARTICLE_RADIUS
            if distance < min_distance and distance > 0:
                # Normalize the collision vector
                normal = r_vec / distance

                # Separate particles to prevent overlap
                overlap = min_distance - distance
                separation = normal * (overlap / 2)
                positions[i] -= separation
                positions[j] += separation

                # Calculate relative velocity
                rel_vel = velocities[i] - velocities[j]

                # Calculate relative velocity along collision normal
                vel_along_normal = np.dot(rel_vel, normal)

                # Only resolve if particles are moving towards each other
                if vel_along_normal > 0:
                    # Calculate impulse for elastic collision
                    # Using conservation of momentum and energy for elastic collision
                    total_mass = masses[i] + masses[j]
                    impulse = (2 * vel_along_normal * masses[j] / total_mass) * RESTITUTION

                    # Apply impulse to velocities
                    velocities[i] -= impulse * normal
                    velocities[j] += impulse * (masses[i] / masses[j]) * normal

def handle_boundary_collisions():
    """Handle collisions with domain boundaries (bounce off walls)."""
    for i in range(NUM_PARTICLES):
        # Left and right boundaries
        if positions[i, 0] - PARTICLE_RADIUS < 0:
            positions[i, 0] = PARTICLE_RADIUS
            velocities[i, 0] = abs(velocities[i, 0]) * RESTITUTION
        elif positions[i, 0] + PARTICLE_RADIUS > DOMAIN_SIZE:
            positions[i, 0] = DOMAIN_SIZE - PARTICLE_RADIUS
            velocities[i, 0] = -abs(velocities[i, 0]) * RESTITUTION

        # Bottom and top boundaries
        if positions[i, 1] - PARTICLE_RADIUS < 0:
            positions[i, 1] = PARTICLE_RADIUS
            velocities[i, 1] = abs(velocities[i, 1]) * RESTITUTION
        elif positions[i, 1] + PARTICLE_RADIUS > DOMAIN_SIZE:
            positions[i, 1] = DOMAIN_SIZE - PARTICLE_RADIUS
            velocities[i, 1] = -abs(velocities[i, 1]) * RESTITUTION

def update_particles():
    """Update particle positions and velocities using Verlet integration."""
    global positions, velocities

    # Calculate gravitational forces
    forces = calculate_gravitational_forces()

    # Calculate accelerations (F = ma => a = F/m)
    accelerations = forces / masses[:, np.newaxis]

    # Update velocities: v = v + a * dt
    velocities += accelerations * DT

    # Update positions: x = x + v * dt
    positions += velocities * DT

    # Handle collisions between particles
    handle_collisions()

    # Handle boundary collisions
    handle_boundary_collisions()

# Initialize particles
initialize_particles()

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, DOMAIN_SIZE)
ax.set_ylim(0, DOMAIN_SIZE)
ax.set_aspect('equal')
ax.set_title(f'Gravitational N-Body Simulation ({NUM_PARTICLES} particles)')
ax.set_xlabel('x')
ax.set_ylabel('y')

# Create boundary rectangle
boundary = patches.Rectangle((0, 0), DOMAIN_SIZE, DOMAIN_SIZE,
                             linewidth=2, edgecolor='black', facecolor='none')
ax.add_patch(boundary)

# Create particle circles with colors based on mass
circles = []
colors = plt.cm.viridis((masses - MIN_MASS) / (MAX_MASS - MIN_MASS))

for i in range(NUM_PARTICLES):
    circle = patches.Circle(positions[i], PARTICLE_RADIUS,
                           facecolor=colors[i], edgecolor='black', linewidth=0.5)
    ax.add_patch(circle)
    circles.append(circle)

def animate(frame):
    """Animation function called for each frame."""
    # Update physics
    update_particles()

    # Update circle positions
    for i, circle in enumerate(circles):
        circle.center = positions[i]

    return circles

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=5000,
                              interval=20, blit=True, repeat=True)

plt.show()
