#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import Utils
from debugger import Debugger
from mail import SendMail
from slack import Slack

if __name__ == '__main__':
    u = Utils()

    u.zip("./日本語音楽.mp3", forOSX=True)
