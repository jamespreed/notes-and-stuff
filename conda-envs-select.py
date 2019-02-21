import subprocess
import json
from tkinter import Tk, Checkbutton, Label, Frame, IntVar
from tkinter.ttk import Button
import re
import os

class EnvSelectWindow:
    def __init__(self, envs):
        self.selection = []
        self.envs = envs
        self.root = Tk()
        self.variables = [IntVar(self.root) for _ in envs]
        label_txt = ('Select the Conda environments to keep.' if envs else
            'You have no Conda environments needing migration. Congrats!')
        self.label = Label(self.root, text=label_txt)
        self.checkboxes = [
            Checkbutton(self.root, text=e, variable=v) for e,v 
            in zip(envs, self.variables)
        ]
        self.button = Button(self.root, text='OK', command=self.select)
        
        # set r to handle case with no environments
        r = 0
        self.label.grid(row=r, sticky='w', padx=10)
        for r, cb in enumerate(self.checkboxes, 1):
            cb.grid(row=r, sticky='w', padx=10)
        self.button.grid(row=r+1, sticky='ew', padx=10)
        
    def select(self):
        self.selection = [
            e for e,v in zip(self.envs, self.variables) if v.get()
        ]
        self.root.destroy()
        self.root.quit()
        
    def show_window(self):
        self.root.mainloop()
        
def filter_envs(envs, path_regex=None, flags=0):
    """
    Filter the environments to only include those in with a path
    that matches `path_regex`.  If `path_regex` is None, it is ignored.  
    `flags` is passed to the re.search.
    """
    if not path_regex:
        return envs
    return [e for e in envs if re.search(path_regex, e, flags)]
    
def export_envs_specs(envs):
    out_dir = os.path.join(
        os.environ.get('homedrive')+os.environ.get('homepath'),
        'conda-env-specs'
    )
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    for env in envs:
        env_name = re.split(r'[\\/]', env)[-1]
        proc = subprocess.Popen(
            ['conda', 'list', '-p', env, '--export'],
            stderr=subprocess.PIPE, 
            stdout=subprocess.PIPE
        )
        
        spec, err = proc.communicate()
        
        if spec:
            spec_path = os.path.join(out_dir, env_name)+'.txt'
            with open(spec_path, 'wb') as fp:
                fp.write(spec)
            print(f'OK: Spec for environment {env_name} written to {spec_path}')
        else:
            print(f'ERROR: Could not create spec file for environment {env_name}')
    
if __name__ == '__main__':
    proc = subprocess.Popen(
        ['conda', 'env', 'list', '--json'], 
        stderr=subprocess.PIPE, 
        stdout=subprocess.PIPE
    )
        
    out, err = proc.communicate()
    envs = filter_envs(
        json.loads(out).get('envs', []),
        r'\.adsfconda'
    )
    
    env_window = EnvSelectWindow(envs)
    env_window.show_window()
    for s in env_window.selection:
        print(s)