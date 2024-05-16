# Importing required libraries
import pygame # Utilised for creating graphics and applications
import random # Used for randomly generating numbers
import sys # Required for modifying the python runtime
import os


pygame.init() # Initialise pygame

screen_width, screen_height = 1920, 1080 # Screen Width/Height Variable
screen = pygame.display.set_mode((screen_width, screen_height)) # Set the resolution to 1920 x 1080
pygame.display.set_caption("Card Craft: The Ultimate Card Game") # Set the application title

# Colours
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
regularFont = pygame.font.Font(None, 70)
titleFont = pygame.font.Font(None, 90)

# Constants
CARD_WIDTH, CARD_HEIGHT = 150, 200
CARD_SPACING = 10  # Adjust the spacing between cards

# Create a deck of cards (you can expand this)
suits = ['c', 'd', 'h', 's'] # Creating an array of letters/strings for the suits
ranks = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13'] # Creating an array of stringed numbers for the ranks

card_images = {}
for suit in suits: # Creating a for loop for each suit in the suits array
    for rank in ranks: # Creating another loop for each rank in the ranks array
        image_path = os.path.join("assets/cards", f"{suit}{rank}.png") # For each card find its file path using the suit and rank variables created from for loop
        card_images[(suit, rank)] = pygame.image.load(image_path) # Load the card into the pygame instance

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = ranks.index(rank) + 2

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, deck):
        self.hand.append(deck.pop())

# Create a deck of cards
deck = [(rank, suit) for suit in suits for rank in ranks]  # This creates a list of tuples
# Convert the tuples to Card instances
deck = [Card(suit, rank) for rank, suit in deck]
random.shuffle(deck) # Shuffling the deck of cards to be in a randomised order

# Create the player and AI opponent
player = Player("Player")
ai_opponent = Player("AI Opponent")

# Deal initial cards
for _ in range(5):
    player.draw_card(deck)
    ai_opponent.draw_card(deck)


# Initialize points for player and AI opponent
player_points = 0
ai_points = 0

def game_play():
            global player_points, ai_points  # Access the global variables
            # Setting the background image
            screen.blit(pygame.image.load('./assets/images/background_image.jpg'), (0, 0))

            

            # Display player and AI points on the screen
            player_points_text = regularFont.render(f"Player Points: {player_points}", True, black)
            ai_points_text = regularFont.render(f"AI Points: {ai_points}", True, black)
            screen.blit(player_points_text, (20, 20))
            screen.blit(ai_points_text, (20, 60))

            # Display the game screen (player's hand, AI's hand, etc.)
            for i, card in enumerate(player.hand):
                card_image = card_images[(card.suit, card.rank)]
                scaled_card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))
                x = i * (CARD_WIDTH + CARD_SPACING)  # Adjust spacing between cards
                y = screen_height - CARD_HEIGHT - 20
                screen.blit(scaled_card_image, (x, y))

            # Initialize a Boolean variable to track whether a card is selected
            card_selected = False

            # Inside your event loop:
            for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # Left mouse button clicked
                                mouse_x, mouse_y = event.pos
                                for i, card in enumerate(player.hand):
                                    card_rect = pygame.Rect(i * (CARD_WIDTH + CARD_SPACING), screen_height - CARD_HEIGHT - 20, CARD_WIDTH, CARD_HEIGHT)
                                    if card_rect.collidepoint(mouse_x, mouse_y):
                                        # Toggle card selection
                                        card_selected = not card_selected
                                        break  # Exit the loop after the first card collision
                
            if card_selected:
                player_selected_card = player.hand.pop(i)  # Remove the selected card from the player's hand
                 # Perform AI's turn (e.g., randomly select a card)
                ai_selected_card = random.choice(ai_opponent.hand)
                 # Display the AI's card (assuming the AI's card is stored in a variable called ai_selected_card)
                if ai_selected_card:
                    ai_card_image = card_images[(ai_selected_card.suit, ai_selected_card.rank)]
                    scaled_ai_card_image = pygame.transform.scale(ai_card_image, (CARD_WIDTH, CARD_HEIGHT))
                    ai_x = (screen_width - CARD_WIDTH) // 2
                    ai_y = 20
                    screen.blit(scaled_ai_card_image, (ai_x, ai_y))
                print(f"AI selected card: {ai_selected_card}")
                 # Compare cards and determine the winner
                if player_selected_card.value > ai_selected_card.value and player.hand != []:
                    player_points += 1  # Update player points
                    
                    # Display player wins round text
                    player_win_text = regularFont.render("Player Wins this round! 🎉", True, black)
                    player_win_rect = player_win_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
                    screen.blit(player_win_text, player_win_rect)

                   
                elif player_selected_card.value < ai_selected_card.value and player.hand != []:
                    ai_points += 1 # Update AI points


                    # Display AI wins round text
                    ai_win_text = regularFont.render("AI Wins this round! 😢", True, black)
                    ai_win_text_rect = ai_win_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
                    screen.blit(ai_win_text, ai_win_text_rect)

                   
                elif player.hand != []:
                    # Display AI wins round text
                    round_tie_text = regularFont.render("It is a tie! 😢", True, black)
                    round_tie_rect = round_tie_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
                    screen.blit(round_tie_text, round_tie_rect)


                # When the player has no more cards left.
                if player.hand == []:
                    if player_points > ai_points:
                        game_win_text = regularFont.render("You win this game! 🎉", True, black)
                    elif ai_points > player_points:
                        game_win_text = regularFont.render("Oh no, you lost! 😢 quitting soon", True, black)
                    else:
                        game_win_text = regularFont.render("IT IS A TIE qutting in 5 seconds", True, black)
                    game_win_rect = game_win_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
                    screen.blit(game_win_text, game_win_rect)

                    pygame.display.flip()
                    pygame.time.delay(5 * 1000)  # 1 second == 1000 milliseconds
                    pygame.quit()
                    sys.exit()

                        

                    # Wait two seconds before continuing
                pygame.display.flip()
                pygame.time.delay(2 * 1000)  # 1 second == 1000 milliseconds

            pygame.display.flip()

# Start Menu Screen
def draw_start_menu():
    # Setting the background image
    screen.blit(pygame.image.load('./assets/images/background_image.jpg'), (0, 0))

    # Draw title
    title_text = titleFont.render("Card Craft: The Ultimate Card Game", True, black) # Setting title text and colour
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3 - 100)) # Setting dimensions
    screen.blit(title_text, title_rect) # Rendering text
    
    # Draw play button 
    play_text = regularFont.render("Play (Space)", True, black) # Setting play text and setting colour
    play_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50)) # Setting dimensions
    screen.blit(play_text, play_rect) # Rendering text
    
    # Draw how to play button
    how_to_play_text = regularFont.render("How to Play (H)", True, black) # Setting how to play text and colour
    how_to_play_rect = how_to_play_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30)) # Setting dimenions 
    screen.blit(how_to_play_text, how_to_play_rect) # Rendering text
    
    # Draw quit button
    quit_text = regularFont.render("Quit (Q)", True, black) # Setting quit text and colour 
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100)) # Setting dimensions 
    screen.blit(quit_text, quit_rect) # Rendering text




# How to Play Screen
def draw_how_to_play():
    # Setting the background image
    screen.blit(pygame.image.load('./assets/images/background_image.jpg'), (0, 0))
    
    # Draw title
    title_text = titleFont.render("How to Play", True, black)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3 - 100))
    screen.blit(title_text, title_rect)
    
    # Draw Bullet Point One
    how_to_play_one = regularFont.render("• Receive 5 cards in hand from the deck of 52 unique cards.", True, black)
    how_to_play_one_rect = how_to_play_one.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(how_to_play_one, how_to_play_one_rect)

    # Draw Bullet Point Two
    how_to_play_two = regularFont.render("• Play card each round, highest played card wins round.", True, black) # Setting how to play text and colour
    how_to_play_two_rect = how_to_play_two.get_rect(center=(screen_width // 2, screen_height // 2 + 30)) # Setting dimenions 
    screen.blit(how_to_play_two, how_to_play_two_rect) # Rendering text
    
    # Draw Bullet Point Three
    how_to_play_three = regularFont.render("• When all cards have been played, player with most wins will win game.", True, black) # Setting quit text and colour 
    how_to_play_rect = how_to_play_three.get_rect(center=(screen_width // 2, screen_height // 2 + 100)) # Setting dimensions 
    screen.blit(how_to_play_three, how_to_play_rect) # Rendering text
    
    # Draw Back button
    back_text = regularFont.render("Back (B)", True, black)
    back_rect = back_text.get_rect(center=(screen_width // 2, screen_height - 100))
    screen.blit(back_text, back_rect)

def draw_play_screen():
    # Setting the background image
    screen.blit(pygame.image.load('./assets/images/background_image.jpg'), (0, 0))
    # Implement game logic here (compare playing_card with AI's card, determine winner, etc.)

    pygame.display.update()


def main(): # Initialising main function
    current_screen = "start_menu"  # Initial screen
    # Main game loop
    in_game = False  # To switch between start menu and game
    playing_card = None  # To track the card being played

    running = True # Setting the running variable to true
    while running: # Whilst the running variable is true do the following...
        for event in pygame.event.get(): # Fetching the pygame event 
            if event.type == pygame.QUIT: # If the event type is QUIT, set the running variable to false
                running = False
            elif event.type == pygame.KEYDOWN: # If the event is a keydown event...
                if event.key == pygame.K_SPACE: # If the key pressed down is spacebar...
                    current_screen = 'start_game'
                elif event.key == pygame.K_h: # If the key pressed down is H...
                   current_screen = 'how_to_play'
                elif event.key == pygame.K_q: # If the key pressed down is Q...
                    # Quit the game
                    pygame.quit()
    
                elif event.key == pygame.K_b and current_screen == "how_to_play": # If on the how to play screen and keydown is B...
                    current_screen = "start_menu" # Switch back to start menu
    
        if current_screen == 'start_menu':
            # Implement game logic here (compare playing_card with AI's card, determine winner, etc.)
            # Display the game screen (player's hand, AI's hand, etc.)
            draw_start_menu()
            pass
        elif current_screen == 'how_to_play':
            # Display the start menu or how-to-play screen
            draw_how_to_play()  # You can switch to draw_how_to_play() if needed
            pass
        elif current_screen == 'start_game':
           game_play()

        pygame.display.flip()

main()