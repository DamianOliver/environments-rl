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
        elif e.key == pygame.K_PAGEUP:
            keyName = 'PAGE_UP'
        elif e.key == pygame.K_PAGEDOWN:
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
        # self.painter.setBrush(QColor(0, 0, 0))
        # self.painter.drawRect(0, 0, self.width - 1, self.height - 1)
        pass

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

    def push(self):
        # self.painter.save()
        pass

    def pop(self):
        # self.painter.restore()
        pass

    def rotate(self, degrees):
        # self.painter.rotate(degrees)
        pass

    def translate(self, x, y):
        # self.painter.translate(x, y)
        pass

    def scale(self, x, y):
        # self.painter.scale(x, y)
        pass

    def setLineColor(self, r, g, b, a=255):
        # self.painter.setPen(QColor(r, g, b, a))
        pass

    def setColor(self, r, g, b, a=255):
        # self.painter.setBrush(QColor(r, g, b, a))
        pass

    def setLineWidth(self, width):
        # pen = self.painter.pen()
        # pen.setWidthF(width)
        # self.painter.setPen(pen)
        pass

    def drawLine(self, x0, y0, x1, y1):
        # self.painter.drawLine(x0, y0, x1, y1)
        pass

    def drawCircle(self, x, y, r):
        # center = QPoint(x, y)
        # self.painter.drawEllipse(center, r, r)
        pass

    def drawPolygon(self, points):
        """Takes a list of points (tuples) as input"""
        # points = map(lambda p: QPoint(p[0], p[1]), points)
        # self.painter.drawPolygon(QPolygon(points))
        pass

    def drawPolyline(self, points):
        # """Takes a list of points (tuples) as input"""
        # points = map(lambda p: QPoint(p[0], p[1]), points)
        # self.painter.drawPolyline(QPolygon(points))
        pass

    def fillRect(self, x, y, width, height, r, g, b, a=255):
        # self.painter.fillRect(QRect(x, y, width, height), QColor(r, g, b, a))
        pass
