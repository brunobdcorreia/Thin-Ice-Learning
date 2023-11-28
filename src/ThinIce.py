'''
Name: Victor Li
Date: 5/7/2020
Description: Pygame remake of Club Penguin's Thin-ice
'''

# Import classes used for the game
from data.classes.sprites import *
from sys import exit
class Game():
    '''This class defines the main game'''

    def __init__(self):
        '''This initializer defines the caption and windows and starts up the game engine config'''
        
        # Starts up the game and the audio
        pg.init()
        pg.mixer.init()
        
        # Set title and icon
        pg.display.set_caption("Thin-Ice!")
        pg.display.set_icon(pg.image.load('data/images/icon.png'))
        
        # Allows to hold down input keys
        pg.key.set_repeat(200, 175)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        

    def loadData(self):
        '''This method loads data from files outside of Python'''
        self.playerSpriteSheet = Spritesheet(PLAYERSPRITE, PLAYERXML)
        self.waterSpriteSheet = Spritesheet(WATERSPRITE, WATERXML)
        self.keySpriteSheet = Spritesheet(KEYSPRITE, KEYXML)
        self.teleporterSpriteSheet = Spritesheet(TELEPORTERSPRITE, TELEPORTERXML)
        
        # Loads the Background music
        pg.mixer.music.load('data/sound/music.ogg')
        pg.mixer.music.set_volume(0.1)
        
        # Sound effect when a player moves
        self.moveSound = pg.mixer.Sound("data/sound/move.ogg")
        self.moveSound.set_volume(0.1)
        
        # Sound effect when a player finishs a level completely
        self.allTileComplete = pg.mixer.Sound("data/sound/allTileComplete.ogg")
        self.allTileComplete.set_volume(0.2)

        # Sound effect when a player dies
        self.deadSound = pg.mixer.Sound("data/sound/dead.ogg")
        self.deadSound.set_volume(0.2)

        # Sound effect when a player touches a treasure bag
        self.treasureSound = pg.mixer.Sound("data/sound/treasure.ogg")
        self.treasureSound.set_volume(0.2)

        # Sound effect when a player moves away from an ice tile
        self.iceBreakSound = pg.mixer.Sound("data/sound/breakIce.ogg")
        self.iceBreakSound.set_volume(0.2)
        
        # Sound effect when a player touches a key or unlocks a key socket
        self.keyGet = pg.mixer.Sound("data/sound/keyGet.ogg")
        self.keyGet.set_volume(0.2)

        # Sound effect when a player is resetted to the start
        self.resetSound = pg.mixer.Sound("data/sound/reset.ogg")
        self.resetSound.set_volume(0.2)
        
        # Sound effect when a player hits a moving block
        self.movingBlockSound = pg.mixer.Sound("data/sound/movingBlockSound.ogg")
        self.movingBlockSound.set_volume(0.2)
        
        # Sound effect when a player teleports
        self.teleportSound = pg.mixer.Sound("data/sound/teleportSound.ogg")
        self.teleportSound.set_volume(0.2)
        

    # Adicionar depois a seleção de níveis
    def loadMap(self, level_number=None):
        '''Load the current level by reading a parameter '''
        
        #Resets the map-related variables
        mapData = []
        totalFree = 0
        
        # Opens the file and appends all the data to mapData
        level_to_load = self.currentLevel if level_number is None else level_number
        fileName = f"data/maps/level{level_to_load}.txt" 
        currentMap = open(fileName, "r")
        for line in currentMap:
            mapData.append(line)
        
        
        # Generates the map based on the text file    
        for row, tiles in enumerate(mapData):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                elif tile == '0':
                    Unused(self, col, row)
                elif tile == 'F':
                    Free(self, col, row)
                    totalFree += 1
                elif tile == 'E':
                    self.endTile = End(self, col, row)
                elif tile == 'I':
                    Ice(self, col, row)
                    totalFree +=2
                elif tile == 'K':
                    Free(self, col, row)
                    self.key = GoldenKey(self, col, row)
                    totalFree +=1
                elif tile == 'B':
                    self.movingBlockTile = MovingBlockTile(self, col, row)
                elif tile == 'T':
                    Free(self, col, row)
                    self.movingBlock = MovingBlock(self, col, row)     
                    totalFree += 1
                elif tile == '%':
                    # exclusive tile only used for level 14,15,16
                    Ice(self, col, row)
                    self.movingBlock = MovingBlock(self,col,row)
                    totalFree += 2
                elif tile == '&':
                    # exclusive tile only used for level 15
                    self.movingBlockTile = MovingBlockTile(self, col, row)
                    self.key = GoldenKey(self, col, row)
                elif tile == '!':
                    # exclusive tile only used for level 16
                    Ice(self, col, row)
                    self.key = GoldenKey(self, col, row)
                    totalFree += 2
                elif tile == '1':
                    # teleporter 1
                    self.firstTeleporter = Teleporter(self, col, row)
                elif tile == '2':
                    # teleporter 2
                    self.secondTeleporter = Teleporter(self, col, row)
                elif tile == 'H':
                    self.keyHole = KeyHole(self, col, row)
                    totalFree += 1
                elif tile == 'M':
                    Free(self, col, row)
                    if (self.lastLevelSolved):
                        self.treasureTile = Treasure(self, col, row)
                    totalFree += 1
                elif tile == 'P':
                    Free(self, col, row)
                    self.player.movetoCoordinate(col,row)
                    totalFree += 1
        
        # subtracting the top row and bottom row free because they're meant for the menu lol            
        self.scoreKeeperTop.totalTiles = (totalFree - (2 * 19))
        self.scoreKeeperTop.completeTiles = 0
        # update current level number
        self.scoreKeeperTop.currentLevel = self.currentLevel

        return mapData
        
    


    def new(self, start_level=1):
        '''This method initializes all the variables and sets up the game '''
        
        # Loads external data
        self.loadData()
        
        # Creates the groups used for event handling later on
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.movable = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.iceSprites = pg.sprite.Group()
        self.scoreSprites = pg.sprite.Group()
        self.updatingBlockGroup = pg.sprite.Group()
        self.noWaterGroup = pg.sprite.Group()
        
        # Currents the player sprite before the map loading
        self.player = Player(self, 0, 0)
        
        # Clock used to set the frame rate
        self.clock = pg.time.Clock()
        
        # Contains the end point of each level for event handling
        self.endTile = object()
        
        # Tells where to move the moving block later
        self.movingBlockTile = object()
        
        # Checks if player can open a key socket
        self.hasKey = False

        # Checks if player has reset once on the map
        self.resetOnce = False
        
        # Checks if the player has moved successfully
        self.moved = False
        
        # Contains the current level of the game
        self.currentLevel = 1
        
        # Lets game remember last level you solved it
        self.lastLevelSolved = True
        
        # Checks if the moving block is moving
        self.blockIsMoving = False
        
        # Checks if the player can still teleport
        self.canTeleport = True            
        
        self.scoreKeeperTop = ScoreKeeperTop(self)
        self.scoreKeeperBottom = ScoreKeeperBottom(self)
        self.resetButton = Button(self, "reset", 65, HEIGHT - 13, 72, 21)
        
        # Load the map
        m = self.loadMap(start_level)
        
        # Plays and infinitely loops the music
        pg.mixer.music.play(-1)

        return m
        

    def run(self, action):
        '''This method is the game loop which runs most of the game '''
        self.clock.tick(FPS)
        state = self.events(action)
        self.update()
        self.draw()
        return state
            
            
    def update(self):
        '''This method updates all classes/objects as part of the game loop '''
        self.allSprites.update()
        self.scoreSprites.update()
    

    def deleteMap(self):
        '''This method deletes all tiles in the current level '''
        for tiles in self.allSprites:
            tiles.kill()
            

    def playResetSounds(self):
        '''This method plays the relevant sounds when you reset or when you die '''
        self.deadSound.play()
        self.resetSound.play()        

               
    def reset(self):
        ''' This method resets the current level '''
        
        # Empty out the map and reload the map
        self.deleteMap()
        self.loadMap()
        
        # Reset the score to 0 or to previous level
        self.scoreKeeperBottom.score = self.scoreKeeperBottom.previousScore
        
        # Reset key status
        self.hasKey = False
        
        # Reset teleporter status
        self.canTeleport = True
        
        # Tells the game the player reset once
        self.resetOnce = True
        
    
    def nextLevel(self):
        ''' This method moves the player to the next level '''
        
        #Updates variables
        self.resetOnce = False
        self.currentLevel += 1
        
        if self.currentLevel == 20:
            # Finish the game
            self.quit()
        
        # Empty out the map and load new map
        self.deleteMap()
        self.loadMap()
        
        # Reset key status
        self.hasKey = False
        
        # Reset teleporter status
        self.canTeleport = True


    def draw(self):
        '''This method draws all the sprites onto the screen '''
        self.allSprites.draw(self.screen)
        self.scoreSprites.draw(self.screen)
        self.updatingBlockGroup.draw(self.screen)
        pg.display.flip()


    def events(self, action):
        '''This method handles the event handling'''
        # CONTROLS
        if action == 'up':
            self.player.checkAndMove(dy=-1)
        elif action == 'down':
            self.player.checkAndMove(dy=1)
        elif action == 'left':
            self.player.checkAndMove(dx=-1)
        elif action == 'right':
            self.player.checkAndMove(dx=1)        
        elif action == 'stay':
            pass

        x_pos = self.player.x
        y_pos = self.player.y
        reward = 0
        moved = self.moved
        death = self.player.checkDeath() if not self.player.collideWithTile(self.endTile) else False
        level = self.currentLevel
        score = self.scoreKeeperBottom.score
        solved = self.player.collideWithTile(self.endTile)
        is_there_key = self.currentLevel > KEYLEVEL
        haskey = self.hasKey
               
        #If player moved, check if he's on the finish line
        if self.moved:
            # Update the scorekeepers
            self.scoreKeeperTop.completeTiles += 1
            self.scoreKeeperBottom.score += 1
            
            # Check if player touched the finish line yet
            if self.player.collideWithTile(self.endTile):
                
                # Checks if bonus score can be applied
                if self.scoreKeeperTop.checkFinish():
                    
                    # Lets game remember last level you solved it
                    self.lastLevelSolved = True
                    
                    # Plays the bonus sound effect
                    self.allTileComplete.play()
                    
                    # Increase the number of solved by 1
                    self.scoreKeeperTop.solvedLevels += 1  
                    
                    # Gives x2 bonus score if no reset/death, otherwise give the normal score
                    if not self.resetOnce:
                        self.scoreKeeperBottom.score += self.scoreKeeperTop.totalTiles * 2
                    else:
                        self.scoreKeeperBottom.score += self.scoreKeeperTop.totalTiles
                    
                
                # Remind game player didn't solve last level    
                else:
                    self.lastLevelSolved = False
                
                # Sets the previous score for the next level
                self.scoreKeeperBottom.previousScore = self.scoreKeeperBottom.score
                
                # Update the total number of tiles the player melted overall in the game so far
                self.scoreKeeperTop.playerMelted += self.scoreKeeperTop.completeTiles
                
                # Go to the next level
                self.nextLevel()
                
            
            # If treasure bag exists, check if player touched treasure bag, treasure only appears after level 3 in original game
            elif self.lastLevelSolved and self.currentLevel > TREASURELEVEL:
                if  self.player.collideWithTile(self.treasureTile):
                    self.treasureTile.kill()
                    self.treasureSound.play()
                    self.scoreKeeperBottom.score += 100
            
            # Check if player touches key, only appears after level 9 in the original game        
            if self.currentLevel > KEYLEVEL:
                if self.player.collideWithTile(self.key):
                    # Lets player open key sockets now
                    self.key.kill()
                    self.keyGet.play()
                    self.hasKey = True
            
            
            # If the player currently has the key, check if he's in the radius of the keyhole
            if self.hasKey:
                if self.player.nearTile(self.keyHole) != 0:
                    #Delete the keyhole and replace with a free tile
                    Free(self, self.keyHole.x, self.keyHole.y)
                    self.keyGet.play()
                    self.keyHole.kill()
                    self.hasKey = False
                    
            # Checks if the player is able to teleport, only after level 16
            if self.currentLevel > TELEPORTLEVEL:
                    # Teleports to you to the other teleporter, make sure not to add score as well
                    if self.player.collideWithTile(self.firstTeleporter):
                        self.scoreKeeperTop.completeTiles -= 1
                        self.scoreKeeperBottom.score -= 1
                        
                        if self.canTeleport:
                            self.player.movetoCoordinate(self.secondTeleporter.x, self.secondTeleporter.y)
                            self.canTeleport = False

                            self.teleportSound.play()
                        
                    elif self.player.collideWithTile(self.secondTeleporter):
                        self.scoreKeeperTop.completeTiles -= 1
                        self.scoreKeeperBottom.score -= 1
                        
                        if self.canTeleport:
                            self.player.movetoCoordinate(self.firstTeleporter.x, self.firstTeleporter.y)
                            self.canTeleport = False

                            self.teleportSound.play()
                                                    
            # If the player collided with the moving block tile, don't add score
            if self.currentLevel > MOVINGBLOCKLEVEL and self.player.collideWithTile(self.movingBlockTile):
                self.scoreKeeperTop.completeTiles -= 1
                self.scoreKeeperBottom.score -= 1        
            
            # Checks if the player is unable to move anymore, continued
            # explaination in Player class
            if self.player.checkDeath():
                # Play death animation and sounds and reset the map when hitting the button
                self.player.setFrame(DYING)
                self.playResetSounds()            
                        
            # Reset moved variable
            self.moved = False

        # return [x_pos, y_pos, reward, moved, death, level, score, solved, is_there_key, haskey]
        return [x_pos, y_pos, moved, death, solved, level]

    def reset_game(self):
        self.reset()
        self.player.setFrame(RESETTING)
        self.playResetSounds()
