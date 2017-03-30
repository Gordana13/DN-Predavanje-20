#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import TaskManager

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class SaveHandler(BaseHandler):
    def post(self):
        to_do = self.request.get("list")
        status = self.request.get("status")
        status_baza = False
        if status == "on":
            status_baza = True

        save = TaskManager(list=to_do, status=status_baza)
        save.put()

        return self.render_template("save.html")

class AllTasksHandler(BaseHandler):
    def get(self):
        tasks = TaskManager.query().fetch()
        output = {"tasks": tasks}

        return self.render_template("tasks.html", output)

class DetailsHandler(BaseHandler):
    def get(self, details_id):
        tasks = TaskManager.get_by_id(int(details_id))
        output = {
            "tasks": tasks
        }
        return self.render_template("details.html", output)

class EditHandler(BaseHandler):
    def get(self, details_id):
        tasks = TaskManager.get_by_id(int(details_id))
        output = {
            "tasks": tasks
        }
        return self.render_template("edit.html", output)

    def post(self, details_id):
        tasks = TaskManager.get_by_id(int(details_id))
        tasks.list = self.request.get("list")
        tasks.status = self.request.get("status")
        tasks.status_baza = False
        if tasks.status == "on":
            tasks.status_baza = True
        tasks.put()

        return self.redirect("/tasks")

class DeleteHandler(BaseHandler):
    def get(self, details_id):
        tasks = TaskManager.get_by_id(int(details_id))
        output = {
            "tasks": tasks
        }
        return self.render_template("delete.html", output)

    def post(self, details_id):
        tasks = TaskManager.get_by_id(int(details_id))
        tasks.key.delete()
        return self.redirect("/tasks")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/save', SaveHandler),
    webapp2.Route('/tasks', AllTasksHandler),
    webapp2.Route('/details/<details_id:\d+>', DetailsHandler),
    webapp2.Route('/details/<details_id:\d+>/edit', EditHandler),
    webapp2.Route('/details/<details_id:\d+>/delete', DeleteHandler),
], debug=True)
