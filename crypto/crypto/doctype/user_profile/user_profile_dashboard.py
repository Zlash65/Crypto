from frappe import _

def get_data():
	# config data for heatmap and graph
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on transactions/Investments that the user adds.'),

		# 'graph': True,",

		'fieldname': 'user_profile',
		'non_standard_fieldnames': {
			'My Investments': 'user_profile',
			'ToDo': 'reference_name',
			'Event': 'ref_name'
		},
		'transactions': [
			{
				'label': _('Exhanges & Investment'),
				'items': ['My Investments']
			},
			{
				'label': _('Tools'),
				'items': ['ToDo', 'Event']
			},
		]
	}