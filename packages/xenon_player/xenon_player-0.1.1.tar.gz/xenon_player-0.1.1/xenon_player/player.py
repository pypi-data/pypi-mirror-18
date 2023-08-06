#! /usr/bin/env python
from threading import Thread

import mplayer
import time

import sys
from xenon_tools.utils import push_in_range, human_time


class XePlayer(Thread):
    p = ''
    finished = False

    len = .1

    playlist = []
    index = -1

    def __init__(self):
        super(XePlayer, self).__init__()
        self.p = mplayer.Player()  # ('-ao', 'alsa:device=hw=1.0'))

    def loadPlaylist(self, plist):
        self.playlist = plist
        self.loadNext()
        time.sleep(1)
        self.pause()

    def loadNext(self):
        self.index += 1
        if self.index >= len(self.playlist):
            self.terminate()
        self.load(self.playlist[self.index])
        self.len = self.p.length

    def loadPrev(self):
        if self.index > 0:
            self.index -= 1
            self.load(self.playlist[self.index])
            self.len = self.p.length

    def load(self, f):
        print 'Starting', f
        self.p.loadfile(f)

    def nowPlaying(self):
        return self.playlist[self.index]

    def pause(self):
        print 'pause'
        self.p.pause()

    def nav(self, amnt):
        self.p.time_pos = push_in_range(self.p.time_pos + amnt, 0, self.len)

    def terminate(self):
        self.finished = True

    def setvol(self, a):
        self.p.volume += a

    def run(self):
        while not self.finished and self.p.time_pos < self.len and self.p.time_pos is not None:
            # if self.p.time_pos:
            #     self.printProgress(self.p.time_pos)
            time.sleep(.5)
        print 'Finished', self.playlist[self.index]
        self.loadNext()

    def printProgress(self, iteration, prefix='', suffix='', decimals=1, barLength=100):
        if self.finished or iteration is None:
            return
        formatStr = "{0:." + str(decimals) + "f}"
        percents = formatStr.format(100 * (iteration / float(self.len)))
        filledLength = int(round(barLength * iteration / float(self.len)))
        bar = '=' * filledLength + '>' + ' ' * (barLength - filledLength)
        sys.stdout.write('\r%s |%s| %s%s %s %s=%s-%s [%shz][%sch][%sbytes/sample]' %
                         (prefix, bar, percents, '%', suffix,
                          human_time(self.p.time_pos), human_time(self.len), human_time(self.len - self.p.time_pos),
                          0, 0, 0))
        sys.stdout.flush()
        if iteration == self.len:
            sys.stdout.write('\n')
            sys.stdout.flush()
