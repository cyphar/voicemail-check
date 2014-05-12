/* acma: finds the telco for a number (and tells you if it is vuln to voicemail attacks)
 * Copyright (C) 2014, Cyphar All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its contributors
 *    may be used to endorse or promote products derived from this software without
 *    specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 * USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

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
				$("#output").text("Was Vulnerable: " + telco + ".");

				$("body").removeClass("error good")
						.addClass("bad");
			} else {
				$("#output").text("Wasn't vulnerable: " + telco + ".");

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
