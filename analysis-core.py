#!/usr/bin/env python
# -*- coding: utf-8-*-
import os, getopt, sys
import SpssClient
import locale
import traceback
import chardet;
reload(sys)
sys.setdefaultencoding('utf-8')


print sys.getdefaultencoding()

def usage():
    print u'''
    usage: python testclient.py 
        -i 语法文件(是一个模板文件，不能直接运行)
        -o 生成的文件所在目录
        -d 存数据的xls文件所在路径
    '''
def executeSPSS(isyntax,datasource_file, output_path):
    SpssClient.StartClient()
    SpssSyntaxDoc=SpssClient.OpenSyntaxDoc(isyntax)
    cmdlist = SpssSyntaxDoc.GetSyntax()
    SpssSyntaxDoc.CloseDocument()
    #cmdlist = cmdlist.encode('utf-8')
    cmdlist = cmdlist.replace(u'[datasource]',datasource_file)
    cmdlist = cmdlist.replace(u'[outputpath]',output_path)
#     print type(cmdlist)
    print cmdlist
    SpssClient.RunSyntax(cmdlist)
    SpssClient.StopClient()
    os.system("taskkill /F /IM stats.exe")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvi:o:d:", ["help","--isyntax", "--output", "--datasource"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    syntax_file = None
    output_dir = None
    datasource_file = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--isyntax"):
            syntax_file = a
        elif o in ("-d", "--datasource"):
            datasource_file = a
        elif o in ("-o", "--output"):
            output_dir = a
        else:
            assert False, "unhandled option"
    print type(output_dir)
    print output_dir
    print datasource_file
    cur_encoding= locale.getdefaultlocale()[1]
    print locale.getdefaultlocale()
    print cur_encoding
    print chardet.detect(output_dir)
    
    syntax_file = syntax_file.decode('utf-8')
    output_dir = output_dir.decode('utf-8')
    datasource_file = datasource_file.decode('utf-8')

    print syntax_file
    print output_dir
    print datasource_file
    sf=syntax_file
    if not os.path.isfile(sf):
        print sf
        usage()
        print 'test2'
        sys.exit(1)
    #go to execute spss syntax
    executeSPSS(syntax_file, datasource_file, output_dir)



if __name__ == "__main__":
    main()