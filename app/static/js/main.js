

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

	$('.fieldlist-add').click(function() {
		console.log('add');
		var $this = $(this);
		var fieldlist = $this.parent().parent().prev('.fieldlist');
		var lastcard = fieldlist.find('.fieldlist-card:last');
		console.log(lastcard);
		//var id = lastcard.find('').find('').split('-');
		var newcard = lastcard.slideDown().clone()
		newcard.find("span.select2.select2-container").remove();
		var new_id_num = 1;
		newcard.find("input, select, textarea").each(function() {
			var id = $(this).attr('id');
			var id_list = id.split('-');
			console.log(id_list);
			var orig_id_num = id_list[1];
			id_list[1] = new_id_num;
			var new_id = id_list.join('-');
			console.log(new_id);
			while (($('#' + new_id).length)) {
				new_id_num += 1;
				id_list[1] = new_id_num;
				new_id = id_list.join('-');
				console.log(new_id);
			}
			$(this).attr('name', new_id);
			$(this).attr('id', new_id);
			$(this).removeAttr('data-select2-id');
			$(this).removeAttr('tabindex');
			$(this).removeClass('select2-hidden-accessible');
			$(this).parent().prev('label').attr('for',new_id);
			$(this).prev('label').attr('for', new_id);
		});
		newcard.appendTo(fieldlist);
		// var newcard = fieldlist.find('.fieldlist-card:last');
		newcard.hide().slideDown();
		$('select[data-type="select2"]').select2();

		if (fieldlist.find('.fieldlist-card').length > 0) {
			$('.fieldlist-remove').show();
		}
	});

	$(document).on('click', '.fieldlist-remove', function() {
		var $this = $(this);
		var fieldlist = $this.parent().parent().parent('.fieldlist');
		var card = $this.parent().parent('.fieldlist-card');
		card.slideUp('slow', function(){ card.remove(); });

		console.log(fieldlist.find('.fieldlist-card').length);
		if (fieldlist.find('.fieldlist-card').length < 3) {
			$('.fieldlist-remove').hide();
		} else {
			$('.fieldlist-remove').show();
		}
	});

});
