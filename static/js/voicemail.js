$(document).ready(function ()  {
	$("#check").click(function () {
		var mobilenumber = $("#number").val();

		var request = $.ajax({
			crossDomain: true,
			dataType: "text",
			url: "https://scripts.cyphar.com/voicemail/api/" + mobilenumber,
			beforeSend: (function (xhr) {
				$("#output").text("Checking number ...")

				$("body").removeClass("good bad error");
			}),
		});

		request.done(function (data) {
			var resp = $.parseJSON(data);

			var isvuln = resp.body.vulnerable;
			var telco = resp.body.telco;

			if(isvuln === null || telco === null) {
				$("#output").text("Cannot find phone number.");

				$("body").removeClass("bad good")
						.addClass("error");
				return
			}

			if(isvuln === true) {
				$("#output").text("Vulnerable: " + telco + ".");

				$("body").removeClass("error good")
						.addClass("bad");
			} else {
				$("#output").text("Not vulnerable: " + telco + ".");

				$("body").removeClass("error bad")
						.addClass("good");
			}
		});

		request.fail(function (_, textstatus) {
			$("#output").text("An unknown error occured.")
		});
	});

	$("#number").keyup(function (e) {
		if(e.keyCode == 13) {
			$("#check").trigger("click");
		}
	});
});
