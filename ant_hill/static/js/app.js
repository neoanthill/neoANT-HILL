$(document).ready(function(){

    $('[data-toggle="tooltip"]').tooltip({
        html: true
    });

    $('#btn_step2').click(function(){

        $('#loader').css("display", "block");
        $("#tab-container").css("display", "none");

        data = getinputdata();

        $.post('/input_processing', data, function(response, status){

            var msg = $.parseJSON(response);

            if(msg["status"] == "success") {

                $('#tab_step2').css('visibility', 'visible');
                $('.nav-tabs a[href="#menu1"]').tab('show');
                $('#tab_step1').css('color', '#00a3b6');
            
            } else{

                $.notify({
                    message: msg["message"]
                },{
                    type: "danger"
                });

            };

        }).always(function() {

            $("#tab-container").css("display", "block");
            $('#loader').css("display", "none");

        });

        
    });

    $('#btn_step3').click(function(){

        data = getfastqdata()

        if (data.function.length === 0) {

            $('#tab_step3').css('visibility', 'visible');
            $('.nav-tabs a[href="#menu2"]').tab('show');
            $('#tab_step2').css('color', '#00a3b6');
            return;
        }

        $('#loader').css("display", "block");
        $("#tab-container").css("display", "none");

        $.post('/additional_processing', data, function(response, status){

            var msg = $.parseJSON(response);

            if(msg["status"] == "success") {
                
                $('#p-allele').append(msg["message"]);
                

            } else {
                $.notify({
                    message: msg["message"]
                },{
                    type: "danger"
                });
            };
        
        }).always(function() {

            $('.nav-tabs a[href="#menu2"]').tab('show');
            $('#tab_step3').css('visibility', 'visible');
            $('#tab_step2').css('color', '#00a3b6');

            $("#tab-container").css("display", "block");
            $('#loader').css("display", "none");

        });
        
    });

    $('#btn_finalstep').click(function(){

        data = getbpdata()

        $('#loader').css("display", "block");
        $("#tab-container").css("display", "none");

        $.post('/binding_prediction', data, function(response, status){

            var msg = $.parseJSON(response);

            if(msg["status"] == "success") {

                window.location.replace("/?status=" + msg["status"]);
                
            } else if(msg["status"] == "warning") {

                window.location.replace("/?status=" + msg["status"]); 
		    
	    } else {

                $.notify({
                    message: msg["message"]
                },{
                    type: "danger"
                });

                $("#tab-container").css("display", "block");
                $('#loader').css("display", "none");
            }

        });

    });

    $('#input-type').change(function(){

        if($(this).val() == "vcf"){
            $('#bam-input').css('display', 'none');
            $('#genome-input').css('display', 'none');
            $('#bam').val('');
            $('#vcf-input').css('display', 'block');
            
        } else{
            $('#vcf-input').css('display', 'none');
            $('#vcf').val('');
            $('#bam-input').css('display', 'block');
            $('#genome-input').css('display', 'block');
        };
        $('#btn_step2').prop('disabled', true);
        $('#btn_step2').removeClass("btn-info");

    });

    $('.input-step1').change(function() {
        if($(this).prop('files')) {
            $('#btn_step2').prop('disabled', false);
            $('#btn_step2').addClass("btn-info");
        } else {
            $('#btn_step2').prop('disabled', true);
            $('#btn_step2').removeClass("btn-info");
        };
    });

    $('.input-step2').change(function() {
        if($(this).prop('files')) {
            $('.function').prop('disabled', false);
            $('.function').prop('checked', true);
        };
    });

	$.each(Object.keys(class1), function(index, method) {
                $('#method')
                .append($("<option></option>")
                .attr("value",method)
                .text(method));
    });

	$.each(class1["iedb_ann"]["alleles"], function(index, allele) {
                $('#allele')
                .append($("<option></option>")
                .attr("value",allele)
                .text(allele));
    });

	$.each(class1["iedb_ann"]["lengths"], function(index, length) {
                $('#length')
                .append($("<option></option>")
                .attr("value",length)
                .text(length));
    });

   	$('#myTabs a').click(function (e) {
		e.preventDefault()
	  	$(this).tab('show')
	});

	$('#class').change(function() {
		$('#length').empty()
		$('#method').empty()
		$('#allele').empty()

		if ($(this).val() == "1"){
			$.each(Object.keys(class1), function(index, method) {
           		     $('#method')
                    	.append($("<option></option>")
                        .attr("value",method)
    	                .text(method));
	        });

			$.each(class1["iedb_ann"]["alleles"], function(index, allele) {
            		$('#allele')
                    	.append($("<option></option>")
                    	.attr("value",allele)
                        .text(allele));
    		});

	        $.each(class1["iedb_ann"]["lengths"], function(index, length) {
            		$('#length')
                        .append($("<option></option>")
    	                .attr("value",length)
            	        .text(length));
	        });

  		} else {
			$.each(Object.keys(class2), function(index, method) {
    	    		$('#method')
                        .append($("<option></option>")
    	                .attr("value",method)
            	        .text(method));
	        });
			
            $.each(class2["iedb_comblib"]["alleles"], function(index, allele) {
                        $('#allele')
                            .append($("<option></option>")
                            .attr("value",allele)
                            .text(allele));
            });

            $.each(class2["iedb_comblib"]["lengths"], function(index, length) {
                $('#length')
                    .append($("<option></option>")
                    .attr("value",length)
                    .text(length));
            });

  		};

	});

	$('#method').change(function() {

		$('#filter').empty()
		$('#allele').empty()
		$('#length').empty()
        $('#allele-check-all').prop('checked', false);
        $('#allele-check-predicted').prop('checked', false);

		if ($('#class').val() == "1"){
			$.each(class1[$(this).val()]["lengths"], function(index, length) {
                $('#length')
                    .append($("<option></option>")
                    .attr("value",length)
                    .text(length));
            });
			
            $.each(class1[$(this).val()]["alleles"], function(index, allele) {
                $('#allele')
                    .append($("<option></option>")
                    .attr("value",allele)
                    .text(allele));
            });

		} else {
			$.each(class2[$(this).val()]["lengths"], function(index, length) {
                $('#length')
                    .append($("<option></option>")
                    .attr("value",length)
                    .text(length));
            });
            $.each(class2[$(this).val()]["alleles"], function(index, allele) {
                $('#allele')
                    .append($("<option></option>")
                    .attr("value",allele)
                    .text(allele));
            });

		};

	});

	$('#submit').click(function() {

		$('#loader').css("display", "block");
		$("#container").css("display", "none");

	});

    $('#allele-check-all').change(function(){

        if ($(this).prop('checked')) {
            $('#allele option').prop('selected', true);
        } else {
            $('#allele option').prop('selected', false);
        };

    });

    $('#allele-check-predicted').change(function(){

        var pal = getpredictedalleles();

        if ($(this).prop('checked')) {
            $('#allele option').each(function(index){
                if($.inArray($(this).text(), pal) >= 0) {
                    $(this).prop('selected', true);
                };
            });
        } else {
            $('#allele option').each(function(index){
                if($.inArray($(this).text(), pal) >= 0) {
                    $(this).prop('selected', false);
                };
            });
        };

    });

});

function getfastqdata() {
    
    var data = {};
    var fastq = $.map($('#fastq').prop('files'), function(val) { return val.name; });
    var fun = [];
    
    $('.function:checked').each(function() {
        fun.push($(this).val());
    });

    data = {
        "function": fun,
        "output": $('#output').val(),
        "fastq": fastq
    }

    return data;
};

function getinputdata() {
    var data = {};
    var input, type;

    if ($('#input-type').val() == "vcf") {
        input = $('#vcf').prop('files')[0].name;
        type = "vcf"
    } else {
        input = $.map($('#bam').prop('files'), function(val) { return val.name; });
        type = "bam"
    };

    data = {
        "input": input,
        "type": type,
        "output": $('#output').val()
    }

    return data;

}

function getbpdata() {

    var data = {};
    var method, len, allele;

    len = $.map($("#length :selected"), function(el) { return $(el).text(); });
    allele = $.map($("#allele :selected"), function(el) { return $(el).text(); });

    data = {
        "class": $('#class option:selected').text(),
        "method": $('#method option:selected').text(),
        "length": len,
        "allele": allele,
        "parallel": $('#parallel option:selected').text(),
        "output": $('#output').val()
    }

    return data;

};

function getpredictedalleles() {
    var pa = $.map($('#p-allele').text().split('\n'), function(line) { return line.split(' ')[0]; });
    return pa;
};

