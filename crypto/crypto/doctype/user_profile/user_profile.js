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
	},
	refresh: function(frm) {
		frm.trigger("make_dashboard");
	},
	onload_post_render: function(frm) {
		frm.trigger("make_dashboard");
	},
	make_dashboard: function(frm) {
		frappe.call({
			method: "crypto.crypto.doctype.user_profile.user_profile.get_dashboard_data",
			args: {
				"username": frm.doc.username
			}
		}).then(r => {
			if(r.message.data.length > 0) {
				$("div").remove(".form-dashboard-section.custom");
				let section = frm.dashboard.add_section(
					frappe.render_template('user_profile_dashboard_template', {
						data: r.message.data,
						columns: r.message.columns
					})
				);
				frm.dashboard.show();
			}
		});
	},
});
