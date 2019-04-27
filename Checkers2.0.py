import pygame
pygame.init()

window_size = window_width, window_height = 800, 800

window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Checkers by David Earnest")
moveSound = pygame.mixer.Sound("untitled.wav")
pygame.mixer.music.load("My Hopes And Your Dreams.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)
font = pygame.font.SysFont(None, 35)


class player:
    color = ''

    def __init__(self):
        self.mouse = (0, 0)
        self.numPieces = 12
        self.holdingPiece = False
        self.pieceLocation = (0, 0)
        self.moved = False

    def print_layer3(self, myLayer2):
        '''
        Prints purple on the squares a piece can move to
        '''
        moves = self.get_valid_moves(myLayer2)

        for move in moves:
            pygame.draw.rect(window, (210, 206, 240), (move[0] * 100, move[1] * 100, 100, 100))

        pygame.display.update()

    def can_jump_top_left(self, position, myLayer2):
        if myLayer2[position[1]][position[0]].color == "Red" or myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the top left corner of the board
            if position[0] > 1 and position[1] > 1:
                # Check if we can jump black piece
                if myLayer2[position[1] - 1][position[0] - 1].color == ("Red", "Black")[self.color == "Red"]:
                    if myLayer2[position[1] - 2][position[0] - 2] == Layer2.empty:
                        return True
        return False

    def can_jump_top_right(self, position, myLayer2):
        if myLayer2[position[1]][position[0]].color == "Red" or myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the top right corner of the board
            if position[0] < 6 and position[1] > 1:
                # Check if we can jump black piece
                if myLayer2[position[1] - 1][position[0] + 1].color == ("Red", "Black")[self.color == "Red"]:
                    if myLayer2[position[1] - 2][position[0] + 2] == Layer2.empty:
                        return True
        return False

    def can_jump_bottom_left(self, position, myLayer2):
        if myLayer2[position[1]][position[0]].color == "Black" or myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the bottom left corner of the board
            if position[0] > 1 and position[1] < 6:
                # Check if we can jump black piece
                if myLayer2[position[1] + 1][position[0] - 1].color == ("Red", "Black")[self.color == "Red"]:
                    if myLayer2[position[1] + 2][position[0] - 2] == Layer2.empty:
                        return True
        return False

    def can_jump_bottom_right(self, position, myLayer2):
        if myLayer2[position[1]][position[0]].color == "Black" or myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the bottom right corner of the board
            if position[0] < 6 and position[1] < 6:
                # Check if we can jump black piece
                if myLayer2[position[1] + 1][position[0] + 1].color == ("Red", "Black")[self.color == "Red"]:
                    if myLayer2[position[1] + 2][position[0] + 2] == Layer2.empty:
                        return True
        return False

    def can_move_top_left(self, position, myLayer2):
        if myLayer2[position[1]][position[0]].color == "Red" or myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the top left corner of the board
            if position[0] > 0 and position[1] > 0:
                # Check if we can move to blank square
                if myLayer2[position[1] - 1][position[0] - 1] == myLayer2.empty:
                    return True
        return False

    def can_move_top_right(self, position, myLayer2):
        if myLayer2[position[1]][position[0]].color == "Red" or myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the top right corner of the board
            if position[0] < 7 and position[1] > 0:
                # Check if we can move to empty square
                if myLayer2[position[1] - 1][position[0] + 1] == Layer2.empty:
                    return True
        return False

    def can_move_bottom_left(self, position, myLayer2):
        if myLayer2[position[1]][position[0]].color == "Black" or myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the bottom left corner of the board
            if position[0] > 0 and position[1] < 7:
                # Check if we can move to empty square
                if myLayer2[position[1] + 1][position[0] - 1] == Layer2.empty:
                    return True
        return False

    def can_move_bottom_right(self, position, myLayer2):
        if myLayer2[position[1]][position[0]].color == "Black" or myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the bottom right corner of the board
            if position[0] < 7 and position[1] < 7:
                # Check if we can move to empty square
                if myLayer2[position[1] + 1][position[0] + 1] == Layer2.empty:
                    return True
        return False

    def can_jump(self, position, myLayer2):
        '''
        Finds pieces that can make a jump move
        If you have an option to jump, you must make a jump move
        '''

        can_jump_top = self.can_jump_top_right(position, myLayer2) or self.can_jump_top_left(position, myLayer2)
        can_jump_bottom = self.can_jump_bottom_right(position, myLayer2) or self.can_jump_bottom_left(position, myLayer2)

        return can_jump_bottom or can_jump_top

    def check_forced_move(self, myLayer2):
        '''
        Finds pieces that are forced to jump
        '''
        forced_pieces = []

        for j in range(8):
            for i in range(8):
                if myLayer2[j][i].color == self.color and self.can_jump((i, j), myLayer2):
                    forced_pieces += [(i, j)]

        return forced_pieces

    def set_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = mouse_x // 100
        mouse_y = mouse_y // 100
        self.mouse = (mouse_x, mouse_y)

    def get_valid_moves(self, myLayer2):
        valid_moves = {}
        jump_move = False

        if self.can_move_bottom_left(self.pieceLocation, myLayer2):
            valid_moves[(self.pieceLocation[0] - 1, self.pieceLocation[1] + 1)] = []
        elif self.can_jump_bottom_left(self.pieceLocation, myLayer2):
            self.get_jumps((self.pieceLocation[0] - 2, self.pieceLocation[1] + 2), myLayer2, valid_moves, [(self.pieceLocation[0] - 1, self.pieceLocation[1] + 1)])
            jump_move = True

        if self.can_move_bottom_right(self.pieceLocation, myLayer2):
            valid_moves[(self.pieceLocation[0] + 1, self.pieceLocation[1] + 1)] = []
        elif self.can_jump_bottom_right(self.pieceLocation, myLayer2):
            self.get_jumps((self.pieceLocation[0] + 2, self.pieceLocation[1] + 2), myLayer2, valid_moves, [(self.pieceLocation[0] + 1, self.pieceLocation[1] + 1)])
            jump_move = True

        if self.can_move_top_left(self.pieceLocation, myLayer2):
            valid_moves[(self.pieceLocation[0] - 1, self.pieceLocation[1] - 1)] = []
        elif self.can_jump_top_left(self.pieceLocation, myLayer2):
            self.get_jumps((self.pieceLocation[0] - 2, self.pieceLocation[1] - 2), myLayer2,valid_moves, [(self.pieceLocation[0] - 1, self.pieceLocation[1] - 1)])
            jump_move = True

        if self.can_move_top_right(self.pieceLocation, myLayer2):
            valid_moves[(self.pieceLocation[0] + 1, self.pieceLocation[1] - 1)] = []
        elif self.can_jump_top_right(self.pieceLocation, myLayer2):
            self.get_jumps((self.pieceLocation[0] + 2, self.pieceLocation[1] - 2), myLayer2, valid_moves, [(self.pieceLocation[0] + 1, self.pieceLocation[1] - 1)])
            jump_move = True

        if jump_move:
            valid_moves = {i: valid_moves[i] for i in valid_moves if not valid_moves[i] == []}
        return valid_moves

    def get_jumps(self, Location, myLayer2, valid_moves, to_delete):
        if myLayer2[self.pieceLocation[1]][self.pieceLocation[0]].rank == True:
            # Booleans that determine if jumps in all directions are valid or not
            invalid_location_bottom_left = Location[0] - 2 < 0 or Location[1] + 2 > 7 or myLayer2[Location[1] + 1][Location[0] - 1].color != ("Red", "Black")[self.color == "Red"]
            go_bottom_left = invalid_location_bottom_left or myLayer2[Location[1] + 2][Location[0] - 2] != Layer2.empty or (Location[0] - 1, Location[1] + 1) in to_delete

            invalid_location_top_right = Location[0] + 2 > 7 or Location[1] - 2 < 0 or myLayer2[Location[1] - 1][Location[0] + 1].color != ("Red", "Black")[self.color == "Red"]
            go_top_right = invalid_location_top_right or myLayer2[Location[1] - 2][Location[0] + 2] != Layer2.empty or (Location[0] + 1, Location[1] - 1) in to_delete

            invalid_location_top_left = Location[0] - 2 < 0 or Location[1] - 2 < 0 or myLayer2[Location[1] - 1][Location[0] - 1].color != ("Red", "Black")[self.color == "Red"]
            go_top_left = invalid_location_top_left or myLayer2[Location[1] - 2][Location[0] - 2] != Layer2.empty or (Location[0] - 1, Location[1] - 1) in to_delete

            invalid_location_bottom_right = Location[0] + 2 > 7 or Location[1] + 2 > 7 or myLayer2[Location[1] + 1][Location[0] + 1].color != ("Red", "Black")[self.color == "Red"]
            go_bottom_right = invalid_location_bottom_right or myLayer2[Location[1] + 2][Location[0] + 2] != Layer2.empty or (Location[0] + 1, Location[1] + 1) in to_delete
        elif self.color == "Red":
            invalid_location_top_right = Location[0] + 2 > 7 or Location[1] - 2 < 0 or myLayer2[Location[1] - 1][Location[0] + 1].color != ("Red", "Black")[self.color == "Red"]
            go_top_right = invalid_location_top_right or myLayer2[Location[1] - 2][Location[0] + 2] != Layer2.empty or (Location[0] + 1, Location[1] - 1) in to_delete

            invalid_location_top_left = Location[0] - 2 < 0 or Location[1] - 2 < 0 or myLayer2[Location[1] - 1][Location[0] - 1].color != ("Red", "Black")[self.color == "Red"]
            go_top_left = invalid_location_top_left or myLayer2[Location[1] - 2][Location[0] - 2] != Layer2.empty or (Location[0] - 1, Location[1] - 1) in to_delete

            go_bottom_left = True
            go_bottom_right = True
        elif self.color == "Black":
            invalid_location_bottom_left = Location[0] - 2 < 0 or Location[1] + 2 > 7 or myLayer2[Location[1] + 1][Location[0] - 1].color != ("Red", "Black")[self.color == "Red"]
            go_bottom_left = invalid_location_bottom_left or myLayer2[Location[1] + 2][Location[0] - 2] != Layer2.empty or (Location[0] - 1, Location[1] + 1) in to_delete

            invalid_location_bottom_right = Location[0] + 2 > 7 or Location[1] + 2 > 7 or myLayer2[Location[1] + 1][Location[0] + 1].color != ("Red", "Black")[self.color == "Red"]
            go_bottom_right = invalid_location_bottom_right or myLayer2[Location[1] + 2][Location[0] + 2] != Layer2.empty or (Location[0] + 1, Location[1] + 1) in to_delete

            go_top_left = True
            go_top_right = True
        def get_jumps_top_left(Location, myLayer2, valid_moves, to_delete):
            to_delete = to_delete[:]

            if go_top_left:
                if go_top_right and go_bottom_right and go_bottom_left:
                    valid_moves[Location] = to_delete
            # Keep looking if the left jump is valid
            else:
                to_delete += [(Location[0] - 1, Location[1] - 1)]
                return self.get_jumps((Location[0] - 2, Location[1] - 2), myLayer2, valid_moves, to_delete)

        def get_jumps_top_right(Location, myLayer2, valid_moves, to_delete):
            to_delete = to_delete[:]

            if go_top_right:
                if go_top_left and go_bottom_left and go_bottom_right:
                    valid_moves[Location] = to_delete
            # Keep looking if the right jump is valid
            else:
                to_delete += [(Location[0] + 1, Location[1] - 1)]
                return self.get_jumps((Location[0] + 2, Location[1] - 2), myLayer2, valid_moves, to_delete)

        def get_jumps_bottom_left(Location, myLayer2, valid_moves, to_delete):
            to_delete = to_delete[:]

            if go_bottom_left:
                if go_bottom_right and go_top_right and go_top_left:
                    valid_moves[Location] = to_delete
            # Keep looking if the left jump is valid
            else:
                to_delete += [(Location[0] - 1, Location[1] + 1)]
                return self.get_jumps((Location[0] - 2, Location[1] + 2), myLayer2, valid_moves, to_delete)

        def get_jumps_bottom_right(Location, myLayer2, valid_moves, to_delete):
            to_delete = to_delete[:]

            if go_bottom_right:
                if go_bottom_left and go_top_left and go_top_right:
                    valid_moves[Location] = to_delete
            # Keep looking if the right jump is valid
            else:
                to_delete += [(Location[0] + 1, Location[1] + 1)]
                return self.get_jumps((Location[0] + 2, Location[1] + 2), myLayer2, valid_moves, to_delete)

        return get_jumps_top_left(Location, myLayer2, valid_moves, to_delete), get_jumps_top_right(Location, myLayer2, valid_moves, to_delete), get_jumps_bottom_left(Location, myLayer2, valid_moves, to_delete), get_jumps_bottom_right(Location, myLayer2, valid_moves, to_delete)

    def can_step(self, position, myLayer2):
        if self.can_move_bottom_left(position, myLayer2):
            return True
        if self.can_move_bottom_right(position, myLayer2):
            return True
        if self.can_move_top_right(position, myLayer2):
            return True
        if self.can_move_top_left(position, myLayer2):
            return True
        return False


class Player2(player):
    color = 'Black'

    def __init__(self):
        self.mouse = (0, 0)
        self.numPieces = 12
        self.holdingPiece = False
        self.pieceLocation = (0, 0)
        self.moved = False

    def player_move(self, myLayer2):
        self.moved = False
        self.set_mouse()
        if not self.check_forced_move(myLayer2) == []:
            if self.mouse in self.check_forced_move(myLayer2):
                self.pieceLocation = self.mouse
                self.holdingPiece = True
            else:
                if self.holdingPiece:
                    self.swap_pieces(myLayer2)
                self.holdingPiece = False
        else:
            if myLayer2[self.mouse[1]][self.mouse[0]].color == "Black":
                self.pieceLocation = self.mouse
                self.holdingPiece = True
            else:
                if self.holdingPiece:
                    self.swap_pieces(myLayer2)
                self.holdingPiece = False

    def swap_pieces(self, myLayer2):
        self.set_mouse()
        valid_moves = self.get_valid_moves(myLayer2)
        if self.mouse in valid_moves:
            self.moved = True
            isAKing = myLayer2[self.pieceLocation[1]][self.pieceLocation[0]].rank
            # Swaps piece and final empty square
            myLayer2[self.pieceLocation[1]][self.pieceLocation[0]] = Layer2.empty

            # If we are on the end of the board we become a king
            # If we are a king we stay a king
            if isAKing == True or self.mouse[1] == 7:
                myLayer2[self.mouse[1]][self.mouse[0]] = Piece(self.color, True)
            else:
                myLayer2[self.mouse[1]][self.mouse[0]] = Piece(self.color, False)
            self.holdingPiece = False

            # Erases Jumped Pieces
            for i in valid_moves[self.mouse]:
                myLayer2[i[1]][i[0]] = Layer2.empty

            # Plays move sound
            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(moveSound)
            pygame.mixer.music.unpause()

    '''def can_step(self, position, myLayer2):

        # Piece is not on the bottom left corner of the board
        if position[0] > 0 and position[1] < 7:
            # Store move if left move is valid
            if myLayer2[position[1] + 1][position[0] - 1] == Layer2.empty:
                return True

        # Piece is not on the bottom right corner of the board
        if position[0] < 7 and position[1] < 7:
            # Store move if right move is valid
            if myLayer2[position[1] + 1][position[0] + 1] == Layer2.empty:
                return True

        if myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the top left corner of the board
            if position[0] > 0 and position[1] > 0:
                # Store move if left move is valid
                if myLayer2[position[1] - 1][position[0] - 1] == Layer2.empty:
                    return True

            # Piece is not on the top right corner of the board
            if position[0] < 7 and position[1] > 0:
                # Store move if right move is valid
                if myLayer2[position[1] - 1][position[0] + 1] == Layer2.empty:
                    return True

        return False'''

    def lose(self, myLayer2):

        for j in range(8):
            for i in range(8):
                if myLayer2[j][i].color == self.color:
                    if self.can_step((i, j), myLayer2) or self.can_jump((i, j), myLayer2):
                        return False
        return True


class Player(player):
    color = 'Red'

    def __init__(self):
        self.mouse = (0, 0)
        self.numPieces = 12
        self.holdingPiece = False
        self.pieceLocation = (0, 0)
        self.moved = False

    def player_move(self, myLayer2):
        self.moved = False
        self.set_mouse()

        # Checks if we have a jump move that we must take
        if not self.check_forced_move(myLayer2) == []:
            if self.mouse in self.check_forced_move(myLayer2):
                self.pieceLocation = self.mouse
                self.holdingPiece = True
            else:
                if self.holdingPiece:
                    self.swap_pieces(myLayer2)
                self.holdingPiece = False
        else:
            if myLayer2[self.mouse[1]][self.mouse[0]].color == "Red":
                self.pieceLocation = self.mouse
                self.holdingPiece = True
            else:
                if self.holdingPiece:
                    self.swap_pieces(myLayer2)
                self.holdingPiece = False

    def swap_pieces(self, myLayer2):
        '''
        Swaps pieces and removes jumped pieces
        '''
        self.set_mouse()
        valid_moves = self.get_valid_moves(myLayer2)
        if self.mouse in valid_moves:
            self.moved = True
            isAKing = myLayer2[self.pieceLocation[1]][self.pieceLocation[0]].rank
            # Swaps piece and final empty square
            myLayer2[self.pieceLocation[1]][self.pieceLocation[0]] = Layer2.empty

            # If we are on the end of the board we become a king
            # If we are a king we stay a king
            if isAKing == True or self.mouse[1] == 0:
                myLayer2[self.mouse[1]][self.mouse[0]] = Piece(self.color, True)
            else:
                myLayer2[self.mouse[1]][self.mouse[0]] = Piece(self.color, False)
            self.holdingPiece = False

            # Erases Jumped Pieces
            for i in valid_moves[self.mouse]:
                myLayer2[i[1]][i[0]] = Layer2.empty

            # Plays move sound
            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(moveSound)
            pygame.mixer.music.unpause()

    '''def can_step(self, position, myLayer2):
        # Piece is not on the top left corner of the board
        if position[0] > 0 and position[1] > 0:
            # Store move if left move is valid
            if myLayer2[position[1] - 1][position[0] - 1] == Layer2.empty:
                return True

        # Piece is not on the top right corner of the board
        if position[0] < 7 and position[1] > 0:
            # Store move if right move is valid
            if myLayer2[position[1] - 1][position[0] + 1] == Layer2.empty:
                return True

        if myLayer2[position[1]][position[0]].rank == True:
            # Piece is not on the bottom left corner of the board
            if position[0] > 0 and position[1] < 7:
                # Store move if left move is valid
                if myLayer2[position[1] + 1][position[0] - 1] == Layer2.empty:
                    return True

            # Piece is not on the bottom right corner of the board
            if position[0] < 7 and position[1] < 7:
                # Store move if right move is valid
                if myLayer2[position[1] + 1][position[0] + 1] == Layer2.empty:
                    return True
        return False'''

    def lose(self, myLayer2):

        for j in range(8):
            for i in range(8):
                if myLayer2[j][i].color == self.color:
                    if self.can_step((i, j), myLayer2) or self.can_jump((i, j), myLayer2):
                        return False
        return True



class Piece:
    '''
    Data type used to hold piece objects
    '''

    def __init__(self, color, is_king):
        self.color = color
        self.rank = is_king
        self.moves = []

    def __str__(self):
        return f"({self.color}, {self.rank})"

    def __repr__(self):
        return f"({self.color}, {self.rank})"


class Layer2:
    '''
    Prints the pieces on the board
    White, red, and kings
    '''

    rows = 8
    columns = 8
    empty = Piece("Empty", "Empty")

    def __init__(self):
        self.squares = [[Layer2.empty for _ in range(Layer2.rows)] for _ in range(Layer2.columns)]
        self.start_position()

    def __getitem__(self, key):
        return self.squares[key]

    def start_position(self):
        # Prints the starting position of board pieces

        add_piece = False

        # Prints black pieces
        for y in range(3):
            for x in range(Layer2.rows):
                if add_piece:
                    self.squares[y][x] = Piece("Black", False)
                add_piece = not add_piece
            add_piece = not add_piece

        # Prints red pieces
        for y in range(5,Layer2.columns):
            for x in range(Layer2.rows):
                if add_piece:
                    self.squares[y][x] = Piece("Red", False)
                add_piece = not add_piece
            add_piece = not add_piece

    def print(self):
        # Prints updated positions of every piece on the board

        for y in range(self.columns):
            for x in range(self.rows):
                if not self.squares[y][x] == Layer2.empty:
                    piece_y = int(y * (window_height / 8) + (window_height / 16))
                    piece_x = int(x * (window_width / 8) + (window_width / 16))

                    # Prints black pieces and kings
                    if self.squares[y][x].color == "Black":
                        pygame.draw.circle(window, (230, 230, 210), (piece_x, piece_y), int(window_height / 16) - 5, 0)
                        if self.squares[y][x].rank:
                            pygame.draw.circle(window, (207, 181, 59), (piece_x, piece_y), int(window_height / 16) - 15, 0)
                        else:
                            pygame.draw.circle(window, (255, 250, 205), (piece_x, piece_y), int(window_height / 16) - 15, 0)

                    # Prints red pieces and kings
                    else:
                        pygame.draw.circle(window, (210, 70, 70), (piece_x, piece_y), int(window_height / 16) - 5, 0)
                        if self.squares[y][x].rank:
                            pygame.draw.circle(window, (207, 181, 59), (piece_x, piece_y), int(window_height / 16) - 15, 0)
                        else:
                            pygame.draw.circle(window, (240, 70, 70), (piece_x, piece_y), int(window_height / 16) - 15, 0)
        pygame.display.update()

def drawLayer1():
    '''
    Prints the Board. Just the white and green squares
    '''

    window.fill((0, 102, 51))
    my_print = True

    square_width = int(window_width/8)
    square_height = int(window_height/8)

    for y_position in range(0,window_height,square_height):
        for x_position in range(0,window_width, square_width):
            if my_print:
                pygame.draw.rect(window, (240,255,240), (x_position, y_position, square_width, square_height))
            my_print = not my_print
        my_print = not my_print

    pygame.display.update()


second_layer = Layer2()
myPlayer = Player()
myPlayer2 = Player2()

# Main Loop
run = True
turn = 0
lose1 = False
lose2 = False
stop = False
while run:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if turn % 2 == 0:
                if not lose1:
                    myPlayer.player_move(second_layer)
                    turn += myPlayer.moved
                else:
                    stop = True
            else:
                if not lose2:
                    myPlayer2.player_move(second_layer)
                    turn += myPlayer2.moved
                else:
                    stop = True

    if not stop:
        drawLayer1()
        second_layer.print()
        if myPlayer.holdingPiece:
            myPlayer.print_layer3(second_layer)
        if myPlayer2.holdingPiece:
            myPlayer2.print_layer3(second_layer)
    else:
        window.fill((0, 0, 0))
        if lose1:
            screen_text = font.render("Player 2 Wins!", True, (255, 255, 255))
        else:
            screen_text = font.render("Player 1 Wins!", True, (255, 255, 255))
        window.blit(screen_text, [310, 310])
        pygame.display.update()

    lose1 = myPlayer.lose(second_layer)
    lose2 = myPlayer2.lose(second_layer)

pygame.quit()