from gsm import *
from utils import *

class State:
    def __init__(self) -> None:
        self.buttons = []
        self.texts = []
    
    def onEnter(self):
        pass

    def onExit(self):
        pass

    def render(self, surface):
        for button in self.buttons:
            button.draw(surface)
        for text in self.texts:
            text.draw(surface)

    def update(self):
        pass

    def handleInput(self, events):
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    if button.checkMouseOver(pos):
                        button.onClickFunc()



class PlayState(State):
    Desk.initDesk()
    def __init__(self) -> None:
        super().__init__()
        self.patients = []
        self.medicines = Player.getmedicinesUnlocked()
        self.medicineBeingDragged = None
        self.draggingPotion = False
        self.draggingPotionImg = None
        self.buttons.append(Button("Brew", pygame.Rect(46, 68, 10, 5), 10, onclickFunc=Desk.cauldron.checkCanBrew, altImage=pygame.transform.scale(pygame.image.load("imgs/brewButton.png"), (WIDTH/195*18, HEIGHT/147*9))))
        self.vials = [
            Vial((39,35)),
            Vial((47,35)),
            Vial((55,35))
        ]
        self.movingVial = None
        
        # make one var for all item that currently be dragged BUG
        self.itemBeingDragged = None

    def render(self, screen):
        Desk.draw(screen)
        Desk.cauldron.draw(screen)
        pos = pygame.mouse.get_pos()
        self.drawMiniMedicine(screen, pos)
        self.drawVials(screen, pos)
        super().render(screen)

    def handleInput(self, events: list):
        super().handleInput(events)
        pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.checkPickedUpAMedicine(pos)
                self.checkPickedUpBrewedPotion(pos)
                self.checkClickedOnVial(pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.depositMedicineInCaudron(pos)
                self.fillVial(pos)
                self.resetMovingItems()

    def resetMovingItems(self):
        self.medicineBeingDragged = None
        for vial in self.vials: # TODO fix that shit
            vial.isMoving = False

    def depositMedicineInCaudron(self, pos: tuple):
        if Desk.cauldron.rect.collidepoint(pos):
            if self.medicineBeingDragged != None:
                Desk.cauldron.addIngredient(self.medicineBeingDragged)
                Desk.cauldron.splash()

    # extract this to vial class
    def fillVial(self, pos: tuple):
        if self.draggingPotion:
            for vial in self.vials:
                if vial.rect.collidepoint(pos):
                    if vial.isEmpty():
                        vial.setPotion(Desk.cauldron.itemsInCauldron, Desk.cauldron.brewColor)
                    Desk.cauldron.reset()
            self.draggingPotion = False

    # extract to medicine class
    def drawMiniMedicine(self, screen: pygame.Surface, pos: tuple):
        if self.medicineBeingDragged != None:
            screen.blit(self.medicineBeingDragged.miniImg, pos)

    def drawVials(self, screen: pygame.Surface, pos: tuple):
        for vial in self.vials:
            vial.draw(screen)
        if self.draggingPotion:
            screen.blit(self.draggingPotionImg , pos)
    

    # these 3 functions are repeat code. put them together please
    def checkClickedOnVial(self, pos: tuple):
        for vial in self.vials:
            if vial.rect.collidepoint(pos) and not vial.isEmpty():
                vial.isMoving = True

    def checkPickedUpBrewedPotion(self, pos: tuple):
        if Desk.cauldron.isBrewed: #checks if you picked up a brewed potion
            if Desk.cauldron.rect.collidepoint(pos):
                self.draggingPotion = True
                self.draggingPotionImg = Cauldron.potionBlobs[Desk.cauldron.brewColor]

    def checkPickedUpAMedicine(self, pos: tuple):
        for medicine in self.medicines: # checks if you picked up any medicines
            if Desk.medicines[medicine].checkClick(pos):
                self.medicineBeingDragged = Desk.medicines[medicine]


class MainMenuState(State):
    pass

class UpgradeState(State):
    pass

    # more time before they explode
    # less chance of exploding other customers
    # less chance of infecting other customers?
    # more money per customer?




stateManager = StateManager()
stateManager.push(PlayState())

