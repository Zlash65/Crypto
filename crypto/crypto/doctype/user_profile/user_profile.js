frappe.ui.form.on('User Profile', {
	onload: function(frm) {
		// override button onclick to set route_options
		$('button[data-doctype="ToDo"]').click(function() {
			frappe.route_options = {
				"reference_type": "User Profile",
				"reference_name": frm.doc.name
			};
		});

		// override button onclick to set route_options
		$('button[data-doctype="Event"]').click(function() {
			frappe.route_options = {
				"ref_type": "User Profile",
				"ref_name": frm.doc.name
			};
		});
	}
});
