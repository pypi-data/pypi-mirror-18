from ..obisutils import *

def eez(uuid, **kwargs):
	'''
	Get details on a GBIF dataset.

	:param uuid: (character) One or more dataset UUIDs. See examples.

	References: http://www.gbif.org/developer/registry#datasetMetrics

	Usage::

			from pygbif import registry
			registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')
			registry.dataset_metrics(uuid='66dd0960-2d7d-46ee-a491-87b9adcfe7b1')
			registry.dataset_metrics(uuid=['3f8a1297-3259-4700-91fc-acc4170b27ce', '66dd0960-2d7d-46ee-a491-87b9adcfe7b1'])
	'''
	def getdata(x, **kwargs):
		url = gbif_baseurl + 'dataset/' + x + '/metrics'
		return gbif_GET(url, {}, **kwargs)

	if len2(uuid) == 1:
		return getdata(uuid)
	else:
		return [getdata(x) for x in uuid]
