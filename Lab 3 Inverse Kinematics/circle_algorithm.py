# Circle Draw Function
# Provided by Prof. Jaramillo

import math

def normalize_deg(deg):
    return (deg + 180.0) % 360.0 - 180.0

def generate_circle_path(n_points, radius_cm, closed=True, ccw=True):
    """
    Generate waypoints (x, y, theta_deg) approximating a circle of i
    radius R, starting and ending at (0,0,0). Circle center is (0, R).
    
    Args:
        n_points (int): number of waypoints to return.
        If closed=True, the first and last points are identical
        (closed loop).
        If closed=False, the endpoint repeat is omitted.
        radius_cm (float): circle radius in cm.
        closed (bool): include the final point equal to the start
        (default
        True).
        ccw (bool): traverse counterclockwise if True, clockwise if
        False.
    Returns:
        list[(float, float, float)]: (x, y, theta_deg) tuples.
    """
    if n_points <= 0:
    return []

    # Circle center such that start/end is (0,0,0)
    cx, cy = 0.0, float(radius_cm)
    
    # Start at bottom of circle so position is (0,0) and tangent is 0°
    phi0 = -math.pi / 2.0
    
    # How many steps along the circle?
    # If closed, we want to include both start and
    # end (same point) -> n_points-1 intervals.
    steps = n_points - 1 if closed and n_points > 1 else n_points - 1
    total_span = 2.0 * math.pi # full circle
    if steps <= 0:
        # Degenerate cases (n_points=1)
        x0 = cx + radius_cm * math.cos(phi0)
        y0 = cy + radius_cm * math.sin(phi0)
        theta0 = normalize_deg(math.degrees(phi0 + (math.pi/2.0)))
    return [(x0, y0, theta0)]
        
    dphi = total_span / steps
    if not ccw:
        dphi = -dphi
    
    points = []
    # When closed=True, iterate i=0..steps so last equals first.
    # When closed=False, iterate i=0..steps-1 so last != first.
    imax = steps if closed else steps
    for i in range(imax + (1 if closed else 0)):
        phi = phi0 + i * dphi
        x = cx + radius_cm * math.cos(phi)
        y = cy + radius_cm * math.sin(phi)
        # Tangent direction: perpendicular to radius.
        # For CCW, tangent angle = phi + 90°.
        # For CW, it flips sign; we can still use phi + 90° because
        # phi itself is walking CW when ccw=False.
        theta_deg = normalize_deg(math.degrees(phi + math.pi / 2.0))
        points.append((x, y, theta_deg))
        
        if not closed and i == steps:
            break
        
    # Ensure first point is exactly (0,0,0)
    points[0] = (0.0, 0.0, 0.0)
    if closed:
        points[-1] = (0.0, 0.0, 0.0)
    
    return points

# Example usage
if __name__ == "__main__":
    # 12 waypoints including the final return to (0,0,0), CCW
    waypoints = generate_circle_path(n_points=12,
                                     radius_cm=30,
                                     closed=True,
                                     ccw=True)
    for wp in waypoints:
        print(wp)
