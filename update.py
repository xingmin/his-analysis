# -*- coding: utf-8-*-
import os,sys
import gtk
import gobject
import threading
import time
reload(sys)
sys.setdefaultencoding('utf-8')
gobject.threads_init()
class UpdateThread(threading.Thread):
    def __init__(self, win):
        super(UpdateThread, self).__init__()
        self.win = win

    def complete_update(self):
        self.win.emit('destroy')
        return False
    def run(self):
        time.sleep(5)
        #import update-core
        gobject.idle_add(self.complete_update)
class UpdateUI: 
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("updateui.glade")
        #self.win=builder.get_object("dialog1")
        self.win=builder.get_object("window_update")
        self.progressbar1=builder.get_object("progressbar1")
        builder.connect_signals(self)
        self.timeout_id = gobject.timeout_add(160, self.on_timeout, None)
    def on_window_update_show(self, widget, data=None):
        ut = UpdateThread(self.win)
        ut.start()
    def on_window_update_destroy(self, widget, data=None):
        gtk.main_quit()
        #print 'destroying'
    def on_timeout(self, user_data):
        self.progressbar1.pulse()
        return True
    def run(self):
#         self.win.run()
#         self.win.destroy()
        self.win.show()
        gtk.main()
    
if __name__ == "__main__":
    upui = UpdateUI()
    upui.run()