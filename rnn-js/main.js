/* I used Andrej Karpathy's char-rnn to train a model in Torch and then I used
 * export_to_recurrentjs.lua (from Davide Testuggine) to convert it to
 * JSON. This is just a small demo to wire it up in the browser.
 */


(function() {

	var modelName = "rnn-js/models/Pope1.3055.json";
	var sampler = RSampler(modelName, {temperature: 0.5});


	var write = document.getElementById("write");
	var clear = document.getElementById("clear");
	var output = document.getElementById("output-text");

	var writeLine = function() {
		var line = sampler.getLine();
		output.innerHTML = output.innerHTML + line + '\n';
	};

	var writeStanza = function() {
		var lines = [];
		while ((line = sampler.getLine())) {
			lines.push(line);
		};
		output.innerHTML = output.innerHTML + lines.join('\n') + '\n\n';
	}


	write.addEventListener("click", function() {
		// var stanza = sampler.getStanza();
		// output.innerHTML = output.innerHTML + stanza + '\n';
		setTimeout(writeStanza, 0);
		clear.disabled = false;
	});

	clear.addEventListener("click", function() {
		output.innerHTML = "";
		clear.disabled = true;
	});





})();


