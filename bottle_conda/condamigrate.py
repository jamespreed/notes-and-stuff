from bottle import jinja2_view, request, route, run, static_file
import subprocess
import os
#from jinja2 import Template

@route('/', name='Hooooome')
@jinja2_view('base.html', template_lookup=['.'])
def root():
    check, msg = check_install()
    return {'msg': msg}

def check_install():
    out = False
    msg = 'No Anaconda installation found.'
    if os.path.exists('C:/Anaconda3/python.exe'):
        out = True
        msg = 'Anaconda properly installed.'
    return out, msg
    
    
@route('/images/<img>')
def server_image(img):
    return static_file(img, root='./images')
    
@route('/conda/<cmd>', methods=['GET', 'POST'])
def conda_cmd(cmd):
    """
    Join multitoken commands with `+`.
    """
    conda = ['C:/Anaconda3/Scripts/activate.bat', 'base', '&', 'conda']
    proc = subprocess.Popen(
        conda + cmd.split('+'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    out, err = proc.communicate()
    return {'out': out.decode('utf8'), 'err': err.decode('utf8')}


run(host='localhost', reload=True, port=8002)