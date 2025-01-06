import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.textbox import TextBox

from .pygame_SpinBox import SpinBox

from constants import WHITE, WIDTH, HEIGHT, BLACK, GREY, BLUE

class CalculationWindow:
    # Class variables for X positions
    SPIN_BOX_X = 150  # X position for spin boxes
    RIGHT_SIDE_X = WIDTH - 350  # X position for elements on the right side

    def __init__(self, return_to_menu_callback):
        # Initialize a new Pygame display (new window)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Initialize the screen first
        pygame.display.set_caption("Force calculation")  # Updated window title
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.running = True
        self.return_to_menu_callback = return_to_menu_callback  # Callback to return to the menu

        # Slider font
        self.slider_font = pygame.font.SysFont("Arial", 16)  # Font for labels

        # Initialize the dropdown (view toggle list) in the top-right corner
        self.dropdown = Dropdown(
            self.screen,  # Surface to draw on
            x=self.RIGHT_SIDE_X,  # X position (top-right corner)
            y=50,  # Y position
            width=200,  # Width of the dropdown
            height=30,  # Height of the dropdown
            name="Select axis",  # Name of the dropdown
            choices=["X", "Y", "Z"],  # Choices for the dropdown
            values=["X", "Y", "Z"],  # Values corresponding to choices
            fontSize=30,  # Font size
            textColour=BLACK,  # Text color
            inactiveColour=GREY,  # Background color when inactive
            hoverColour=GREY  # Background color when hovered
        )

        # SpinBoxes (replacing sliders)
        self.beam_waist_spin_box = SpinBox(
            self.screen,  # Surface to draw on
            x=self.SPIN_BOX_X,  # X position
            y=50,  # Y position (shifted up by 50 pixels)
            width=150,  # Width of the spin box
            height=30,  # Height of the spin box
            min_value=0.1,  # Minimum value
            max_value=10.0,  # Maximum value
            step=0.1,  # Step size
            initial_value=1.0  # Initial value
        )
        self.laser_power_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=110,  # Increased vertical spacing (shifted up by 50 pixels)
            width=150,
            height=30,
            min_value=0.1,
            max_value=100.0,
            step=0.1,
            initial_value=10.0
        )
        self.n_particle_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=170,  # Increased vertical spacing (shifted up by 50 pixels)
            width=150,
            height=30,
            min_value=1,
            max_value=1000,
            step=1,
            initial_value=100
        )
        self.n_medium_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=230,  # Increased vertical spacing (shifted up by 50 pixels)
            width=150,
            height=30,
            min_value=1.0,
            max_value=2.0,
            step=0.01,
            initial_value=1.33
        )
        self.dt_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=290,  # Increased vertical spacing (shifted up by 50 pixels)
            width=150,
            height=30,
            min_value=0.01,
            max_value=1.0,
            step=0.01,
            initial_value=0.1
        )
        self.viscosity_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=350,  # Increased vertical spacing (shifted up by 50 pixels)
            width=150,
            height=30,
            min_value=1,
            max_value=10,
            step=0.1,
            initial_value=1
        )
        self.temperature_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=410,  # Increased vertical spacing (shifted up by 50 pixels)
            width=150,
            height=30,
            min_value=100,
            max_value=500,
            step=1,
            initial_value=300
        )
        self.radius_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=470,  # Increased vertical spacing (shifted up by 50 pixels)
            width=150,
            height=30,
            min_value=1,
            max_value=100,
            step=1,
            initial_value=10
        )
        self.num_rays_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=530,  # Increased vertical spacing (shifted up by 50 pixels)
            width=150,
            height=30,
            min_value=1,
            max_value=1000,
            step=1,
            initial_value=100
        )

        # Labels for spin boxes
        self.beam_waist_label = self.slider_font.render("Beam Waist (µm)", True, BLACK)
        self.laser_power_label = self.slider_font.render("Laser Power (mW)", True, BLACK)
        self.n_particle_label = self.slider_font.render("Number of Particles", True, BLACK)
        self.n_medium_label = self.slider_font.render("Refractive Index (Medium)", True, BLACK)
        self.dt_label = self.slider_font.render("dt (s)", True, BLACK)
        self.viscosity_label = self.slider_font.render("Viscosity (mPa·s)", True, BLACK)
        self.temperature_label = self.slider_font.render("Temperature (K)", True, BLACK)
        self.radius_label = self.slider_font.render("Radius (µm)", True, BLACK)
        self.num_rays_label = self.slider_font.render("Number of Rays", True, BLACK)

        # TextBox for path to save (only one text box remains)
        self.path_box = TextBox(
            self.screen,
            x=self.RIGHT_SIDE_X,  # X position (right side)
            y=HEIGHT - 370,  # Y position (100px above Min point spin box)
            width=400,  # Width of the text box
            height=30,  # Height of the text box
            fontSize=20,  # Font size
            borderThickness=1,  # Border thickness
            radius=5,  # Border radius
            textColour=BLACK,  # Text color
            borderColour=GREY  # Border color
        )
        self.path_label = self.font.render("Path to save:", True, BLACK)

        # SpinBoxes for "Min point, µm" and "Max point, µm"
        self.min_point_label = self.slider_font.render("Min point, µm", True, BLACK)
        self.min_point_spin_box = SpinBox(
            self.screen,
            x=self.RIGHT_SIDE_X,  # X position (right side)
            y=HEIGHT - 270,  # Y position (100px below path_box)
            width=200,  # Width of the spin box
            height=30,  # Height of the spin box
            min_value=-100,  # Minimum value
            max_value=100,  # Maximum value
            step=1,  # Step size
            initial_value=-10  # Default value
        )
        self.max_point_label = self.slider_font.render("Max point, µm", True, BLACK)
        self.max_point_spin_box = SpinBox(
            self.screen,
            x=self.RIGHT_SIDE_X,  # X position (right side)
            y=HEIGHT - 210,  # Y position (60px below Min point spin box)
            width=200,  # Width of the spin box
            height=30,  # Height of the spin box
            min_value=-100,  # Minimum value
            max_value=100,  # Maximum value
            step=1,  # Step size
            initial_value=10  # Default value
        )

        # Calculate and save results button (placed just above the Exit button with 40px spacing)
        self.calculate_button = Button(
            self.screen,
            x=self.RIGHT_SIDE_X,  # X position (right side)
            y=HEIGHT - 110,  # Y position (40px above Exit button)
            width=200,  # Width of the button
            height=50,  # Height of the button
            text="Calculate and Save",  # Button text
            fontSize=20,  # Font size
            margin=20,  # Margin between text and button edges
            inactiveColour=GREY,  # Color when not hovered
            hoverColour=BLUE,  # Color when hovered
            pressedColour=WHITE,  # Color when clicked
            radius=10  # Border radius
        )

        # Exit button (placed at the bottom-right)
        self.exit_button = Button(
            self.screen,  # Surface to draw on
            x=self.RIGHT_SIDE_X,  # X position (right side)
            y=HEIGHT - 50,  # Y position
            width=200,  # Width of the button
            height=50,  # Height of the button
            text="Exit",  # Button text
            fontSize=20,  # Font size
            margin=20,  # Margin between text and button edges
            inactiveColour=GREY,  # Color when not hovered
            hoverColour=BLUE,  # Color when hovered
            pressedColour=WHITE,  # Color when clicked
            radius=10  # Border radius
        )

    def run(self):
        while self.running:
            events = pygame.event.get()
            self.screen.fill(WHITE)
            self.handle_events(events)

            # Draw the dropdown
            self.dropdown.draw()

            # Draw the spin boxes and their labels
            self.screen.blit(self.beam_waist_label, (self.SPIN_BOX_X, 20))
            self.beam_waist_spin_box.draw()
            self.screen.blit(self.laser_power_label, (self.SPIN_BOX_X, 80))
            self.laser_power_spin_box.draw()
            self.screen.blit(self.n_particle_label, (self.SPIN_BOX_X, 140))
            self.n_particle_spin_box.draw()
            self.screen.blit(self.n_medium_label, (self.SPIN_BOX_X, 200))
            self.n_medium_spin_box.draw()
            self.screen.blit(self.dt_label, (self.SPIN_BOX_X, 260))
            self.dt_spin_box.draw()
            self.screen.blit(self.viscosity_label, (self.SPIN_BOX_X, 320))
            self.viscosity_spin_box.draw()
            self.screen.blit(self.temperature_label, (self.SPIN_BOX_X, 380))
            self.temperature_spin_box.draw()
            self.screen.blit(self.radius_label, (self.SPIN_BOX_X, 440))
            self.radius_spin_box.draw()
            self.screen.blit(self.num_rays_label, (self.SPIN_BOX_X, 500))
            self.num_rays_spin_box.draw()

            # Draw the path to save input
            self.screen.blit(self.path_label, (self.RIGHT_SIDE_X, HEIGHT - 400))
            self.path_box.draw()

            # Draw the "Min point, µm" and "Max point, µm" spin boxes
            self.screen.blit(self.min_point_label, (self.RIGHT_SIDE_X, HEIGHT - 300))
            self.min_point_spin_box.draw()
            self.screen.blit(self.max_point_label, (self.RIGHT_SIDE_X, HEIGHT - 240))
            self.max_point_spin_box.draw()

            # Draw the calculate button
            self.calculate_button.draw()

            # Draw the exit button
            self.exit_button.draw()

            pygame.display.flip()
            self.clock.tick(100)
            

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.return_to_menu_callback()  # Return to the menu
    
        # Check if the exit button is clicked
        if self.exit_button.clicked:
            self.running = False
            self.return_to_menu_callback()  # Return to the menu
    
        # Check if the calculate button is clicked
        if self.calculate_button.clicked:
            self.calculate_and_save_results()
            self.calculate_button.clicked = False  # Reset the clicked state

        pygame_widgets.update(events)  # Update pygame_widgets

    def calculate_and_save_results(self):
        # Get the selected view
        selected_view = self.dropdown.getSelected()

        # Get spin box values
        beam_waist = self.beam_waist_spin_box.getValue()
        laser_power = self.laser_power_spin_box.getValue()
        n_particle = self.n_particle_spin_box.getValue()
        n_medium = self.n_medium_spin_box.getValue()
        dt = self.dt_spin_box.getValue()
        viscosity = self.viscosity_spin_box.getValue()
        temperature = self.temperature_spin_box.getValue()
        radius = self.radius_spin_box.getValue()
        num_rays = self.num_rays_spin_box.getValue()

        # Get the save path
        save_path = self.path_box.getText()

        # Get "Min point, µm" and "Max point, µm" values
        min_point = self.min_point_spin_box.getValue()
        max_point = self.max_point_spin_box.getValue()

        # Perform calculations and save results (placeholder logic)
        print(f"Selected View: {selected_view}")
        print(f"Beam Waist: {beam_waist}, Laser Power: {laser_power}, Number of Particles: {n_particle}")
        print(f"Refractive Index (Medium): {n_medium}, dt: {dt}, Viscosity: {viscosity}")
        print(f"Temperature: {temperature}, Radius: {radius}, Number of Rays: {num_rays}")
        print(f"Save Path: {save_path}")
        print(f"Min Point: {min_point}, Max Point: {max_point}")

        # Add your calculation and saving logic here

