$(document).ready(function() {

	$('.mkSelect2').select2();
	$('select[data-type="select2"]').select2();
	$('select[data-type="select2-tags"]').select2({
		tags: true
	});

	$("blockquote").addClass("blockquote");

	$('.mkSelect2').select2({
		closeOnSelect: true
	});

	$('.datatable').DataTable({
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
	});

	$('.datatable-desc').DataTable({
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		"order": [[ 0, "desc"]]
	});

	$('.datatable-sort3d').DataTable({
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		"order": [[ 2, "desc"]]
	});

	$(function () {
		$('[data-toggle="tooltip"]').tooltip();
	});

	$(function () {
		$('.jquery-tooltip').tooltip();
	});

	$('#scroll-top').click(function() {
			$("html, body").animate({
				scrollTop: 0
			}, 100);
			return false;
	});

});
