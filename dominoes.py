import random as r

class DominoGame:

    def __init__(self):
        self.domino_snake = []
        self.status = None


    def make_set(self):
        self.full_set = []
        for i in range(7):
            for x in range(i + 1):
                self.full_set.append([i, x])
        r.shuffle(self.full_set)


    def distribute_pieces(self):
        self.make_set()
        self.computer = []
        self.player = []
        self.stock_pieces = []
        for i in range(7):
            self.player.append(self.full_set.pop())
            self.computer.append(self.full_set.pop())
        self.stock_pieces = self.full_set
        # sort player's pieces in descending order
        self.computer.sort(reverse=True, key=lambda x: sum(x))
        self.player.sort(reverse=True, key=lambda x: sum(x))


    def initialize_game(self):
        self.distribute_pieces()
        first_piece = False
        computer_piece = False
        player_piece = False
        # find the largest double piece for both players
        while first_piece == False:
            for i in self.player:
                if i[0] == i[1]:
                    player_piece = i
                    first_piece = True
                    break
            for x in self.computer:
                if x[0] == x[1]:
                    computer_piece = x
                    first_piece = True
                    break
            # if no doubles found re-make set and redistribute
            if first_piece == False:
                self.distribute_pieces()
        # find the largest double between players
        if computer_piece and player_piece:
            if computer_piece > player_piece:
                first_piece = computer_piece
            else:
                first_piece = player_piece
        elif computer_piece:
            first_piece = computer_piece
        else:
            first_piece = player_piece
        # remove found double piece from player's inventory
        if first_piece in self.computer:
            self.computer.remove(first_piece)
            self.status = self.computer
        elif first_piece in self.player:
            self.player.remove(first_piece)
            self.status = self.player
        # add first piece to domino snake
        self.domino_snake.append(first_piece)
        self.change_turn()


    def change_turn(self):
        if self.status == self.player:
            self.status = self.computer
        else:
            self.status = self.player


    def check_end_condition(self, move):
        if len(self.player) == 0:
            return "The game is over. You won!"
        elif len(self.computer) == 0:
            return "The game is over. The computer won!"
        elif self.domino_snake[0][0] == self.domino_snake[-1][-1]:
            c = 0
            x = d1.domino_snake[0][0]
            for i in range(len(d1.domino_snake)):
                if x in d1.domino_snake[i]:
                    c += d1.domino_snake[i].count(x)
            if c == 8:
                return "The game is over. It's a draw!"
        elif move == 0:
            if len(self.stock_pieces) == 0:
                return "The game is over. It's a draw!"


    def display_board(self):
        header = "=" * 70
        print(header)
        print(f"Stock size: {len(self.stock_pieces)}")
        print(f"Computer pieces: {len(self.computer)}\n")


    def display_snake(self):
        if len(self.domino_snake) < 7:
            for i in self.domino_snake:
                print(i, end='')
        else:
            for x in self.domino_snake[:3]:
                 print(x, end='')
            print("...", end='')
            for y in self.domino_snake[-3:]:
                print(y, end='')
#            print(f"{self.domino_snake[:3]}...{self.domino_snake[-3:]}", end='')
        print("\n")


    def display_player_pieces(self):
        print("Your pieces:")
        for i in range(1, len(self.player) + 1):
            print(f"{i}:{self.player[i - 1]}")
        print("")


    def take_turn(self, legal=False):
        if self.status == self.player:
            move = input("Status: It's your turn to make a move. Enter your command.\n")
            while not legal:
                try:
                    move = int(move)
                except:
                    move = input("Invalid input. Please try again.")
                    continue
                if move < -len(self.player) or move > len(self.player):
                    move = input("Invalid input. Please try again.")
                else:
                    legal = self.legal_move(move)
                    if not legal:
                        move = input("Illegal move. Please try again.")
            return move
        elif self.status == self.computer:
            junk_variable = input("Status: Computer is about to make a move. Press Enter to continue...\n")
            move = self.computer_ai()
            return move

    def computer_ai(self):
        status_values = [j for i in self.status for j in i]    # un-nest status list to use .count()
        domino_snake_values = [j_1 for i_1 in self.domino_snake for j_1 in i_1]    # un-nest domino_snake list to use .count()

        # create dictionary {unique piece values: number of occurrences}
        status_set = set(status_values)
        values_dict = {}
        for i_2 in status_set:
            values_dict.update({i_2: status_values.count(i_2) + domino_snake_values.count(i_2)})

        # create list of piece value occurrences
        value_sums_list = [sum([values_dict[i_3[0]], values_dict[i_3[1]]]) for i_3 in self.status]

        # use max value in value_sums_list, check if it is legal, if not, remove from list
        legal = False
        while not legal:
            move = self.status.index(self.status[value_sums_list.index(max(value_sums_list))]) + 1
            legal = self.legal_move(move) or self.legal_move(-move)
            if not legal:
                value_sums_list.remove(value_sums_list[move - 1])
            if len(value_sums_list) == 0:    # no pieces are legal, computer draws a piece
                move = 0
                legal = True
        if self.legal_move(move):
            return move
        else:
            return -move

    def legal_move(self, move):
        if move < 0:
            if self.domino_snake[0][0] not in self.status[abs(move + 1)]:
                return False
            else:
                return True
        elif move > 0:
            if self.domino_snake[-1][-1] not in self.status[move - 1]:
                return False
            else:
                return True
        else:
            return True

    def move_pieces(self, move):
        def swap(piece):
            piece[0], piece[1] = piece[1], piece[0]

        if move == 0:
            if len(self.stock_pieces) == 0:
                pass
            else:
                self.status.append(self.stock_pieces.pop())
        elif move < 0:
            if self.status[abs(move + 1)][1] != self.domino_snake[0][0]:
                swap(self.status[move + 1])
            self.domino_snake.insert(0, self.status.pop(abs(move + 1)))
        else:
            if self.status[move - 1][0] != self.domino_snake[-1][-1]:
                swap(self.status[move - 1])
            self.domino_snake.append(self.status.pop(move - 1))


    def rtx_on(self):
        self.display_board()
        self.display_snake()
        self.display_player_pieces()


    def game_loop(self):
        while True:
            move = self.take_turn()
            self.move_pieces(move)
            self.change_turn()
            self.rtx_on()
            end = self.check_end_condition(move)
            if end:
                print(f"Status: {end}")
                break


d1 = DominoGame()
d1.initialize_game()
d1.rtx_on()
d1.game_loop()

