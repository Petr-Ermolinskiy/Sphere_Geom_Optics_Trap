import pygame
import numpy as np
import math

from constants import BOLTZMANN_CONSTANT, WIDTH, HEIGHT, BLUE, POINT_COLOR, CONE_COLOR

from optical_force import calculate_force_and_torque

class Sphere:
    def __init__(self, radius):
        self.pos = pygame.Vector3(0, 0, 0)
        self.radius = radius

    def brownian_motion(self, dt, temperature, viscosity):
        radius_meters = self.radius * 1e-6
        viscosity_pas = viscosity * 1e-3
        D = (BOLTZMANN_CONSTANT * temperature * dt) / (6 * math.pi * viscosity_pas * radius_meters)
        displacement_std = math.sqrt(2 * D * dt)
        displacement_std_um = displacement_std * 1e6
        displacement = np.random.normal(0, displacement_std_um, 3)
        displacement = pygame.Vector3(displacement.tolist())
        self.pos += displacement

    def central_force(self, dt):
        center = pygame.Vector3(0, 0, 0)
        displacement = center - self.pos
        displacement_length = displacement.length()
        if displacement_length > 0:
            displacement_normalized = displacement / displacement_length
            displacement_magnitude = min(displacement_length**2 * dt, displacement_length)
            self.pos += displacement_normalized * displacement_magnitude

    def laser_trapping_force(self, dt, n_medium, n_particle, P, w0, viscosity, number_of_rays):
        radius_meters = self.radius * 1e-6
        viscosity_pas = viscosity * 1e-3
        gamma = 6 * np.pi * viscosity_pas * radius_meters
        F, torque, _ = calculate_force_and_torque(radius_meters, number_of_rays, w0, P, n_medium, n_particle, self.pos*1e-6)
        x = (F[0] / gamma) * dt * 1e6
        y = (F[1] / gamma) * dt * 1e6
        z = (F[2] / gamma) * dt * 1e6
        self.pos += pygame.Vector3(x, y, z)

    def draw(self, screen, mode, scale):
        sphere_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        x, y = self.project_3d_to_2d(mode, scale)
        if not (math.isnan(x) or math.isnan(y)):
            pygame.draw.circle(sphere_surface, BLUE, (int(x), int(y)), int(self.radius * scale))
            screen.blit(sphere_surface, (0, 0))

    def project_3d_to_2d(self, mode, scale):
        if mode == "xy":
            return self.pos.x * scale + WIDTH // 2, self.pos.y * scale + HEIGHT // 2
        elif mode == "xz":
            return self.pos.x * scale + WIDTH // 2, self.pos.z * scale + HEIGHT // 2
        elif mode == "yz":
            return self.pos.y * scale + WIDTH // 2, self.pos.z * scale + HEIGHT // 2
        else:
            # Default to xz mode if an invalid mode is provided
            return self.pos.x * scale + WIDTH // 2, self.pos.z * scale + HEIGHT // 2

class Cones:
    def __init__(self):
        self.light_wavelength = 1.064
        self.height = 200

    def update_base_radius(self, beam_waist):
        angle = self.light_wavelength / (np.pi * beam_waist)
        self.base_radius = 2 * math.tan(angle) * self.height

    def draw(self, screen, mode, scale, beam_waist, force_field):
        if force_field != "Laser Trapping Force":
            return None
        self.update_base_radius(beam_waist)
        if mode == "xy":
            point_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(point_surface, POINT_COLOR, (WIDTH // 2, HEIGHT // 2), 3)
            screen.blit(point_surface, (0, 0))
        else:
            cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            base_radius = self.base_radius * scale
            height = self.height * scale
            pygame.draw.polygon(cone_surface, CONE_COLOR, [
                (WIDTH // 2, HEIGHT // 2),
                (WIDTH // 2 - base_radius, HEIGHT // 2 - height),
                (WIDTH // 2 + base_radius, HEIGHT // 2 - height)
            ])
            pygame.draw.polygon(cone_surface, CONE_COLOR, [
                (WIDTH // 2, HEIGHT // 2),
                (WIDTH // 2 - base_radius, HEIGHT // 2 + height),
                (WIDTH // 2 + base_radius, HEIGHT // 2 + height)
            ])
            screen.blit(cone_surface, (0, 0))
