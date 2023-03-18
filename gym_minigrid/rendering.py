import numpy as np
import pygame
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor, QPolygon
# from PyQt5.QtCore import QPoint, QSize, QRect
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit
# from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QFrame

class Window:
    """
    Simple application window to render the environment into
    """

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('MiniGrid Gym Environment')

        # # Image label to display the rendering
        # self.imgLabel = QLabel()
        # self.imgLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        # # Text box for the mission
        # self.missionBox = QTextEdit()
        # self.missionBox.setReadOnly(True)
        # self.missionBox.setMinimumSize(400, 100)

        # # Center the image
        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(self.imgLabel)
        # hbox.addStretch(1)

        # # Arrange widgets vertically
        # vbox = QVBoxLayout()
        # vbox.addLayout(hbox)
        # vbox.addWidget(self.missionBox)

        # # Create a main widget for the window
        # mainWidget = QWidget(self)
        # self.setCentralWidget(mainWidget)
        # mainWidget.setLayout(vbox)

        # # Show the application window
        # self.show()
        # self.setFocus()

        self.closed = False

        # # Callback for keyboard events
        self.keyDownCb = None

    def setWindowTitle(self, title):
        pygame.display.set_caption(title)

    def closeEvent(self, event=None):
        self.closed = True
        pass

    def setPixmap(self, pixmap):
        # self.imgLabel.setPixmap(pixmap)
        pass

    def setText(self, text):
        # self.missionBox.setPlainText(text)
        pass

    def setKeyDownCb(self, callback):
        self.keyDownCb = callback
        pass

    def keyPressEvent(self, e):
        if self.keyDownCb == None:
            return

        keyName = None
        if e.key == pygame.K_LEFT:
            keyName = 'LEFT'
        elif e.key == pygame.K_RIGHT:
            keyName = 'RIGHT'
        elif e.key == pygame.K_UP:
            keyName = 'UP'
        elif e.key == pygame.K_DOWN:
            keyName = 'DOWN'
        elif e.key == pygame.K_SPACE:
            keyName = 'SPACE'
        elif e.key == pygame.K_RETURN:
            keyName = 'RETURN'
        elif e.key == pygame.K_LALT or e.key == pygame.K_RALT:
            keyName = 'ALT'
        elif e.key == pygame.K_LCTRL or e.key == pygame.K_RCTRL:
            keyName = 'CTRL'
        elif e.key == pygame.K_PAGEUP or e.key == pygame.K_u:
            keyName = 'PAGE_UP'
        elif e.key == pygame.K_PAGEDOWN or e.key == pygame.K_d:
            keyName = 'PAGE_DOWN'
        elif e.key == pygame.K_BACKSPACE:
            keyName = 'BACKSPACE'
        elif e.key == pygame.K_ESCAPE:
            keyName = 'ESCAPE'

        if keyName == None:
            return
        self.keyDownCb(keyName)
        pass

class Renderer:
    def __init__(self, width, height, ownWindow=False):
        self.width = width
        self.height = height

        # self.img = QImage(width, height, QImage.Format_RGB888)
        # self.painter = QPainter()

        self.window = None
        if ownWindow:
            self.screen = pygame.display.set_mode((width, height))
            pygame.init()
            self.window = Window()
        #     self.app = QApplication([])
        pass

    def close(self):
        """
        Deallocate resources used
        """
        self.window.closeEvent()
        pass

    def beginFrame(self):
        # self.painter.begin(self.img)
        # self.painter.setRenderHint(QPainter.Antialiasing, False)

        # # Clear the background
        self.screen.fill((0, 0, 0))
        self.setLineColor(255, 255, 255)
        self.setColor(255, 255, 255)
        self.setLineWidth(1)
        # self.painter.setBrush(QColor(0, 0, 0))
        # self.painter.drawRect(0, 0, self.width - 1, self.height - 1)
        self.transforms = []
        self.transform = np.identity(3)
        self.transforms.append(self.transform)

    def endFrame(self):
        pygame.display.flip()
        # self.painter.end()

        if self.window:
            if self.window.closed:
                pygame.quit()
                self.window = None
            else:
                # self.window.setPixmap(self.getPixmap())
                self.processEvents()
        pass

    def getPixmap(self):
        # return QPixmap.fromImage(self.img)
        return None

    def processEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.window.closeEvent(event)
            if event.type == pygame.KEYDOWN:
                self.window.keyPressEvent(event)

    def getArray(self):
        """
        Get a numpy array of RGB pixel values.
        The array will have shape (height, width, 3)
        """

        # numBytes = self.width * self.height * 3
        # buf = self.img.bits().asstring(numBytes)
        # output = np.frombuffer(buf, dtype='uint8')
        # output = output.reshape((self.height, self.width, 3))

        # return output
        return None

    def apply_transform(self, t):
        self.transforms[-1] = np.dot(self.transforms[-1], t)
        self.transform = np.dot(self.transform, t)

    def transform_point(self, x, y):
        p =  np.dot(self.transform, np.array((x, y, 1)))
        return (p[0], p[1])

    def push(self):
        self.transforms.append(np.identity(3))

    def pop(self):
        del self.transforms[-1]
        if len(self.transforms) == 0:
            self.push()
        self.transform = np.identity(3)
        for t in self.transforms:
            self.transform = np.dot(self.transform, t)
    
    def rotate(self, degrees):
        theta = np.radians(degrees)
        c  , s = np.cos(theta), np.sin(theta)
        t = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))
        self.apply_transform(t)

    def translate(self, x, y):
        self.apply_transform(np.array(((1, 0, x), (0, 1, y), (0, 0, 1))))

    def scale(self, x, y):
        self.apply_transform(np.array(((x, 0, 0), (0, y, 0), (0, 0, 1))))

    def setLineColor(self, r, g, b, a=255):
        self.line_color = (r, g, b, a)

    def setColor(self, r, g, b, a=255):
        self.fill_color = (r, g, b, a)

    def setLineWidth(self, width):
        self.line_width = width

    def drawLine(self, x0, y0, x1, y1):
        p1 = self.transform_point(x0, y0)
        p2 = self.transform_point(x1, y1)
        pygame.draw.line(self.screen, self.line_color, p1, p2, self.line_width)

    def drawCircle(self, x, y, r):
        steps = 8
        step = np.radians(360) / steps
        points = []
        for i in range(steps):
            theta = i * step
            points.append((x + r * np.cos(theta),y + r * np.sin(theta)))

        self.drawPolygon(points)

    def drawPolygon(self, points):
        transformed_points = list(map(lambda p: self.transform_point(p[0], p[1]), points))
        """Takes a list of points (tuples) as input"""
        if self.fill_color[3] == 255: 
            # Draw only if visible
            pygame.draw.polygon(self.screen, self.fill_color, transformed_points, 0)
        elif self.fill_color[3] != 0: 
            # Draw in separate surface if transparent
            minx, miny, maxx, maxy = float('inf'), float('inf'), 0, 0
            for p in transformed_points:
                minx = min(minx, p[0])
                miny = min(miny, p[1])
                maxx = max(minx, p[0])
                maxy = max(maxy, p[1])
            surface_points = []
            for p in transformed_points:
                surface_points.append((p[0] - minx, p[1] - miny))

            s = pygame.Surface((maxx-minx, maxy-miny)) 
            s.set_alpha(self.fill_color[3]) 
            pygame.draw.polygon(s, self.fill_color, surface_points, 0)
            self.screen.blit(s, (minx, miny))
        
        if self.line_color[3] != 0: # Draw only if visible
            pygame.draw.polygon(self.screen, self.line_color, transformed_points, self.line_width)

    def drawPolyline(self, points):
        transformed_points = list(map(lambda p: self.transform_point(p[0], p[1]), points))
        """Takes a list of points (tuples) as input"""
        pygame.draw.lines(self.screen, self.line_color, False, transformed_points, self.line_width)

    def fillRect(self, x, y, width, height, r, g, b, a=255):
        self.setColor(r, g, b, a)
        self.setLineColor(0, 0, 0, 0)
        points = [ (x, y), 
                   (x, y + height), 
                   (x + width, y + height), 
                   (x + width, y)]
        self.drawPolygon(points)
