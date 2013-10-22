# -*- coding: utf-8-*-
import uuid
import config
import sys, os
import chardet
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

def getstatusoutput_my(cmd): 
    """Return (status, output) of executing cmd in a shell."""
    """This new implementation should work on all platforms."""
    import subprocess
    reload(sys)  
    sys.setdefaultencoding('utf-8') 

    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, universal_newlines=True) 
#     output = u''.join(pipe.stdout.readlines()) 
    output=u''
    for line in pipe.stdout:
        end = chardet.detect(line)['encoding']
        if end=='utf-8' or end =='ascii':
            output= output+ line.decode('utf-8')
        elif end=='GB2312':
            output= output+ line.decode('cp936')
    sts = pipe.returncode
    if sts is None: sts = 0
    return sts, output
uuid_template = uuid.uuid1()
uuid_app = uuid.uuid1()
curr_path = cur_file_dir()
cmdstr=u"./update-core.sh -a %s -b %s -p %s -t %s" %(config.APPLICATION_REPO, config.TEMPLATES_REPO, uuid_app, uuid_template)
cmdstr = "sh --login -c \"%s\"" % cmdstr
print cmdstr
getstatusoutput_my(cmdstr)