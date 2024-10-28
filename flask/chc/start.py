from fabric.api import run, env

env.hosts = ['example1.com', 'example2.com']
env.user = 'bjhee'
env.password = '111111'

def hello():
    run('ls -l /home/bjhee/')
