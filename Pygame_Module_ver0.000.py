import pygame
import sys

class PygameHelper:
    def __init__(self, screen_size):
        """
        Initializes the Pygame window.

        Parameters:
        - screen_size: Tuple (width, height) specifying the screen size.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Pygame Helper")
        self.clock = pygame.time.Clock()
        self.running = True
        self.bg_color = (0, 0, 0)  # Default background color: black

    def set_background_color(self, color):
        """Sets the background color."""
        self.bg_color = color

    def draw_rectangle(self, x, y, width, height, color):
        """
        Draws a rectangle on the screen.

        Parameters:
        - x, y: Top-left corner of the rectangle.
        - width, height: Size of the rectangle.
        - color: Tuple (R, G, B) for the rectangle color.
        """
        pygame.draw.rect(self.screen, color, (x, y, width, height))

    def draw_circle(self, x, y, radius, color):
        """
        Draws a circle on the screen.

        Parameters:
        - x, y: Center of the circle.
        - radius: Radius of the circle.
        - color: Tuple (R, G, B) for the circle color.
        """
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def draw_text(self, text, x, y, font_size, color):
        """
        Draws text on the screen.

        Parameters:
        - text: The string to display.
        - x, y: Top-left corner of the text.
        - font_size: Size of the font.
        - color: Tuple (R, G, B) for the text color.
        """
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_gradient_circle(self, center, radius, outer_color, inner_color):
        """
        Draws a gradient-filled circle on the screen using a surface.

        Parameters:
        - center: Tuple (x, y) for the circle center.
        - radius: Radius of the circle.
        - outer_color: Tuple (R, G, B) for the inner color.
        - inner_color: Tuple (R, G, B) for the outer color.
        """
        gradient_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        for r in range(radius, 0, -1):
            # Calculate the interpolated color
            t = r / radius  # Normalized distance (0 to 1)
            color = (
                int(outer_color[0] * t + inner_color[0] * (1 - t)),
                int(outer_color[1] * t + inner_color[1] * (1 - t)),
                int(outer_color[2] * t + inner_color[2] * (1 - t)),
                255  # Alpha channel
            )
            pygame.draw.circle(gradient_surface, color, (radius, radius), r)
        self.screen.blit(gradient_surface, (center[0] - radius, center[1] - radius))

    def main_loop(self, draw_callback):
        """
        Starts the Pygame main loop.

        Parameters:
        - draw_callback: A function that takes `self` as an argument and contains drawing logic.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.bg_color)
            draw_callback(self)  # Call the user's drawing function
            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 FPS

        pygame.quit()
        sys.exit()

# Example usage
if __name__ == "__main__":
    def draw_example(helper):
        # Draw a gradient circle
        helper.draw_gradient_circle(
            center=(400, 300),       # Center of the circle
            radius=100,              # Radius
            outer_color=(70, 50, 50), # Red at the center
            inner_color=(50, 150, 50)  # Blue at the edge
        )

    # Initialize the helper
    game_helper = PygameHelper((800, 600))  # 800x600 window
    game_helper.set_background_color((50, 50, 50))  # Set background to dark blue

    # Run the main loop with the example drawing logic
    game_helper.main_loop(draw_example)
