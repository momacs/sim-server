#from flask import Flask, render_template, request
from jinja2 import Template
import random
import string
import cherrypy
from os.path import abspath
from render import Render
from pramr import PramRunner

CP_CONF = {
        '/': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': abspath('./dist') # staticdir needs an absolute path
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('./dist/css')
        },
         '/assets': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('./dist/assets')
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('./dist/js')
        },
        '/scripts': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('./dist/scripts')
        }
}


class PramWebServer(object):
    render = Render()
    pram = PramRunner()
    @cherrypy.expose
    def index(self):
        return self.render.getpage("index.html")

    @cherrypy.expose
    def index2(self):
        data = self.render.getpage("dist/index.html")
        tm = Template(str(data))
        job = "NONE RUNNING"
        out = "NO JOBS"
        rez = tm.render(jobname=job, output=out)
        return str(rez) 

    @cherrypy.expose
    def simple(self):
       name = "Simple Simulation"
       out = self.pram.simple()
       return self.render.setjob(name,out)

   @cherrpy.expose
   def graph(self):
       name = "Graph Example"
       out = self.pram.graph()
       return self.render.setjob(name, out, graph)
    

if __name__ == '__main__':
    cherrypy.quickstart(PramWebServer(),'/', CP_CONF)
