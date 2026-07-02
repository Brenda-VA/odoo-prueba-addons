# from odoo import http


# class OwlCourse(http.Controller):
#     @http.route('/owl_course/owl_course', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/owl_course/owl_course/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('owl_course.listing', {
#             'root': '/owl_course/owl_course',
#             'objects': http.request.env['owl_course.owl_course'].search([]),
#         })

#     @http.route('/owl_course/owl_course/objects/<model("owl_course.owl_course"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('owl_course.object', {
#             'object': obj
#         })

