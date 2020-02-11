import pygame
pygame.init()

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage
import matplotlib.colors as mcolors
import math

'''
initializes variables: 
- x as the origin position for the items when they are first formed
- discRadius as the origin radius of the crescent
- innerRadius asthe origial radius for the inner crescent circle
- amplitude as the original brightness for both the crescent and the gaussian
- sigma as the blurriness for the crescent
- sigmaX as the horizontal scale for the gaussian
- sigmaY asthe vertical scale for the gaussian
- crescentPhi as the original angle for thecrescent
- gaussianPhi as the original angle for the gaussian 

initializes initialQualities as the list for the original crescent
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

'''
creates the colormap: four arguments are made in colors which are
red, green, blue, and transparency. c goes up to one instead of 255.
the colormap is called cmapred and has 100 possible colors
'''
colors=[(c,c**4,c**7,c**2) for c in np.linspace(0,1,100)]
cmapred=mcolors.LinearSegmentedColormap.from_list('mycmap', colors, N=100)


'''
initializes various other qualities:
- display_width is the width of the screen
- display_height is the height of the sceen
- various colors: black, lightGrey, darkGrey, and white.
- sets the name of the window with set_caption
- sets the pygame display to aforementioned display_width and display_height
- starts the clock
'''
display_width=1000
display_height=800
black=(0,0,0)
lightGrey=(200,200,200)
grey=(150,150,150)
darkGrey=(100,100,100)
white=(255,255,255)
pygame.display.set_caption('black hole modeling interface')
gameDisplay=pygame.display.set_mode((display_width,display_height))
clock=pygame.time.Clock()

'''
initializes the fonts and the text rectangle. sets the original font to
calibri light at 20px.
'''
font=pygame.font.SysFont('calibril.ttf', 20)
text=font.render('labels', True, white)
textRect=text.get_rect()

'''
some random initializations:
- sets done to false, basically makes main code loop until done is set 
  to true.
- sets sliderClicked to 12 because the crescent only takes 8 paramaters
- sets selectedShape to zero becuase no shape is selected
- sets the values for the maximum crescent and gaussian labels
- sets the inital qualities for the crescent
- makes the names for the crescent and gaussian sliders
- initializes the shape quality and type dictionaries
'''
done=False
sliderClicked=12
selectedShape=0
namesOfRightCrescentLabels=[800,800,40,400,1,5,6.28,10]
namesOfRightGaussianLabels=[800,800,1,20,20,6.28]
initialQualitiesForCrescent=[820,820,884,862,980,916,820,884]

namesOfCrescentSliders=[
    'x-center','y-center','radius of entire disk',
    'radius of inner disk','brightness','sigma',
    'angle','center displacement'
    ]
namesOfGaussianSliders=[
    'x-center','y-center','amplitude',
    'width','height', 'angle'
    ]

oldShapeQualities={}
oldShapeTypes={}

'''
the class Model is the class used for each crescent and gaussian item. it has
the functions:
- _init_, which initializes the function to the given name and sets placed to 
  false
- defineShape, which sets the shape to either a crescent or a gaussian and 
  gives it the base qualities
- makePlaced and makeUnplaced. these are self explanatory.
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
        else:
            print('the shape is neither crescent nor gaussian')
    def makePlaced(self):
        self.placed=False
    def makeUnplaced(self,x,y):
        self.placed=True
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
    plt.savefig(saveName, bbox_inches='tight',
        pad_inches=0, transparent=True)
    #splt.show()

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
    plt.clf()
    im_arr=np.zeros((100,100))
    
    for r, row in enumerate(im_arr):
        for c, col in enumerate(row):
            yDist=((c-50)**2+(r-50)**2)**0.5\
                *math.sin(gaussianPhi+math.atan((c-50)/(r-50.001)))
            xDist=((c-50)**2+(r-50)**2)**0.5\
                *math.cos(gaussianPhi+math.atan((c-50)/(r-50.001)))
            im_arr[r][c]=(((1.)/(2.*np.pi*sigmaX*sigmaY))\
                *np.exp(-0.5*((xDist)/(sigmaX))**2-0.5*((yDist)/(sigmaY))**2))
    im_arr=scipy.ndimage.gaussian_filter(im_arr, sigma)

    plt.imshow(im_arr,cmap=cmapred, interpolation ='gaussian')
    #plt.colorbar()
    plt.axis('off')
    plt.savefig(saveName, bbox_inches='tight',
        pad_inches=0, transparent=True)
    #plt.show()

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
crescentIcon=pygame.image.load('crescentIcon.png')
crescentIcon=pygame.transform.scale(crescentIcon, (250,250))
gaussianIcon=Model('gaussianIcon')
gaussianIcon.defineShape('gaussian')
gaussianCreate(
    gaussianIcon.qualities[2],
    gaussianIcon.qualities[3],
    gaussianIcon.qualities[4],
    gaussianIcon.qualities[5],
    str(gaussianIcon.name + '.png'))
gaussianIcon=pygame.image.load('gaussianIcon.png')
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
            if the selected shape is greater than zero, or if a shape is
            selected, then go check if the mouse is over the slider bar and 
            then check if the mouse is over the ellipse. if so, then sets the 
            sliderClicked variable to the number slider that is clicked
            '''
            if selectedShape>0:
                if pos[0]>820 and pos[0]<980 and pos[1]>300:
                    for i in range(8):
                        if pos[1]>325+60*i\
                                and pos[1]<335+60*i\
                                and pos[0]<sliderPositions[i]+20\
                                and pos[0]>sliderPositions[i]-10:
                            sliderClicked=i
            '''
            if the mouse is over the crescent icon, then if a shape is already
            selected add its quality and type to the dictionary. either way,
            add 1 to the selectedShape variable and create a model named
            crescent.png with size 800 by 800 pixels. places the icon.
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
                    str(currentModel.name + '.png'))
                currentModelImage=pygame.image.load('crescent.png')
                currentModelImage=pygame.transform.scale(currentModelImage,
                    (800,800))
                currentModel.makePlaced()
            '''
            if the mouse is over the gaussian icon, then do basically the same
            as the above if statement about the crescent icon.
            '''
            if pos[0]<950 and pos[0]>800 and pos[1]<270 and pos[1]>144:
                if selectedShape == 1:
                    oldShapeQualities['1']=currentModel.qualities
                    oldShapeTypes['1']=currentModel.shape
                elif selectedShape>1:
                    oldShapeQualities[str(selectedShape)]=\
                        currentModel.qualities
                    oldShapeTypes[str(selectedShape)]=currentModel.shape
                selectedShape += 1
                currentModel=Model('gaussian' + str(selectedShape))
                currentModel.defineShape('gaussian')
                currentModel.changeQuality(3,10)
                gaussianCreate(
                    currentModel.qualities[2],
                    currentModel.qualities[3],
                    currentModel.qualities[4],
                    currentModel.qualities[5],
                    str(currentModel.name + '.png'))
                currentModelImage=pygame.image.load('gaussian'
                                                    + str(selectedShape) 
                                                    + '.png')
                currentModelImage=pygame.transform.scale(currentModelImage,
                                                        (800,800))    
                currentModel.makePlaced()
        '''
        if unclicked, then if a selected shapes become unplaced and selected
        sliders are unselected
        '''
        if event.type == pygame.MOUSEBUTTONUP:
            if selectedShape>0:
                currentModel.makeUnplaced(pos[0],pos[1])
            if sliderClicked<10:
                sliderClicked=12

    if sliderClicked<10:
        '''
        if a slider is clicked and the current selected shape is a crescent
        - if the x position is too low (past the edge of the slider), bring
          the value up and deselect the slider
        - if the x pos is too high, then it brings the value down and deselcts
          the slider
        - otherwise, bring the value to the position of the slider and creates
          a new model unless the slider is the first or second (position) one.
        does the same thing, but with gaussians
        '''
        if currentModel.shape == 'crescent':
            if pos[0]<830:
                currentModel.qualities[sliderClicked]=\
                    namesOfRightCrescentLabels[sliderClicked]*0.005
                sliderClicked=12
            elif pos[0]>980:
                currentModel.qualities[sliderClicked]=\
                    namesOfRightCrescentLabels[sliderClicked]*0.95
                sliderClicked=12
            else:
                currentModel.qualities[sliderClicked]=\
                    currentModel.qualities[sliderClicked]\
                    *((pos[0]-833)/(sliderPositions[sliderClicked]-820.1))
                if sliderClicked>1:
                    crescentCreate(
                        currentModel.qualities[2],
                        currentModel.qualities[3],
                        currentModel.qualities[4],
                        currentModel.qualities[5],
                        currentModel.qualities[6],
                        currentModel.qualities[7],
                        str(currentModel.name + '.png'))
                    currentModelImage=pygame.image.load('crescent.png')
                    currentModelImage=\
                        pygame.transform.scale(currentModelImage,(800,800))
        elif currentModel.shape == 'gaussian':
            if pos[0]<830:
                currentModel.qualities[sliderClicked]=\
                    namesOfRightGaussianLabels[sliderClicked]*0.005
                sliderClicked=12
            elif pos[0]>980:
                currentModel.qualities[sliderClicked]=\
                    namesOfRightGaussianLabels[sliderClicked]*0.95
                sliderClicked=12
            else:
                currentModel.qualities[sliderClicked]=\
                    currentModel.qualities[sliderClicked]\
                    *((pos[0]-833)/(sliderPositions[sliderClicked]-820.1))
                if sliderClicked>1:
                    gaussianCreate(
                        currentModel.qualities[2],
                        currentModel.qualities[3],
                        currentModel.qualities[4],
                        currentModel.qualities[5],
                        str('gaussian.png'))
                    currentModelImage=pygame.image.load('gaussian.png')
                    currentModelImage=\
                        pygame.transform.scale(currentModelImage, (800,800))
    '''
    goes through the history of models and creates each one at the right
    coordinates
    '''
    for i in range(len(oldShapeQualities)):
        if oldShapeTypes[str(i+1)] == 'crescent':
            crescentCreate(
                oldShapeQualities[str(i+1)][2],
                oldShapeQualities[str(i+1)][3],
                oldShapeQualities[str(i+1)][4],
                oldShapeQualities[str(i+1)][5],
                oldShapeQualities[str(i+1)][6],
                oldShapeQualities[str(i+1)][7],
                str('oldShape.png'))
        elif oldShapeTypes[str(i+1)] == 'gaussian':
            gaussianCreate(
                oldShapeQualities[str(i+1)][2],
                oldShapeQualities[str(i+1)][3],
                oldShapeQualities[str(i+1)][4],
                oldShapeQualities[str(i+1)][5],
                str('oldShape.png'))
        currentOldImage=pygame.image.load('oldShape.png')
        currentOldImage=pygame.transform.scale(currentOldImage, (800,800))
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
        if pos[0]<= 800:
            currentModel.changeQuality(0,pos[0])
            currentModel.changeQuality(1,pos[1])
        gameDisplay.blit(currentModelImage,(currentModel.qualities[0]-400,
                                            currentModel.qualities[1]-400))
    elif selectedShape>0 and currentModel.placed:
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
        multiplues each value by a constant and adds 820 to it
        '''
        if currentModel.shape == 'crescent':
            sliderPositions=[
                currentModel.qualities[0]*0.2+820,
                currentModel.qualities[1]*0.2+820,
                currentModel.qualities[2]*4+820,
                currentModel.qualities[3]*4+820,
                currentModel.qualities[4]*0.00625+820,
                currentModel.qualities[5]*16+820,
                currentModel.qualities[6]*25.46+820,
                currentModel.qualities[7]*16+820
                ]
        elif currentModel.shape == 'gaussian':
            sliderPositions=[
                currentModel.qualities[0]*0.2+820,
                currentModel.qualities[1]*0.2+820,
                currentModel.qualities[2]*0.00625+820,
                currentModel.qualities[3]*8+820,
                currentModel.qualities[4]*8+820,
                currentModel.qualities[5]*25.464+820
                ]
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
                                (sliderPositions[i],323+60*i,20,20))
    else:
        '''
        if no shape is selected, then show the base values for the sliders/
        Shows the zeroes, the crescent values, the crescent names, and the
        crescent number of sliders. displays undifined for each slider value
        '''
        for i in range(len(initialQualities)):
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


    pygame.display.update()
    clock.tick(500)

pygame.quit()
quit()