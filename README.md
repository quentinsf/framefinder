# FrameFinder

This is a little Python Qt app designed for capturing frames from videos to get sample images e.g. for training machine learning systems.  It assumes you want to store example frames which meet some particular criteria, and also 'negative' example frames which don't.  You can ignore the negative options if you don't need them.

You'll need to `pip install pyqt5` to run it.  You'll also need `ffmpeg` on your system.

You give it a directory full of MP4 files and the names of two output directories, one for positive samples and one for negative ones.  E.g.

    ./framefinder.py movies pos_snapshots neg_snapshots

It will display the first movie, and allow you to play it forward or backwards at different speeds and pause when you get to a representative frame.  Then you can press a key to store the snapshot JPEG either in the positive or negative directory.  Repeat as required until you have enough sample images.

The snapshots are named with the video file followed by the timestamp in milliseconds, e.g. from approx 43 secs into `mymovie.mp4`, you might get `mymovie_43256.jpg`.

Pressing the Next Movie button will move onto the next MP4 file.

Most of the buttons have keyboard shortcuts displayed on them.


[Quentin Stafford-Fraser](http://quentinsf.com)
