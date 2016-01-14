class AjaxResourceClass {
	
	constructor() {		
		this.promises = {};
	}

	/**
	 * Simple get function expecting a json response
	 * @param {string} The url to query
	 */
	get(url) {
		if ( ! this.promises[url] ) {
			// TODO: change to http://visionmedia.github.io/superagent ?
			this.promises[url] = new Promise(function(resolve, reject) {
				// Do the usual XHR stuff
				var req = new XMLHttpRequest();
				req.open('GET', url);

				req.onload = function() {
					// This is called even on 404 etc
					// so check the status
					if (req.status == 200) {
						// Resolve the promise with the response text
						resolve({ 
							id : url, 
							data : JSON.parse(req.response)
						});
					}
					else {
						// Otherwise reject with the status text
						// which will hopefully be a meaningful error
						reject(Error(req.statusText));
					}
				};

				// Handle network errors
				req.onerror = function() {
					reject(Error("Network Error"));
				};

				// Make the request
				req.send();
  			});
		} 
		return this.promises[url];
	}
}

const AjaxResource = new AjaxResourceClass();

export default AjaxResource;