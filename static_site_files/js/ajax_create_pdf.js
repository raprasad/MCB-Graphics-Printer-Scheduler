$(function() {

	$("#button_back").click(function() {
		window.history.back();
	    });

	$("#button_download_pdf").click(function() {
		var html_str = "";
		html_str += "<!doctype html>\n";
		html_str += "<html>\n";
		html_str += "<head>\n";
		html_str += "<link href=\"/static/css/mcb_graphics_print.css\" type=\"text/css\" rel=\"stylesheet\">\n";
		html_str += "<link href=\"/static/css/preview_styles.css\" type=\"text/css\" rel=\"stylesheet\">\n";
		html_str += "</head>\n";
		html_str += "<body>\n";
		var preview_content = $("#preview_div").html().replace('"', '\"');
		html_str += preview_content + "\n";
		html_str += "</body>\n";
		html_str += "</html>\n";
		alert(html_str);
	    });
});