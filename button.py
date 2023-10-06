import pygame
import essential_functions


class Button:
    def __init__(self, x, y, taille, texte, surface, screen, couleur_texte=None, taille_texte=36, pressed_surface=None):
        self.largeur = surface.get_width()
        self.hauteur = surface.get_height()
        self.surface = pygame.transform.scale(surface, (int(self.largeur * taille), int(self.hauteur * taille)))
        if pressed_surface:
            self.pressed_surface = pygame.transform.scale(pressed_surface, (int(self.largeur * taille), int(self.hauteur * taille)))
        else:
            self.pressed_surface = None
        self.rect = self.surface.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.texte = texte
        self.couleur_texte = couleur_texte
        self.taille_texte = taille_texte
        self.screen = screen

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                if self.pressed_surface:
                    self.screen.blit(self.pressed_surface, (self.rect.x, self.rect.y + 5))
                    essential_functions.place_text(self.rect.center[0], self.rect.center[1] + 5, self.texte, self.taille_texte, self.screen)
                    pygame.display.update()
                    pygame.time.delay(100)
                    self.screen.blit(self.surface, (self.rect.x, self.rect.y))
                    essential_functions.place_text(self.rect.center[0], self.rect.center[1], self.texte, self.taille_texte, self.screen)
                    pygame.display.update()
                    pygame.time.delay(100)
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.screen.blit(self.surface, (self.rect.x, self.rect.y))
        essential_functions.place_text(self.rect.center[0], self.rect.center[1], self.texte, self.taille_texte, self.screen)

        return action

    def initier_click(self):
        if self.pressed_surface:
            self.screen.blit(self.pressed_surface, (self.rect.x, self.rect.y + 5))
            essential_functions.place_text(self.rect.center[0], self.rect.center[1] + 5, self.texte, self.taille_texte, self.screen)
            pygame.display.update()
            pygame.time.delay(1000)
        self.screen.blit(self.surface, (self.rect.x, self.rect.y))
        essential_functions.place_text(self.rect.center[0], self.rect.center[1], self.texte, self.taille_texte, self.screen)
        pygame.display.update()
        return True
