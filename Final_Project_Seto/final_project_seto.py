import pygame
import sys
import random
import os

class PygameUI:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Blackjack")

        self.font = pygame.font.Font(None, 36)

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_cards(self, player, x, y):
        for i, card in enumerate(player.hand):
            image_folder = os.path.join(os.path.dirname(__file__), "images")
            suit_name = card.suit.lower() if card.suit.lower() != "hearts" else "hearts_clubs"
            image_filename = os.path.join(image_folder, f"{str(card.rank.lower())}_{str(card.suit.lower())}_white.png")
            image_filename = image_filename.replace(" ", "_")
            print(f"Attempting to load image: {image_filename}")
            card_image = pygame.image.load(image_filename)
            self.screen.blit(card_image, (x + i * 60, y))

    def draw_buttons(self):
        pygame.draw.rect(self.screen, (0, 128, 255), (300, 500, 100, 50))
        self.draw_text("Hit", 330, 515)

        pygame.draw.rect(self.screen, (0, 128, 255), (500, 500, 100, 50))
        self.draw_text("Stand", 520, 515)

    def update_display(self, game, reveal_dealer_card=False):
        self.screen.fill((0, 0, 0))

        self.draw_cards(game.player, 50, 300, reveal_second_card=True)
    
        if reveal_dealer_card:
            self.draw_cards(game.dealer, 50, 50, reveal_second_card=True)
            self.draw_text(f"Dealer's Hand: {', '.join(str(card) for card in game.dealer.hand)}", 50, 20)
        else:
            self.draw_cards(game.dealer, 50, 50)
            self.draw_text(f"Dealer's Hand: {str(game.dealer.hand[0])} and an unknown card", 50, 20)

        self.draw_text(f"Your Hand: {', '.join(str(card) for card in game.player.hand)}", 50, 270)

        self.draw_buttons()

        pygame.display.flip()
    
    def draw_cards(self, player, x, y, reveal_second_card=False):
        for i, card in enumerate(player.hand):
            image_folder = os.path.join(os.path.dirname(__file__), "images")
            suit_name = card.suit.lower() if card.suit.lower() != "hearts" else "hearts_clubs"
            image_filename = os.path.join(image_folder, f"{str(card.rank.lower())}_{str(card.suit.lower())}_white.png")
            image_filename = image_filename.replace(" ", "_")

            if i == 1 and not reveal_second_card:
                image_filename = os.path.join(image_folder, "card_back.png")

            print(f"Attempting to load image: {image_filename}")
            card_image = pygame.image.load(image_filename)
            self.screen.blit(card_image, (x + i * 60, y))

class Card:
    def __init__(self, suit, rank, color):
        self.suit = suit
        self.rank = rank
        self.color = color

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_value(self):
        if self.rank.isdigit():
            return int(self.rank)
        elif self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11  # this is defaulted to 11 as of right now in the code but will be changed within the program if the user wants it to be 1

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King', 'Ace']
        colors = {'Hearts': 'red', 'Diamonds': 'red', 'Clubs': 'black', 'Spades': 'black'}
        self.cards = [Card(suit, rank, color) for suit in suits for rank in ranks for color in colors]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def calculate_hand_value(self):
        value = sum(card.get_value() for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.rank == 'Ace')

        # this is where the ace value gets adjusted according to the user/dealer's hands
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.reset_game()

    def reset_game(self):
        self.deck.shuffle()
        self.player.hand = []
        self.dealer.hand = []

    def welcome_message(self):
        print("Welcome to Blackjack!")
        print("Try to get as close to 21 as possible without going over.")
        print("Face cards are worth 10. Aces are worth 1 or 11.")
        print("Good luck!\n")

    def display_rules(self):
        print("\nRules:")
        print("1. The goal is to get as close to 21 as possible without going over.")
        print("2. Face cards (Jack, Queen, King) are worth 10. Aces are worth 1 or 11.")
        print("3. The dealer must draw until their hand is at least 17.")
        print("4. If your hand exceeds 21, you lose (bust).")
        print("5. The winner is the one with the highest hand value without exceeding 21.\n")

    def display_game_status(self, reveal_dealer_card=False):
        print("\n--- Current Game ---")
        print(f"{self.player.name}'s Hand: {', '.join(str(card) for card in self.player.hand)}")

        dealer_hand = self.dealer.hand
        if reveal_dealer_card:
            print(f"{self.dealer.name}'s Hand: {', '.join(str(card) for card in dealer_hand)}")
        else:
            print(f"{self.dealer.name}'s Hand: {str(dealer_hand[0])} and an unknown card")

        print("----------------------")

    def play_game(self):
        self.reset_game()
        self.ui = PygameUI()
        game_over = False

        for _ in range(2):
            self.player.add_card(self.deck.deal())
            self.dealer.add_card(self.deck.deal())

        while not game_over:
            self.ui.update_display(self)
            pygame.time.delay(100)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 300 < event.pos[0] < 400 and 500 < event.pos[1] < 550:
                        drawn_card = self.deck.deal()
                        self.player.add_card(drawn_card)

                        if self.player.calculate_hand_value() > 21:
                            self.ui.update_display(self, reveal_dealer_card=True)
                            self.ui.draw_text("Bust! You went over 21. You lose.", 50, 400, (255, 0, 0))
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            game_over = True

                    elif 500 < event.pos[0] < 600 and 500 < event.pos[1] < 550:
                        while self.dealer.calculate_hand_value() < 17:
                            self.dealer.add_card(self.deck.deal())

                        self.ui.update_display(self, reveal_dealer_card=True)

                        if self.dealer.calculate_hand_value() > 21:
                            self.ui.draw_text("Dealer busts! You win!", 50, 400, (0, 255, 0))
                        elif self.dealer.calculate_hand_value() >= self.player.calculate_hand_value():
                            self.ui.draw_text("Dealer wins!", 50, 400, (255, 0, 0))
                        else:
                            self.ui.draw_text("You win!", 50, 400, (0, 255, 0))

                        pygame.display.flip()
                        pygame.time.delay(2000)
                        game_over = True
        pygame.quit()
        sys.exit()

    def start_game(self):
        self.welcome_message()

        while True:
            menu_options = ["1. Play Blackjack", "2. View Rules", "3. Quit"]
            print("\nMenu:")
            for option in menu_options:
                print(option)

            choice = input("Select an option (1-3): ")

            if choice == '1':
                self.play_game()
            elif choice == '2':
                self.display_rules()
            elif choice == '3':
                print("Thanks for playing! See you next time.")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 3.")

if __name__ == "__main__":
    game = BlackjackGame()
    game.start_game()
