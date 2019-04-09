import sys
import numpy as np
import random


class Board:

	def __init__(self):
		self.num_rows=8
		self.num_cols=8


	def createBoard(self):
		self.Board= [[0 for x in range(self.num_cols)] for y in range(self.num_rows)]
		self.ScoreBoard= [[0 for x in range(self.num_cols)] for y in range(self.num_rows)]
		
		#putting scores in each cell
		for x in range(8):
			for y in range(self.num_cols):
				if(x==0):
					self.ScoreBoard[x][y]=0
				if(x==1):
					self.ScoreBoard[x][y]=1
				if(x==2):
					self.ScoreBoard[x][y]=2
				if(x==3):
					self.ScoreBoard[x][y]=3
				if(x==4):
					self.ScoreBoard[x][y]=4
				if(x==5):
					self.ScoreBoard[x][y]=5
				if(x==6):
					self.ScoreBoard[x][y]=6
				if(x==7):
					self.ScoreBoard[x][y]=7



		#initailizing the rows of pawns for player at the top of the board
		for x in range(2):
			for y in range(self.num_cols):
				self.Board[x][y]='*'

		# initializing the empty rows in the middle of the board
		for x in range(2,self.num_rows-2):
			for y in range(self.num_cols):

				self.Board[x][y]=' '

		# initializing the rows for the bottom of the board
		for x in range(self.num_rows-2, self.num_rows):
			for y in range(self.num_cols):
				self.Board[x][y]='o'



	def displayBoard(self):
		#This function displays the board
		print('  '+' ' + ' '.join('{0:^3s}'.format(str(x)) for x in range(len(self.Board))))
		print('  '+ ' ' + ' '.join('{0:^3s}'.format('___') for x in range(len(self.Board))))
		for i,position in enumerate(self.Board):
			print(str(i)+' '+'|' + '|'.join('{0:^3s}'.format(x) for x in position) + '|')
			print('  '+ ' ' + ' '.join('{0:^3s}'.format('___') for x in range(len(position))))

	

	def getBoards(self):
		#This function returns both gameboard and hueristic score board
		return self.Board,self.ScoreBoard


	def endofGame(self):
		#This function is checking who wins the game
		for x in range(1):
			for y in range(self.num_cols):
				if self.Board[x][y]=='o':
					return "Human player wins"
		
		for x in range(self.num_rows-1,self.num_rows):
			for y in range(self.num_cols):
				if self.Board[x][y]=='*':
					return "Computer wins"
		return False

class HumanPlayer:
	def __init__(self,board):
		self.symbol='o'
		self.Board=board[0]
		self.num_rows=8
		self.num_cols=8

	def move(self):
		while True:
			pawn=input('Please select the o pawn you want to move enter the row and column of pawn\n ie. 6,0 : ')
			try:
				pawn_position=pawn.split(',')
				pawn_position=[int(pawn_position[0]),int(pawn_position[1])]
				if self.Board[pawn_position[0]][pawn_position[1]] == self.symbol:
					break
				else:
					print("Invalid Pawn Selection")
			except IndexError:
				print("Invalid Pawn Selection")
			except ValueError:
				print("Invalid Pawn Selection")
		valid_moves=self.player_valid_moves(pawn_position)
		while True:
			try:
				move=input('Please select a valid move?')
				move=move.split(',')
				move=[int(move[0]),int(move[1])]
				if move in valid_moves:
					break
			except IndexError:
				print("Invalid Move Try Again")
			except ValueError:
				print("Invalid Move Try Again")
		self.makeMove(move,pawn_position)

	def player_valid_moves(self,pawn_position):
		valid_moves=[]
		move_forward=[pawn_position[0]-1,pawn_position[1]]
		if self.Board[move_forward[0]][move_forward[1]]== ' ':
			valid_moves.append(move_forward)
		if pawn_position[1]-1 > 0:
			move_left_diagonal=[pawn_position[0]-1,pawn_position[1]-1]
			if self.Board[move_left_diagonal[0]][move_left_diagonal[1]]== ' ' or self.Board[move_left_diagonal[0]][move_left_diagonal[1]]== '*' :
				valid_moves.append(move_left_diagonal)
		if pawn_position[1]+1 < self.num_cols:
			move_right_diagonal=[pawn_position[0]-1,pawn_position[1]+1]
			if self.Board[move_right_diagonal[0]][move_right_diagonal[1]]== ' ' or self.Board[move_right_diagonal[0]][move_right_diagonal[1]]== '*' :
				valid_moves.append(move_right_diagonal)


		return valid_moves
	
	
	def makeMove(self,move,old_position):
		self.Board[old_position[0]][old_position[1]]=" "
		self.Board[move[0]][move[1]]=self.symbol

	def updateBoard(self,board):
		self.board=board




class ComputerPlayer:
	def __init__(self,board,mode):
		self.symbol='*'
		self.Board=board[0]
		self.ScoreBoard=board[1]
		self.num_rows=8
		self.num_cols=8
		self.mode=mode


	def offensive(self,moves):
		previous_score=0
		previous_move=[0,0]
		previous_old_position=[]
		random.shuffle(moves)
		for pawn in moves:
			
			old_position=pawn[0]

			for possible_move in pawn[1]:
				y=possible_move[0]
				x=possible_move[1]
				top_right=y+1,x+1
				top_left=y+1,x-1
				bottom_right=y-1,x+1
				bottom_left=y-1,x-1
				forward_extra=y+1,x
			
				current_score=self.ScoreBoard[y][x]


				self.Board[old_position[0]][old_position[1]]=" "
				#for checking if there is a teamate on top right,top left...

				#if the enemy is on y-axis <=2 kill him 
				try:
					if(self.Board[y][x]=='o' and y<=2):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=110
				except IndexError:
					continue


				#----------------------------------------------


				#if you can win in 2 moves than do it
				try:
					if(self.Board[top_left[0]][top_left[1]]==' ' and self.Board[top_right[0]][top_right[1]]==' ' and y==6):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=1000+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue

				try:
					if(self.Board[top_left[0]][top_left[1]]=='o' and self.Board[top_right[0]][top_right[1]]=='o' 
						and self.Board[bottom_left[0]][bottom_left[1]]=='*' and self.Board[bottom_right[0]][bottom_right[1]]=='*' and y==6):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=100+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue

				try:
					if(self.Board[top_left[0]][top_left[1]]=='o' and self.Board[bottom_left[0]][bottom_left[1]]=='*' and self.Board[bottom_right[0]][bottom_right[1]]=='*' and y==6 or
						self.Board[top_right[0]][top_right[1]]=='o' and self.Board[bottom_left[0]][bottom_left[1]]=='*' and self.Board[bottom_right[0]][bottom_right[1]]=='*' and y==6):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=120+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue

				try:
					if(self.Board[top_left[0]][top_left[1]]=='o' and self.Board[bottom_left[0]][bottom_left[1]]=='*' and y==6 or
						self.Board[top_right[0]][top_right[1]]=='o' and self.Board[bottom_right[0]][bottom_right[1]]=='*' and y==6):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=120+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue




				#if you can win in your next move, than move there
				try:
					if(y==7):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=1000000
				except IndexError:
					continue
				#------------------------------------------------------

				try:
					if(self.Board[y][x]=='o'):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=3+self.ScoreBoard[y][x]
				except IndexError:
					continue


				try:
					if(self.Board[y][x]=='o' and self.Board[bottom_right[0]][bottom_right[1]] != '*' and self.Board[bottom_left[0]][bottom_left[0]] != '*'):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=5+self.ScoreBoard[y][x]
				except IndexError:
					continue


				try:
					if(self.Board[y][x]=='o' and self.Board[bottom_right[0]][bottom_right[1]] == '*' and self.Board[bottom_left[0]][bottom_left[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_left[0]][top_left[1]] == '*' and self.Board[top_right[0]][top_right[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_left[0]][top_left[1]] == '*' and self.Board[bottom_left[0]][bottom_left[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_left[0]][top_left[1]] == '*' and self.Board[bottom_right[0]][bottom_right[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_right[0]][top_right[1]] == '*' and self.Board[bottom_right[0]][bottom_right[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_right[0]][top_right[1]] == '*' and self.Board[bottom_left[0]][bottom_left[0]] == '*'):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=15+self.ScoreBoard[y][x]
				except IndexError:
					continue

				try:
					if(self.Board[y][x]=='o' and self.Board[bottom_right[0]][bottom_right[1]] == '*' or 
						self.Board[y][x]=='o' and self.Board[bottom_left[0]][bottom_left[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_right[0]][top_right[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_left[0]][top_left[0]] == '*'):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=10+self.ScoreBoard[y][x]
				except IndexError:
					continue



				#next four is to esablish backup

				try:
					if(self.Board[top_right[0]][top_right[1]]=='*'):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=3+self.ScoreBoard[top_right[0]][top_right[1]]
				except IndexError:
					continue
				try:
					if(self.Board[top_left[0]][top_left[1]]=='*'):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=3+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue

				try:
					if(self.Board[bottom_right[0]][bottom_right[1]]=='*'):
						if(bottom_right[0]>=0 and bottom_right[1]>=0):
							current_score+=3+self.ScoreBoard[bottom_right[0]][bottom_right[1]]
				except IndexError:
					continue
				try:
					if(self.Board[bottom_left[0]][bottom_left[1]]=='*'):
						if(bottom_left[0]>=0 and bottom_left[1]>=0):
							current_score+=3+self.ScoreBoard[bottom_left[0]][bottom_left[1]]
				except IndexError:
					continue

				self.Board[old_position[0]][old_position[1]]="*"
				if(current_score>previous_score):
					previous_score=current_score
					previous_move=possible_move
					previous_old_position=old_position
				

		
		self.Board[previous_old_position[0]][previous_old_position[1]]=" "
		self.Board[previous_move[0]][previous_move[1]]=self.symbol
		print('\n')
		print("Computer Moved from "+ ','.join(str(x) for x in previous_old_position) + " to "+ ','.join(str(x) for x in previous_move))
		print('\n')






	def defensive(self,moves):
		previous_score=0
		previous_move=[0,0]
		previous_old_position=[]
		random.shuffle(moves)
		for pawn in moves:
			old_position=pawn[0]

			for possible_move in pawn[1]:
				
				y=possible_move[0]
				x=possible_move[1]
				top_right=y+1,x+1
				top_left=y+1,x-1
				bottom_right=y-1,x+1
				bottom_left=y-1,x-1
				forward_extra=y+1,x
				current_score=self.ScoreBoard[y][x]


				self.Board[old_position[0]][old_position[1]]=" "
				#for checking if there is a teamate on top right,top left...

				#if the enemy is on y-axis <=2 kill him 
				try:
					if(self.Board[y][x]=='o' and y<=2):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=110
				except IndexError:
					continue


				#----------------------------------------------


				#if you can win in 2 moves than do it
				try:
					if(self.Board[top_left[0]][top_left[1]]==' ' and self.Board[top_right[0]][top_right[1]]==' ' and y==6):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=1000+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue

				try:
					if(self.Board[top_left[0]][top_left[1]]=='o' and self.Board[top_right[0]][top_right[1]]=='o' 
						and self.Board[bottom_left[0]][bottom_left[1]]=='*' and self.Board[bottom_right[0]][bottom_right[1]]=='*' and y==6):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=100+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue

				try:
					if(self.Board[top_left[0]][top_left[1]]=='o' and self.Board[bottom_left[0]][bottom_left[1]]=='*' and self.Board[bottom_right[0]][bottom_right[1]]=='*' and y==6 or
						self.Board[top_right[0]][top_right[1]]=='o' and self.Board[bottom_left[0]][bottom_left[1]]=='*' and self.Board[bottom_right[0]][bottom_right[1]]=='*' and y==6):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=120+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue

				try:
					if(self.Board[top_left[0]][top_left[1]]=='o' and self.Board[bottom_left[0]][bottom_left[1]]=='*' and y==6 or
						self.Board[top_right[0]][top_right[1]]=='o' and self.Board[bottom_right[0]][bottom_right[1]]=='*' and y==6):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=120+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue




				#if you can win in your next move, than move there
				try:
					if(y==7):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=1000000
				except IndexError:
					continue
				#------------------------------------------------------

				try:
					if(self.Board[y][x]=='o'):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=3+self.ScoreBoard[y][x]
				except IndexError:
					continue


				try:
					if(self.Board[y][x]=='o' and self.Board[bottom_right[0]][bottom_right[1]] != '*' and self.Board[bottom_left[0]][bottom_left[0]] != '*'):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=5+self.ScoreBoard[y][x]
				except IndexError:
					continue


				try:
					if(self.Board[y][x]=='o' and self.Board[bottom_right[0]][bottom_right[1]] == '*' and self.Board[bottom_left[0]][bottom_left[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_left[0]][top_left[1]] == '*' and self.Board[top_right[0]][top_right[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_left[0]][top_left[1]] == '*' and self.Board[bottom_left[0]][bottom_left[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_left[0]][top_left[1]] == '*' and self.Board[bottom_right[0]][bottom_right[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_right[0]][top_right[1]] == '*' and self.Board[bottom_right[0]][bottom_right[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_right[0]][top_right[1]] == '*' and self.Board[bottom_left[0]][bottom_left[0]] == '*'):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=15+self.ScoreBoard[y][x]
				except IndexError:
					continue

				try:
					if(self.Board[y][x]=='o' and self.Board[bottom_right[0]][bottom_right[1]] == '*' or 
						self.Board[y][x]=='o' and self.Board[bottom_left[0]][bottom_left[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_right[0]][top_right[0]] == '*' or
						self.Board[y][x]=='o' and self.Board[top_left[0]][top_left[0]] == '*'):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=10+self.ScoreBoard[y][x]
				except IndexError:
					continue



				#next four is to esablish backup

				try:
					if(self.Board[top_right[0]][top_right[1]]=='*'):
						if(top_right[0]>=0 and top_right[1]>=0):
							current_score+=30+self.ScoreBoard[top_right[0]][top_right[1]]
				except IndexError:
					continue
				try:
					if(self.Board[top_left[0]][top_left[1]]=='*'):
						if(top_left[0]>=0 and top_left[1]>=0):
							current_score+=30+self.ScoreBoard[top_left[0]][top_left[1]]
				except IndexError:
					continue

				try:
					if(self.Board[bottom_right[0]][bottom_right[1]]=='*'):
						if(bottom_right[0]>=0 and bottom_right[1]>=0):
							current_score+=30+self.ScoreBoard[bottom_right[0]][bottom_right[1]]
				except IndexError:
					continue
				try:
					if(self.Board[bottom_left[0]][bottom_left[1]]=='*'):
						if(bottom_left[0]>=0 and bottom_left[1]>=0):
							current_score+=30+self.ScoreBoard[bottom_left[0]][bottom_left[1]]
				except IndexError:
					continue

				self.Board[old_position[0]][old_position[1]]="*"
				if(current_score>previous_score):
					previous_score=current_score
					previous_move=possible_move
					previous_old_position=old_position
				
				
		self.Board[previous_old_position[0]][previous_old_position[1]]=" "
		self.Board[previous_move[0]][previous_move[1]]=self.symbol
		print('\n')
		print("Computer Moved from "+ ','.join(str(x) for x in previous_old_position) + " to "+ ','.join(str(x) for x in previous_move))
		print('\n')

	def randomMovePlayer(self,moves):
		random_pawn=random.choice(moves)
		old_position=random_pawn[0]
		random_valid_move= random.choice(random_pawn[1])

		self.Board[old_position[0]][old_position[1]]=" "
		self.Board[random_valid_move[0]][random_valid_move[1]]=self.symbol
		print('\n')
		print("Computer Moved from "+ ','.join(str(x) for x in old_position) + " to "+ ','.join(str(x) for x in random_valid_move))
		print('\n')
	
	def move(self):
		moves=[]
		for x in range(len(self.Board)):
			for y in range(len(self.Board)):
				if self.Board[x][y]==self.symbol:
					valid_moves=self.comp_valid_moves([x,y])
					print(valid_moves)
					if valid_moves:
						moves.append([[x,y],valid_moves])
		if self.mode==1:
			self.randomMovePlayer(moves)
		elif self.mode==2:
			self.offensive(moves)
		else:
			self.defensive(moves)



		

	def comp_valid_moves(self,pawn_position):
		valid_moves=[]
		move_forward=[pawn_position[0]+1,pawn_position[1]]
		if self.Board[move_forward[0]][move_forward[1]]== ' ':
			valid_moves.append(move_forward)
		if pawn_position[1]-1 > 0:
			move_right_diagonal=[pawn_position[0]+1,pawn_position[1]-1]
			if self.Board[move_right_diagonal[0]][move_right_diagonal[1]]== ' ' or self.Board[move_right_diagonal[0]][move_right_diagonal[1]]== 'o' :
				valid_moves.append(move_right_diagonal)
		if pawn_position[1]+1 < self.num_cols:
			move_left_diagonal=[pawn_position[0]+1,pawn_position[1]+1]
			if self.Board[move_left_diagonal[0]][move_left_diagonal[1]]== ' ' or self.Board[move_left_diagonal[0]][move_left_diagonal[1]]== 'o' :
				valid_moves.append(move_left_diagonal)


		return valid_moves
	
	def updateBoard(self,board):
		self.Board=board[0]


def main():

	gameBoard=Board()
	gameBoard.createBoard()
	players=['Human','Comp']
	game_info=print("Welcome to our Breakthrough Game please select a computer player \nyou would like to play against: \n 1. random player\n 2. offensive player\n 3. defensive player")
	while True:
		game_mode=int(input("Please Enter 1 2 or 3 "))
		if int(game_mode) in [1,2,3]:
			break
		else:
			print("please select a valid game mode")
	whoStarts=random.choice(players)
	board=gameBoard.getBoards()
	human=HumanPlayer(board)
	comp=ComputerPlayer(board,game_mode)
	if whoStarts =='Human':
		player=human
	else:
		player=comp
	game=True
	while game:
		gameBoard.displayBoard()
		player.move()
		if player==human:
			player=comp
		else:
			player=human
		player.updateBoard(gameBoard.getBoards())
		if gameBoard.endofGame()=="Human player wins" or gameBoard.endofGame() == "Computer wins":
			game=False
			print(gameBoard.displayBoard)
			print(gameBoard.endofGame())




if __name__== "__main__":
  main()
