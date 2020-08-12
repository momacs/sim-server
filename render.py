from jinja2 import Template
import random
import string
import cherrypy
from os.path import abspath

class Render(object):

    def getpage(self, path):
        with open(path) as file:
            data = file.readlines()
            page = ''.join(data)
            return str(page)

    def setjob(self,jobname,jobtext):
        data = self.getpage("dist/index.html")
        tm = Template(str(data))
        job = jobname
        out = jobtext
        rez = tm.render(jobname=job, output=out)
        return str(rez)
