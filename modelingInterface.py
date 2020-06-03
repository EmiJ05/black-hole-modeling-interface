import os
import sys
import math
import pygame
import cProfile
import numpy as np
import scipy.ndimage
from PIL import Image
from pygame.locals import *
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


'''
initializes various other qualities:
- does this weird flag thing that improves speed
- starts pygame
- sets the allowed events to quit, mousedown, and mouseup
- display_width is the width of the screen
- display_height is the height of the sceen
- various colors: black, lightGrey, darkGrey, and white.
- sets the name of the window with set_caption
- sets the pygame display to aforementioned display_width and display_height
- starts the clock
'''

flags = FULLSCREEN | DOUBLEBUF
pygame.init()
pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
display_width=1000
display_height=800
black=(0,0,0)
lightGrey=(200,200,200)
grey=(150,150,150)
darkGrey=(100,100,100)
white=(255,255,255)
pygame.display.set_caption('black hole modeling interface')
gameDisplay=pygame.display.set_mode((display_width,display_height),flags)

clock=pygame.time.Clock()

gameDisplay.set_alpha(None)

'''
initializes variables: 
- x as the origin position for the items when they are first formed
- discRadius ares the origin radius of the crescent
- innerRadius asthe origial radius for the inner crescent circle
- amplitude as the original amplitude for both the crescent and the gaussian
- sigma as the blurriness for the crescent
- sigmaX as the horizontal scale for the gaussian
- sigmaY asthe vertical scale for the gaussian
- crescentPhi as the original angle for thecrescent
- gaussianPhi as the original angle for the gaussian 
- i'm gonna keep working on this project because it is FUN and i'm LEARNING

initializes initialQualities as the list for the original crescent
initializes shapeMultiplies as a dictionary to give as the value to convert
the slider positions into the shape's properties
'''

x=800
y=100
discRadius=20
innerRadius=13
amplitude=1
sigma=3
sigmaX=10
sigmaY=15
crescentPhi=0
gaussianPhi=0.7853
centerDisplacement=3
initialQualities=[
    x,y,discRadius,innerRadius,amplitude,
    sigma,crescentPhi,centerDisplacement
    ]
shapeMultipliers={
    'crescent': [0.2,0.2,4,4,160,15,25.46,16],
    'gaussian': [0.2,0.2,160,8,8,25.464]
    }
previousOldShapeLength=0

'''
initializes the fonts and the text rectangle. sets the original font to
calibri light at 20px.
'''
font=pygame.font.SysFont('calibril.ttf', 20)
text=font.render('labels', True, white)
textRect=text.get_rect()

'''
creates the colormap: four arguments are made in colors which are
red, green, blue, and transparency. c goes up to one instead of 255.
the colormap is called cmapred and has 100 possible colors
'''
colors=[(c,c**4,c**7,c**2) for c in np.linspace(0,1,7)]
cmapred=mcolors.LinearSegmentedColormap.from_list('mycmap', colors, N=100)

'''
some random initializations:
- sets done to false, basically makes main code loop until done is set 
  to true.
- sets the mouseClicked variable to not clicked
- sets sliderClicked to 12 because the crescent only takes 8 paramaters
- sets selectedShape to zero becuase no shape is selected
- sets the values for the maximum crescent and gaussian labels
- sets the inital qualities for the crescent
- makes the names for the crescent and gaussian sliders
- initializes the sliderPositions list
- initializes the shape quality and type dictionaries
'''
done=False
mouseClicked=False
sliderClicked=12
selectedShape=0
namesOfRightCrescentLabels=[800,800,40,40,1,5,6.28,10]
namesOfRightGaussianLabels=[800,800,1,20,20,6.28]
initialQualitiesForCrescent=[820,820,884,862,980,916,820,884]

namesOfCrescentSliders=[
    'x-center','y-center','radius of entire disk',
    'radius of inner disk','amplitude','sigma',
    'angle','center displacement'
    ]
namesOfGaussianSliders=[
    'x-center','y-center','amplitude',
    'width','height', 'angle'
    ]
sliderPositions=[]
oldShapeQualities={}
oldShapeTypes={}

'''
the class Model is the class used for each crescent and gaussian item. it has
the functions:
- _init_, which initializes the function to the given name and sets placed to 
  false
- defineShape, which sets the shape to either a crescent or a gaussian and 
  gives it the base qualities
- changeQuality, which sets a quality of the model to a given value

'''
class Model:
    def __init__(self,name):
        self.name=name
        self.placed=False
    def defineShape(self,shape):
        self.shape=shape
        if self.shape == 'crescent':
            self.qualities=[x,y,discRadius,innerRadius,amplitude,
                                sigma,crescentPhi,centerDisplacement]
        elif self.shape == 'gaussian':
            self.qualities=[x,y,amplitude, sigmaX, sigmaY, gaussianPhi]
    def changeQuality(self,quality,value):
        self.qualities[quality]=value

'''
the crescentCreate function creates a crescent with the given parameters
discRadius, innerRadius, amplitude, sigma, crescentPhi, centerDisplacement,
and saveName. It exports an image with name saveName.

It creates the crescent by making an array of 100 by 100 values and setting
each of those values to the amplitude. it then blurs the image with
gaussian_filter and smooths it with interpolation = 'gaussian'.
'''
def crescentCreate(
        discRadius,
        innerRadius,
        amplitude,
        sigma,
        crescentPhi,
        centerDisplacement,
        saveName):
    amplitude = 0.5*amplitude+0.5
    if amplitude<=1 and amplitude>=0:
        '''
        creates the colormap: four arguments are made in colors which are
        red, green, blue, and transparency. c goes up to one instead of 255.
        the colormap is called cmapred and has 100 possible colors
        '''
        colors=[(c,c**4,c**7,c**2) for c in np.linspace(0,amplitude,7)]
        cmapred=mcolors.LinearSegmentedColormap.from_list('mycmap', colors,\
                                                        N=100)
    plt.clf()
    im_arr=np.zeros((100,100))
    for r, row in enumerate(im_arr):
        for c, col in enumerate(row):
            bigRadius=np.sqrt((r-50)**2. + (c-50)**2.)
            smallRadius=np.sqrt(
                (r-(50+centerDisplacement\
                *math.cos(crescentPhi+math.pi/2)))**2
                + (c-(50+centerDisplacement*math.sin(crescentPhi
                + math.pi/2)))**2)
            if bigRadius<discRadius and smallRadius>innerRadius:
                im_arr[r][c]=amplitude
    im_arr=scipy.ndimage.gaussian_filter(im_arr, sigma)

    plt.imshow(im_arr,cmap=cmapred, interpolation ='gaussian')
    #plt.colorbar()
    plt.axis('off')
    plt.savefig(saveName,figsize=(800/227, 800/227),dpi=227,
        bbox_inches='tight',pad_inches=0, transparent=True)
    #plt.show()

'''
the gaussianCreate function is similar to the crescentCreate function, but it
creates a gaussian with the given parameters amplitude, sigmaX, sigmaY, 
gaussianPhi, and saveName. It exports an image with name saveName.

It creates the gaussian by using the two-dimensional normal distribution
function. It also rotates the gaussian by rotating the coordinates it is 
given. it then blurs the image withgaussian_filter and smooths it with 
interpolation = 'gaussian'.
''' 

def gaussianCreate(
        amplitude,
        sigmaX,
        sigmaY,
        gaussianPhi,
        saveName):
    amplitude = 0.5*amplitude+0.5
    plt.clf()
    im_arr=np.zeros((100,100))
    if amplitude<=1 and amplitude>=0:
        '''
        creates the colormap: four arguments are made in colors which are
        red, green, blue, and transparency. c goes up to one instead of 255.
        the colormap is called cmapred and has 100 possible colors
        '''
        colors=[(c,c**4,c**7,c**2) for c in np.linspace(0,amplitude,7)]
        cmapred=mcolors.LinearSegmentedColormap.from_list('mycmap', colors, N=100)
    for r, row in enumerate(im_arr):
        for c, col in enumerate(row):
            yDist=((c-50)**2+(r-50)**2)**0.5\
                *math.sin(gaussianPhi+math.atan((c-50)/(r-50.001)))
            xDist=((c-50)**2+(r-50)**2)**0.5\
                *math.cos(gaussianPhi+math.atan((c-50)/(r-50.001)))
            im_arr[r][c]=(((1.)/(2.*np.pi*sigmaX*sigmaY+0.01))\
                *np.exp(-0.5*((xDist)/(sigmaX+0.01))**2
                -0.5*((yDist)/(sigmaY+0.01))**2))
    #im_arr=scipy.ndimage.gaussian_filter(im_arr, sigma)

    plt.imshow(im_arr,cmap=cmapred, interpolation ='gaussian')
    #plt.colorbar()
    plt.axis('off')
    plt.savefig(saveName,figsize=(800/192, 800/192),dpi=192,
        bbox_inches='tight',pad_inches=0, transparent=True)
    #plt.show()

'''
SaveImage function. It doesn't do anything now, but soon it will be able to
export a final saved image ADD COMMENT
'''
def saveImage():
    if previousOldShapeLength>0:
        background = Image.open("blackBackground.png")
        overlay = Image.open("oldShape1.png")
        background = background.convert("RGBA")
        overlay = overlay.convert("RGBA")
        background.paste(overlay, box=None, mask=overlay)
        for i in oldShapeQualities:
            i=int(i)
            if int(i+1)<=previousOldShapeLength:
                overlay = Image.open("oldShape%d.png" % int(i+1))
                background = background.convert("RGBA")
                overlay = overlay.convert("RGBA")
                background.paste(overlay, box=None, mask=overlay)
    else:
        background = Image.open("blackBackground.png")
    overlay = Image.open("currentModel.png")
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")
    background.paste(overlay, box=None, mask=overlay)
    overlay = background
    background = Image.open("blackBackground.png")
    background.paste(overlay, box=None, mask=overlay)
    background.save("finalImage.png","PNG")
    os.remove("gaussianIcon.png")
    os.remove("crescentIcon.png")
    os.remove("currentModel.png")
    for i in oldShapeQualities:
        os.remove("oldShape%d.png" % int(i))
    print("Thank you for using my black hole modeling software! The "
            + "image outputs in a file called finalImage.png - check "
            + " it out! Contact emilia.jacobsen@winsor.edu for any "
            + " questions about how the software works.")
    sys.exit()



'''
A function that simplifies the code; basically just changes the slider
positions. It goes through the length of the shape multipliers (which shows
how many sliders will be needed) and appends a value of a slider corresponding
to the currentModel qualities. It exports a list that the code will use for 
slider positions.
'''
def changeSliderPositions():
    sliderPositions = []
    for i in range(len(shapeMultipliers[currentModel.shape])):
        sliderPositions.append(currentModel.qualities[i]*\
            (shapeMultipliers[currentModel.shape][i])+820)
    return(sliderPositions)



'''
this chunk of code creates the crescent and gaussian icons. it first calls
the model class and names it crescentIcon. it creates a crescent with the 
original qualities, loads it as the image crescentIcon.png, and resizes it to
250 by 250 pixels. it does the same thing with the gaussian icon

'''

crescentIcon=Model('crescentIcon')
crescentIcon.defineShape('crescent')
crescentCreate(
    crescentIcon.qualities[2],
    crescentIcon.qualities[3],
    crescentIcon.qualities[4],
    crescentIcon.qualities[5],
    crescentIcon.qualities[6],
    crescentIcon.qualities[7],
    str(crescentIcon.name + '.png'))
crescentIcon=pygame.image.load('crescentIcon.png').convert_alpha()
crescentIcon=pygame.transform.scale(crescentIcon, (250,250))
gaussianIcon=Model('gaussianIcon')
gaussianIcon.defineShape('gaussian')
gaussianCreate(
    gaussianIcon.qualities[2],
    gaussianIcon.qualities[3],
    gaussianIcon.qualities[4],
    gaussianIcon.qualities[5],
    str(gaussianIcon.name + '.png'))
gaussianIcon=pygame.image.load('gaussianIcon.png').convert_alpha()
gaussianIcon=pygame.transform.scale(gaussianIcon, (250,250))

'''
the big ole loop
'''

while not done:
    '''
    fills the background with black, gets the mouse position, gets the events,
    and goes through each one in a for loop
    '''
    gameDisplay.fill(black)
    pos=pygame.mouse.get_pos()
    events=list(pygame.event.get())
    for event in events:
        if event.type == pygame.QUIT:
            done=True
        if event.type == pygame.MOUSEBUTTONDOWN:
            '''
            sets mouse clicked to true
            '''
            mouseClicked=True

            '''
            if the selected shape is greater than zero, or if a shape is
            selected, then go check if the mouse is over the slider bar and 
            then check if the mouse is over the ellipse. if so, then sets the 
            sliderClicked variable to the number slider that is clicked
            '''
            if selectedShape>0:
                if pos[0]>800 and pos[0]<1000 and pos[1]>300:
                    for i in range(8):
                        if pos[1]>320+60*i\
                                and pos[1]<340+60*i\
                                and pos[0]<sliderPositions[i]+35\
                                and pos[0]>sliderPositions[i]-25:
                            sliderClicked=i
            '''
            if the mouse is over the crescent icon, then if a shape is already
            selected add its quality and type to the dictionary. either way,
            add 1 to the selectedShape variable and create a model named
            crescent.png with size 800 by 800 pixels. places the icon.
            it also makes the sliderPositions list
            '''
            if pos[0]<950 and pos[0]>800 and pos[1]<160 and pos[1]>10:
                if selectedShape>0:
                    oldShapeQualities[str(selectedShape)]=\
                        currentModel.qualities
                    oldShapeTypes[str(selectedShape)]=currentModel.shape
                selectedShape += 1
                currentModel=Model('crescent')
                currentModel.defineShape('crescent')
                crescentCreate(
                    currentModel.qualities[2],
                    currentModel.qualities[3],
                    currentModel.qualities[4],
                    currentModel.qualities[5],
                    currentModel.qualities[6],
                    currentModel.qualities[7],
                    'currentModel.png')
                currentModelImage=pygame.image.load('currentModel.png').\
                    convert_alpha()
                sliderPositions = changeSliderPositions()
            '''
            if the mouse is over the gaussian icon, then do basically the same
            as the above if statement about the crescent icon.
            '''
            if pos[0]<950 and pos[0]>800 and pos[1]<270 and pos[1]>144:
                if selectedShape>0:
                    oldShapeQualities[str(selectedShape)]=\
                        currentModel.qualities
                    oldShapeTypes[str(selectedShape)]=currentModel.shape
                selectedShape += 1
                currentModel=Model('gaussian')
                currentModel.defineShape('gaussian')
                gaussianCreate(
                    currentModel.qualities[2],
                    currentModel.qualities[3],
                    currentModel.qualities[4],
                    currentModel.qualities[5],
                    'currentModel.png')
                currentModelImage=pygame.image.load('currentModel.png').\
                    convert_alpha()
                sliderPositions = changeSliderPositions()
            '''
            if the savebutton is clicked, call the saveImage functon
            '''
            if pos[0]>850 and pos[0]<950 and pos[1]>770 and pos[1]<790:
                saveImage()
                done = True
        '''
        if mouse is unclicked, then if a selected shapes become unplaced and 
        selected sliders are unselected
        '''
        if event.type == pygame.MOUSEBUTTONUP:
            mouseClicked=False
            if selectedShape>0:
                currentModel.placed=True
            if sliderClicked<10:
                sliderClicked=12

    if sliderClicked<10:
        '''
        if a slider is clicked
        - if the x position is too low (past the edge of the slider), set the
          value to zero
        - if the x pos is too high, then it brings the value up to the maximum
        - otherwise, bring the value to the position of the slider and creates
          a new model unless the slider is the first or second (position) one.
        '''
        if currentModel.shape=='crescent':
            if pos[0]<830:
                currentModel.qualities[sliderClicked]=0
            elif pos[0]>980:
                currentModel.qualities[sliderClicked]=\
                namesOfRightCrescentLabels[sliderClicked]
            else:
                currentModel.qualities[sliderClicked]=\
                    (pos[0]-825)/(shapeMultipliers[currentModel.shape]\
                    [sliderClicked])
            sliderPositions = changeSliderPositions()
            if sliderClicked>1:
                crescentCreate(
                    currentModel.qualities[2],
                    currentModel.qualities[3],
                    currentModel.qualities[4],
                    currentModel.qualities[5],
                    currentModel.qualities[6],
                    currentModel.qualities[7],
                    str('currentModel.png'))
                currentModelImage=pygame.image.load('currentModel.png').\
                    convert_alpha()
        if currentModel.shape=='gaussian':
            if pos[0]<830:
                currentModel.qualities[sliderClicked]=0
            elif pos[0]>980:
                currentModel.qualities[sliderClicked]=\
                namesOfRightGaussianLabels[sliderClicked]
            else:
                currentModel.qualities[sliderClicked]=\
                    (pos[0]-833)/(shapeMultipliers[currentModel.shape]\
                    [sliderClicked])
            sliderPositions = changeSliderPositions()
            if sliderClicked>1:
                gaussianCreate(
                    currentModel.qualities[2],
                    currentModel.qualities[3],
                    currentModel.qualities[4],
                    currentModel.qualities[5],
                    str('currentModel.png'))
                currentModelImage=pygame.image.load('currentModel.png').\
                    convert_alpha()
    '''
    goes through the history of models and creates each one at the right
    coordinatess
    '''
    for i in range(len(oldShapeQualities)):
        if len(oldShapeQualities)>previousOldShapeLength:
            if oldShapeTypes[str(previousOldShapeLength+1)] == 'crescent':
                crescentCreate(
                    oldShapeQualities[str(previousOldShapeLength+1)][2],
                    oldShapeQualities[str(previousOldShapeLength+1)][3],
                    oldShapeQualities[str(previousOldShapeLength+1)][4],
                    oldShapeQualities[str(previousOldShapeLength+1)][5],
                    oldShapeQualities[str(previousOldShapeLength+1)][6],
                    oldShapeQualities[str(previousOldShapeLength+1)][7],
                    str('oldShape%d.png' % (previousOldShapeLength+1)))
            elif oldShapeTypes[str(previousOldShapeLength+1)] == 'gaussian':
                gaussianCreate(
                    oldShapeQualities[str(previousOldShapeLength+1)][2],
                    oldShapeQualities[str(previousOldShapeLength+1)][3],
                    oldShapeQualities[str(previousOldShapeLength+1)][4],
                    oldShapeQualities[str(previousOldShapeLength+1)][5],
                    str('oldShape%d.png' % (previousOldShapeLength+1)))
            previousOldShapeLength += 1
        if previousOldShapeLength>0:
            currentOldImage=pygame.image.load(str('oldShape%d.png' %\
                int(i+1))).convert_alpha()
            gameDisplay.blit(currentOldImage,
                (oldShapeQualities[str(i+1)][0]-400,
                oldShapeQualities[str(i+1)][1]-400))

    '''
    displays the axes and the axes labels
    '''
    font=pygame.font.SysFont('calibril.ttf', 15)
    text=font.render('200', True, white)
    textRect.center=(209, 16) 
    gameDisplay.blit(text, textRect)
    text=font.render('600', True, white)
    textRect.center=(609, 16)
    gameDisplay.blit(text, textRect)
    text=font.render('400', True, white)
    textRect.center=(409, 19)
    gameDisplay.blit(text, textRect)
    text=font.render('200', True, white)
    textRect.center=(25, 209)
    gameDisplay.blit(text, textRect)
    text=font.render('600', True, white)
    textRect.center=(25, 609)
    gameDisplay.blit(text, textRect)
    text=font.render('400', True, white)
    textRect.center=(25, 409)
    gameDisplay.blit(text, textRect)
    pygame.draw.rect(gameDisplay, white, (0, 0, 5, 800))
    pygame.draw.rect(gameDisplay, white, (0, 0, 800, 5))
    pygame.draw.rect(gameDisplay, white, (0, 400, 12, 2))
    pygame.draw.rect(gameDisplay, white, (400, 0, 2, 12))
    pygame.draw.rect(gameDisplay, white, (0, 200, 8, 2))
    pygame.draw.rect(gameDisplay, white, (0, 600, 8, 2))
    pygame.draw.rect(gameDisplay, white, (200, 0, 2, 8))
    pygame.draw.rect(gameDisplay, white, (600, 0, 2, 8))

    '''
    if a shape is selected and not placed, then follow the position of the
    mouse. if it is placed, then show it at the final position
    '''
    if selectedShape>0 and not currentModel.placed:
        pos=pygame.mouse.get_pos()
        sliderPositions = changeSliderPositions()
        if pos[0]<= 800:
            currentModel.changeQuality(0,pos[0])
            currentModel.changeQuality(1,pos[1])
        gameDisplay.blit(currentModelImage,(currentModel.qualities[0]-400,
                                            currentModel.qualities[1]-400))
    elif selectedShape>0 and currentModel.placed:
        '''
        if the mouse is clicked, the shape is placed, and the mouse isn't in
        the sidebar, then bring the shape to the mouse. Basically a click and
        drag function.
        '''
        if mouseClicked and pos[0]<800:
            pos=pygame.mouse.get_pos()
            currentModel.changeQuality(0,pos[0])
            currentModel.changeQuality(1,pos[1])
            sliderPositions = changeSliderPositions()
        gameDisplay.blit(currentModelImage,(currentModel.qualities[0]-400,
                                            currentModel.qualities[1]-400))

    '''
    displays the grey sidebar and the light grey separator line
    '''
    pygame.draw.rect(gameDisplay, darkGrey, (800, 0, 200, 1000))
    pygame.draw.rect(gameDisplay, lightGrey, (800,295,200,2))

    '''
    this block shows the grey slider bars and the positions of the sliders
    '''
    if selectedShape>0:

        '''
        creates the positions of the ellipse in correspondence to the values;
        multiplies each value by a constant and adds 820 to it
        '''

        '''
        for every slider, 
        - displays the zero at the beginning of each slider
        - displays the value at the end of each slider
        - displays the name of each slider
        - displays the value of each slider in a different color. if the value
          is less than ten, then move it over to center it with the others
        '''
        for i in range(len(currentModel.qualities)):
            textRect.center=(837, 350+60*i)
            text=font.render('0', True, white)
            gameDisplay.blit(text, textRect)
            if currentModel.shape == 'crescent':
                textRect.center=(980, 350+60*i)
                text=font.render(str(namesOfRightCrescentLabels[i]), 
                                    True, white)
                gameDisplay.blit(text, textRect)
                text=font.render(namesOfCrescentSliders[i],
                                    True, white)
            if currentModel.shape == 'gaussian':
                textRect.center=(980, 350+60*i)
                text=font.render(str(namesOfRightGaussianLabels[i]),
                                    True, white)
                gameDisplay.blit(text, textRect)
                text=font.render(namesOfGaussianSliders[i],
                                    True, white)
            textRect.center=(837, 315+60*i)
            gameDisplay.blit(text, textRect)
            if currentModel.qualities[i]<= 10:
                textRect.center=(995, 315+60*i)
            else:
                textRect.center=(980, 315+60*i)
            text=font.render(str(currentModel.qualities[i]),
                                    True, lightGrey)
            gameDisplay.blit(text, textRect)
            pygame.draw.rect(gameDisplay, lightGrey, (820,330+60*i,160,5))
            pygame.draw.ellipse(gameDisplay, black,
                                (sliderPositions[i]-5,323+60*i,20,20))
    else:
        '''
        if no shape is selected, then show the base values for the sliders/
        Shows the zeroes, the crescent values, the crescent names, and the
        crescent number of sliders. displays undifined for each slider value
        '''
        for i in range(len(initialQualitiesForCrescent)):
            textRect.center=(837, 350+60*i)
            text=font.render('0', True, white)
            gameDisplay.blit(text, textRect)
            textRect.center=(837, 315+60*i)
            text=font.render(namesOfCrescentSliders[i], True, white)
            gameDisplay.blit(text, textRect)
            textRect.center=(960, 315+60*i)
            text=font.render('undefined', True, lightGrey)
            gameDisplay.blit(text, textRect)
            pygame.draw.rect(gameDisplay, lightGrey, (820,330+60*i,160,5))
            pygame.draw.ellipse(gameDisplay, black, (820,323+60*i,20,20))
            textRect.center=(980, 315+60*i)
            pygame.draw.rect(gameDisplay, lightGrey, (820,330+60*i,160,5))
            pygame.draw.ellipse(gameDisplay, black, (820,323+60*i,20,20))
            textRect.center=(980, 350+60*i)
            text=font.render(str(namesOfRightCrescentLabels[i]), True, white)
            gameDisplay.blit(text, textRect)

    '''
    shows the crescent and gaussian icons
    '''
    gameDisplay.blit(crescentIcon,(760,-50))
    gameDisplay.blit(gaussianIcon,(760,80))

    '''
    draws save button and label
    '''
    pygame.draw.rect(gameDisplay,white, (850,770,100,20))
    textRect.center=(885,782)
    text=font.render('save and quit', True, black)
    gameDisplay.blit(text, textRect)
    pygame.display.update()
    clock.tick(500)
pygame.quit()
quit()