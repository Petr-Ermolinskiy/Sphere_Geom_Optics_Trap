
import sys
import pygame
import pygame_widgets
from pygame_widgets.button import Button

from .simulation import Simulation
from .calculation import CalculationWindow

from constants import WIDTH, HEIGHT, BLACK, WHITE, GREY, CONE_COLOR

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)  # Larger font for the title
        self.running = True
        self.clock = pygame.time.Clock()  # Initialize the clock
        self.create_menu()

    def create_menu(self):
        # Split the title into two lines
        self.title_lines = [
            "Sphere in the Optical Trap:",
            "Geometrical Optics"
        ]

        # Render each line of the title
        self.title_surfaces = [self.font.render(line, True, BLACK) for line in self.title_lines]

        # Calculate the vertical position for each line
        self.title_rects = []
        y_offset = 50  # Starting Y position for the first line
        for surface in self.title_surfaces:
            rect = surface.get_rect(center=(WIDTH // 2, y_offset))
            self.title_rects.append(rect)
            y_offset += 50  # Adjust the Y position for the next line

        # Buttons
        self.real_time_button = Button(
            self.screen,  # Surface to draw on
            x=WIDTH // 2 - 100,  # X position
            y=200,  # Y position
            width=300,  # Width of the button
            height=50,  # Height of the button
            text="Real-time Simulation",  # Button text
            fontSize=20,  # Font size
            margin=20,  # Margin between text and button edges
            inactiveColour=GREY,  # Color when not hovered
            hoverColour=CONE_COLOR,  # Color when hovered
            pressedColour=WHITE,  # Color when clicked
            radius=10  # Border radius
        )
        self.force_torque_button = Button(
            self.screen,
            x=WIDTH // 2 - 100,
            y=300,
            width=300,
            height=50,
            text="Force/Torque Calculation",
            fontSize=20,
            margin=20,
            inactiveColour=GREY,
            hoverColour=CONE_COLOR,
            pressedColour=WHITE,
            radius=10
        )
        self.exit_button = Button(
            self.screen,
            x=WIDTH // 2 - 100,
            y=400,
            width=300,
            height=50,
            text="Exit",
            fontSize=20,
            margin=20,
            inactiveColour=GREY,
            hoverColour=CONE_COLOR,
            pressedColour=WHITE,
            radius=10
        )

    def clear_widgets(self):
        # Hide all buttons and the title
        self.real_time_button.hide()
        self.force_torque_button.hide()
        self.exit_button.hide()
        self.title_surfaces = []  # Clear the title surfaces

    def show_widgets(self):
        # Show all buttons and the title
        self.real_time_button.show()
        self.force_torque_button.show()
        self.exit_button.show()
        # Recreate the title surfaces
        self.title_surfaces = [self.font.render(line, True, BLACK) for line in self.title_lines]

    def hide_all_except_selected(self):
        # List of widgets to keep visible
        widgets_to_keep = [self.real_time_button, self.force_torque_button, self.exit_button]
    
        # Create a copy of the widgets list for iteration
        widgets_copy = list(pygame_widgets.WidgetHandler._widgets)
        
        # Hide all widgets except the selected ones
        for widget in widgets_copy:
            if widget not in widgets_to_keep:
                widget.hide()

    def start_real_time_simulation(self):
        print("Real-time Simulation button clicked!")  # Debugging line
        self.clear_widgets()  # Hide all widgets
        self.sim = Simulation(self.return_to_menu)  # Pass the return_to_menu callback
        self.sim.run()
        del self.sim

    def start_force_torque_calculation(self):
        print("Force/Torque Calculation button clicked!")  # Debugging line
        # Add your logic for force/torque calculation here
        self.clear_widgets()  # Hide all widgets
        self.calc = CalculationWindow(self.return_to_menu)  # Pass the return_to_menu callback
        self.calc.run()
        del self.calc


    def exit_application(self):
        print("Exit button clicked!")  # Debugging line
        self.running = False
        pygame.quit()
        sys.exit()

    def return_to_menu(self):
        # Delete the simulation object
        if hasattr(self, 'sim'):
            del self.sim  # Delete the simulation object
            self.sim = None
            print("Simulation object deleted.")  # Debugging line
        if hasattr(self, 'calc'):
            del self.calc  # Delete the simulation object
            self.calc = None
            print("Simulation object deleted.")  # Debugging line
        
        self.real_time_button.clicked = False
        self.force_torque_button.clicked = False

        self.hide_all_except_selected()
        """
        pygame_widgets.WidgetHandler._widgets = [widget for widget in pygame_widgets.WidgetHandler._widgets 
                                                 if isinstance(widget, Button) 
                                                 and widget in [self.real_time_button, 
                                                                self.force_torque_button, 
                                                                self.exit_button]]
        """
        # Restore the menu
        self.show_widgets()  # Show all widgets again
        self.run_menu()  # Restart the menu loop

    

    def run_menu(self):
        while self.running:
            events = pygame.event.get()
            self.screen.fill(WHITE)
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                # Pass events to the buttons
                self.real_time_button.listen(event)
                self.force_torque_button.listen(event)
                self.exit_button.listen(event)

            # Check if buttons are clicked
            if self.real_time_button.clicked:
                self.start_real_time_simulation()
                self.real_time_button.clicked = False
            if self.force_torque_button.clicked:
                self.start_force_torque_calculation()
                self.force_torque_button.clicked = False
            if self.exit_button.clicked:
                self.exit_application()

            # Draw the title lines
            for surface, rect in zip(self.title_surfaces, self.title_rects):
                self.screen.blit(surface, rect)

            # Draw the buttons
            self.real_time_button.draw()
            self.force_torque_button.draw()
            self.exit_button.draw()

            pygame.display.flip()
            pygame_widgets.update(events)  # Update pygame_widgets
            self.clock.tick(1000)