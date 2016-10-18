QT += core
QT += network
QT -= gui

TARGET = Quiz
CONFIG += console
CONFIG -= app_bundle

QMAKE_CXXFLAGS += -std=c++11

TEMPLATE = app

SOURCES += \
    Crawler.cpp \
    Main.cpp \
    NetworkAccessManager.cpp \
    Levenshtein.cpp

HEADERS += \
    Crawler.h \
    NetworkAccessManager.h \
    Levenshtein.h

OTHER_FILES += \
    LEIAME.txt
