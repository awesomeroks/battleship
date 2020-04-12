import pygame


class pyWindow:
    """Class to handle PyGame input and output"""
    colours = {
        "water": pygame.color.Color("blue"),
        "ship": pygame.color.Color("gray"),
        "hit": pygame.color.Color("red"),
        "miss": pygame.color.Color("lightcyan"),
        "background": pygame.color.Color("navy"),
        "text": pygame.color.Color("white")
    }

    def __init__(self, boardDimensions=10):
        self.boardDimensions = boardDimensions
        self.cellWidth = 32
        self.sideMargin = 10

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Montserrat", 14)

        self.displayWidth = 2 * self.cellWidth * \
            self.boardDimensions + 2 * self.sideMargin
        self.displayHeight = 2 * self.cellWidth * \
            self.boardDimensions + 2 * self.sideMargin
        self.screen = pygame.display.set_mode(
            [self.displayWidth, self.displayHeight])
        pygame.display.set_caption("BATTLESHIP: Battle of the Legends")

    def show(self):
        for y in range(self.board_size):
            for x in range(self.board_size):
                pygame.draw.rect(self.screen, upper_colours[y][x],
                                     [self.margin + x * self.cell_size,
                                      self.margin + y * self.cell_size,
                                      self.cell_size, self.cell_size])

    def get_input(self):
        """Converts MouseEvents into board corrdinates, for input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Display.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                y = y % (self.board_size * self.cell_size + self.margin)
                x = (x - self.margin) // self.cell_size
                y = (y - self.margin) // self.cell_size
                if x in range(self.board_size) and y in range(self.board_size):
                    return x, y
        return None, None

    def show_text(self, text, upper=False, lower=False):
        """Displays text on the screen, either upper or lower """
        x = self.margin
        y_up = x
        y_lo = self.board_size * self.cell_size + self.margin
        label = self.font.render(text, True, Display.colours["text"])
        if upper:
            self.screen.blit(label, (x, y_up))
        if lower:
            self.screen.blit(label, (x, y_lo))

    @classmethod
    def flip(cls):
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    @classmethod
    def close(cls):
        pygame.display.quit()
        pygame.quit()
