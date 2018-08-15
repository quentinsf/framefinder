#! /usr/bin/env python3

import glob
import itertools
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget


class FFWindow(QtWidgets.QWidget):

    def __init__(self, video_files):
        super().__init__()

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.video_files = video_files

        # w = QtWidgets.QWidget()
        self.setWindowTitle('FrameFinder')
        
        l1 = QtWidgets.QLabel()
        l1.setText("Select the best frame")

        self.video_widget = QVideoWidget()
        
        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.playButton = QtWidgets.QPushButton()
        self.playButton.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.playtoggle)

        self.errorLabel = QtWidgets.QLabel()
        # self.errorLabel.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
        #     QtWidgets.QSizePolicy.Maximum)

        self.fileLabel = QtWidgets.QLabel()

        self.next_but = QtWidgets.QPushButton()
        self.next_but.setText("Next")
        self.next_but.clicked.connect(self.next_video)

        video_vbox = QtWidgets.QVBoxLayout()
        video_vbox.addWidget(self.video_widget, 1)
        video_vbox.addWidget(self.position_slider)
        video_vbox.addWidget(self.playButton)
        video_vbox.addWidget(self.errorLabel)
        video_vbox.addWidget(self.fileLabel)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(l1)
        # v_box.addStretch()
        v_box.addLayout(video_vbox)
        v_box.addWidget(self.next_but)
        # v_box.addStretch()

        self.setLayout(v_box)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.status_changed)
        # self.media_player.availabilityChanged.connect(self.status_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.error.connect(self.handleError)

        self.next_video()

        # Set up some keyboard shortcuts
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("p"), self)
        shortcut.activated.connect(self.playtoggle)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("n"), self)
        shortcut.activated.connect(self.next_video)


    def next_video(self):
        # Display the next file if there is one
        try:
            self.errorLabel.clear()
            next_video = os.path.join(os.getcwd(), next(self.video_files))
            print(next_video)

            self.pause()
            self.media = QMediaContent(
                QtCore.QUrl.fromLocalFile(next_video)
            )
            self.media_player.setMedia(self.media)
            self.fileLabel.setText(next_video)
            self.play()

        except StopIteration:
            pass

    def playtoggle(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def pause(self):
        print("Pausing")
        self.media_player.pause()

    def play(self):
        print("Playing")
        self.media_player.play()
        
    def status_changed(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.playButton.repaint()
        # print ("Status", self.media_player.mediaStatus())

    def position_changed(self, position):
        print("Position changed to", position)
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        print("Duration changed to", duration)
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def handleError(self):
        self.errorLabel.setText("Error: " + self.media_player.errorString())


def main():
    app = QtWidgets.QApplication(sys.argv)
    videos = itertools.cycle(iter(glob.glob("movies/*.mp4")))
    w = FFWindow(videos)
    w.resize(1024, 768)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
