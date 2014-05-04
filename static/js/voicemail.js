$(document).ready(function ()  {
	$("#check").click(function () {
		var mobilenumber = $("#number").val();

		var request = $.ajax({
			crossDomain: true,
			dataType: "text",
			url: "https://scripts.cyphar.com/voicemail/api/" + mobilenumber,
			beforeSend: (function (xhr) {
				$("#output").text("")
							.hide();

				$("body").removeClass("good bad error");
			}),
		});

		request.done(function (data) {
			var resp = $.parseJSON(data);

			var isvuln = resp.body.vulnerable;
			var telco = resp.body.telco;

			if(isvuln === null || telco === null) {
				$("#output").text("Cannot find phone number")
							.show();

				$("body").removeClass("bad good")
						.addClass("error");
				return
			}

			if(isvuln === true) {
				$("#output").text("Vulnerable: " + telco)
							.show();

				$("body").removeClass("error good")
						.addClass("bad");
			} else {
				$("#output").text("Not Vulnerable: " + telco)
							.show();

				$("body").removeClass("error bad")
						.addClass("good");
			}
		});

		request.fail(function (_, textstatus) {
			console.log("Error! " + textstatus);
		});
	});

	$("#number").keyup(function (e) {
		if(e.keyCode == 13) {
			$("#check").trigger("click");
		}
	});
});
