#! /usr/bin/env python3
#
# (c) Quentin Stafford-Fraser 
# quentinsf.com


import glob
import itertools
import os
import subprocess
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaMetaData
from PyQt5.QtMultimediaWidgets import QVideoWidget


class FFWindow(QtWidgets.QWidget):

    def __init__(self, movie_dir, pos_snapshot_dir, neg_snapshot_dir):
        super().__init__()

        self.media_player = QMediaPlayer( None, QMediaPlayer.VideoSurface)

        self.movie_dir = movie_dir
        video_list = glob.glob(os.path.join(self.movie_dir, "*.mp4"))
        print("{} movies found".format(len(video_list)))
        # We want to be able to cycle through them
        self.video_files = itertools.cycle(iter(video_list))
        
        # Check the output directories exist
        self.pos_snapshot_dir = pos_snapshot_dir
        if not os.path.exists(self.pos_snapshot_dir):
            os.makedirs(self.pos_snapshot_dir)
        self.neg_snapshot_dir = neg_snapshot_dir
        if not os.path.exists(self.neg_snapshot_dir):
            os.makedirs(self.neg_snapshot_dir)

        self.setWindowTitle('FrameFinder')
        
        self.video_widget = QVideoWidget()
        # self.video_widget.setFixedSize(640, 360)
        # self.video_widget.
        self.video_widget.setMinimumSize(640, 360)
        self.video_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)
        self.media_player.setVideoOutput(self.video_widget)

        
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

        self.pos_snapshot_but = QtWidgets.QPushButton()
        self.pos_snapshot_but.setText("Snapshot Positive [P]")
        self.pos_snapshot_but.clicked.connect(self.pos_snapshot)

        self.neg_snapshot_but = QtWidgets.QPushButton()
        self.neg_snapshot_but.setText("Snapshot Negative [O]")
        self.neg_snapshot_but.clicked.connect(self.neg_snapshot)

        self.next_but = QtWidgets.QPushButton()
        self.next_but.setText("Next movie [N]")
        self.next_but.clicked.connect(self.next_video)

        video_vbox = QtWidgets.QVBoxLayout()
        video_vbox.addWidget(self.video_widget)
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
        file_box.addWidget(self.pos_snapshot_but)
        file_box.addWidget(self.neg_snapshot_but)
        file_box.addWidget(self.next_but)

        v_box = QtWidgets.QVBoxLayout()
        # v_box.addStretch()
        v_box.addLayout(video_vbox)

        v_box.addLayout(file_box)
        # v_box.addStretch()

        self.setLayout(v_box)

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

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(" "), self)
        shortcut.activated.connect(self.play_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("f"), self)
        shortcut.activated.connect(self.slow_forward_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("g"), self)
        shortcut.activated.connect(self.forward_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("h"), self)
        shortcut.activated.connect(self.fast_forward_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("p"), self)
        shortcut.activated.connect(self.pos_snapshot_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("o"), self)
        shortcut.activated.connect(self.neg_snapshot_but.animateClick)

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("n"), self)
        shortcut.activated.connect(self.next_but.animateClick)



    def playtoggle(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def pause(self):
        self.media_player.pause()

    def play(self):
        self.media_player.play()
        # This is a nasty hack.  The video tends to zoom to 1:1
        # when you play, but rescales itself when you resize the window.
        # Faking a window resize is the only way I could find to fix the zoom.
        size = self.size()
        self.resize(size.width()+1, size.height()+1)
        self.resize(size.width(), size.height())


    def rewind(self):
        self.media_player.setPlaybackRate(-1)
        self.errorLabel.setText("Rewind 1x")
        self.play()

    def slow_rewind(self):
        self.media_player.setPlaybackRate(-0.25)
        self.errorLabel.setText("Rewind 0.25x")
        self.play()

    def slow_forward(self):
        self.media_player.setPlaybackRate(0.25)
        self.errorLabel.setText("Forward 0.25x")
        self.play()

    def forward(self):
        self.media_player.setPlaybackRate(1.0)
        self.errorLabel.setText("Forward 1x")
        self.play()

    def fast_forward(self):
        self.media_player.setPlaybackRate(2.0)
        self.errorLabel.setText("Forward 2x")
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

    def pos_snapshot(self):
        self.snapshot(self.pos_snapshot_dir)

    def neg_snapshot(self):
        self.snapshot(self.neg_snapshot_dir)

    def snapshot(self, snap_dir):
        video_path = self.media.canonicalUrl().path()
        position = self.media_player.position()
        video_file, extension = os.path.splitext(os.path.basename(video_path))
        snapshot_file = os.path.join(snap_dir, "{}_{}.jpg".format(video_file, position))
        # Use ffmpeg because it's not clear how to get 
        # the frame back from the video surface
        cmd = [
            "ffmpeg",
            "-ss", str(position/1000),
            "-i", video_path,
            "-frames", "1",
            snapshot_file
        ]
        print(" ".join(cmd))
        retcode = subprocess.call(cmd)
        if retcode == 0:
            self.errorLabel.setText("Saved {}".format(snapshot_file))
        else:
            self.errorLabel.setText("Error running ffmpeg")

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
    if len(sys.argv) < 4:
        print("{} MOVIE_DIR POS_SNAPSHOT_DIR NEG_SNAPSHOT_DIR".format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    app = QtWidgets.QApplication(sys.argv)
    w = FFWindow(sys.argv[1], sys.argv[2], sys.argv[3])
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
