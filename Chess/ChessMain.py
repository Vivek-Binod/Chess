import pygame
import pygame as pg
import pygame.time

import ChessEngine, SmartMoveFinder

width=height=700
move_log_panel_width = 250
move_log_panel_height = height
dimension=8
sq_size=height//dimension
max_fps=15  #animation
images={}


#initialise a global dict of images.will be called exactly once

def loadImages():
    pieces=['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
    for piece in pieces:
        images[piece]=pg.transform.scale(pg.image.load("Images_SVG/"+piece+".svg"),(sq_size*2.5,sq_size*2.5))

#Main driver(handles user input and uploads graphics)

def main():
    pg.init()
    screen=pg.display.set_mode((width + move_log_panel_width,height),pg.RESIZABLE)
    clock=pg.time.Clock()
    screen.fill(pg.Color("white"))
    moveLogFont = pg.font.SysFont("Arial", 15, False, False)
    gs=ChessEngine.GameState()
    validMoves=gs.getValidMoves()
    moveMade=False #flag var for when move is made
    animate = False#flag var for when we should animate
    loadImages()
    running=True
    sqSelected=() #no sq selected initially
    playerClicks=[] #keep track of player clicks(2 tuples)
    gameOver = False
    playerOne = True #If human playing white then true, if AI playing false
    playerTwo = True #same as above but for black
    
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in pg.event.get():
            if e.type==pg.QUIT:
                running=False
            #mouse clicks handler
            elif e.type==pg.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:                   
                    location=pg.mouse.get_pos() #coor of mouse
                    col=location[0]//sq_size
                    row=location[1]//sq_size
                    if sqSelected==(row,col) or col >= 8: #if user clicks same square twice
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
                                # Handle promotion if it happened
                                if validMoves[i].isPawnPromotion:
                                    promoting = True
                                    while promoting:
                                        for ev in pg.event.get():
                                            if ev.type == pg.QUIT:
                                                pg.quit()
                                                exit()
                                            if ev.type == pg.KEYDOWN:
                                                if ev.key == pg.K_q:
                                                    gs.board[validMoves[i].endRow][validMoves[i].endCol] = validMoves[i].pieceMoved[0] + "Q"
                                                    promoting = False
                                                elif ev.key == pg.K_r:
                                                    gs.board[validMoves[i].endRow][validMoves[i].endCol] = validMoves[i].pieceMoved[0] + "R"
                                                    promoting = False
                                                elif ev.key == pg.K_b:
                                                    gs.board[validMoves[i].endRow][validMoves[i].endCol] = validMoves[i].pieceMoved[0] + "B"
                                                    promoting = False
                                                elif ev.key == pg.K_n:
                                                    gs.board[validMoves[i].endRow][validMoves[i].endCol] = validMoves[i].pieceMoved[0] + "N"
                                                    promoting = False
                                        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)
                                        pg.display.flip()
                                gs.moveLog[-1].isPawnPromotion = False  # clear flag after handling

                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []

                        if not moveMade:
                                playerClicks=[sqSelected]
            #key handlers
            elif e.type == pygame.KEYDOWN:
                if e.key == pg.K_z: #undo when  is pressed
                   gs.undoMove()
                   moveMade = True
                   animate = False
                   gameOver = False
                if e.key == pg.K_r: #reset board
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        #AI move finder
        if not gameOver and not humanTurn:
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            if AIMove.isPawnPromotion:
                AIMove.promotionChoice = 'Q'
            gs.makeMove(AIMove)
            moveMade = True
            animate = True


        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs ,validMoves, sqSelected, moveLogFont)
        if gs.checkMate or gs.staleMate:
            gameOver = True
            if gs.staleMate:
                text = 'Stalemate'
            else:
                if gs.whiteToMove:
                    text = 'Black wins by checkmate'
                else:
                    text = 'White wins by checkmate'

            drawEndGameText(screen, text)
        clock.tick(max_fps)
        pg.display.flip()

def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)  #draws squares
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen,gs.board)  #draws pieces on top of squares
    drawMoveLog(screen, gs, moveLogFont)


def drawBoard(screen):
    global colors
    colors=[pg.Color("white"),pg.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color=colors[((r+c)%2)]
            pg.draw.rect(screen,color,pg.Rect(c*sq_size,r*sq_size,sq_size,sq_size))



#Highlight square selected and moves for piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sq selected is a peice that can be moved
            #highlight selected sqaure
            s = pg.Surface((sq_size, sq_size))
            s.set_alpha(100) #transparency value
            s.fill(pg.Color('blue'))
            screen.blit(s, (c*sq_size, r*sq_size))
            #highlight moves from that square
            s.fill(pg.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sq_size, move.endRow*sq_size))


def drawPieces(screen,board):
    for r in range(dimension):
        for c in range(dimension):
            piece=board[r][c]
            if piece != "--":
                screen.blit(images[piece],pg.Rect(c*sq_size,r*sq_size,sq_size,sq_size))

def drawMoveLog(screen, gs, font):#draws movelog
    moveLogRect = pg.Rect(width, 0, move_log_panel_width, move_log_panel_height)
    pg.draw.rect(screen, pg.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i+1]) + "  "
        moveTexts.append(moveString)
    movesPerRow = 3
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i+j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True ,pg.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

#animating move
def animateMove(move, screen, board, clock):
    global colors
    coords = []#list of coords that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c= ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = pg.Rect(move.endCol * sq_size, move.endRow * sq_size, sq_size, sq_size)
        pg.draw.rect(screen, color, endSquare)
        if move.isEnpassantMove:
            captureRow = move.endRow + 1 if move.pieceMoved[0] == 'w' else move.endRow - 1
            captureSquare = pg.Rect(move.endCol * sq_size, captureRow * sq_size, sq_size, sq_size)
            screen.blit(images[move.pieceCaptured], captureSquare)
        elif move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(images[move.pieceMoved], pg.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
        pg.display.flip()
        clock.tick(60)

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # Kingside
                rookStartCol, rookEndCol = 7, move.endCol - 1
            else:  # Queenside
                rookStartCol, rookEndCol = 0, move.endCol + 1
            rookRow = move.endRow
            dRookC = rookEndCol - rookStartCol
            rookC = rookStartCol + dRookC * frame / frameCount
            rookPiece = 'wR' if move.pieceMoved[0] == 'w' else 'bR'
            screen.blit(images[rookPiece], pg.Rect(rookC * sq_size, rookRow * sq_size, sq_size, sq_size))

        # Draw the moving piece (king or any other)
        screen.blit(images[move.pieceMoved], pg.Rect(c * sq_size, r * sq_size, sq_size, sq_size))
        pg.display.flip()
        clock.tick(60)
        
def drawEndGameText(screen, text):
    font = pg.font.SysFont("Hevitca", 32, True, False)
    textObject = font.render(text, 0 ,pg.Color('Gray'))
    textLocation = pg.Rect(0, 0, width, height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pg.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

    
main()


