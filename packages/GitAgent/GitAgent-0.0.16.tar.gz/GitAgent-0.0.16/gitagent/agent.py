#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2016-07-14 14:35
# @Author  : Alexa (AlexaZhou@163.com)
# @Link    : 
# @Disc    : 

import os
import fcntl
import subprocess
import tornado.ioloop
import tornado.web
import tornado.websocket
import time
import json
import git
import threading
import logging
from gitagent import auth


settings = {
    'debug' : True,
	"static_path": os.path.join(os.path.dirname(__file__), "static")
}

repo_lock = {}
client_sockets = {}

pretty_json_dump = lambda x:json.dumps( x,sort_keys=True,indent=4,ensure_ascii=False )

config = None

def get_config(  ):
    return config

def set_config( value ):
    global config
    config = value

class git_work_progress( git.RemoteProgress ):
    def __init__(self,delegate):
        git.RemoteProgress.__init__(self)
        self.delegate = delegate

    def update(self,op_code,cur_count,max_count=None,message=""):
        print( '-->',op_code,cur_count,max_count,message )
        self.delegate.console_output( '\r' + "working with op_code[%s] progress[%s/%s] %s"%(op_code,cur_count,max_count,message) )

class GitWorker():
    def __init__(self, repo_path, git_branch, git_hash, command=None, console_id=None, GIT_SSH_COMMAND=None):
        self.repo_path = repo_path
        self.git_branch = git_branch
        self.git_hash = git_hash
        self.console_id = console_id  
        self.GIT_SSH_COMMAND = GIT_SSH_COMMAND
        self.finish_ret = None
        self.output = ''
        self.err_msg = None
        self.command = command

    def console_output(self,s):
        print('console [%s]>>'%self.console_id,s )
        if self.console_id != None:
            
            try:
                ws_cocket = client_sockets[ self.console_id ]
                msg = {}
                msg['type'] = 'output'
                msg['content'] = s
                ws_cocket.write_message( msg )

            except Exception as e:
                print('write to websocket failed:',e)

    def non_block_read(self, output):
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            ret = output.read().decode('utf-8')
            if ret == None:
                ret = ""
            return ret
        except:
            return ""

    def worker(self):
        print( "-"*20 + "git checkout " + "-"*20 )
        print( "branch:" + self.git_branch )
        print( "hash:" + str(self.git_hash))
        
        progress_delegate = git_work_progress( self )
        
        try:
            repo=git.Repo( self.repo_path )
            if self.GIT_SSH_COMMAND != None:
                repo.git.update_environment( GIT_SSH_COMMAND=self.GIT_SSH_COMMAND )
            
            branch_now = None
            if repo.head.is_detached == False:
                branch_now = repo.active_branch.name
            
            print( 'Now repo is on branch:',branch_now )
            if self.git_branch in repo.branches:
                #make sure on right branch

                if branch_now != self.git_branch:
                    self.console_output( 'checkout branch %s...'%self.git_branch )
                    repo.branches[self.git_branch].checkout()
                #pull
                self.console_output( 'pull...' )
                repo.remotes['origin'].pull( progress= progress_delegate )
            else:
                #if the target branch is not existed in local, checkout out it at first
                self.console_output( 'branch %s not existed local. update remote branches...'%self.git_branch )
                origin = repo.remotes['origin']
                origin.update(  )
                self.console_output( 'checkout branch %s...'%self.git_branch )
                origin.refs[self.git_branch].checkout( b=self.git_branch )
            
            if self.git_hash != None:
                #TODO:判断本地是否存在 hash 对应的commit，如果存在则跳过 pull 的动作
                self.console_output( 'git checkout %s...'%self.git_hash )
                git_exec = repo.git
                git_exec.checkout( self.git_hash )

            if self.command != None:
                self.console_output('Exec command: %s'%self.command)
                p_command = subprocess.Popen(self.command, shell=True, bufsize=1024000, cwd=self.repo_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p_returncode = None

                while True:
                    p_output = self.non_block_read(p_command.stdout)
                    if len(p_output) != 0:
                        self.console_output( p_output )

                    p_returncode = p_command.poll()
                    if p_returncode != None:
                        break

                    time.sleep(0.01)

                if p_returncode != 0:
                    raise Exception("exce command [%s] return code !=0"%self.command)
            
            self.finish_ret = 'success'
        except Exception as e:
            print('Exception:',e)
            self.err_msg = str(e)
            self.finish_ret = 'failed'
        
        print( "-"*20 + "git checkout finish:" + self.finish_ret + "-"*20 )

    def start(self):
        t = threading.Thread( target = self.worker )
        t.start()


def return_json(fn):
    def wrapper( self, *args, **kwargs ):
        self.set_header("Content-Type", "application/json; charset=UTF-8") 
        return fn( self, *args, **kwargs )
        
    return wrapper

def verify_request( request ):

    config = get_config()
    if 'password' in config:
        password = config['password']

        method = request.method
        uri = request.path
        request_args = {}
        for name in request.arguments:
            request_args[name] = request.arguments[name][0].decode('utf-8')

        #use password directly auth
        if request_args.get('password') == password:
            return True

        #use password sign auth
        request_time = int(request_args['time'])
        if abs(request_time - time.time()) > 60:
            print( 'time diff too much, auth failed' )
            return False
        
        sign = request_args['sign']
        del request_args['sign']

        sign_right = auth.sign( method, uri, request_args, password, time_stamp = request_args['time'] )['sign']
        print( 'sign_right:',sign_right )

        if sign_right != sign:
            print( 'verify request failed due to sign not match' )
            return False

        return True

def auth_verify(fn):
    def wrapper( self, *args, **kwargs ):
        if verify_request(self.request) == False:
            raise tornado.web.HTTPError(501)
        return fn( self, *args, **kwargs )

    return wrapper

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, GitAgent~")

class RepoHandler(tornado.web.RequestHandler):
    @return_json
    @auth_verify
    def get(self):
        config = get_config()
        ret = list(config['repo'].keys())
        self.write( pretty_json_dump(ret) )

class StatusHandler(tornado.web.RequestHandler):
    @return_json
    @auth_verify
    def get(self,repo):
        config = get_config()
        if repo not in config['repo']:
            raise tornado.web.HTTPError(404)

        repo_path = config['repo'][ repo ]['repo_path']
        repo = git.Repo( repo_path )
        commit = repo.commit("HEAD")
        
        info = {}

        if repo.head.is_detached == True:
            info['branch'] = None
        else:
            info['branch'] = repo.active_branch.name

        info['hash'] = commit.hexsha
        info['author'] = str(commit.author)
        info['message'] = commit.message
        info['busy'] = repo in repo_lock
        info['dirty'] = repo.is_dirty()
        info['untracked_files'] = repo.untracked_files
        info['changed_files'] = {}

        change = info['changed_files']
        diff = repo.index.diff(None)

        name_getter = lambda diff:diff.a_path
        for change_type in "ADRM":
            print( 'change_type:',change_type )
            change[change_type] = list(map( name_getter, diff.iter_change_type( change_type )))

        self.write( pretty_json_dump(info) )

class PullHandle(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self,repo):
        self.set_header("Content-Type", "application/json; charset=UTF-8") 
        config = get_config()

        if verify_request(self.request) == False:
            raise tornado.web.HTTPError(501)

        if repo not in config['repo']:
            raise tornado.web.HTTPError(404)
        
        block = self.get_argument( 'block', '0')
        git_branch = self.get_argument( 'git_branch', 'master')
        git_hash = self.get_argument( 'git_hash', None)
        console_id = self.get_argument( 'console_id', None)
        cmd = self.get_argument( 'command', None)
        GIT_SSH_COMMAND = None
        
        ret = {}
        ret['ret'] = 'success'
        ret['err_msg'] = None
        command = None
        
        if cmd != None:
            if cmd not in config['repo'][repo]['command']:
                raise tornado.web.HTTPError(501)
            else:
                command = config['repo'][repo]['command'][cmd]
            
        if repo in repo_lock:
            ret['ret'] = 'failure'
            ret['err_msg'] = 'repo is busying'
            self.write( pretty_json_dump(ret))
            self.finish()
            return
        else:
            repo_lock[repo] = True
            
        repo_path = config['repo'][ repo ]['repo_path']
        if 'GIT_SSH_COMMAND' in config['repo'][repo]:
            GIT_SSH_COMMAND = config['repo'][repo]['GIT_SSH_COMMAND']
            print('use GIT_SSH_COMMAND:',GIT_SSH_COMMAND)

        git_worker = GitWorker( repo_path, git_branch, git_hash, command, console_id, GIT_SSH_COMMAND)
        git_worker.start()

        if block == '0':#no block
            ret['ret'] = 'success'
        else:#block until git worker finish
            while git_worker.finish_ret == None:
                yield tornado.gen.sleep(0.01)
            
            ret['ret'] = git_worker.finish_ret
            ret['err_msg'] = git_worker.err_msg
        
        self.write( pretty_json_dump(ret))
        self.finish()
        del repo_lock[repo]

class CommandHandle(tornado.web.RequestHandler):
    def post(self,repo):
        pass
        
class ConsoleHandler(tornado.websocket.WebSocketHandler):
    """docstring for ConsoleHandler"""

    def check_origin(self, origin):
        return True

    def open(self):
        print("websocket open")
        self.write_message(json.dumps({
          'type': 'sys',
          'message': 'Welcome to WebSocket',
          'id': str(id(self)),
        }))
        client_sockets[ str(id(self)) ] = self

    def on_close(self):
        print("websocket close")
        del client_sockets[ str(id(self)) ]


application = tornado.web.Application([
    ("/repo/([^/]+)/exec", CommandHandle),
    ("/repo/([^/]+)/pull", PullHandle),
    ("/repo/([^/]+)", StatusHandler),
    ("/repo", RepoHandler ),
    ("/console", ConsoleHandler ),
    ("/", MainHandler),
],**settings)

def start_server():

    logging.basicConfig()
    logging.root.setLevel(logging.INFO)
    
    config = get_config()
    application.listen( config['port'], address=config['bind_ip'] )
    tornado.ioloop.IOLoop.instance().start()
