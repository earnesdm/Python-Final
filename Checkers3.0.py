import random
import pygame


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
                if myLayer2[position[1] - 1][position[0] - 1] == Layer2.empty:
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
        # Returns a dictionary with all of the moves a piece can make
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
            invalid_location_bottom_left = Location[0] - 2 < 0 or Location[1] + 2 > 7 or myLayer2[Location[1] + 1][
                Location[0] - 1].color != ("Red", "Black")[self.color == "Red"]
            go_bottom_left = invalid_location_bottom_left or myLayer2[Location[1] + 2][
                Location[0] - 2] != Layer2.empty or (Location[0] - 1, Location[1] + 1) in to_delete

            invalid_location_top_right = Location[0] + 2 > 7 or Location[1] - 2 < 0 or myLayer2[Location[1] - 1][
                Location[0] + 1].color != ("Red", "Black")[self.color == "Red"]
            go_top_right = invalid_location_top_right or myLayer2[Location[1] - 2][Location[0] + 2] != Layer2.empty or (
            Location[0] + 1, Location[1] - 1) in to_delete

            invalid_location_top_left = Location[0] - 2 < 0 or Location[1] - 2 < 0 or myLayer2[Location[1] - 1][
                Location[0] - 1].color != ("Red", "Black")[self.color == "Red"]
            go_top_left = invalid_location_top_left or myLayer2[Location[1] - 2][Location[0] - 2] != Layer2.empty or (
            Location[0] - 1, Location[1] - 1) in to_delete

            invalid_location_bottom_right = Location[0] + 2 > 7 or Location[1] + 2 > 7 or myLayer2[Location[1] + 1][
                Location[0] + 1].color != ("Red", "Black")[self.color == "Red"]
            go_bottom_right = invalid_location_bottom_right or myLayer2[Location[1] + 2][
                Location[0] + 2] != Layer2.empty or (Location[0] + 1, Location[1] + 1) in to_delete
        elif self.color == "Red":
            invalid_location_top_right = Location[0] + 2 > 7 or Location[1] - 2 < 0 or myLayer2[Location[1] - 1][
                Location[0] + 1].color != ("Red", "Black")[self.color == "Red"]
            go_top_right = invalid_location_top_right or myLayer2[Location[1] - 2][Location[0] + 2] != Layer2.empty or (
            Location[0] + 1, Location[1] - 1) in to_delete

            invalid_location_top_left = Location[0] - 2 < 0 or Location[1] - 2 < 0 or myLayer2[Location[1] - 1][
                Location[0] - 1].color != ("Red", "Black")[self.color == "Red"]
            go_top_left = invalid_location_top_left or myLayer2[Location[1] - 2][Location[0] - 2] != Layer2.empty or (
            Location[0] - 1, Location[1] - 1) in to_delete

            go_bottom_left = True
            go_bottom_right = True
        elif self.color == "Black":
            invalid_location_bottom_left = Location[0] - 2 < 0 or Location[1] + 2 > 7 or myLayer2[Location[1] + 1][
                Location[0] - 1].color != ("Red", "Black")[self.color == "Red"]
            go_bottom_left = invalid_location_bottom_left or myLayer2[Location[1] + 2][
                Location[0] - 2] != Layer2.empty or (Location[0] - 1, Location[1] + 1) in to_delete

            invalid_location_bottom_right = Location[0] + 2 > 7 or Location[1] + 2 > 7 or myLayer2[Location[1] + 1][
                Location[0] + 1].color != ("Red", "Black")[self.color == "Red"]
            go_bottom_right = invalid_location_bottom_right or myLayer2[Location[1] + 2][
                Location[0] + 2] != Layer2.empty or (Location[0] + 1, Location[1] + 1) in to_delete

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
        # Checks to see if we can make a standard move
        if self.can_move_bottom_left(position, myLayer2):
            return True
        if self.can_move_bottom_right(position, myLayer2):
            return True
        if self.can_move_top_right(position, myLayer2):
            return True
        if self.can_move_top_left(position, myLayer2):
            return True
        return False


class Tree:
    # I took this class from composingprograms.com
    def __init__(self, label, branches=[]):
        self.label = label
        for branch in branches:
            assert isinstance(branch, Tree)
        self.branches = branches

    def __repr__(self):
        if self.branches:
            return 'Tree({0}, {1})'.format(self.label, repr(self.branches))
        else:
            return 'Tree({0})'.format(repr(self.label))

    def is_leaf(self):
        return not self.branches


class Node:
    def __init__(self, board, score = "Empty"):
        self.board = board
        self.score = score


class AI(player):
    color = "Black"

    def __init__(self):
        #self.mouse = (0, 0)
        #self.numPieces = 12
        #self.holdingPiece = False
        self.pieceLocation = (0, 0)
        self.moved = False
        self.move_list = []
        self.board_tree = Tree("Empty")

    def board_score(self, board):
        #Returns a score evaluating how desirable a board is.
        #AI wants I high number player wants a low number

        score = 0

        for j in range(8):
            for i in range(8):
                if board[j][i].rank == True:
                    if board[j][i].color == "Black":
                        score += 3
                    if board[j][i].color == "Red":
                        score -= 3
                else:
                    if board[j][i].color == "Black":
                        score += 1
                    if board[j][i].color == "Red":
                        score -= 1
        return score

    def get_moves(self, parent_board, color):
        # Sets move_list based on parent_board
        self.color = color

        forced_pieces = self.check_forced_move(parent_board)
        all_pieces = []
        self.move_list = []

        if forced_pieces != []:
            for i in forced_pieces:
                self.pieceLocation = i
                valid_moves = self.get_valid_moves(parent_board)
                for j in valid_moves:
                    self.move_list += [(i, j, valid_moves[j])]

        else:
            for j in range(8):
                for i in range(8):
                    if parent_board[j][i].color == self.color:
                        all_pieces += [(i, j)]

            for n in all_pieces:
                self.pieceLocation = n
                valid_moves = self.get_valid_moves(parent_board)
                for j in valid_moves:
                    self.move_list += [(n, j, valid_moves[j])]

    def node_of_boards(self, parent_board):
        nodes = []

        for move in self.move_list:
            temp_board = [row[:] for row in parent_board]

            # color neutral move piece to destination
            temp_board[move[1][1]][move[1][0]] = temp_board[move[0][1]][move[0][0]]

            # If we move to the end of the board we become a king
            if (move[1][1] == 0) or (move[1][1] == 7):
                temp_board[move[1][1]][move[1][0]] = Piece(("Red", "Black")[temp_board[move[0][1]][move[0][0]].color == "Black"], True)

            temp_board[move[0][1]][move[0][0]] = Layer2.empty
            # delete jumped pieces
            for to_delete in move[2]:
                temp_board[to_delete[1]][to_delete[0]] = Layer2.empty

            nodes += [Tree(Node(temp_board))]
        #print("Loading AI Move...")
        return nodes

    def fill_tree(self, parent_board, my_tree, n):
        # fills self.board_tree with n level tree of boards

        if n == 0:
            return

        # place all moves to move list
        self.get_moves(parent_board, ("Black", "Red")[n%2 == 1])

        # add boards to branches
        my_tree.branches = self.node_of_boards(parent_board)

        for i in my_tree.branches:
            self.fill_tree(i.label.board, i, n-1)

    def calc_tree_score(self, parent_tree, n):
        # find the score for each board state
        if parent_tree.branches == []:
            parent_tree.label.score = self.board_score(parent_tree.label.board)
        else:
            for i in parent_tree.branches:
                self.calc_tree_score(i, n + 1)

            if n % 2 == 0:
                parent_tree.label.score = max([i.label.score for i in parent_tree.branches])
            else:
                parent_tree.label.score = min([i.label.score for i in parent_tree.branches])

    def play_AI_move(self, myLayer2):
        # fills tree, calculates scores, and plays the best move
        self.board_tree = Tree(Node(myLayer2.squares))
        self.fill_tree(self.board_tree.label.board, self.board_tree, 6) # N here changes how deep we look
        self.calc_tree_score(self.board_tree, 0)
        best_boards = []

        best_score = self.board_tree.label.score

        for i in self.board_tree.branches:
            if i.label.score == best_score:
                best_boards += [i.label.board]
                myLayer2.squares = i.label.board
                break

        # Plays move sound
        pygame.mixer.music.pause()
        pygame.mixer.Sound.play(moveSound)
        pygame.mixer.music.unpause()

    def lose(self, myLayer2):
        # If we have no pieces or we cannot make a move we lose
        for j in range(8):
            for i in range(8):
                if myLayer2[j][i].color == "Black":
                    if self.can_step((i, j), myLayer2) or self.can_jump((i, j), myLayer2):
                        return False
        return True


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
        # Checks if we have a forced jump
        if not self.check_forced_move(myLayer2) == []:
            if self.mouse in self.check_forced_move(myLayer2):
                self.pieceLocation = self.mouse
                self.holdingPiece = True
            else:
                if self.holdingPiece:
                    self.swap_pieces(myLayer2)
                self.holdingPiece = False
        # standard move
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

    def lose(self, myLayer2):
        # If we have no pieces or we cannot make a move we lose
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
        # standard move
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


if __name__ == '__main__':
    pygame.init()

    window_size = window_width, window_height = 800, 800

    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Checkers by David Earnest")
    moveSound = pygame.mixer.Sound("untitled.wav")
    #pygame.mixer.music.load("My Hopes And Your Dreams.mp3")
    #pygame.mixer.music.set_volume(0.01)
    #pygame.mixer.music.play(-1)
    font = pygame.font.SysFont(None, 35)

    second_layer = Layer2()
    myPlayer = Player()
    myAI = AI()

    # draw the board and pieces
    drawLayer1()
    second_layer.print()

    # Main Loop
    turn = 0
    lose1 = False
    lose2 = False
    stop = False

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if turn % 2 == 0:
                if not lose1:
                    myPlayer.player_move(second_layer)
                    turn += myPlayer.moved

                    # if we moved, so it is now the AI's turn
                    if turn % 2 == 1:
                        # Prints board and all pieces
                        drawLayer1()
                        second_layer.print()

                        if not lose2:
                            myAI.play_AI_move(second_layer)
                            turn += 1
                        else:
                            stop = True
                else:
                    stop = True

            # Prints board and all pieces
            drawLayer1()
            second_layer.print()
            if myPlayer.holdingPiece:
                myPlayer.print_layer3(second_layer)

            if stop:
                # Prints game over screen
                window.fill((0, 0, 0))
                if lose1:
                    screen_text = font.render("Player 2 Wins!", True, (255, 255, 255))
                else:
                    screen_text = font.render("Player 1 Wins!", True, (255, 255, 255))
                window.blit(screen_text, [310, 310])
                pygame.display.update()

            lose1 = myPlayer.lose(second_layer)
            lose2 = myAI.lose(second_layer)
