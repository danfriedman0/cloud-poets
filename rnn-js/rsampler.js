/**
 * Simple wrapper to sample from a pre-trained model using
 * Andrej Karpathy's recurrent.js.
 *
 * Most of this is based on code from recurrentjs/character_demo.html
 */



var RSampler = function(modelName, opts) {
	if (window === this) return new RSampler(modelName, opts);

	this.max_chars_gen = 100;
	this.letterToIndex;
	this.indexToLetter;
	this.generator;
	this.hidden_sizes;
	this.model;

	this.temperature = opts && opts.temperature ? opts.temperature : 0.4;
	this.samplei = opts && opts.samplei ? opts.samplei : true;

	this.prev = {};

	// Karpathy


	// AJAX to load the model, from @KryptoniteDove on codepen
	var loadJson = function(filename, callback) {
		var xobj = new XMLHttpRequest();
		xobj.overrideMimeType("application/json");
		xobj.open("GET", filename, true);
		xobj.onreadystatechange = function() {
			if (xobj.readyState == 4 && xobj.status == "200") {
				console.log(xobj.responseText);
				callback(xobj.responseText);
			}
		}
		xobj.send(null);
	};

	// Load the model when the sampler is initialized
	loadJson(modelName, function(response) {
		this.loadModel(JSON.parse(response));
	}.bind(this));
};


RSampler.prototype.loadModel = function(j) {
	this.hidden_sizes = j.hidden_sizes;
	this.generator = j.generator;
	this.model = {};
	for (var k in j.model) {
		if (j.model.hasOwnProperty(k)) {
			this.model[k] = new R.Mat(1,1);
			this.model[k].fromJSON(j.model[k]);
		}
	}
	this.letterToIndex = j['letterToIndex'];
	this.indexToLetter = j['indexToLetter'];
};

/* forwardIndex and predictSentence are from Karpathy */
RSampler.prototype.forwardIndex = function(G, model, ix, prev) {
	var x = G.rowPluck(model['Wil'], ix);
	return R.forwardLSTM(G, model, this.hidden_sizes, x, prev);
};

RSampler.prototype.predictSentence = function(max_chars_gen) {
	var model = this.model,
		prev = this.prev,
		samplei = this.samplei,
		temperature = this.temperature;

	console.log(model);

	if (!max_chars_gen) max_chars_gen = this.max_chars_gen;

	var G = new R.Graph(false);
	var s = '';

	while(true) {

		// RNN tick
		var ix = s.length === 0 ? 0 : this.letterToIndex[s[s.length-1]];
		var lh = this.forwardIndex(G, model, ix, prev);
		prev = lh;

		// sample predicted letter
		logprobs = lh.o;
		if(temperature !== 1.0 && samplei) {
			// scale log probabilities by temperature and renormalize
			// if temperature is high, logprobs will go towards zero
			// and the softmax outputs will be more diffuse. if
			// temperature is very low, the softmax outputs will be
			// more peaky
			for(var q=0,nq=logprobs.w.length;q<nq;q++) {
				logprobs.w[q] /= temperature;
			}
		}

		probs = R.softmax(logprobs);
		if(samplei) {
			var ix = R.samplei(probs.w);
		} else {
			var ix = R.maxi(probs.w);  
		}
		
		if(ix === 0) break; // END token predicted, break out
		if(s.length > max_chars_gen) { break; } // something is wrong
		var letter = this.indexToLetter[ix];
		if (letter)
			s += letter;
		else
			s += ' ';
	};
	this.prev = prev;
	return s;
};


/* API */

RSampler.prototype.getLine = function() {
	return this.predictSentence();
};

RSampler.prototype.getStanza = function() {
	var lines = [];
	var line;
	while ((line = this.predictSentence())) {
		lines.push(line);
	}
	return lines.join('\n');
};

RSampler.prototype.getChar = function() {
	return this.predictSentence(1);
};

RSampler.prototype.setTemp = function(temp) {
	this.temperature = temp;
};












