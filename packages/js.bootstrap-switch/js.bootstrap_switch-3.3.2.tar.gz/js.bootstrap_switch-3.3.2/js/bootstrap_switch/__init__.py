from fanstatic import Library, Resource, Group
import js.jquery

library = Library('bootstrap_switch', 'resources')

bootstrap_switch_js = Resource(
    library, 'js/bootstrap-switch.js',
    minified='js/bootstrap-switch.min.js',
    depends=[js.jquery.jquery])

bootstrap_switch_css = Resource(
    library, 'css/bootstrap-switch.css',
    minified='css/bootstrap-switch.min.css')

bootstrap_switch = Group([
    bootstrap_switch_js, bootstrap_switch_css
])
