class Menu:
    def __init__(self, punkts=[120, 140, u'Punkt', (250, 250, 30), (250, 30, 250)]):
        self.punkts = punkts
        self.screen = pygame.display.set_mode((720, 460))

    def render(self, screen, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                screen.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))