# Importing required libraries
import pygame # Utilised for creating graphics and applications
import random # Used for randomly generating numbers
import os # Used for card image path finding
import sys # Used for exiting the application

pygame.init() # Initialise pygame

screen_width, screen_height = 1920, 1080 # Setting variables for the screen height/width
screen = pygame.display.set_mode((screen_width, screen_height)) # Set the resolution to 1920 x 1080
pygame.display.set_caption("Card Craft: The Ultimate Card Game") # Set the application title

# Constants
CARD_SUITS = ['c', 'd', 'h', 's']
CARD_RANKS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']
CARD_WIDTH, CARD_HEIGHT = 150, 200 # Variables for the card widths and heights
PLAYER_POINTS = 0 # Initialising player points variable
AI_POINTS = 0 # Initialising ai points variable
TEXT_FONT = pygame.font.Font(None, 70) # Font used throughout most of the text displayed in the game
CARD_IMAGES = {} # Initialising card_images object

for suit in CARD_SUITS: # Creating a for loop for each suit in the suits array
    for rank in CARD_RANKS: # Creating another loop for each rank in the ranks array
        image_path = os.path.join("assets/cards", f"{suit}{rank}.png") # For each card find its file path using the suit and rank variables created from for loop
        CARD_IMAGES[(suit, rank)] = pygame.image.load(image_path) # Load the card into the pygame instance

# Creating playing card class
class Card:
    def __init__(self, suit, rank): # Initialise new card instance
        self.suit = suit # Append suit of the card
        self.rank = rank # Append rank of the card
        self.value = CARD_RANKS.index(rank) + 2  # Use CARD_RANKS array to find index of cards rank, +2 due to index being started from 01

# Creating player class
class Player:
    def __init__(self, name): # Initialise new player instance
        self.name = name # Used for identifying whether player is AI or real
        self.hand = [] # Represents players hand, currently empty until cards are appended

    def draw_card(self, deck): # Function for drawing a new card
        self.hand.append(deck.pop()) # Removes last card from the deck array and adds to players hand.


deck = [Card(suit, rank) for suit in CARD_SUITS for rank in CARD_RANKS] # Create a list of Card instances directly from the suits and ranks
random.shuffle(deck) # Shuffling deck of cards to be in a random order

# Create the player and AI opponent
player = Player("Player")
ai_opponent = Player("AI Opponent")

# Deal initial cards
for _ in range(5): # Deals 5 cards to each player
    player.draw_card(deck) # Uses shuffled deck of cards to draw cards
    ai_opponent.draw_card(deck) # Uses shuffled deck of cards to draw cards


### FUNCTIONS ###

# Main game loop function
def game_play():
    global PLAYER_POINTS, AI_POINTS # Access global variables for player/AI points
    card_selected = False # Initialising boolean to track whether a card is selected
    
    screen.blit(pygame.image.load('./assets/images/background_image.jpg'), (0, 0)) # Setting the background image

    # Display player and AI points on the screen
    screen.blit(TEXT_FONT.render(f"Player Points: {PLAYER_POINTS}          AI Points: {AI_POINTS}", True, (255, 255, 255)), (20, 20))

    # Displaying the players cards on screen
    for card_number, card in enumerate(player.hand):
            card_image = CARD_IMAGES[(card.suit, card.rank)] # Fetching card image from players hand
            scaled_card_image = pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT)) # Scaling card image to CARD_WIDTH/CARD_HEIGHT variables
            screen.blit(scaled_card_image, (card_number * (CARD_WIDTH + 10), screen_height - CARD_HEIGHT - 20)) # Rendering cards, 10px spacing and positioning on screen
    
    # Listening for MOUSEBUTTONDOWN event
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # If the event registered is a MOUSEBUTTONDOWN event and left mouse button is clicked (1)...
            mouse_x, mouse_y = event.pos # Fetch mouse position and store in variable
            for card_number, card in enumerate(player.hand): # For each card in players hand...
                card_box = pygame.Rect(card_number * (CARD_WIDTH + 10), screen_height - CARD_HEIGHT - 20, CARD_WIDTH, CARD_HEIGHT) # Creating collision box for cards

                if card_box.collidepoint(mouse_x, mouse_y): # If mouse collides with card box...
                    card_selected = not card_selected # Set the card_selected boolean to true
                    break;

    # If a player selects a card do the following...
    if card_selected:
        player_card = player.hand.pop(card_number) # Store card as variable and remove from players hand
        ai_card = random.choice(ai_opponent.hand) # Randomly choosing AI card and store as variable

        # Displaying AI's selected card on screen
        if ai_card:
             ai_card_image = CARD_IMAGES[(ai_card.suit, ai_card.rank)] # Fetching card image from players hand
             scaled_ai_card_image = pygame.transform.scale(ai_card_image, (CARD_WIDTH, CARD_HEIGHT)) # Scaling card image to CARD_WIDTH/CARD_HEIGHT variables
             screen.blit(scaled_ai_card_image, ((screen_width - CARD_WIDTH) // 2, 20)) # Rendering cards, 10px spacing and positioning on screen

        # Comparing cards and determining winner
        if player_card.value > ai_card.value and player.hand != []: # If player card is higher and players hand isn't empty...
            PLAYER_POINTS += 1 # Add a point to the player

            # Displaying player wins round text
            win_text = TEXT_FONT.render(r"Woohoo! You won this round \(•-•)/", True, (255, 255, 255))
            win_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            screen.blit(win_text, win_rect)     

        elif player_card.value < ai_card.value and player.hand != []: # If AI card is higher and players hand isn't empty...
            AI_POINTS += 1 # Add a point to the AI

            # Displaying player wins round text
            win_text = TEXT_FONT.render("Oh no! You lost this round (´;o;`)", True, (255, 255, 255))
            win_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            screen.blit(win_text, win_rect)   

        elif player.hand != []: # If round is a tie and players hand isn't empty...
            
            # Displaying player wins round text
            win_text = TEXT_FONT.render("Oh no! It's a tie (´;o;`)", True, (255, 255, 255))
            win_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            screen.blit(win_text, win_rect) 

    
        # If player has no more cards left...
        if player.hand == []:
            # If player has more points...
            if PLAYER_POINTS > AI_POINTS:
                game_win_text = TEXT_FONT.render(r"Congratulations! You won the game \(•-•)/", True, (255, 255, 255))
            
            # If AI has more points...
            elif AI_POINTS > PLAYER_POINTS:
                game_win_text = TEXT_FONT.render("Womp Womp! You lost the game (´;o;`)", True, (255, 255, 255))

            # If game is a tie...
            else:
                game_win_text = TEXT_FONT.render("Uh oh! It's a tie (´;o;`)", True, (255, 255, 255))

            # Displaying game results text
            screen.blit(game_win_text, game_win_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100)))
            # Displaying the quit text
            screen.blit(TEXT_FONT.render("Game Quitting (5 Seconds)", True, (255, 255, 255)), game_win_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150)))

            pygame.display.flip() # Update display
            pygame.time.delay(5 * 1000) # Display text for 5 seconds
            pygame.quit() # Quit the game
            sys.exit() # Exit application
        
        # Wait two seconds before continuing
        pygame.display.flip()
        pygame.time.delay(2 * 1000)  # 1 second == 1000 milliseconds



# Start Menu Screen
def start_menu():
    screen.blit(pygame.image.load('./assets/images/background_image.jpg'), (0, 0)) # Setting the background image

    # Creating title
    title_text = pygame.font.Font(None, 90).render("Card Craft: The Ultimate Card Game", True, (255, 255, 255)) # Setting title text and colour
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3 - 100)) # Setting dimensions
    screen.blit(title_text, title_rect) # Rendering text

     # Draw play button 
    play_text = TEXT_FONT.render("Play (Space)", True, (255, 255, 255)) # Setting play text and setting colour
    play_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50)) # Setting dimensions
    screen.blit(play_text, play_rect) # Rendering text
    
    # Draw how to play button
    how_to_play_text = TEXT_FONT.render("How to Play (H)", True, (255, 255, 255)) # Setting how to play text and colour
    how_to_play_rect = how_to_play_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30)) # Setting dimenions 
    screen.blit(how_to_play_text, how_to_play_rect) # Rendering text
    
    # Draw quit button
    quit_text = TEXT_FONT.render("Quit (Q)", True, (255, 255, 255)) # Setting quit text and colour 
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100)) # Setting dimensions 
    screen.blit(quit_text, quit_rect) # Rendering text

# How to play screen
def how_to_play():
    screen.blit(pygame.image.load('./assets/images/background_image.jpg'), (0, 0))  # Setting the background image
    
    # Draw title
    title_text = pygame.font.Font(None, 90).render("How to Play", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3 - 100))
    screen.blit(title_text, title_rect)
    
    # Draw Bullet Point One
    how_to_play_one = TEXT_FONT.render("• Receive 5 cards in hand from the deck of 52 unique cards.", True, (255, 255, 255))
    how_to_play_one_rect = how_to_play_one.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(how_to_play_one, how_to_play_one_rect)

    # Draw Bullet Point Two
    how_to_play_two = TEXT_FONT.render("• Play card each round, highest played card wins round.", True, (255, 255, 255)) # Setting how to play text and colour
    how_to_play_two_rect = how_to_play_two.get_rect(center=(screen_width // 2, screen_height // 2 + 30)) # Setting dimenions 
    screen.blit(how_to_play_two, how_to_play_two_rect) # Rendering text
    
    # Draw Bullet Point Three
    how_to_play_three = TEXT_FONT.render("• When all cards have been played, player with most wins will win game.", True, (255, 255, 255)) # Setting quit text and colour 
    how_to_play_rect = how_to_play_three.get_rect(center=(screen_width // 2, screen_height // 2 + 100)) # Setting dimensions 
    screen.blit(how_to_play_three, how_to_play_rect) # Rendering text
    
    # Draw Back button
    back_text = TEXT_FONT.render("Back (B)", True, (255, 255, 255))
    back_rect = back_text.get_rect(center=(screen_width // 2, screen_height - 100))
    screen.blit(back_text, back_rect)


# Initialising main function
def main():
    current_screen = "start_menu"  # Initial screen

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
                    pygame.quit() # Quit the game
                    sys.exit() # Exit application
    
                elif event.key == pygame.K_b and current_screen == "how_to_play": # If on the how to play screen and keydown is B...
                    current_screen = "start_menu" # Switch back to start menu
    
        if current_screen == 'start_menu':
            # Implement game logic here (compare playing_card with AI's card, determine winner, etc.)
            # Display the game screen (player's hand, AI's hand, etc.)
            start_menu()
            pass
        elif current_screen == 'how_to_play':
            # Display the start menu or how-to-play screen
            how_to_play()  # You can switch to draw_how_to_play() if needed
            pass
        elif current_screen == 'start_game':
           game_play()

        pygame.display.flip()

main()