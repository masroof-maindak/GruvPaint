from tkinter import *
from tkinter import filedialog
from PIL import ImageGrab
from PIL import Image,ImageTk
import time
import math

class Paint(object):
    def __init__(self):
        self.root = Tk()
        self.root.configure(background = '#282828')

        #Colours
        self.colourPicker = LabelFrame(self.root, relief = FLAT, bg = '#282828', highlightthickness = 0)
        self.colourPicker.grid(row = 0, column = 0, columnspan=2, rowspan = 5)
        colours = ['#282828', '#cc241d', '#98971a', '#d79921', '#458588', 
                   '#b16286', '#689d6a', '#a89984', '#d65d0e', '#ebdbb2']
        a = b = 0
        for bruh in colours:
            Button(self.colourPicker, bg = bruh, width = 3, relief = FLAT, height = 1, highlightthickness = 0,
                   command = lambda col = bruh : self.updateColour(col)).grid(row = a, column = b)
            a += 1
            if a == 5:
                a = 0
                b = 1

        #Pen
        self.penImg = PhotoImage(file = "Assets/paintbrushGruv.png")
        self.penButton = Button(self.root, highlightthickness = 0, relief = FLAT, bg = '#282828', 
                                command=self.usePen, image = self.penImg)
        self.penButton.place(x = 10, y = 260)

        #Eraser
        self.eraserImg = PhotoImage(file = "Assets/eraserGruv.png")
        self.eraserButton = Button(self.root, highlightthickness = 0,relief = FLAT, bg = '#282828', 
                                   command=self.useEraser, image = self.eraserImg)
        self.eraserButton.place(x = 75, y = 260)

        #ColourDropper
        self.pickerImg = PhotoImage(file = "Assets/pickerGruv.png")
        self.pickerButton = Button(self.root, highlightthickness = 0, relief = FLAT, bg = '#282828', 
                                   command = lambda: self.setActiveTool("dropper"), image = self.pickerImg)
        self.pickerButton.place(x = 5, y = 340)

        #Shapes Dropdown Menu
        self.shapesImg = PhotoImage(file = "Assets/shapesGruv.png")
        self.shapesButton = Menubutton(self.root, highlightthickness=0, fg= '#ebdbb2',
                                       relief=FLAT, bg='#282828', image = self.shapesImg)
        self.shapesButton.place(x = 10, y = 450)
        self.shapesButton.menu = Menu(self.shapesButton, tearoff=0)
        self.shapesButton['menu'] = self.shapesButton.menu
        # Add shapes to the shapes dropdown menu
        self.addOption(self.shapesButton.menu, "Rectangle")
        self.addOption(self.shapesButton.menu, "Curve")
        self.addOption(self.shapesButton.menu, "Circle")
        self.addOption(self.shapesButton.menu, "Line")
        self.addOption(self.shapesButton.menu, "Oval")
        self.addOption(self.shapesButton.menu, "Star")
        
        #Zoom
        self.zoomImg = PhotoImage(file = "Assets/magnifyGruv.png")
        self.zoomButton = Button(self.root, highlightthickness = 0,relief = FLAT, bg = '#282828', 
                                 command = lambda: self.setActiveTool("zoom"), image = self.zoomImg)
        self.zoomButton.place(x = 75, y = 450)

        #Bucket
        self.fillImg = PhotoImage(file = "Assets/bucketGruv.png")
        self.bucketButton = Button(self.root, highlightthickness = 0, relief = FLAT, bg = '#282828', 
                                   command = lambda: self.setActiveTool("bucket"), image = self.fillImg)
        self.bucketButton.place(x = 10, y = 530)
        #pixelJump
        self.pJump = Entry(self.root, width = 3, highlightthickness=0, justify="center", 
                            bg= '#ebdbb2', relief = FLAT, fg = '#282828')
        self.pJump.place(x = 80, y = 540)
        self.pJump.insert(0, "20")

        # N-Polygon Button
        self.N = PhotoImage(file = "Assets/hexagonGruv.png")
        self.nPolygonButton = Button(self.root, highlightthickness=0, relief = FLAT, bg = '#282828', 
                                     command = lambda: self.setActiveTool("ngon"), image = self.N)
        self.nPolygonButton.place(x = 10, y = 610)
        # N Entry
        self.nEntry = Entry(self.root, width = 3, highlightthickness=0, justify="center", 
                            bg= '#ebdbb2', relief = FLAT, fg = '#282828')
        self.nEntry.place(x = 80, y = 620)
        self.nEntry.insert(0, "3")

        #Select
        self.select = PhotoImage(file = "Assets/selectGruv.png")
        self.selectButton = Button(self.root, highlightthickness = 0, relief = FLAT, bg = '#282828', 
                                   command = lambda: self.setActiveTool("sele"), image = self.select)
        self.selectButton.place(x = 10, y = 720)

        #Clear
        self.trashImg = PhotoImage(file = "Assets/binGruv.png")
        self.clearButton = Button(self.root, highlightthickness = 0, relief = FLAT, bg = '#282828', 
                                  command = self.clearScreen, image = self.trashImg)
        self.clearButton.place(x = 75, y = 720)

        #Save
        self.save = PhotoImage(file = "Assets/downloadGruv.png")
        self.saveButton = Button(self.root, highlightthickness = 0, relief = FLAT, bg = '#282828', 
        command = self.saveCanvas, image = self.save)
        self.saveButton.place(x = 5, y = 800)

        #Load
        self.load = PhotoImage(file = "Assets/uploadGruv.png")
        self.loadButton = Button(self.root, highlightthickness = 0, relief = FLAT, bg = '#282828', 
        command = self.loadCanvas, image = self.load)
        self.loadButton.place(x = 75, y = 800)

        #Pen Width
        self.sizeSlider = Scale(self.root, from_=40, to=20, highlightthickness = 0, 
                                        fg = '#ebdbb2', orient=VERTICAL, bg = '#282828')
        self.sizeSlider.grid(row=16, column=0, rowspan = 4, sticky='NS', padx=25, pady = 20)

        self.can = Canvas(self.root, bg='#ebdbb2', width=1920, height=1080)
        self.can.grid(rowspan = 20, column=2, row = 0)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.defaultColour = '#282828' 
        self.backgroundColour = '#ebdbb2'
        #pen
        self.prev_x = None
        self.prev_y = None
        self.eraserActive = False
        #shapes
        self.firstX = None
        self.firstY = None
        self.shapeItem = None
        #selection
        self.finalX = None
        self.finalY = None
        #loadcanvas + select
        self.image = None
        #zoom
        self.zoomScale = 2
        self.zoomed = False
        self.zoomX = None 
        self.zoomY = None
        #general
        self.lineWidth = 5
        self.colour = self.defaultColour
        self.activeTool = "pen"
        self.shapes =  ("line", "curv", "rect", "oval", "squa", "circ", "star", "ngon")
        self.controlPoints = []
        #binds
        self.can.bind('<Button-1>', self.tap)
        self.can.bind('<B1-Motion>', self.drag)
        self.can.bind('<ButtonRelease-1>', self.lift)

    def addOption(self, menu, label):
        menu.add_command(label=label, command=lambda: self.setActiveTool(label))

    def usePen(self):
        self.can.delete(self.shapeItem)
        self.setActiveTool("pen")
        self.eraserActive = False

    def getHexOfPixel(self, x, y):
        #taking a 'screenshot'
        image = ImageGrab.grab()
        #getting the colours from that screenshot
        rgb = image.getpixel((x, y))
        #converts rgb code to hex code and returns
        return '#%02x%02x%02x' % rgb

    def getPixelColour(self, event):
        #Coordinates of clicked pixel

        # self.root.winfo_x = starting x pixel of program on the screen
        # 140 =               compensate for the button menu
        # event.x =           x pixel of JUST the click point on the canvas from the NW anchor
        x = self.root.winfo_x() + 140 + event.x
        y = self.root.winfo_y() + event.y
        #get hex value
        hex = self.getHexOfPixel(x, y)
        #calls updateColour function with the hex
        self.updateColour(hex)
        #changing the tool back to pen again
        self.setActiveTool("pen")
        self.eraserActive = False

    def updateColour(self, col):
        print("COLOUR UPDATED:",col)
        self.eraserActive = False
        self.colour = col

    def clearScreen(self):
        print("Screen cleared.")
        if self.activeTool != "move": #usual
            self.can.delete("all") 
        else:                       #clear when area is selected
            self.can.create_rectangle(self.firstX, self.firstY, self.finalX, self.finalY,
                                      width = 0, fill = self.backgroundColour)
            self.setActiveTool("select")
            self.finalX = None
            self.finalY = None
            self.firstX = None
            self.firstY = None
            self.can.delete(self.shapeItem)

    def useEraser(self):
        self.setActiveTool("pen")
        self.eraserActive = True

    def saveCanvas(self):
        print("Image saved.")
        #filename = filedialog.askopenfilename(initialdir = "/home/vagabond/Documents/Paint/Saved",title = "Select file",filetypes = (("png files","*.png"), ("all files", "*.*")))
        saveDate = time.strftime("%I:%M:%S", time.localtime())
        dir = "/home/vagabond/Documents/Paint/Saved/canvas_" + saveDate + ".png"
        x = self.root.winfo_x() + 140
        y = self.root.winfo_y()
        ImageGrab.grab(bbox = (x, y, x + 1780, y + 1080)).save(dir)

    def loadCanvas(self):
        filename = filedialog.askopenfilename(initialdir = "/home/vagabond/Documents/Paint/Saved",title = "Select file",filetypes = (("png files","*.png"), ("all files", "*.*")))
        self.image = ImageTk.PhotoImage(Image.open(filename))
        self.can.create_image(0, 0, image = self.image, anchor = NW)
        self.can.delete(self.image)
        print("Image loaded.")

    def paint(self, event):
        self.lineWidth = self.sizeSlider.get()
        if self.zoomed:
            self.lineWidth *= 2
        if self.eraserActive:
            paintColour = self.backgroundColour
        else:
            paintColour = self.colour
        if self.prev_x and self.prev_y:
            self.can.create_line(self.prev_x, self.prev_y, event.x, event.y,
                               width=self.lineWidth, fill=paintColour,
                               capstyle=ROUND, smooth=TRUE)
        self.prev_x = event.x 
        self.prev_y = event.y

    def fillColour(self, event):
        pixelJump = 20
        pJump = self.pJump.get()
        if pJump.isdigit():
            if int(pJump) >= 5 and int(pJump) <= 20:
                pixelJump = int(pJump)
            else:
                print("Invalid value of pixelJump.")

        #Coordinates of clicked pixel
        x = self.root.winfo_x() + 140 + event.x
        y = self.root.winfo_y() + event.y

        #For drawing later
        xMinus = (140 + self.root.winfo_x())
        yMinus = self.root.winfo_y()

        #For upper canvas bounds
        xLimit = self.root.winfo_x() + 1920
        yLimit = self.root.winfo_y() + 1080

        #hexcode of click point
        originalHex = self.getHexOfPixel(x, y)

        #Hardcoding in the first point
        oldX, oldY = x, y
        pixels = [(x, y)]
        pixelCount = 1;

        #Big brain memoization idea holy fucking shit
        pixelsChecked = set()

        #While pixels exists
        while pixels:
            #Assign top-most value in list to newX & newY
            newX, newY = pixels.pop(0)
            pixelCount -= 1
            print("Current number of pixels to check:",pixelCount)

            #if within bounds and un-visited
            if 0 < newX < xLimit and 0 < newY < yLimit and (newX, newY) not in pixelsChecked:
                #Get the pixel color at the current position
                newHex = self.getHexOfPixel(newX, newY)
                #Check if the pixel color is the same as the original color
                if newHex == originalHex:
                    #Set the fill color at the current position
                    self.can.create_line(oldX - xMinus, oldY - yMinus, newX - xMinus, newY - yMinus, 
                                 width = pixelJump, smooth=True, capstyle=ROUND, fill = self.colour)
                    #Adding cardinal directions to pixels
                    pixels.extend([(newX + pixelJump, newY), (newX - pixelJump, newY), 
                                   (newX, newY + pixelJump), (newX, newY - pixelJump)])
                    pixelCount += 4
                    pixelsChecked.add((newX, newY))
                    #Replacing values
                    oldX, oldY = newX, newY

    def setActiveTool(self, tool):
        tool = tool.lower()
        if len(tool) > 4:
            tool = tool[0:4]
        self.activeTool = tool
        print("NEW TOOL: " + tool)

    def updateFirstPixel(self, event):
        self.firstX = event.x
        self.firstY = event.y

    def zoomer(self, event):
        if not self.zoomed:
            print("ZOOMED IN.")
            x, y = event.x, event.y
            self.zoomX, self.zoomY = x, y
            self.can.scale('all', x, y, self.zoomScale, self.zoomScale)
        else:
            print("ZOOMED OUT.")
            self.can.scale('all', self.zoomX, self.zoomY, 1/self.zoomScale, 1/self.zoomScale)
        self.zoomed = not self.zoomed
        self.setActiveTool("pen")

    def drawLine(self, event):
        self.lineWidth = self.sizeSlider.get()
        if self.zoomed:
            self.lineWidth *= 2
        if self.shapeItem:
            self.can.delete(self.shapeItem)
        self.shapeItem = self.can.create_line(self.firstX, self.firstY, event.x, event.y, 
                                              width=self.lineWidth, fill = self.colour,
                                              capstyle=ROUND, smooth=TRUE)
        
    def drawCurve(self, event):
        self.lineWidth = self.sizeSlider.get()
        if self.zoomed:
            self.lineWidth *= 2
        if self.shapeItem:
            self.can.delete(self.shapeItem)

        if event.x >= self.firstX and event.y <= self.firstY:
            startAngle = 0
            endAngle = 180
        elif event.x <= self.firstX and event.y <= self.firstY:
            startAngle = 180
            endAngle = 0
        elif event.x >= self.firstX and event.y >= self.firstY:
            startAngle = 0
            endAngle = -180
        elif event.x <= self.firstX and event.y >= self.firstY:
            startAngle = -180
            endAngle = 0

        self.shapeItem = self.can.create_arc(self.firstX, self.firstY, event.x, event.y, 
                                             start = startAngle, extent = endAngle - startAngle,
                                            width=self.lineWidth, fill=self.colour, style = ARC)                                        
    
    def drawRect(self, event, squareBool = False):
        self.lineWidth = self.sizeSlider.get()
        if self.zoomed:
            self.lineWidth *= 2
        if self.shapeItem:
            self.can.delete(self.shapeItem)
        if not squareBool:
            self.shapeItem = self.can.create_rectangle(self.firstX, self.firstY, event.x, event.y, 
                                                       width=self.lineWidth, outline = self.colour)
        else:
            length = max(abs(event.x - self.firstX), abs(event.y - self.firstY))
            self.shapeItem = self.can.create_rectangle(self.firstX, self.firstY, 
                                                       self.firstX + length, self.firstY + length, 
                                                       width=self.lineWidth, outline = self.colour)

    def drawOval(self, event, circleBool = False):
        self.lineWidth = self.sizeSlider.get()
        if self.zoomed:
            self.lineWidth *= 2
        if self.shapeItem:
            self.can.delete(self.shapeItem)
        if not circleBool:
            self.shapeItem = self.can.create_oval(self.firstX, self.firstY, event.x, event.y, 
                                                  width=self.lineWidth, outline = self.colour)
        else:
            length = max(abs(event.x - self.firstX), abs(event.y - self.firstY))
            self.shapeItem = self.can.create_oval(self.firstX, self.firstY, 
                                                  self.firstX + length, self.firstY + length,
                                                  width=self.lineWidth, outline = self.colour)

    def drawStar(self, event):
        self.lineWidth = self.sizeSlider.get()
        if self.zoomed:
            self.lineWidth *= 2
        if self.shapeItem:
            self.can.delete(self.shapeItem)
        xMid = (event.x + self.firstX) / 2
        yMid = (event.y + self.firstY) / 2
        d = math.dist([self.firstX, self.firstY], [event.x, event.y])
        angle = math.atan2(event.y - self.firstY, event.x - self.firstX)
        points = []
        for i in range(10):
            if i % 2 == 0:
                theta = angle + i * math.pi / 5
                x = xMid + d * math.cos(theta)
                y = yMid + d * math.sin(theta)
            else:
                theta = angle + i * math.pi / 5
                x = xMid + (d / 2) * math.cos(theta)
                y = yMid + (d / 2) * math.sin(theta)
            points.append(x)
            points.append(y)
        self.shapeItem = self.can.create_polygon(points, fill='', outline=self.colour, width=self.lineWidth)

    def drawPoly(self, event):
        N = 3
        n = self.nEntry.get()  # Get the value of N from the entry
        if n.isdigit():
            if int(n) >= 3:
                N=int(n)
            elif int(n) <= 3:
                print("Invalid input for N.")
        self.lineWidth = self.sizeSlider.get()
        if self.zoomed:
            self.lineWidth *= 2
        if self.shapeItem:
            self.can.delete(self.shapeItem)
        points = []
        xMid = event.x
        yMid = event.y
        radius = abs(self.firstX - event.x)
        angle = -math.pi / 2  # Starting angle (-90 degrees) for proper alignment
        for i in range(N):
            x = xMid + radius * math.cos(2 * math.pi * i / N + angle)
            y = yMid + radius * math.sin(2 * math.pi * i / N + angle)
            points.append((x, y))
        self.shapeItem = self.can.create_polygon(points, fill='', outline=self.colour, width=self.lineWidth)

    def makeSelection(self, event):
        if self.shapeItem:
            self.can.delete(self.shapeItem)
        self.shapeItem = self.can.create_rectangle(self.firstX, self.firstY, event.x, event.y, 
                                                       width=1, outline = self.defaultColour)

    def moveTap(self, event):
        x = self.root.winfo_x() + 140
        y = self.root.winfo_y()

        self.can.delete(self.shapeItem)
        self.can.delete(self.image)

        a, b, c, d = self.firstX, self.firstY, self.finalX, self.finalY
        if self.finalX < self.firstX:
            self.firstX, self.finalX = self.finalX, self.firstX
        if self.finalY < self.firstY:
            self.firstY, self.finalY = self.finalY, self.firstY
        #Image object formed.
        saveDate = time.strftime("%I:%M:%S", time.localtime())
        dir = "/home/vagabond/Documents/Paint/MovingJunk/cut_" + saveDate + ".png"
        
        #saving as image
        ImageGrab.grab(bbox = (x + self.firstX + 1, y + self.firstY + 1, x + self.finalX, y + self.finalY)).save(dir)
        
        #deleting the backside
        self.can.create_rectangle(a, b, c, d, width = 0, fill = self.backgroundColour)
        
        #importing as image
        image = ImageTk.PhotoImage(Image.open(dir))
        self.image = self.can.create_image(a, b, anchor = NW, image = image)
        self.image.show()
        
    def moveImage(self, event):
        if self.prev_x and self.prev_y:
            x = event.x - self.prev_x
            y = event.y - self.prev_y
            self.can.move(self.image, x, y)
        self.prev_x, self.prev_y = event.x, event.y
        
    def drag(self, event):
        match self.activeTool:
            case "pen":
                self.paint(event)
            case "line":
                self.drawLine(event)
            case "squa":
                self.drawRect(event, True)
            case "circ":
                self.drawOval(event, True)
            case "ngon":
                self.drawPoly(event)
            case "star":
                self.drawStar(event)
            case "oval":
                self.drawOval(event)
            case "rect":
                self.drawRect(event)
            case "curv":
                self.drawCurve(event)
            case "sele":
                self.makeSelection(event)
            case "move":
                self.moveImage(event)

    def tap(self, event):
        if self.activeTool == "drop":
            self.getPixelColour(event)
        elif self.activeTool == "buck":
            self.fillColour(event)
        elif (self.activeTool in self.shapes) or (self.activeTool == "sele"):
            self.updateFirstPixel(event)    
        elif self.activeTool == "move":
            self.moveTap(event)   
        elif self.activeTool == "zoom":
            self.zoomer(event)

    def lift(self, event):
        if self.activeTool == "pen":
            self.resetXY()
        elif self.activeTool in self.shapes:
            self.resetShape()
        elif self.activeTool == "sele":
            self.finishSelection(event)
        elif self.activeTool == "move":
            self.finishMoving()
            
    def finishMoving(self):
        self.firstX = None
        self.firstY = None
        self.prev_x = None        
        self.prev_y = None                
        self.image = None
        self.setActiveTool("pen")

    def resetShape(self):
        print("Shape drawn.")
        self.shapeItem = None
        self.firstX = None
        self.firstY = None
    
    def finishSelection(self, event):
        if self.shapeItem:
            self.finalX, self.finalY = event.x, event.y
            self.setActiveTool("move")

    def resetXY(self):
        self.prev_x, self.prev_y = None, None
           
if __name__ == '__main__':
    Paint()
