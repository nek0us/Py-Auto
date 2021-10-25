#coding=utf-8

from logging import Logger
from config import py_path,run_time
import config
import tools
from tools import logger,begin,fenge
import threading
import time
import datetime
import re
import queue
import os
import sys



qgit = queue.Queue()
qpy = queue.Queue()



def git_pull(qgit):
    try:
        
        while not qgit.empty():
            this_git_cmd = ''.join(qgit.get())
            logger.info("正在进行git pull的目录："+this_git_cmd)
            git_cmd = 'git -C "' + this_git_cmd[:-1] + '"  pull origin master'
            r = os.popen(git_cmd)
            r.read()
            r.close()
        qgit.task_done()
    except:
        logger.info("git拉取失败")



def get_list():
    arg = []
    begin("准备读取项目")

    try:
        with open("run_list.txt","r") as f:
            for line in f.readlines():
                line = line.strip('\n')
                
                pat_git = r".\:([\\a-zA-Z0-9-_\.\s]+\\)+"
                res_git = re.match(pat_git,line).group()
                qgit.put(res_git)

                pat_arg = r"\t[0-9a-zA-Z-_' '\\/]+"
                res_arg = re.search(pat_arg,line)

                pat = r"\.py"
                res = re.split(pat,line)

                if res_arg:
                    res_arg = res_arg.group()
                    res = ''.join(res[:1]) + '.py" ' + ''.join(res_arg[1:])
                else:
                    res = ''.join(res[:1]) + '.py" '

                
                
                qpy.put(res)
                

                #pat_qpy = r".\:([\\\w-.\s]+\\)+([\w\s-.])+\.py"
                #res_qpy = re.search(pat_qpy,line)
                #logger.info(res_qpy)
                #res_qpy = res_qpy.group()
                #logger.info(res_qpy)
                #qpy.put(res_qpy)


                
                #pat = r"(\\[a-zA-Z0-9-_\.\s]+\\)+"
                #res = re.findall(pat,line)
                #res = res[-1:]
                #res = ''.join(res)[1:-1]
                #run_list.append(res)

        return arg
                

    except:
       logger.info("读取run_List失败")


    #return run_list

def git_update():
    fenge()
    begin("准备更新项目")
    threads = []
    for x in range(0,2):
        t = threading.Thread(target=git_pull,args=(qgit,))
        threads.append(t)
    for t in threads:
        #t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

def run_object(qpy):
    try:
        while not qpy.empty():
            py_name = qpy.get()
            logger.info("准备运行\""+py_name)
            py_cmd = r'cmd/c start ' + py_path + ' "' + ''.join(py_name)
            r = os.popen(py_cmd)
            r.read()
            bl = r.close()
            if not bl:
                logger.info("运行结束"+py_name)
        qpy.task_done()
    except:
        logger.info("运行出错，请检查")

def run_py():
    fenge()
    begin("准备运行项目")
    threads = []
    for x in range(0,2):
        t = threading.Thread(target=run_object,args=(qpy,))
        threads.append(t)
    for t in threads:
        #t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()



def check():
    chk_err = False
    if not py_path:
        logger.info("python环境变量未填入，请检查config.py文件")
        chk_err = True
    with open("run_list.txt","r") as f:
        if not f.read():
            logger.info("run_list列表为空，无项目运行")
            chk_err = True
    f.close()
    if not config.run_time:
        logger.info("运行时间未填写，默认使用 00:00:00")
        config.run_time = "00:00:00"
    else:
        logger.info("预设运行时间为每日"+config.run_time)
    if chk_err:
        sys.exit(1)

def everyday():
    begin("准备检查配置")
    fenge()
    check()
    fenge()
    logger.info("未到预定运行时间，等待中...")
    while 1:
        now_time = ''.join(time.strftime("%H:%M:%S", time.localtime()))
   
        if run_time == now_time:
        #if 1:
            fenge()
            logger.info("到时间了，开冲！")
            try:
                get_list()
            except:
                logger.info("读取程序出现异常，请检查")
            try:
                if config.git_status:
                    git_update()
            except:
                logger.info("git pull出现异常，请检查")
            try:
                run_py()
            except:
                logger.info("py运行程序出现异常，请检查")
            logger.info("本次运行结束，等待着美好的明天到来~")
            fenge()
        #else:
            #logger.info(now_time)

        time.sleep(1)


if __name__ == '__main__':
    everyday()