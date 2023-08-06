# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


from . import *  # imports __init__
from .. import *

# from .. import main
# from ..core.utils import *

# TEMPLATE: HTML BASIC


#
# ===========
# Comments:
# ===========
#





def run(graph, save_on_github=False, main_entity=None):
	"""
	From a graph instance outputs a nicely formatted html documentation file.
	2015-10-21: mainly used with w3c template

	Django templates API: https://docs.djangoproject.com/en/dev/ref/templates/api/

	output = string

	2016-02-24: added <save_on_github>
	"""

	try:
		ontology = graph.ontologies[0]
		uri = ontology.uri
	except:
		ontology = None
		uri = ";".join([s for s in graph.sources])

	# ontotemplate = open("template.html", "r")
	ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "javadoc.html", "r")

	t = Template(ontotemplate.read())


	c = Context({
					"ontology": ontology,
					"main_uri" : uri,
					"classes": graph.classes,
					"objproperties": graph.objectProperties,
					"dataproperties": graph.datatypeProperties,
					"annotationproperties": graph.annotationProperties,
					"skosConcepts": graph.skosConcepts,
					"instances": []
				})

	rnd = t.render(c)

	return safe_str(rnd)







if __name__ == '__main__':
	import sys
	try:

		# script for testing - must launch this module
		# >python -m viz.viz_html

		func = locals()["run"] # main func dynamically
		run_test_viz(func)

		sys.exit(0)

	except KeyboardInterrupt as e: # Ctrl-C
		raise e



