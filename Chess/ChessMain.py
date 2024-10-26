import pygame
import pygame as pg
import pygame.time

from Chess import ChessEngine

pg.init()
screen_info=pg.display.Info()
screen_width,screen_height=screen_info.current_w,screen_info.current_h
board_size=int(min(screen_width,screen_height)*0.91)
width=height=board_size
dimension=8
sq_size=board_size//dimension
max_fps=15  #animation
images={}
screen=pg.display.set_mode((board_size,board_size))

#initialise a global dict of images.will be called exactly once

def loadImages():
    pieces=['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
    for piece in pieces:
        images[piece]=pg.transform.scale(pg.image.load("Images_SVG/"+piece+".svg"),(sq_size*2.5,sq_size*2.5))

#Main driver(handles user input and uploads graphics)

def main():
    screen=pg.display.set_mode((width,height),pg.RESIZABLE)
    clock=pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs=ChessEngine.GameState()
    validMoves=gs.getValidMoves()
    moveMade=False #flag var for when move is made
    loadImages()
    running=True
    sqSelected=() #no sq selected initially
    playerClicks=[] #keep track of player clicks(2 tuples)

    while running:
        for e in pg.event.get():
            if e.type==pg.QUIT:
                running=False
            #mouse clicks handler
            elif e.type==pg.MOUSEBUTTONDOWN:
                location=pg.mouse.get_pos() #coor of mouse
                col=location[0]//sq_size
                row=location[1]//sq_size
                if sqSelected==(row,col): #if user clicks same square twice
                    sqSelected=() #deselect
                    playerClicks=[] #basically restarts turn
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #appending 1st and 2nd clicks
                if len(playerClicks)==2: #after 2nd click
                    move=ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade=True
                            sqSelected=() #reset user clicks
                            playerClicks=[]
                    if not moveMade:
                            playerClicks=[sqSelected]
            #key handlers
            elif e.type==pygame.KEYDOWN:
                if e.key==pg.K_z: #undo when  is pressed
                   gs.undoMove()
                   moveMade=True
        if moveMade:
            validMoves=gs.getValidMoves()
            moveMade=False

        drawGameState(screen,gs)
        clock.tick(max_fps)
        pg.display.flip()


def drawGameState(screen,gs):
    drawBoard(screen)  #draws squares
    drawPieces(screen,gs.board)  #draws pieces on top of squares

def drawBoard(screen):
    colors=[pg.Color("white"),pg.Color("purple")]
    for r in range(dimension):
        for c in range(dimension):
            color=colors[((r+c)%2)]
            pg.draw.rect(screen,color,pg.Rect(c*sq_size,r*sq_size,sq_size,sq_size))


def drawPieces(screen,board):
    for r in range(dimension):
        for c in range(dimension):
            piece=board[r][c]
            if piece != "--":
                screen.blit(images[piece],pg.Rect(c*sq_size,r*sq_size,sq_size,sq_size))



main()


