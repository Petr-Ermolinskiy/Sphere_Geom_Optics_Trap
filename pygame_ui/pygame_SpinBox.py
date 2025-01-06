from pygame_widgets.button import Button
import pygame


from constants import WHITE, BLACK, GREY, BLUE

class SpinBox:
    def __init__(self, screen, x, y, width, height, min_value, max_value, step, initial_value, font_size=20):
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
        self.value_surface = self.font.render(f"{self.value:.2f}", True, BLACK)
        self.value_rect = self.value_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

    def decrement(self):
        self.value = max(self.min_value, self.value - self.step)
        self.update_value_display()

    def increment(self):
        self.value = min(self.max_value, self.value + self.step)
        self.update_value_display()

    def update_value_display(self):
        self.value_surface = self.font.render(f"{self.value:.2f}", True, BLACK)
        self.value_rect = self.value_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

    def draw(self):
        # Draw the decrement button
        self.decrement_button.draw()

        # Draw the increment button
        self.increment_button.draw()

        # Draw the value display
        self.screen.blit(self.value_surface, self.value_rect)

    def listen(self, events):
        self.decrement_button.listen(events)
        self.increment_button.listen(events)

    def getValue(self):
        return self.value
