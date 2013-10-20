# -*- coding: utf-8-*-
import os,sys
import gtk
import commands
import locale
import gobject
import threading
reload(sys)
sys.setdefaultencoding('utf-8')
import chardet;
import datetime


gobject.threads_init()

# print sys.getdefaultencoding()
# print locale.getdefaultlocale()


class MyThread(threading.Thread):
    def __init__(self, window, execbutton, cmdstr, output):
        super(MyThread, self).__init__()
        self.window = window
        self.execbutton = execbutton
        self.cmdstr = cmdstr
        self.output_dir = output
        self.origin_execbutton_text = self.execbutton.get_label()
        
    def showMessage(self, msg):
        md = gtk.MessageDialog(self.window,
                       gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                       gtk.BUTTONS_CLOSE, msg)
        md.run()
        md.destroy()
    def getstatusoutput_my(self,cmd): 
        """Return (status, output) of executing cmd in a shell."""
        """This new implementation should work on all platforms."""
        import subprocess
        reload(sys)  
        sys.setdefaultencoding('utf-8') 
    
        pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True) 
        output=u'' 
    #     infos = pipe.stdout.readlines()
    #     output = u''.join(infos) 
        
        for line in pipe.stdout:
            end = chardet.detect(line)['encoding']
            if end=='utf-8' or end =='ascii':
                output= output+ line.decode('utf-8')
            elif end=='GB2312':
                output= output+ line.decode('cp936')
        sts = pipe.returncode
        if sts is None: sts = 0
        return sts, output
    def lock_window(self, locked):
        self.window.set_deletable(not locked)
        self.execbutton.set_sensitive(not locked)
        if locked:
            self.execbutton.set_label("正在生成，请稍后...")
        else:
            self.execbutton.set_label(self.origin_execbutton_text)
        return False
    def open_output_dir(self, cmd_explorer):
        os.system(cmd_explorer)
        return False
    def run(self):
        gobject.idle_add(self.lock_window, True)
        (status, output) = self.getstatusoutput_my(self.cmdstr)
        print status
        print output        
        gobject.idle_add(self.lock_window, False)
        gobject.idle_add(self.showMessage, "生成分析文件成功，请到报告输出目录查看。")
        cmd_explorer = 'explorer.exe %s' % self.output_dir
        gobject.idle_add(self.open_output_dir, cmd_explorer.encode('cp936'))
class analysisui:
    def on_imagemenuitem_about_activate(self, menuitem, data=None):
        self.aboutui = AboutUI(self.window)
        self.aboutui.run()
    def on_window_analysis_destroy(self, widget, data=None):
        gtk.main_quit()
    def on_button_sel_data_file_clicked(self, widget, data=None):
        datafile_path = self.entry_datafile.get_text()
        self.dataset_chooser.show()
    def on_button_analysis_output_clicked(self, widget, data=None):
        self.fcd_analysis_output.show()
    def showMessage(self, msg):
        md = gtk.MessageDialog(self.window,
                       gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
                       gtk.BUTTONS_CLOSE, msg)
        md.run()
        md.destroy()
    def on_button_exec_analysis_clicked(self, widget, data=None):
        tv = self.treeview.get_treeview()
        tvselected = tv.get_selection().get_selected()
        syntax =tvselected[0].get(tvselected[1],1)[0]
        syntax=syntax.decode('utf-8')
        if tvselected[1] == None or not os.path.isfile(syntax):
            self.showMessage("请重新选择模板")
            return
       
        datasource = self.entry_datafile.get_text()        
        report_output = self.entry_analysis_output.get_text()
        
        if syntax == '' or datasource == '' or report_output=='':
            self.showMessage("数据/模板/报告有为空的，请重新设置!")
            return
        print report_output.decode('utf-8')
        cmdstr = "python analysis-core.py -i \"%s\" -d \"%s\" -o \"%s\""%(syntax, datasource, report_output)
        #cmdstr = cmdstr.encode('utf-8')
        print cmdstr.decode('utf-8')
        cmdstr = cmdstr.replace("\\","/")
        
        logfile = open("./analysis.log",'a')
        logfile.write("[%s]%s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),cmdstr))
        logfile.close()
        
        t = MyThread(self.window, self.button_exec_analysis, cmdstr, report_output)
        t.start()
    def on_filechooserdialog_dataset_close(self, widget, data=None):
        self.dataset_chooser.hide()
        filename = self.dataset_chooser.get_filename()
        if filename != None:
            self.entry_datafile.set_text(filename)
            
    def on_button_sel_dataset_ok_clicked(self, widget, data=None):
        self.on_filechooserdialog_dataset_close(widget,data)
    def on_button_sel_dataset_cancel_clicked(self, widget, data=None):
        self.dataset_chooser.hide()
        
    def filechooserdialog_analysis_output_close_cb(self, widget, data=None):
        self.fcd_analysis_output.hide()
        filename = self.fcd_analysis_output.get_filename()
        if filename != None:
            self.entry_analysis_output.set_text(filename)        
    def on_button_ok_output_clicked(self, widget, data=None):
        self.filechooserdialog_analysis_output_close_cb(widget, data)
    def on_button_cancel_analysis_clicked(self, widget, data=None):
        self.fcd_analysis_output.hide()
        
    def add_filters_to_file_chooser(self, chooser):
      
#         filter_name = "所有文件"
#         filter_pattern="*"
#         filter_file = gtk.FileFilter()
#         filter_file.set_name(filter_name)
#         filter_file.add_pattern(filter_pattern)
#         chooser.add_filter(filter_file)        
        
        filter_name = "Excel文件"
        filter_pattern="*.xls"
        filter_file = gtk.FileFilter()
        filter_file.set_name(filter_name)
        filter_file.add_pattern(filter_pattern)
        chooser.add_filter(filter_file)    

    def init_fcd_analysis_output(self, builder):
        self.fcd_analysis_output = builder.get_object("filechooserdialog_analysis_output")
        #print self.fcd_analysis_output
        self.entry_analysis_output = builder.get_object("entry_analysis_output")
    def lock_window(self, locked):
        self.window.set_deletable(not locked)
        self.button_exec_analysis.set_sensitive(not locked)
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("analysisui.glade")
         
        self.window=builder.get_object("window_analysis")
        self.entry_datafile=builder.get_object("entry_datafile")
        self.entrybuffer_file = builder.get_object("entrybuffer_file")        
        
        self.dataset_chooser = builder.get_object("filechooserdialog_dataset")
        #print self.dataset_chooser
        self.button_exec_analysis = builder.get_object("button_exec_analysis")
        self.add_filters_to_file_chooser(self.dataset_chooser)
        
        self.init_fcd_analysis_output(builder)

        self.treeview = TemplateTreeView(builder)
        self.aboutui = None
        builder.connect_signals(self) 
 
        self.window.show()
class AboutUI: 
    def __init__(self, mainwin):
        builder = gtk.Builder()
        builder.add_from_file("aboutui.glade")
        self.mainwin= mainwin
        self.window=builder.get_object("aboutdialog_analysis")
       
        builder.connect_signals(self) 
    def run(self):
        response = self.window.run()
        if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CANCEL:
            self.window.destroy()

        
class TemplateTreeView:
    def __init__(self, builder):
        self.treeview = builder.get_object("treeview_template")
        self.init_treeview()
    def init_treeview(self):
        model = self.treeview.get_model()
        parents = {}
        root = '.\\templates'
        root = os.path.abspath(root)
        for dir, dirs, files in os.walk(root):
            dir= dir.decode('cp936').encode('utf-8')
            for subdir in dirs:
                subdir = subdir.decode('cp936').encode('utf-8')
                subdir_full = os.path.join(dir, subdir)
                parents[subdir_full] = model.append(parents.get(dir, None), [subdir, subdir_full])
            for item in files:
                item= item.decode('cp936').encode('utf-8')
                item_full = os.path.join(dir, item)
                model.append(parents.get(dir, None), [item, item_full])
    def get_treeview(self):
        return self.treeview;

#以下代码来自:http://hi.baidu.com/nivrrex/item/a0d47c0f4bd9fdce905718a0
#获取脚本文件的当前路径
def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
#打印结果

def run_analysis():
    os.chdir(cur_file_dir())
    analysisui = analysisui()
    gtk.main()       
if __name__ == "__main__":
    run_analysis()
