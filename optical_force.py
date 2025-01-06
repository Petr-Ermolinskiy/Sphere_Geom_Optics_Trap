import numpy as np

from constants import SPEED_OF_LIGHT

# Discretize the laser beam into rays
def generate_rays(num_rays, w0, P, beam_focus=np.array([0, 0, 0]), lambda_=1064e-9):
    # Divergence angle of the Gaussian beam
    theta = lambda_ / (np.pi * w0)  # Divergence angle (radians)
    
    r = np.random.uniform(0, w0, num_rays)  # Radial position of rays
    theta_ray = np.random.uniform(-theta, theta, num_rays)  # Angular divergence of rays
    phi = np.random.uniform(0, 2 * np.pi, num_rays)  # Azimuthal angle of rays
    power_per_ray = P / num_rays  # Power carried by each ray
    
    # Ray directions in 3D space
    dx = np.sin(theta_ray) * np.cos(phi)
    dy = np.sin(theta_ray) * np.sin(phi)
    dz = np.cos(theta_ray)
    
    # Ray positions in 3D space (z = beam_focus[2])
    x_beam = r * np.cos(phi) + beam_focus[0]
    y_beam = r * np.sin(phi) + beam_focus[1]
    z_beam = np.full(num_rays, beam_focus[2])  # All rays are in the z = beam_focus[2] plane
    
    # Ray directions (normalized)
    ray_directions = np.vstack((dx, dy, dz)).T
    ray_directions /= np.linalg.norm(ray_directions, axis=1)[:, np.newaxis]
    
    return x_beam, y_beam, z_beam, ray_directions, power_per_ray

# Calculate momentum transfer for a single ray
def momentum_transfer(ray_direction, intersection_point, sphere_center, n_medium, n_particle):
    # Surface normal at the intersection point
    n = (intersection_point - sphere_center) / np.linalg.norm(intersection_point - sphere_center)
    
    # Angle of incidence
    cos_theta_i = np.dot(-ray_direction, n)
    cos_theta_i = np.clip(cos_theta_i, -1.0, 1.0)  # Clamp to avoid numerical errors
    theta_i = np.arccos(cos_theta_i)
    
    # Snell's law for refraction
    theta_r = np.arcsin((n_medium / n_particle) * np.sin(theta_i))  # Angle of refraction
    
    # Fresnel coefficients for reflection and transmission
    R = ((n_medium * np.cos(theta_i) - n_particle * np.cos(theta_r)) /
         (n_medium * np.cos(theta_i) + n_particle * np.cos(theta_r)))**2
    T = 1 - R  # Transmission coefficient
    
    # Change in momentum due to reflection
    delta_p_reflection = 2 * np.cos(theta_i) * n
    
    # Change in momentum due to transmission
    transmitted_direction = n_medium / n_particle * ray_direction + (n_medium / n_particle * np.cos(theta_i) - np.cos(theta_r)) * n
    delta_p_transmission = ray_direction - transmitted_direction
    
    # Total change in momentum
    delta_p = (R * delta_p_reflection + T * delta_p_transmission) * (n_medium / SPEED_OF_LIGHT)
    return delta_p

# Calculate scattering force and torque
def calculate_force_and_torque(radius, num_rays, w0, P, n_medium, n_particle, sphere_position, 
                               beam_focus=np.array([0, 0, 0]), lambda_=1064e-9):
    x_beam, y_beam, z_beam, ray_directions, power_per_ray = generate_rays(num_rays, w0, P, beam_focus, lambda_)
    F_scattering = np.zeros(3)  # Scattering force vector
    torque = np.zeros(3)  # Torque vector
    intersection_points = []  # Store intersection points for visualization
    
    for i in range(num_rays):
        # Ray direction
        d = ray_directions[i]
        
        # Sphere center relative to beam focus
        sphere_center = sphere_position - beam_focus
        
        # Calculate intersection of ray with sphere
        # Ray equation: r = r0 + t * d, where r0 is the ray origin (beam_focus), d is the ray direction
        # Sphere equation: |r - sphere_center|^2 = radius^2
        r0 = beam_focus
        oc = r0 - sphere_center
        a = np.dot(d, d)
        b = 2 * np.dot(oc, d)
        c = np.dot(oc, oc) - radius**2
        discriminant = b**2 - 4 * a * c
        
        if discriminant >= 0:  # Ray intersects the sphere
            t = (-b - np.sqrt(discriminant)) / (2 * a)  # Use the smaller root for the first intersection
            intersection_point = r0 + t * d
            intersection_points.append(intersection_point)
            
            # Calculate momentum transfer
            delta_p = momentum_transfer(d, intersection_point, sphere_center, n_medium, n_particle)
            
            # Force direction (positive of momentum change)
            force_direction = +delta_p  # Positive of change in momentum (momentum conservation)
            
            # Scattering force (momentum transfer per unit time)
            F_scattering += force_direction * power_per_ray
            
            # Torque (cross product of position vector and force)
            position_vector = intersection_point - sphere_center
            torque += np.cross(position_vector, force_direction * power_per_ray)
    
    return F_scattering, torque, intersection_points

