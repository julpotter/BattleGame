import random
from typing import Type
import pygame


class BattleGame:
    def __init__(self, round_number: int, items=["Strength Potion", "Defense Potion", "Old Boot"]) -> None:
        self.round_number = round_number
        self.items = items


class Player:
    def __init__(self, name: str, sprite=None, inventory=None, hp=100, strength=1, defense=1, ) -> None:
        self.sprite = pygame.image.load("battlegame_fighter.png")
        self.inventory = inventory if inventory is not None else []
        self.hp = hp
        self.strength = strength
        self.defense = defense
        self.bg = BattleGame(1)
        self.items = [StrengthPotion(self), DefensePotion(self), OldBoot(self), HealthPotion(self)]
        self.name = name

    def defend(self) -> None:
        self.defense += 0.1

    def rummage(self) -> None:
        item = random.choice(self.items)
        if len(self.inventory) < 10:
            self.inventory.append(item)

    def heal(self) -> None:
        self.hp += 5

    def __str__(self) -> str:
        inv = '\n'.join(str(obj) for obj in self.inventory)
        return f"This player has: \n {self.hp} hp, \n {self.strength} strength, \n {self.defense} defense, \n and an inventory containing: \n {inv}"


class Item:
    def __init__(self, player: Type[Player]) -> None:
        self.player = player

    def use(self) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


class StrengthPotion(Item):
    def use(self) -> None:
        self.player.strength += 0.3

    def __str__(self) -> str:
        return "Strength Potion (s)"


class DefensePotion(Item):
    def use(self) -> None:
        self.player.defense += 0.3

    def __str__(self) -> str:
        return "Defense Potion (e)"


class OldBoot(Item):
    def use(self) -> None:
        pass

    def __str__(self) -> str:
        return "Old Boot"


class HealthPotion(Item):
    def use(self) -> None:
        self.player.hp += 20

    def __str__(self) -> str:
        return "Health Potion (p)"


'''
class Player1(Player):
  def attack(self) -> None:
    Player2.super().__init__().hp -= Player1.super().__init__().strength + 10

class Player2(Player):
  def attack(self) -> None:
    Player1.super().__init__().hp -= Player2.super().__init__().strength * 10 + 10
'''


def attack(attacker: Type[Player], target: Type[Player]) -> None:
    target.hp -= attacker.strength * 10 / target.defense


def main() -> None:
    X = 1080
    Y = 720
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    player2.inventory.append(DefensePotion(player2))
    pygame.init()
    screen = pygame.display.set_mode((X, Y))
    running = True
    color = (255, 255, 255)
    clock = pygame.time.Clock()
    player1_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 2)
    player2_pos = pygame.Vector2(screen.get_width() / 2 + screen.get_width() / 4, screen.get_height() / 2)
    dt = 0
    font = pygame.font.Font('freesansbold.ttf', 12)
    pygame.event.clear()

    # src: https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame?answertab=scoredesc#tab-top
    # Code to print multiple lines of text on screen
    def blit_text(surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    ##################################################################
    # src: https://www.makeuseof.com/start-menu-and-game-over-screen-with-pygame/
    def draw_game_over_screen(winner: Player):
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render(f'{winner} wins!', True, (255, 255, 255))
        restart_button = font.render('R - Restart', True, (255, 255, 255))
        quit_button = font.render('Q - Quit', True, (255, 255, 255))
        screen.blit(title, (X / 2 - title.get_width() / 2, Y / 2 - title.get_height() / 3))
        screen.blit(restart_button,
                    (X / 2 - restart_button.get_width() / 2, Y / 1.9 + restart_button.get_height()))
        screen.blit(quit_button,
                    (X / 2 - quit_button.get_width() / 2, Y / 2 + quit_button.get_height() / 2))
        pygame.display.update()

    #######################################################################
    # Game state
    game_state = "game"
    # players
    curr_player = player1
    other_player = player2
    # Sprites and shapes
    rect1 = player1.sprite.get_rect()
    rect1.center = player1_pos
    rect2 = player2.sprite.get_rect()
    rect2.center = player2_pos
    img1 = player1.sprite
    img1.convert()
    img2 = player2.sprite
    img2 = pygame.transform.flip(img2, True, False)
    img2.convert()
    curr_rect = rect1
    other_rect = rect2
    while running:
        if game_state == "game_over":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_state = "game"
                main()
            if keys[pygame.K_q]:
                pygame.quit()
                quit()

        if game_state == "game":
            screen.fill(color)
            text1 = player1.__str__()
            text2 = player2.__str__()
            blit_text(screen, text1, (20, 20), font)
            blit_text(screen, text2, (500, 20), font)
            screen.blit(img1, rect1)
            screen.blit(img2, rect2)
            pygame.draw.rect(screen, "red", curr_rect, 1)
            pygame.display.update()

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and game_state == "game":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                attack(curr_player, other_player)
            if keys[pygame.K_d]:
                curr_player.defend()
            if keys[pygame.K_r]:
                curr_player.rummage()
            if keys[pygame.K_u]:
                try:
                    item = random.choice(curr_player.inventory)
                    item.use()
                    curr_player.inventory.remove(item)
                except:
                    pass
            if keys[pygame.K_h]:
                curr_player.heal()
            if keys[pygame.K_e]:
                for x in curr_player.inventory:
                    if type(x) == DefensePotion:
                        x.use()
                        curr_player.inventory.remove(x)
                        break
            if keys[pygame.K_s]:
                for x in curr_player.inventory:
                    if type(x) == StrengthPotion:
                        x.use()
                        curr_player.inventory.remove(x)
                        break
            if keys[pygame.K_p]:
                for x in curr_player.inventory:
                    if type(x) == HealthPotion:
                        x.use()
                        curr_player.inventory.remove(x)
                        break

            if curr_player.hp <= 0:
                game_state = "game_over"
                draw_game_over_screen(other_player.name)
            if other_player.hp <= 0:
                game_state = "game_over"
                draw_game_over_screen(curr_player.name)

            curr_player, other_player = other_player, curr_player
            curr_rect, other_rect = other_rect, curr_rect

    pygame.quit()


if __name__ == "__main__":
    main()
