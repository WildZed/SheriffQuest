import random, sys, time, math, pygame
from pygame.locals import *
# Use common stuff from CandySeller until we've moved it into a Lib directory.

sys.path.append( '../GameEngine' )

from geometry import *
import viewport, game, game_map, game_dynamics
from game_objects import *
from game_constants import *


# Constants.

WINWIDTH = 800  # Width of the program's window, in pixels.
WINHEIGHT = 800 # Height in pixels.

BACKGROUND_COLOUR = (231, 211, 114)

MOVERATE = Vector( 17, 10 ) # How fast the player moves in the x and y direction.
BOUNCERATE = 6              # How fast the player bounces (large is slower).
BOUNCEHEIGHT = 10           # How high the player bounces.
COWBOYSIZE = 120            # How big the man is.




class SheriffQuest( game.Game ):
    def __init__( self, viewPort ):
        # set up generic game one time set up
        game.Game.__init__( self, 'Sheriff Quest', 'Sheriff Quest Icon', viewPort )

        # game one time setup
        self.setDrawOrder( 'Player' )
        self.setCursor()
        viewPort.loadMusic( 'Gun.ogg' )


    def loadImages( self ):
        images = self.images

        # L_COWBOY_IMG = pygame.image.load('Cowboy Carl.png')
        # R_COWBOY_IMG = pygame.transform.flip(L_COWBOY_IMG, True, False)
        # FWD_COWBOY_IMG = pygame.image.load('Cowboy Carl Forward.png')
        # BWD_COWBOY_IMG = pygame.image.load('Cowboy Carl Backward.png')

        # Might need to define a new ImageStore style Left Forward Backward Right.
        images.load( 'Cowboy Carl', 'RL' )
        images.load( 'Cowboy Carl Forward' )
        images.load( 'Cowboy Carl Backward' )
        # images.load( 'LFBR', 'Cowboy Carl', 'Cowboy Carl Forward', 'Cowboy Carl Backward' )
        # images.load( 'bush' )
        # images.load( 'ingredients store' )
        # images.load( 'jumpscare monster' )
        # images.load( 'money' )
        # images.load( 'shop', range( 1, 4 ) )
        # images.load( 'arrow', range( 1, 4 ) )


    # Per game initialisation.
    # game.Game calls this.
    def init( self ):
        self.winMode = False           # If the player has won.
        self.invulnerableMode = False  # If the player is invulnerable.
        self.invulnerableStartTime = 0 # Time the player became invulnerable.
        self.gameOverMode = False      # If the player has lost.
        self.gameOverStartTime = 0     # Time the player lost.
        # self.moneyScore = 0
        self.player = None

        game.Game.init( self )


    def initMap( self ):
        viewPort = self.viewPort
        gameMap = self.gameMap
        images = self.images

        gameMap.setImageStore( images )

        gameMap.createScene( 'Dusty Dunes', backGroundColour=BACKGROUND_COLOUR )

        # Create scene objects.

        # Start off with some shops on the screen.
        # self.createShops( gameMap )

        # Start off with some bushes on the screen.
        # gameMap.addObject( Bush( Point( -200, 400 ), images.bush, size=BUSHSIZE ) )
        # gameMap.addObject( Bush( Point( 928, 400 ), images.bush, size=BUSHSIZE ) )

        # Start off with some arrows on the screen.
        # self.createArrows( gameMap )

        # Start off with some money on the screen.
        # self.createCoins( gameMap, 4 )

        # gameMap.createScene( 'insideShop1', SHOP_FLOOR_COLOUR )
        # gameMap.changeScene( 'insideShop1' )
        # gameMap.addObject( BackGround( ORIGIN, images.ingredients_store, size=WINWIDTH ) )
        # self.createCoins( gameMap, 4 )
        #
        # gameMap.changeScene( 'shops' )
        #
        # gameMap.addOverlay( Score( Point( viewPort.width - 180, 20 ), self.moneyScore ) )

        self.player = self.createPlayer()
        gameMap.addObject( self.player )


    def createPlayer( self ):
        viewPort = self.viewPort
        images = self.images
        # How big the player starts off.
        playerStartPos = Point( viewPort.halfWidth, viewPort.halfHeight )

        # Sets up the movement style of the player.
        # playerBounds = game_dynamics.RectangleBoundary( Rectangle( Point( 0, 220 ), Point( 900, 550 ) ) )
        playerBounds = game_dynamics.CollisionBoundary()
        moveStyle = game_dynamics.KeyMovementStyle( boundaryStyle=playerBounds )
        moveStyle.setMoveRate( MOVERATE )
        moveStyle.setBounceRates( BOUNCERATE, BOUNCEHEIGHT )

        return Player( playerStartPos, moveStyle, size=COWBOYSIZE, ratio=1.0, positionStyle='centre',
                       imageL=images.Cowboy_CarlL, imageR=images.Cowboy_CarlR,
                       imageUp=images.Cowboy_Carl_Forward, imageDown=images.Cowboy_Carl_Backward )


    # Could move cursor description into a file and read from there.
    def setCursor( self ):
        thickarrow_strings = ( # sized 24x24
            "    XX                  ",
            "   X..X                 ",
            "  X....X                ",
            " X......X               ",
            "XXXXXXXXXX              ",
            "   X..X                 ",
            "   X..X                 ",
            "   X..X                 ",
            "   X..X                 ",
            "   XXXX                 ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ",
            "                        ")
        datatuple, masktuple = pygame.cursors.compile( thickarrow_strings,
                                      black='X', white='.', xor='o' )
        pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )


    def processEvent( self, event ):
        game.Game.processEvent( self, event )

        viewPort = self.viewPort
        gameMap = self.gameMap
        player = self.player

        if event.type == KEYDOWN:
            # Check if the key moves the player in a given direction.
            player.setMovement( key=event.key )

            if event.key == K_r and self.winMode:
                self.running = False
            # elif event.key is K_q:
            #     # Releases the jumpscare if you press 'q'.
            #     viewPort.playSound( "Jumpscare V2" )
            #     monster = self.createMonster()
            #     gameMap.addSprite( monster )
        elif event.type == KEYUP:
            # Check if the key stops the player in a given direction.
            player.stopMovement( key=event.key )

            # if event.key is K_q:
            #     gameMap.deleteAllObjectsOfType( 'Monster' )
            # elif event.key is K_i:
            #     viewPort.resetCamera()
            #     player.pushPos( Point( viewPort.halfWidth, viewPort.halfHeight ), offsetOldPos=Point( 0, 20 ) )
            #     gameMap.changeScene( 'insideShop1' )
            # elif event.key is K_o:
            #     player.popPos()
            #     gameMap.changeScene( 'shops' )
        elif event.type == MOUSEBUTTONUP:
            pass
            # if None is self.dragPos:
            #     arrow = gameMap.objectsOfType( 'Arrow' )[0]
            #
            #     # Does the click point collide with a colour that is not the background colour.
            #     if viewPort.collisionOfPoint( self.clickPos, arrow ):
            #         viewPort.playSound( 'Money Ping' )


    def updateState( self ):
        game.Game.updateState( self )

        if self.gameOverMode:
            return

        viewPort = self.viewPort
        gameMap = self.gameMap
        player = self.player

        # Adjust camera if beyond the "camera slack".
        playerCentre = Point( player.x + int( ( float( player.size ) + 0.5 ) / 2 ), player.y + int( ( float( player.size ) + 0.5 ) / 2 ) )
        viewPort.adjustCamera( playerCentre )


    # Update the positions of all the map objects according to the camera and new positions.
    def updateMap( self ):
        # Update the generic map stuff.
        game.Game.updateMap( self )

        viewPort = self.viewPort
        gameMap = self.gameMap
        player = self.player

        # Update the player man.
        player.update( viewPort.camera, gameOverMode=self.gameOverMode, invulnerableMode=self.invulnerableMode )


    def run( self ):


        game.Game.run( self )


# Move image stuff into loadImages.
# Game control is already in game.Game.
# def main():
#     global L_COWBOY_IMG, R_COWBOY_IMG, FWD_COWBOY_IMG, BWD_COWBOY_IMG
#
#     pygame.init()
#     FPSCLOCK = pygame.time.Clock()
#     pygame.display.set_icon(pygame.image.load('Sheriff Quest Icon.png'))
#     DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
#     pygame.display.set_caption('Sheriff Quest')
#     BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
#
#     # load the image files
#     L_COWBOY_IMG = pygame.image.load('Cowboy Carl.png')
#     R_COWBOY_IMG = pygame.transform.flip(L_COWBOY_IMG, True, False)
#     FWD_COWBOY_IMG = pygame.image.load('Cowboy Carl Forward.png')
#     BWD_COWBOY_IMG = pygame.image.load('Cowboy Carl Backward.png')


# def runGame():
#     # set up variables for the start of a new game
#
#     # camera is the top left of where the camera view is
#     camera = Point( 0, 0  )
#
#     thickarrow_strings = (               #sized 24x24
#         "    XX                  ",
#         "   X..X                 ",
#         "  X....X                ",
#         " XXXXXXXX               ",
#         "    XX                  ",
#         "    XX                  ",
#         "    XX                  ",
#         "    XX                  ",
#         "    XX                  ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ",
#         "                        ")
#     datatuple, masktuple = pygame.cursors.compile( thickarrow_strings,
#                                   black='X', white='.', xor='o' )
#     pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )
#
#
#     # stores the player object:
#     playerObj = {'surface': pygame.transform.scale(L_COWBOY_IMG, (STARTSIZE, STARTSIZE)),
#                  'facing': LEFT,
#                  'size': STARTSIZE,
#                  'x': HALF_WINWIDTH,
#                  'y': HALF_WINHEIGHT,
#                  'bounce':0}
#
#     while True: # main game loop
#
#         # draw the sandy background
#         DISPLAYSURF.fill( BACKGROUND_COLOUR )
#
#         # draw the player cowboy
#         drawPlayer( camera, playerObj )
#
#
# def adjustCamera( camera, playerCentre ):
#     if ( camera.x + HALF_WINWIDTH ) - playerCentre.x > CAMERASLACK:
#         camera.x = playerCentre.x + CAMERASLACK - HALF_WINWIDTH
#     elif playerCentre.x - ( camera.x + HALF_WINWIDTH ) > CAMERASLACK:
#         camera.x = playerCentre.x - CAMERASLACK - HALF_WINWIDTH
#
#     if ( camera.y + HALF_WINHEIGHT ) - playerCentre.y > CAMERASLACK:
#         camera.y = playerCentre.y + CAMERASLACK - HALF_WINHEIGHT
#     elif playerCentre.y - ( camera.y + HALF_WINHEIGHT ) > CAMERASLACK:
#         camera.y = playerCentre.y - CAMERASLACK - HALF_WINHEIGHT
#
#
# def drawPlayer( camera, playerObj ):
#
#     playerObj['rect'] = pygame.Rect( ( playerObj['x'] - camera.x,
#                                        playerObj['y'] - camera.y - getBounceAmount( playerObj['bounce'], BOUNCERATE, BOUNCEHEIGHT ),
#                                        playerObj['size'],
#                                        playerObj['size'] ) )
#     DISPLAYSURF.blit( playerObj['surface'], playerObj['rect'] )


def main():
    viewPort = viewport.ViewPort( WINWIDTH, WINHEIGHT )
    game = SheriffQuest( viewPort )

    while True:
        game.run()
        # Re-initialised the game state.
        game.reset()


if __name__ == '__main__':
    main()
