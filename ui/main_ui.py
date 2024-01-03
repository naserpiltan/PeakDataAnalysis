import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView
from PySide6 import QtCore
import os
import sys

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType
from controller import Controller

def qt_message_handler(mode, context, message):
    if mode == QtCore.QtI:
        mode = 'Info'
    elif mode == QtCore.QtWarningMsg:
        mode = 'Warning'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'critical'
    elif mode == QtCore.QtFatalMsg:
        mode = 'fatal'
    else:
        mode = 'Debug'
    print("%s: %s (%s:%d, %s)" % (mode, message, context.file, context.line, context.file))

if __name__ == "__main__":
    #os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    #QtCore.qInstallMessageHandler(qt_message_handler)

    app = QGuiApplication(sys.argv)
    #controller = Controller()
    engine = QQmlApplicationEngine()
    qmlRegisterType(Controller, 'Controller', 1, 0, 'Controller')

    #engine.rootContext().setContextProperty("controller", controller)
    engine.load('main.qml')
    engine.quit.connect(app.quit)
    sys.exit(app.exec())
