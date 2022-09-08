import pygame
import sys
import os
import math
from random import choice

pygame.init()
WIDTH = 1000
HEIGHT = 700


def gradient(col1, col2, surface):
    col1 = col1.copy()
    col2 = col2.copy()
    height = surface.get_height()
    inc1 = (col2[0] - col1[0])/height
    inc2 = (col2[1] - col1[1])/height
    inc3 = (col2[2] - col1[2])/height
    color = col1
    for i in range(height):
        pygame.draw.line(surface, color, (0,i), (surface.get_width(),i),1)
        color[0] += inc1
        color[1] += inc2
        color[2] += inc3

def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)

def clampColor(val):
    if val > 255:
        val = 255
    if val < 0:
        val = 0
    return int(val)

def convertRect(rectTuple):
    newRect = rectTuple
    return pygame.Rect(WIDTH/100*newRect[0], HEIGHT/100*newRect[1], WIDTH/100*newRect[2], HEIGHT/100*newRect[3])

class Colors:
    col1 = [0,0,0]
    col2 = [237, 87, 82]
    col3 = [255,255,255]
    col4 = [214, 233, 252]
    col5 = [146, 170, 199]

    textCol = col3.copy()
    bgCol1 = col1.copy()
    bgCol2 = col1.copy()
    buttonCol1 = col4.copy()
    buttonCol2 = col5.copy()
    accentCol = col2.copy()

class Surf:
    surface = None

class Fonts:
    WIDTH = WIDTH
    HEIGHT = HEIGHT
    fonts = {
        "title": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/14), bold=False, italic=False),
        "subtitle": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/20), bold=False, italic=False),
        "paragraph": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/26), bold=False, italic=False),
        "button": pygame.font.Font(resource_path("font.ttf"), int(WIDTH/54), bold=False, italic=False)
    }

    def resizeFonts(screen):
        Fonts.WIDTH = screen.get_width()
        Fonts.fonts = {
            "title": pygame.font.Font(resource_path("font.ttf"), int(Fonts.WIDTH/14), bold=False, italic=False),
            "subtitle": pygame.font.Font(resource_path("font.ttf"), int(Fonts.WIDTH/20), bold=False, italic=False),
            "paragraph": pygame.font.Font(resource_path("font.ttf"), int(Fonts.WIDTH/26), bold=False, italic=False),
            "button": pygame.font.Font(resource_path("font.ttf"), int(Fonts.WIDTH/54), bold=False, italic=False)
        }

class Text:
    texts = []
    def __init__(self, text, font, color, position, centered, underline = False) -> None:
        self.content = str(text)
        self.fontSize = font
        self.font = Fonts.fonts[font]
        self.color = color
        self.pos = position
        self.centered = centered
        self.text = self.font.render(self.content, True, self.color)
        self.rect = pygame.Rect(0,0,0,0)
        Text.texts.append(self)
        self.underline = underline

    def resize(self):
        self.font = Fonts.fonts[self.fontSize]
        self.text = self.font.render(self.content, True, self.color)

    def reset(self, color, content):
        self.color = color
        self.content = content
        self.font = Fonts.fonts[self.fontSize]
        self.text = self.font.render(self.content, True, self.color)

    def draw(self, surface):
        if self.centered:
            self.rect = pygame.Rect(surface.get_width()/100*self.pos[0]-self.text.get_width()/2, surface.get_height()/100*self.pos[1], self.text.get_width(), self.text.get_height())
            surface.blit(self.text, (surface.get_width()/100*self.pos[0]-self.text.get_width()/2, surface.get_height()/100*self.pos[1]))
            if self.underline:
                smallMargin = surface.get_width()/100*3
                xCoord1 = surface.get_width()/100*(self.pos[0])-self.text.get_width()/2 + smallMargin
                xCoord2 = xCoord1 + self.text.get_width() - 2*smallMargin
                yCoord = surface.get_height()/100 * (self.pos[1]) + self.text.get_height()
                pygame.draw.line(surface, Colors.accentCol, (xCoord1, yCoord), (xCoord2, yCoord), 5)
        else:
            self.rect = pygame.Rect(surface.get_width()/100*self.pos[0], surface.get_height()/100*self.pos[1], self.text.get_width(), self.text.get_height())
            surface.blit(self.text, (surface.get_width()/100*self.pos[0], surface.get_height()/100*self.pos[1]))
            if self.underline:
                smallMargin = surface.get_width()/100*3
                xCoord1 = surface.get_width()/100*(self.pos[0]) + smallMargin
                xCoord2 = xCoord1 + self.text.get_width() - 2*smallMargin
                yCoord = surface.get_height()/100 * (self.pos[1]+1) + self.text.get_height()
                pygame.draw.line(surface, Colors.accentCol, (xCoord1, yCoord), (xCoord2, yCoord), 5)

    def checkMouseOver(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True

    def resizeAll(surface):
        Fonts.resizeFonts(surface)
        for text in Text.texts:
            text.resize()

class Button:
    buttons = []
    def __init__(self, text, rect, cornerRadius, textColor=Colors.textCol, gradCol1=Colors.buttonCol1, gradCol2=Colors.buttonCol2, onclickFunc=None, altImage=None) -> None:
        if altImage == None:
            self.unconvertedRect: pygame.Rect = rect
            self.rect = convertRect((self.unconvertedRect.x, self.unconvertedRect.y, self.unconvertedRect.width, self.unconvertedRect.height))
            self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        else:
            self.unconvertedRect = pygame.Rect(rect.x, rect.y, altImage.get_width(), altImage.get_height())
            self.rect = convertRect((self.unconvertedRect.x, self.unconvertedRect.y, self.unconvertedRect.width, self.unconvertedRect.height))
            self.rect.width, self.rect.height = altImage.get_size()
            self.surface = altImage
        self.hoverSurface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.textContent = text
        self.textColor = textColor
        self.cornerRadius = cornerRadius
        self.gradCol1 = gradCol1
        self.gradCol2 = gradCol2
        self.hovering = False
        self.onClickFunc = onclickFunc
        self.altImage = altImage
        self.drawImage(self.gradCol1, self.gradCol2, self.textColor, self.surface)
        self.drawImage(self.darken(self.gradCol1, .9), self.darken(self.gradCol2, .9), self.darken(self.textColor, .9), self.hoverSurface)
        self.resizedSurface = pygame.transform.scale(self.surface, (self.rect.width, self.rect.height))
        self.resizedHoverSurface = pygame.transform.scale(self.hoverSurface, (self.rect.width, self.rect.height))

        Button.buttons.append(self)

    def drawImage(self, gradCol1, gradCol2, textCol, surface):
        if self.altImage == None:
            color = gradCol1.copy()
            inc1 = (gradCol2[0] - gradCol1[0])/(self.rect.height - self.cornerRadius)
            inc2 = (gradCol2[1] - gradCol1[1])/(self.rect.height - self.cornerRadius)
            inc3 = (gradCol2[2] - gradCol1[2])/(self.rect.height - self.cornerRadius)
            for i in range(self.rect.height - self.cornerRadius):
                pygame.draw.rect(surface, color, pygame.Rect(0, i, self.rect.width, self.cornerRadius), border_radius=self.cornerRadius)
                color[0] += inc1
                color[1] += inc2
                color[2] += inc3
        text = Fonts.fonts["button"].render(self.textContent, True, textCol)
        surface.blit(text, (surface.get_width()/2-text.get_width()/2, surface.get_height()/2-text.get_height()/2))

    def darken(self, color, val):
        newCol = color.copy()
        newCol = [clampColor(newCol[0] * val), clampColor(newCol[1] * val), clampColor(newCol[2] * val)]
        return newCol

    def draw(self, surface):
        if self.hovering == False:
            surface.blit(self.resizedSurface, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.resizedHoverSurface, (self.rect.x, self.rect.y))

    def checkMouseOver(self, pos):
        if self.rect.collidepoint(pos):
            return True

    def resize(self, surface):
        self.rect = convertRect(surface, (self.unconvertedRect.x, self.unconvertedRect.y, self.unconvertedRect.width, self.unconvertedRect.height))
        self.resizedSurface = pygame.transform.scale(self.surface, (self.rect.width, self.rect.height))
        self.resizedHoverSurface = pygame.transform.scale(self.hoverSurface, (self.rect.width, self.rect.height))

class Item:
    def __init__(self, imageName: str, pos: tuple) -> None:
        if imageName != None:
            self.image = pygame.image.load("imgs/" + imageName + ".png")
        else:
            self.image = pygame.image.load("imgs/peeJar.png")
        self.pos: tuple = pos
        self.rect = pygame.Rect(0,0,0,0)
    
    def checkClick(self, pos):
        if self.rect.collidepoint(pos):
            return True

    def draw(self, surface: pygame.Surface):
        self.rect = pygame.Rect(WIDTH/100*self.pos[0], HEIGHT/100*self.pos[1], WIDTH/195*self.image.get_width(), HEIGHT/147*self.image.get_height())
        surface.blit(self.image, (surface.get_width()/100*self.pos[0], surface.get_height()/100*self.pos[1]))

class Medicine(Item):
    def __init__(self, imageName: str, miniImgName: str, pos: tuple) -> None:
        super().__init__(imageName, pos)
        if miniImgName != None:
            self.miniImg = pygame.image.load("imgs/" + miniImgName + ".png")
            self.miniImg = pygame.transform.scale(self.miniImg, (WIDTH/195*self.miniImg.get_width(), HEIGHT/147*self.miniImg.get_height()))
        else:
            self.miniImg = pygame.image.load("imgs/eyeMini.png")
        self.isClickedOn : bool = False

class Light(Item):
    def __init__(self, imageName: str, pos: tuple) -> None:
        super().__init__(imageName, pos)
        # add the little flames and maybe the ring of light too

class Cauldron(Item):
    brewColors = [
        "red",
        "orange",
        "yellow",
        "green",
        "lightBlue",
        "blue"
    ]

    potionBlobs = {
        "red" : pygame.transform.scale(pygame.image.load("imgs/redPotionBlob.png"), (WIDTH/195*6, HEIGHT/147*6)),
        "orange" : pygame.transform.scale(pygame.image.load("imgs/orangePotionBlob.png"), (WIDTH/195*6, HEIGHT/147*6)),
        "yellow" : pygame.transform.scale(pygame.image.load("imgs/yellowPotionBlob.png"), (WIDTH/195*6, HEIGHT/147*6)),
        "green" : pygame.transform.scale(pygame.image.load("imgs/greenPotionBlob.png"), (WIDTH/195*6, HEIGHT/147*6)),
        "lightBlue" : pygame.transform.scale(pygame.image.load("imgs/lightBluePotionBlob.png"), (WIDTH/195*6, HEIGHT/147*6)),
        "blue" : pygame.transform.scale(pygame.image.load("imgs/bluePotionBlob.png"), (WIDTH/195*6, HEIGHT/147*6))
    }

    def __init__(self, imageName: str, pos: tuple) -> None:
        super().__init__(imageName, pos)
        self.itemsInCauldron = []
        self.image = pygame.transform.scale(self.image, (WIDTH/195*self.image.get_width(), HEIGHT/147*self.image.get_height()))
        self.animations = {
            "idle" : [],
            "splash" : [],
            "brew" : []
        }
        self.currentAnimation = "idle"
        self.isBrewed = False
        self.brewColor = None

    def splash(self):
        self.currentAnimation = "splash"

    def brew(self):
        print("yeee!!!")
        self.currentAnimation = "brew"
        self.isBrewed = True
        self.brewColor = choice(Cauldron.brewColors)

    
    def checkCanBrew(self):
        if len(self.itemsInCauldron) > 1 and not self.isBrewed:
            self.brew()

    def draw(self, surface: pygame.Surface):
        self.rect = pygame.Rect(WIDTH/100*self.pos[0], HEIGHT/100*self.pos[1], self.image.get_width(), self.image.get_height()/3)
        surface.blit(self.image, (surface.get_width()/100*self.pos[0], surface.get_height()/100*self.pos[1]))
        #### implement the animations.
        # for i in range(len(self.itemsInCauldron)):
        #     surface.blit(self.itemsInCauldron[i].miniImg, (WIDTH * 30/100 + WIDTH * 5/100 * i, HEIGHT * 75/100 + HEIGHT * 10/100))
    
    def addIngredient(self, item: Medicine):
        self.itemsInCauldron.append(item)

    def reset(self):
        self.itemsInCauldron = []
        self.isBrewed = False

class Vial(Item):
    potionColors = {
        "red" : pygame.transform.scale(pygame.image.load("imgs/redPotion.png"), (WIDTH/195*10, HEIGHT/147*11)),
        "orange" : pygame.transform.scale(pygame.image.load("imgs/orangePotion.png"), (WIDTH/195*10, HEIGHT/147*11)),
        "yellow" : pygame.transform.scale(pygame.image.load("imgs/yellowPotion.png"), (WIDTH/195*10, HEIGHT/147*11)),
        "green" : pygame.transform.scale(pygame.image.load("imgs/greenPotion.png"), (WIDTH/195*10, HEIGHT/147*11)),
        "lightBlue" : pygame.transform.scale(pygame.image.load("imgs/lightBluePotion.png"), (WIDTH/195*10, HEIGHT/147*11)),
        "blue" : pygame.transform.scale(pygame.image.load("imgs/bluePotion.png"), (WIDTH/195*10, HEIGHT/147*11))
    }

    for key in potionColors:
        potionColors[key].set_alpha(220)

    def __init__(self, pos: tuple) -> None:
        super().__init__("emptyVialAlpha", pos)
        self.image = pygame.transform.scale(self.image, (WIDTH/195*self.image.get_width(), HEIGHT/147*self.image.get_height()))
        self.contents = None
        self.potionImg = None
        self.color = None
        self.isMoving = False

    def setPotion(self, ingredients, color):
        self.contents = ingredients
        self.color = color
        self.potionImg = Vial.potionColors[self.color]

    def draw(self, surface: pygame.Surface):
        if self.isMoving:
            surface.blit(self.potionImg, (pygame.mouse.get_pos()[0]+self.image.get_width()/12, pygame.mouse.get_pos()[1]+self.image.get_height()*4/15))
            surface.blit(self.image, pygame.mouse.get_pos())
        else:
            if self.potionImg != None:
                surface.blit(self.potionImg, (surface.get_width()/100*self.pos[0]+self.image.get_width()/12, surface.get_height()/100*self.pos[1]+self.image.get_height()*4/15))
            surface.blit(self.image, (surface.get_width()/100*self.pos[0], surface.get_height()/100*self.pos[1]))
            self.rect = pygame.Rect(WIDTH/100*self.pos[0], HEIGHT/100*self.pos[1], self.image.get_width(), self.image.get_height())
        

    
    def isEmpty(self):
        if self.contents != [] and self.potionImg != None:
            print("Isnt Empty!")
            return False
        else:
            print("is Empty!")
            return True

# make 
class MovableItem(Item):
    def __init__(self, imageName: str, typeOfItem: str, pos: tuple) -> None:
        super().__init__(imageName, pos)
        self.isPickedUp = False
        self.typeOfItem = typeOfItem
        

    def draw(self, surface):
        if self.isPickedUp:
            # BUG make it not set rect every frame please
            self.rect = pygame.Rect(WIDTH/100*self.pos[0], HEIGHT/100*self.pos[1], WIDTH/195*self.image.get_width(), HEIGHT/147*self.image.get_height())
            surface.blit(self.image, pygame.mouse.get_pos())
            


class Disease:
    def __init__(self, cure: list[Medicine], timeToCure: int) -> None:
        self.cure = cure
        self.timeToCure = timeToCure


'''
Patients:
    - Have symptoms
    - a timer
    - cure progress bar
    - particles for explosion
    - urgency level?
'''

class Patient:
    def __init__(self) -> None:
        self.disease = None
        self.image = None
        self.pos = None
        self.particles = []
        self.initParticles()

    def explode(self):
        pass

    def initParticles(self):
        pass

    def setDisease(self):
        pass


'''
Player 
    - number of lawsuits
    - amount of money 
    - achievements unlocked
    - cures unlocked
    - level
    - num patients cured
    - num patients dead
    - rating
    - maybe cutscene data
'''

class Player:
    money = 0
    lawsuits = 0
    level = 0
    numPatientsCured = 0
    numDeadPatients = 0

    medicines = {
        "eyeballs": True,
        "frog": True,
        "dragon blood": True,
        "lion hearts": True,
        "rat": True,
        "bull balls": True,
        "leeches": True,
        "pee": True,
        "stones": True,
        "poo": True,
        "bone dust": True,
        "raspberry herb": True,
        "cannybids": True,
        "magic beans": True,
        "mold": True
    }

    @staticmethod
    def getmedicinesUnlocked() -> list[str]:
        medicinesUnlocked = []
        for key in Player.medicines:
            if Player.medicines[key] == True:
                medicinesUnlocked.append(key)
        return medicinesUnlocked


class Desk:
    medicines = {
        "eyeballs": Medicine("eyesJar", "eyeMini", (5, 35)),
        "frog": Medicine("frogJar", "frogMini", (17, 38)),
        "dragon blood": Medicine("bloodJar", "bloodMini", (13, 43)),
        "lion hearts": Medicine("lionHeartsJar", "heartMini", (3, 41)),
        "rat": Medicine("ratJar", "ratMini", (22, 47)),
        "bull balls": Medicine("bullTesticlesJar", "ballsMini", (11, 54)),
        "pee": Medicine("peeJar", "peeMini", (18, 51)),
        "leeches": Medicine("leechesJar", "leechMini", (5, 49)),
        "stones": Medicine("stonesBowl", "stoneMini", (79, 40)),
        "poo": Medicine("pooBowl", "pooMini", (69, 49)),
        "bone dust": Medicine("boneDustBowl", "boneMini", (72, 56)),
        "magic beans": Medicine("magicBeansBag", None, (86, 89)),
        "raspberry herb": Medicine("raspberryHerbBag", "raspberryMini", (80, 77)),
        "cannybids": Medicine("cannybidsBag", "cannybidsMini", (72, 83)),
        "mold": Medicine("moldPile", None, (2, 83))
    }
    trinkets = {
        "book": Item("book", (36, 75)),
        "potionStand": Item("potionStand", (38, 40)),
        "skullBook": Item("skullBook", (6, 63)),
        # "vial": Item("emptyVialAlpha", (45, 36)),
        "magnifyingGlass": Item("magnifyingGlassAlpha", (28, 58))
    }
    lights = {
        "wallLight1" : Light("wallLight", (15, 10)),
        "wallLight2" : Light("wallLight", (70, 10)),
        "candle": Light("bookCandle", (14, 60))
    }

    background = pygame.image.load("imgs/backgroundMain.png")
    cauldron = Cauldron("cauldron", (41, 52))

    @staticmethod
    def initDesk():
        medicines = Player.getmedicinesUnlocked()
        for medicine in medicines:
            Desk.medicines[medicine].draw(Desk.background)
        for key in Desk.trinkets:
            Desk.trinkets[key].draw(Desk.background)
        for key in Desk.lights:
            Desk.lights[key].draw(Desk.background)
        # Desk.cauldron.draw(Desk.background)
        

    @staticmethod
    def draw(surface: pygame.Surface):
        surface.blit(pygame.transform.scale(Desk.background, (surface.get_width(), surface.get_height())), (0,0))



