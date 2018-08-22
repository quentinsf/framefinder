#! /usr/bin/env python3

import glob
import itertools
import os
import subprocess
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaMetaData
from PyQt5.QtMultimediaWidgets import QVideoWidget


class FFWindow(QtWidgets.QWidget):

    def __init__(self, video_files):
        super().__init__()

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.video_files = video_files

        self.setWindowTitle('FrameFinder')
        
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 360)
        
        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)


        self.errorLabel = QtWidgets.QLabel()
        # self.errorLabel.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
        #     QtWidgets.QSizePolicy.Maximum)

        self.fileLabel = QtWidgets.QLabel()

        self.rewind_but = QtWidgets.QPushButton()
        self.rewind_but.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_ArrowLeft))
        self.rewind_but.setText("Normal [A]")
        self.rewind_but.clicked.connect(self.rewind)

        self.slow_rewind_but = QtWidgets.QPushButton()
        self.slow_rewind_but.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_ArrowLeft))
        self.slow_rewind_but.setText("Slow [S]")
        self.slow_rewind_but.clicked.connect(self.slow_rewind)

        self.play_but = QtWidgets.QPushButton()
        self.play_but.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.play_but.setText("[D]")
        self.play_but.clicked.connect(self.playtoggle)

        self.slow_forward_but = QtWidgets.QPushButton()
        self.slow_forward_but.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_ArrowRight))
        self.slow_forward_but.setText("Slow [F]")
        self.slow_forward_but.clicked.connect(self.slow_forward)

        self.forward_but = QtWidgets.QPushButton()
        self.forward_but.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_ArrowRight))
        self.forward_but.setText("Normal [G]")
        self.forward_but.clicked.connect(self.forward)

        self.fast_forward_but = QtWidgets.QPushButton()
        self.fast_forward_but.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_ArrowRight))
        self.fast_forward_but.setText("Fast [H]")
        self.fast_forward_but.clicked.connect(self.fast_forward)

        self.snapshot_but = QtWidgets.QPushButton()
        self.snapshot_but.setText("Snapshot [P]")
        self.snapshot_but.clicked.connect(self.take_snapshot)

        self.mark_but = QtWidgets.QPushButton()
        self.mark_but.setText("Mark")
        self.mark_but.clicked.connect(self.mark)

        self.next_but = QtWidgets.QPushButton()
        self.next_but.setText("Next")
        self.next_but.clicked.connect(self.next_video)

        video_vbox = QtWidgets.QVBoxLayout()
        video_vbox.addWidget(self.video_widget, 100)
        video_vbox.addWidget(self.position_slider)
        control_box = QtWidgets.QHBoxLayout()
        control_box.addWidget(self.rewind_but)
        control_box.addWidget(self.slow_rewind_but)
        control_box.addWidget(self.play_but)
        control_box.addWidget(self.slow_forward_but)
        control_box.addWidget(self.forward_but)
        control_box.addWidget(self.fast_forward_but)
        video_vbox.addLayout(control_box)

        video_vbox.addWidget(self.errorLabel)
        video_vbox.addWidget(self.fileLabel)

        file_box = QtWidgets.QHBoxLayout()
        file_box.addWidget(self.snapshot_but)
        file_box.addWidget(self.mark_but)
        file_box.addWidget(self.next_but)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addLayout(video_vbox)

        v_box.addLayout(file_box)
        v_box.addStretch()

        self.setLayout(v_box)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.status_changed)
        # self.media_player.availabilityChanged.connect(self.status_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.error.connect(self.handleError)

        self.next_video()

        # Set up some keyboard shortcuts

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("a"), self)
        shortcut.activated.connect(self.rewind_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("s"), self)
        shortcut.activated.connect(self.slow_rewind_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("d"), self)
        shortcut.activated.connect(self.play_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("f"), self)
        shortcut.activated.connect(self.slow_forward_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("g"), self)
        shortcut.activated.connect(self.forward_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("h"), self)
        shortcut.activated.connect(self.fast_forward_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("p"), self)
        shortcut.activated.connect(self.snapshot_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("n"), self)
        shortcut.activated.connect(self.next_but.animateClick)



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


    def rewind(self):
        self.media_player.setPlaybackRate(-1)
        print("<")
        self.play()

    def slow_rewind(self):
        self.media_player.setPlaybackRate(-0.25)
        print("<S")
        self.play()

    def slow_forward(self):
        self.media_player.setPlaybackRate(0.25)
        print("S>")
        self.play()

    def forward(self):
        self.media_player.setPlaybackRate(1.0)
        print(">")
        self.play()

    def fast_forward(self):
        self.media_player.setPlaybackRate(2.0)
        print(">>")
        self.play()


    def status_changed(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_but.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.play_but.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.play_but.repaint()
        # print ("Status", self.media_player.mediaStatus())

    def position_changed(self, position):
        # print("Position changed to", position)
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        print("Duration changed to", duration)
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def take_snapshot(self):
        video_file = self.media.canonicalUrl().path()
        position = self.media_player.position()
        # Use ffmpeg because it's not clear how to get 
        # the frame back from the video surface
        snapshot_file = "{}_{}.jpg".format(video_file, position)
        cmd = [
            "ffmpeg",
            "-ss", str(position/1000),
            "-i", video_file,
            "-frames", "1",
            snapshot_file
        ]
        print(" ".join(cmd))
        retcode = subprocess.call(cmd)
        if retcode == 0:
            self.errorLabel.setText("Saved {}".format(snapshot_file))
        else:
            self.errorLabel.setText("Error running ffmpeg")

    def mark(self):
        print("Should mark location")

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

    def handleError(self):
        self.errorLabel.setText("Error: " + self.media_player.errorString())


def main():
    app = QtWidgets.QApplication(sys.argv)
    videos = itertools.cycle(iter(glob.glob("movies/*.mp4")))
    w = FFWindow(videos)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
