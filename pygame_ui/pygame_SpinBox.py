from pygame_widgets.button import Button
import pygame


from constants import WHITE, BLACK, GREY, BLUE

class SpinBox:
    def __init__(self, screen, x, y, width, height, min_value, max_value, step, initial_value, font_size=22, round_to=2):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = initial_value
        self.font = pygame.font.SysFont("Arial", font_size)
        self.round_to = round_to

        # Decrement button
        self.decrement_button = Button(
            self.screen,
            x=self.x,
            y=self.y,
            width=30,
            height=self.height,
            text="-",
            fontSize=font_size,
            margin=10,
            inactiveColour=GREY,
            hoverColour=BLUE,
            pressedColour=WHITE,
            radius=5,
            onClick=self.decrement
        )

        # Increment button
        self.increment_button = Button(
            self.screen,
            x=self.x + self.width - 30,
            y=self.y,
            width=30,
            height=self.height,
            text="+",
            fontSize=font_size,
            margin=10,
            inactiveColour=GREY,
            hoverColour=BLUE,
            pressedColour=WHITE,
            radius=5,
            onClick=self.increment
        )

        # Value display
        self.value_surface = self.font.render(f"{round(self.value, self.round_to)}", True, BLACK)
        self.value_rect = self.value_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        
        # Input active state
        self.active_input = False  # Tracks whether the spin box is in input mode
        self.input_buffer = ""  # Stores the current input for the value

    def decrement(self):
        self.value = max(self.min_value, self.value - self.step)
        self.update_value_display()

    def increment(self):
        self.value = min(self.max_value, self.value + self.step)
        self.update_value_display()

    def update_value_display(self):
        # Update the displayed value
        if self.active_input:
            # Show the input buffer while typing
            self.value_surface = self.font.render(self.input_buffer, True, BLACK)
        else:
            # Show the current value
            self.value_surface = self.font.render(f"{round(self.value, self.round_to)}", 
                                                  True, 
                                                  BLACK)
        self.value_rect = self.value_surface.get_rect(center=(self.x + self.width // 2, 
                                                              self.y + self.height // 2))
        # self.value_surface = self.font.render(f"{round(self.value, self.round_to)}", True, BLACK)
        # self.value_rect = self.value_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

    def draw(self):
        self.decrement_button.draw()
        self.increment_button.draw()
        self.screen.blit(self.value_surface, self.value_rect)

    def listen(self, events):        
        for event in events: 
            # Handle click on the value display
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.value_rect.collidepoint(event.pos):  # Check if the value text is clicked
                    self.active_input = True  # Activate input mode
                    self.input_buffer = str(self.value)  # Initialize the input buffer with the current value

            # Handle keyboard input
            if event.type == pygame.KEYDOWN and self.active_input:
                if event.key == pygame.K_BACKSPACE:
                    self.input_buffer = self.input_buffer[:-1]  # Remove last character
                elif event.key == pygame.K_RETURN:
                    # Apply the input buffer to the value
                    if self.input_buffer:
                        try:
                            new_value = float(self.input_buffer)
                            if self.min_value <= new_value <= self.max_value:
                                self.value = new_value
                        except ValueError:
                            pass  # Ignore invalid input
                    self.active_input = False  # Deactivate input mode
                else:
                    # Append the typed character to the input buffer
                    if event.unicode.isdigit() or event.unicode == '.' or event.unicode == '-':
                        self.input_buffer += event.unicode

                # Update the display while typing
                self.update_value_display()
    
    def getValue(self):
        return self.value
