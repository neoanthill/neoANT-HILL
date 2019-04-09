$(document).ready(function(){

	var table = $('#result-table').DataTable({
		responsive: true,
		dom: 'lBfrtip',
		buttons: [{
			extend: 'copyHtml5',
	        exportOptions: {
	            columns: ':visible'
	        }
		  },
		  {
		  	extend: 'csvHtml5',
	        exportOptions: {
	            columns: ':visible'
	        }
		  }, 
		  'colvis'
		],
	
	});

	table.buttons().container().appendTo( $('.col-sm-6:eq(0)', table.table().container() ) );

	$('#gene-result-table').DataTable();

});
