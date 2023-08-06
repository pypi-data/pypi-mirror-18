function isblank(s) {
	for (var j=0; j<s.length; j++) {
		var a = s.charAt(j);
		if ((a != ' ') && (a != '\\n') && (a != '\\t') && (a != '\\r')) return false;
	}
	return true;
}

// Old function that used to check the login with username and password
function checkBlankLogin(f) {
	if (isblank(f.username.value) || isblank(f.password.value)) {
		alert("Please fill in the form with both username and password\n");
		return false;
	}
	return true;
}

function checkRegistration(f) {
	if (isblank(f.name.value) || isblank(f.surname.value) || 
	   isblank(f.email.value) || isblank(f.institution.value)) {
		alert("Please fill all the fields of the form\n");
                return false;
        }
	if (!checkEmail(f)) {
		return false;
	}
	if (!compareEmails(f)) {
		return false;
	}
	return true
}

function checkEmail(f) {
	var email = f.email;
	var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

    	if (!filter.test(email.value)) {
    		alert('Please provide a valid email address');
    		email.focus;
    		return false;
	}
	return true;
}

function compareEmails(f) {
        var email1 = f.email.value;
        var email2 = f.email_confirm.value;
        if (email1 == email2) {
                return true;
        } else {
                alert("The email addresses do not match");
                return false;
        }
}

function toggleSnps() {
	if (document.getElementById("select_snps").value == "diagram_custom" | 
		document.getElementById("select_snps").value == "magic_custom") {
		document.getElementById("custom").className = "";
	} else {
		document.getElementById("custom").className = "hiddenRow";
	}
}

function toggleUpload() {
	if (document.getElementById("snp_upload").value != "" | 
		document.getElementById("regions_upload").value != "") {
		document.getElementById("upload_button").disabled = false;
	} else {
		document.getElementById("upload_button").disabled = true;
	}
}

function uploadit() {
	if (document.getElementById("snp_upload").value == "" & document.getElementById("regions_upload").value == "") {
		alert("Please select a file to download");
		return false;
	}
	var i = 2;
	var msg = "";
	if (document.getElementById("regions_upload").value != "") {
		msg = document.getElementById("regions_upload").value;
		document.getElementById("uploaded_" + i).innerHTML = 'Uploading ' + msg + ' ...';
		i += 1;
	} 
	if (document.getElementById("snp_upload").value != "") {
		msg = document.getElementById("snp_upload").value;
		document.getElementById("uploaded_" + i).innerHTML = 'Uploading ' + msg + ' ...';
	}
	document.getElementById("action").value = "upload";
	return true;
}

function setMessage() {
	var action = document.getElementById("action").value;
	var msg_1 = "";
	var msg_2 = "";

	if (action == "upload") {
		msg_1 = "Uploading...";
		msg_2 = "Uploading, please wait...";
	} else if (action == "submit") {
		msg_1 = "Generating plot...";
		msg_2 = "Generating plot, please wait...";
	} else if (action == "clear") {
		return true;
	} else if (action == "infos") {
		return true;
	} else {
		return true;
	}

	document.getElementById("loader").alt = msg_1;
	document.getElementById("loader_caption").innerHTML = msg_2;
	document.getElementById("loader_caption").style.display = "inline";
	document.getElementById("loader").style.display = "";

	return true;
}

function showUploaded() {
	var i = 0;
	var msg = " dataset uploaded";

	// Set "snp_diagram", "snp_magic" and "snp_custom" to FALSE
	document.getElementById("snp_diagram").value = 'FALSE';
	document.getElementById("snp_magic").value = 'FALSE';
	document.getElementById("snp_custom").value = 'FALSE';

	if (document.getElementById("select_snps").value == "diagram" | 
		document.getElementById("select_snps").value == "diagram_magic" | 
		document.getElementById("select_snps").value == "diagram_custom") {
		i += 1;
		document.getElementById("uploaded_" + i).innerHTML = 'DIAGRAM' + msg;
		document.getElementById("snp_diagram").value = 'TRUE';
	}
	if (document.getElementById("select_snps").value == "magic" |
		document.getElementById("select_snps").value == "diagram_magic" |
		document.getElementById("select_snps").value == "magic_custom") {
		i += 1;
        	document.getElementById("uploaded_" + i).innerHTML = 'MAGIC' + msg;
		document.getElementById("snp_magic").value = 'TRUE';
	}
	if (document.getElementById("select_snps").value == "diagram" | 
		document.getElementById("select_snps").value == "magic") {
		i += 1; document.getElementById("uploaded_" + i).innerHTML = '';
		i += 1; document.getElementById("uploaded_" + i).innerHTML = '';
	}
	if (document.getElementById("select_snps").value == "diagram_custom" | 
		document.getElementById("select_snps").value == "magic_custom") {
		i = 2;
		var loaded = false;
		var db_name = "";

		if (document.getElementById("upload_snp_in").value != "None" & 
			document.getElementById("upload_snp_in").value != "") {
			loaded = true;
			db_name = document.getElementById("upload_snp_in").value;
		}
		if (loaded) {
			document.getElementById("uploaded_" + i).innerHTML = "File " + db_name + " uploaded";
			document.getElementById("snp_custom").value = 'TRUE';
		} else {
			document.getElementById("uploaded_" + i).innerHTML = '';
			document.getElementById("snp_custom").value = 'FALSE';
		}
		document.getElementById("upload_button").disabled = false; 
	}
}

function notAvailableYet() {
	alert("The region upload feature is not available yet");
}

function catchKey(event) {
	if (event.which || event.keyCode) {
		if ((event.which == 13) || (event.keyCode == 13)) {
			if (confirmall() && setMessage()) {
				//alert("ok!");
				document.getElementById("action").value = "submit";
				document.getElementById("form1").submit();
 				return true;
			} else {
				//alert("no!");
				return false;
			}
 		}
 	} else {
 			return false;
 	}
}

