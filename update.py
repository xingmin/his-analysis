import uuid
import config
import sys, os

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
    output = u''.join(pipe.stdout.readlines()) 
    
#     for line in pipe.stdout:
#         end = chardet.detect(line)['encoding']
#         if end=='utf-8' or end =='ascii':
#             output= output+ line.decode('utf-8')
#         elif end=='GB2312':
#             output= output+ line.decode('cp936')
    sts = pipe.returncode
    if sts is None: sts = 0
    return sts, output
uuid_template = uuid.uuid1()
uuid_app = uuid.uuid1()
curr_path = cur_file_dir()
cmdstr=u'''
#首先更新templates文件夹下的模板
echo -n "updating templates... "
git clone --depth 1 %s %s
if [[ ! -d templates ]]; then  
    mkdir templates
fi 
cp %s/* templates
rm -rf %s
echo "done."
#更新整个程序文件
echo -n "updating application... "
cd ..
git clone --depth 1 %s %s
cp %s/* %s
rm -rf %s
cd %s
echo "done."
'''%(config.TEMPLATES_REPO, uuid_template, uuid_template, uuid_template, 
     config.APPLICATION_REPO, uuid_app, curr_path, uuid_app, curr_path)
getstatusoutput_my(cmdstr)