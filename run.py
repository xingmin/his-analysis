# -*- coding: utf-8-*-
import sys, os
import update
import subprocess
upui = update.UpdateUI()
upui.run()

subprocess.Popen(["analysis.py"],shell=True)


