import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

from .objects import Sphere, Cones
from constants import HEIGHT, WIDTH, BLACK, WHITE, GREY, BLUE


class Simulation:
    def __init__(self, return_to_menu_callback):
        # pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("3D Brownian Motion Simulation")
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()

        # Input active
        self.active_input = None  # Tracks which coordinate is being edited (0: x, 1: y, 2: z)
        self.input_buffer = ""  # Stores the current input for the active coordinate

        # Sliders with labels (shifted 25 pixels higher)
        self.dt_slider = Slider(self.screen, 50, HEIGHT - 275, 200, 20, min=0.01, max=1, step=0.01, initial=0.01)
        self.viscosity_slider = Slider(self.screen, 50, HEIGHT - 225, 200, 20, min=1, max=10, step=0.1, initial=1)
        self.temperature_slider = Slider(self.screen, 50, HEIGHT - 175, 200, 20, min=100, max=500, step=1, initial=300)
        self.radius_slider = Slider(self.screen, 50, HEIGHT - 125, 200, 20, min=1, max=100, step=1, initial=10)
        self.n_medium_slider = Slider(self.screen, 50, HEIGHT - 325, 200, 20, min=1.0, max=2.0, step=0.01, initial=1.33)
        self.n_particle_slider = Slider(self.screen, 50, HEIGHT - 375, 200, 20, min=1.0, max=2.0, step=0.01, initial=1.59)
        self.laser_power_slider = Slider(self.screen, 50, HEIGHT - 425, 200, 20, min=1, max=40, step=0.1, initial=1)
        self.beam_waist_slider = Slider(self.screen, 50, HEIGHT - 475, 200, 20, min=0.5, max=10, step=0.1, initial=0.5)
        self.number_of_rays_slider = Slider(self.screen, 50, HEIGHT - 75, 200, 20, min=500, max=10000, step=100, initial=1000)

        # Buttons
        self.zoom_in_button = Button(self.screen, WIDTH - 150, 50, 40, 40, text="+", fontSize=20)
        self.zoom_out_button = Button(self.screen, WIDTH - 100, 50, 40, 40, text="-", fontSize=20)
        self.restart_button = Button(self.screen, WIDTH - 150, 100, 100, 40, text="Restart", fontSize=20)
        self.stop_button = Button(self.screen, WIDTH - 150, 150, 100, 40, text="Stop/Start", fontSize=20)
        self.exit_button = Button(self.screen, WIDTH - 150, 200, 100, 40, text="Exit", fontSize=20)

        # Dropdowns
        self.mode_dropdown = Dropdown(self.screen, WIDTH - 150, 250, 100, 30, name="View",
                                      choices=["xy", "xz", "yz"], values=["xy", "xz", "yz"], fontSize=20)
        self.force_dropdown = Dropdown(self.screen, 10, 10, 300, 30, name="Force Mode",
                                       choices=["Laser Trapping Force", "No Force", "Central Force"],
                                       values=["Laser Trapping Force", "No Force", "Central Force"], fontSize=30)

        # Sphere and Cones
        self.sphere = Sphere(self.radius_slider.getValue())
        self.cones = Cones()

        # Simulation state
        self.running = True
        self.simulation_active = True
        self.scale = 1.0
        
        # return!!!!!!!!
        self.return_to_menu_callback = return_to_menu_callback  # Callback to return to the menu

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            self.exit_button.listen(event)
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the current position window is clicked
                window_rect = pygame.Rect(WIDTH - 200, HEIGHT - 100, 180, 80)
                if window_rect.collidepoint(event.pos):
                    # Determine which coordinate is clicked
                    x, y = event.pos
                    if window_rect.y + 10 <= y <= window_rect.y + 30:
                        self.active_input = 0  # x
                    elif window_rect.y + 30 <= y <= window_rect.y + 50:
                        self.active_input = 1  # y
                    elif window_rect.y + 50 <= y <= window_rect.y + 70:
                        self.active_input = 2  # z
                    self.input_buffer = ""  # Reset input buffer
            if event.type == pygame.KEYDOWN:
                if self.active_input is not None:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_buffer = self.input_buffer[:-1]  # Remove last character
                    elif event.key == pygame.K_RETURN:
                        # Apply the input buffer to the active coordinate
                        if self.input_buffer:
                            try:
                                value = float(self.input_buffer)
                                if self.active_input == 0:
                                    self.sphere.pos.x = value
                                elif self.active_input == 1:
                                    self.sphere.pos.y = value
                                elif self.active_input == 2:
                                    self.sphere.pos.z = value
                            except ValueError:
                                pass  # Ignore invalid input
                        self.active_input = None  # Finish editing
                    else:
                        # Append the typed character to the input buffer
                        if event.unicode.isdigit() or event.unicode == '.' or event.unicode == '-':
                            self.input_buffer += event.unicode
        

        # Handle button clicks
        if self.zoom_in_button.clicked:
            self.scale *= 1.05
        if self.zoom_out_button.clicked:
            self.scale /= 1.05
        if self.restart_button.clicked:
            self.sphere.pos = pygame.Vector3(0, 0, 0)
            self.simulation_active = True
            
        # Manual button click detection
        if self.stop_button.clicked:
            self.simulation_active = not self.simulation_active
            self.stop_button.clicked = not self.stop_button.clicked

        
        if self.exit_button.clicked:
            self.running = False
            self.return_to_menu_callback()  # Return to the menu

        # Update sliders
        self.sphere.radius = self.radius_slider.getValue()

        # Update widgets
        pygame_widgets.update(events)

    def draw_scale_bar(self):
        scale_length_pixels = 100
        scale_length_um = scale_length_pixels / self.scale
        bar_x = WIDTH // 2 - scale_length_pixels // 2
        bar_y = HEIGHT - 50
        pygame.draw.line(self.screen, BLACK, (bar_x, bar_y), (bar_x + scale_length_pixels, bar_y), 3)
        label = self.font.render(f"{scale_length_um:.1f} µm", True, BLACK)
        self.screen.blit(label, (bar_x + scale_length_pixels // 2 - label.get_width() // 2, bar_y - 25))

    def draw_position_window(self):
            # Create a window to display the position of the sphere
            window_rect = pygame.Rect(WIDTH - 200, HEIGHT - 100, 180, 80)
            pygame.draw.rect(self.screen, GREY, window_rect)
    
            # Display the position in micrometers
            pos_um = self.sphere.pos  # Already in micrometers
            labels = [
                f"x: {pos_um.x:.2f} µm",
                f"y: {pos_um.y:.2f} µm",
                f"z: {pos_um.z:.2f} µm"
            ]
    
            # Draw the labels and highlight the active input field
            for i, label in enumerate(labels):
                text_color = BLACK
                if self.active_input == i:
                    text_color = BLUE  # Highlight the active input field
                    label = f"{['x', 'y', 'z'][i]}: {self.input_buffer}"  # Show the input buffer
    
                label_surface = self.font.render(label, True, text_color)
                self.screen.blit(label_surface, (window_rect.x + 10, window_rect.y + 10 + i * 20))
    
            # Add abbreviation
            self.screen.blit(self.font.render("Current Position:", True, BLACK), 
                             (window_rect.x + 10, window_rect.y - 20))

    
    def draw_indicator(self, text):
        indicator_surface = self.font.render(text, True, BLACK)
        self.screen.blit(indicator_surface, (5, HEIGHT - 30))

    def draw_slider_labels(self):
        # Draw labels above sliders with values in parentheses
        labels = [
            ("dt (s)", self.dt_slider),
            ("Viscosity (mPa·s)", self.viscosity_slider),
            ("Temperature (K)", self.temperature_slider),
            ("Radius (µm)", self.radius_slider),
            ("n_medium", self.n_medium_slider),
            ("n_particle", self.n_particle_slider),
            ("Laser Power (mW)", self.laser_power_slider),
            ("Beam Waist (µm)", self.beam_waist_slider),
            ("Number of Rays", self.number_of_rays_slider),
        ]
        for label_text, slider in labels:
            value = slider.getValue()
            label = self.font.render(f"{label_text} ({value:.2f})", True, BLACK)
            self.screen.blit(label, (slider.getX(), slider.getY() - 25))

    def run(self):
        import time
        while self.running:
            start = time.time()
            self.screen.fill(WHITE)
            self.handle_events()

            if self.simulation_active:
                dt = self.dt_slider.getValue()
                viscosity = self.viscosity_slider.getValue()
                temperature = self.temperature_slider.getValue()
                self.sphere.brownian_motion(dt, temperature, viscosity)

                if self.force_dropdown.getSelected() == "Central Force":
                    self.sphere.central_force(dt)
                elif self.force_dropdown.getSelected() == "Laser Trapping Force":
                    n_medium = self.n_medium_slider.getValue()
                    n_particle = self.n_particle_slider.getValue()
                    P = self.laser_power_slider.getValue() * 1e-3
                    w0 = self.beam_waist_slider.getValue() * 1e-6
                    number_of_rays = int(self.number_of_rays_slider.getValue())
                    self.sphere.laser_trapping_force(dt, n_medium, n_particle, P, w0, viscosity, number_of_rays)

            self.cones.draw(self.screen, self.mode_dropdown.getSelected(), self.scale,
                            self.beam_waist_slider.getValue(), self.force_dropdown.getSelected())
            self.sphere.draw(self.screen, self.mode_dropdown.getSelected(), self.scale)

            self.draw_scale_bar()
            self.draw_position_window()
            self.draw_slider_labels()  # Draw slider labels with values

            end = int(1000 * (time.time() - start))
            delta_time = int(self.dt_slider.getValue() * 1000) - end
            delta_time = delta_time if delta_time > 0 else 0

            string_to_show = f"step simulation time = {end} ms; dt = {int(self.dt_slider.getValue() * 1000)} ms."
            string_to_show = "Real time: " + string_to_show if delta_time > 0 else "Not real time: " + string_to_show
            self.draw_indicator(string_to_show if self.simulation_active else "Simulation is stopped...")

            pygame.display.flip()
            pygame.time.delay(delta_time)
            # self.clock.tick(int(self.dt_slider.getValue() * 1000))

        pygame.quit()
