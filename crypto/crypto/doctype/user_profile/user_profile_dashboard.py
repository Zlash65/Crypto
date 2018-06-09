from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on transactions/Investments that the user adds.'),

		# 'graph': True,
		# 'graph_method': "frappe.utils.goal.get_monthly_goal_graph_data",
		# 'graph_method_args': {
		# 	'title': _('Sales'),
		# 	'goal_value_field': 'monthly_sales_target',
		# 	'goal_total_field': 'total_monthly_sales',
		# 	'goal_history_field': 'sales_monthly_history',
		# 	'goal_doctype': 'Sales Invoice',
		# 	'goal_doctype_link': 'company',
		# 	'goal_field': 'base_grand_total',
		# 	'date_field': 'posting_date',
		# 	'filter_str': 'status != "Draft"',
		# 	'aggregation': 'sum'
		# },

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