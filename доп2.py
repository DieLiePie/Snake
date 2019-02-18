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

    def menu(self):
        done = True
        font_menu = pygame.font.SysFont('monaco', 50)
        punkt = 0
        while done:
            self.screen.fill((255, 255, 255))

            np = pygame.mouse.get_pos()
            for i in self.punkts:
                if np[0] > i[0] and np[0] < i[0] + 55 and np[1] > i[1] and np[1] < i[1] + 50:
                    punkt = i[5]
            self.render(self.screen, font_menu, punkt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if event.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        pygame.quit()
                        sys.exit()
                self.screen.blit(self.screen, (0, 0))
            pygame.display.flip()