# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains Python-based physics simulations using matplotlib for animation. The simulations demonstrate bouncing objects with collision detection in 2D space.

## Architecture

The codebase consists of two independent animation modules:

1. **square.py** - Basic bouncing square animation
   - Single square bouncing inside a fixed boundary
   - Simple boundary collision detection with velocity reversal

2. **square_circle.py** - Multi-object collision simulation
   - Two independent objects (square and circle) bouncing within a boundary
   - Implements three collision detection systems:
     - Square-to-boundary collision (check_square_boundary_collision)
     - Circle-to-boundary collision (check_circle_boundary_collision)
     - Square-to-circle collision (check_square_circle_collision)
   - Uses separating axis theorem for square-circle collision detection
   - Implements elastic collision physics with equal mass assumption

### Key Physics Algorithms

**Square-Circle Collision Detection** (square_circle.py:92-148):
- Finds closest point on square to circle center
- Calculates distance to determine overlap
- Computes collision normal for separation and velocity adjustment
- Uses relative velocity along normal to determine bounce direction
- Applies elastic collision response

## Running the Code

**Run basic square animation:**
```bash
python3 square.py
```

**Run square-circle collision simulation:**
```bash
python3 square_circle.py
```

Both scripts require matplotlib. Install if needed:
```bash
pip3 install matplotlib numpy
```

## Animation Parameters

All animation parameters are defined as global variables at the top of each file:
- Boundary size: `outer_size`
- Object dimensions: `square_size`, `circle_radius`, `inner_size`
- Initial positions: `pos_x/y`, `square_x/y`, `circle_x/y`
- Initial velocities: `vel_x/y`, `square_vx/vy`, `circle_vx/vy`

To modify simulation behavior, adjust these values before running.

## Code Structure

Each file follows the same pattern:
1. Import dependencies (matplotlib.pyplot, animation, patches, numpy)
2. Define animation parameters
3. Initialize figure and axes
4. Create patches (Rectangle, Circle)
5. Define collision detection functions
6. Define animate() function that updates positions per frame
7. Create FuncAnimation object and display with plt.show()

The animate() function is called repeatedly by matplotlib's FuncAnimation with the interval parameter controlling frame rate (20ms = ~50 fps).
