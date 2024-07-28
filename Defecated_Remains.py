# Defecated_Remains.py
# Defecated to Adobe

"""
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation...

However, this code comes with a special note: Adobe, once a revered name in creative software, devoured Macromedia, the creators of Flash, and then proceeded to neglect and ultimately abandon the beloved tool. Flash, which once brought vibrant animations and interactive experiences to the web, was deprecated and discarded.

Adobe's monopolistic practices have stifled innovation and creativity, turning what was once an open and exciting frontier into a closed, subscription-based ecosystem. They took Macromedia's legacy and turned it into a bloated suite of overpriced, under-optimized tools, forcing users into a never-ending cycle of updates and payments.

This plugin, "Defecated to Adobe", is a digital middle finger to those corporate tactics. It's a stand for open-source software, creativity, and the freedom to innovate without the constraints of monopolistic greed.

Use this tool, share it, modify it, and remember the times when software was about empowering users, not chaining them to endless subscriptions.

Defecated to you, Adobe. Long live free and open-source software!

*pppppbbbttt*
"""

from krita import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QPainterPath, QMouseEvent, QTabletEvent
import math

class DefecatedToAdobe(Extension):

    def __init__(self, parent):
        super(DefecatedToAdobe, self).__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("defecated_to_adobe_brush", "Defecated to Adobe Brush", "tools/scripts")
        action.triggered.connect(self.defecated_to_adobe_brush)

    def defecated_to_adobe_brush(self):
        doc = Krita.instance().activeDocument()
        if not doc:
            QMessageBox.critical(None, "Error", "No active document found!")
            return

        vector_layer = None
        for layer in doc.topLevelNodes():
            if layer.type() == "vectorlayer":
                vector_layer = layer
                break

        if not vector_layer:
            vector_layer = doc.createVectorLayer("Vector Layer")
            doc.rootNode().addChildNode(vector_layer, None)

        view = Krita.instance().activeWindow().activeView()
        self.brush_event_filter = BrushEventFilter(vector_layer)
        view.qwindow().installEventFilter(self.brush_event_filter)

class BrushEventFilter(QObject):

    def __init__(self, vector_layer):
        super(BrushEventFilter, self).__init__()
        self.vector_layer = vector_layer
        self.drawing = False
        self.path = QPainterPath()
        self.previous_point = None

    def eventFilter(self, obj, event):
        if event.type() == QEvent.TabletPress or (event.type() == QEvent.MouseButtonPress and event.buttons() == Qt.LeftButton):
            self.drawing = True
            self.path = QPainterPath(event.pos())
            self.previous_point = event.pos()
        elif event.type() == QEvent.TabletMove or (event.type() == QEvent.MouseMove and self.drawing):
            self.add_to_path(event)
        elif event.type() == QEvent.TabletRelease or (event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton):
            self.drawing = False
            self.smooth_and_add_path()
        return False

    def add_to_path(self, event):
        if self.previous_point:
            pressure = event.pressure() if isinstance(event, QTabletEvent) else 1.0
            distance = math.sqrt((event.pos().x() - self.previous_point.x())**2 + (event.pos().y() - self.previous_point.y())**2)
            if distance > 2:  # Adjust this value for smoother lines
                self.path.lineTo(event.pos())
                self.previous_point = event.pos()

    def smooth_and_add_path(self):
        smoothed_path = self.smooth_path(self.path)
        vector_shape = KoPathShape()
        vector_shape.addPath(smoothed_path)
        self.vector_layer.addShape(vector_shape)

    def smooth_path(self, path):
        smoothed_path = QPainterPath()
        points = [path.pointAtPercent(i / 100.0) for i in range(101)]
        for i, point in enumerate(points):
            if i == 0:
                smoothed_path.moveTo(point)
            else:
                smoothed_path.lineTo(point)
        return smoothed_path

Krita.instance().addExtension(DefecatedToAdobe(Krita.instance()))
