# FrameFinder

This is a little Python Qt app designed for capturing frames from videos to get sample images e.g. for training machine learning systems.

You'll need to `pip install pyqt5` to run it.  You'll also need `ffmpeg` on your system.

You give it a directory full of MP4 files and the names of two output directories, one for positive samples and one for negative ones. 

It will display the first movie, and allow you to play it forward or backwards at different speeds and pause when you get to a representative frame.  Then you can press a key to store the snapshot JPEG either in the positive or negative directory.  Repeat as required until you have enough sample images.

The snapshots are named with the video file followed by the timestamp in milliseconds, e.g. from approx 43 secs into mymovie.mp4, you might get mymovie_43256.jpg.

Pressing the Next Movie button will move onto the next MP4 file.


[Quentin Stafford-Fraser](http://quentinsf.com)
