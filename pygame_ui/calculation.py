import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.textbox import TextBox

from .pygame_SpinBox import SpinBox

from calc_force_and_save import calc_and_save

from constants import WHITE, WIDTH, HEIGHT, BLACK, GREY, BLUE

class CalculationWindow:
    # All spin boxes are placed at the same X position
    SPIN_BOX_X = 150
    RIGHT_SIDE_X = WIDTH - 350

    def __init__(self, return_to_menu_callback):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Force calculation")
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.running = True
        self.return_to_menu_callback = return_to_menu_callback  # Callback to return to the menu

        # Slider font
        self.slider_font = pygame.font.SysFont("Arial", 20)

        self.dropdown = Dropdown(
            self.screen,
            x=self.RIGHT_SIDE_X,
            y=50, 
            width=200, 
            height=30, 
            name="Select axis",  
            choices=["X", "Y", "Z"],  
            values=["X", "Y", "Z"],  
            fontSize=30,  
            textColour=BLACK,  
            inactiveColour=GREY,  
            hoverColour=GREY  
        )

        # SpinBoxes (replacing sliders)
        self.beam_waist_spin_box = SpinBox(
            self.screen,  
            x=self.SPIN_BOX_X,  
            y=50,  
            width=150,  
            height=30,  
            min_value=0.1,  
            max_value=10.0,  
            step=0.1,  
            initial_value=1.0 
        )
        self.laser_power_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=110,  
            width=150,
            height=30,
            min_value=1,
            max_value=200,
            step=1,
            initial_value=10,
            round_to=0
        )
        self.n_particle_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=170,  
            width=150,
            height=30,
            min_value=1.0,
            max_value=2.0,
            step=0.01,
            initial_value=1.59
        )
        self.n_medium_spin_box = SpinBox(
            self.screen,
            x=self.SPIN_BOX_X,
            y=230,  
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
            y=290,  
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
            y=350,  
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
            y=410,  
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
            y=470,  
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
            y=530,  
            width=150,
            height=30,
            min_value=100,
            max_value=10000,
            step=100,
            initial_value=1000,
            round_to=0
        )

        # Labels for spin boxes
        self.beam_waist_label = self.slider_font.render("Beam Waist (µm)", True, BLACK)
        self.laser_power_label = self.slider_font.render("Laser Power (mW)", True, BLACK)
        self.n_particle_label = self.slider_font.render("Refractive Index (Particle)", True, BLACK)
        self.n_medium_label = self.slider_font.render("Refractive Index (Medium)", True, BLACK)
        self.dt_label = self.slider_font.render("dt (sec.)", True, BLACK)
        self.viscosity_label = self.slider_font.render("Viscosity (mPa·s)", True, BLACK)
        self.temperature_label = self.slider_font.render("Temperature (K)", True, BLACK)
        self.radius_label = self.slider_font.render("Radius (µm)", True, BLACK)
        self.num_rays_label = self.slider_font.render("Number of Rays", True, BLACK)

        # TextBox for path to save
        self.path_box = TextBox(
            self.screen,
            x=self.RIGHT_SIDE_X,  
            y=HEIGHT - 370,  
            width=300,  
            height=30,  
            fontSize=20,  
            borderThickness=1, 
            radius=5,  
            textColour=BLACK,  
            borderColour=GREY  
        )
        self.path_label = self.font.render("Path to save:", True, BLACK)

        # SpinBoxes for "Min point, µm" and "Max point, µm"
        self.min_point_label = self.slider_font.render("Min point, µm", True, BLACK)
        self.min_point_spin_box = SpinBox(
            self.screen,
            x=self.RIGHT_SIDE_X, 
            y=HEIGHT - 270,  
            width=200,  
            height=30,  
            min_value=-100, 
            max_value=100,  
            step=1, 
            initial_value=-10  
        )
        self.max_point_label = self.slider_font.render("Max point, µm", True, BLACK)
        self.max_point_spin_box = SpinBox(
            self.screen,
            x=self.RIGHT_SIDE_X,  
            y=HEIGHT - 210,  
            width=200,  
            height=30,  
            min_value=-100,  
            max_value=100,  
            step=1, 
            initial_value=10  
        )

        # Calculate and save results button
        self.calculate_button = Button(
            self.screen,
            x=self.RIGHT_SIDE_X,  
            y=HEIGHT - 110,  
            width=200,  
            height=50,  
            text="Calculate and Save",  
            fontSize=20,  
            margin=20,  
            inactiveColour=GREY,  
            hoverColour=BLUE,  
            pressedColour=WHITE,  
            radius=10  
        )

        # Exit button (placed at the bottom-right)
        self.exit_button = Button(
            self.screen,  
            x=self.RIGHT_SIDE_X,  
            y=HEIGHT - 50,  
            width=200,  
            height=50,  
            text="Exit",  
            fontSize=20,  
            margin=20,  
            inactiveColour=GREY,  
            hoverColour=BLUE,  
            pressedColour=WHITE,  
            radius=10  
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
            self.beam_waist_spin_box.listen(events)
            self.screen.blit(self.laser_power_label, (self.SPIN_BOX_X, 80))
            self.laser_power_spin_box.draw()
            self.laser_power_spin_box.listen(events)
            self.screen.blit(self.n_particle_label, (self.SPIN_BOX_X, 140))
            self.n_particle_spin_box.draw()
            self.n_particle_spin_box.listen(events)
            self.screen.blit(self.n_medium_label, (self.SPIN_BOX_X, 200))
            self.n_medium_spin_box.draw()
            self.n_medium_spin_box.listen(events)
            self.screen.blit(self.dt_label, (self.SPIN_BOX_X, 260))
            self.dt_spin_box.draw()
            self.dt_spin_box.listen(events)
            self.screen.blit(self.viscosity_label, (self.SPIN_BOX_X, 320))
            self.viscosity_spin_box.draw()
            self.viscosity_spin_box.listen(events)
            self.screen.blit(self.temperature_label, (self.SPIN_BOX_X, 380))
            self.temperature_spin_box.draw()
            self.temperature_spin_box.listen(events)
            self.screen.blit(self.radius_label, (self.SPIN_BOX_X, 440))
            self.radius_spin_box.draw()
            self.radius_spin_box.listen(events)
            self.screen.blit(self.num_rays_label, (self.SPIN_BOX_X, 500))
            self.num_rays_spin_box.draw()
            self.num_rays_spin_box.listen(events)

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
        dict_parameters = {}
        
        # Get the selected view
        dict_parameters['selected_view'] = self.dropdown.getSelected()

        # Get spin box values
        dict_parameters['w0'] = self.beam_waist_spin_box.getValue()
        dict_parameters['P'] = self.laser_power_spin_box.getValue()
        dict_parameters['n_particle'] = self.n_particle_spin_box.getValue()
        dict_parameters['n_medium'] = self.n_medium_spin_box.getValue()
        dict_parameters['dt'] = self.dt_spin_box.getValue()
        dict_parameters['viscosity'] = self.viscosity_spin_box.getValue()
        dict_parameters['temperature'] = self.temperature_spin_box.getValue()
        dict_parameters['radius'] = self.radius_spin_box.getValue()
        dict_parameters['num_rays'] = self.num_rays_spin_box.getValue()

        # Get the save path
        dict_parameters['save_path'] = self.path_box.getText()

        # Get "Min point, µm" and "Max point, µm" values for the selected view
        dict_parameters['min_point'] = self.min_point_spin_box.getValue()
        dict_parameters['max_point'] = self.max_point_spin_box.getValue()
        
        print(dict_parameters)
        # call the function to calculate and save the results
        calc_and_save(dict_parameters)

