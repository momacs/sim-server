from jinja2 import Template
import random
import string
import cherrypy
from os.path import abspath

class RuleDownloader(object):

    def downloadlocalrule(self, path):
        p = "/usr/local/lib/python3.6/dist-packages/pram/rule.py"
        with open(path) as f:
            lines = f.readlines()
            lines = [l for l in lines]
            with open(p, "w") as f1:
                f1.writelines(lines)

    def downloadhostedrule(self,jobname,jobtext):
        print("NOTHING FOR NOW")
