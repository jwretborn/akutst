import AjaxResource from '../utils/ajax-resource.js';
import AppDispatcher from '../dispatchers/app-dispatcher.js';
import { EventEmitter } from 'events'
import ApiConstants from '../constants/api-constants.js';

var CHANGE_EVENT = 'change';

class ApiStoreClass extends EventEmitter {

	constructor(urlPattern) {
		super();

		if (urlPattern === undefined) {
			urlPattern = '';
		}

		this.url = '/api/';
		this.cache = {};
	}

	get(query) {
		var url = this.parseUrl(query);
		if ( ! this.cache[url] ) {
			// load request
			AjaxResource.get(url).then(this.updateFromServer, this.errorFromServer);
			this.cache[url] = 'loading';
		}

		return this.cache[url];
	}

	updateFromServer(response) {
		AppDispatcher.dispatch({
			type : ApiConstants.DATA_FROM_SERVER,
			payload : response
		});
	}

	errorFromServer(error) {
		console.log(error);
	}

	handleDataFromServer(action) {
		this.cache[action.payload.id] = action.payload.data;
	}

	/**
	 * Emit change event
	 */
	emitChange() {
		this.emit(CHANGE_EVENT);
	}

	/**
	 * Add callback to the emitter
	 * @param {function} callback
	 */
	addChangeListener(callback) {
		this.on(CHANGE_EVENT, callback);
	}

	/**
	 * Remove callback from the emitter
	 * @param {function} callback
	 */
	removeChangeListener(callback) {
		this.removeListener(CHANGE_EVENT, callback);
	}

	parseUrl(part) {
		var url = '';

		if (part === undefined) {
			part = '';
		}

		// Check if we have a number
		if ((typeof part === 'number') && (part % 1 === 0) ) {
			// Check if we have a pattern
			if (this.url.indexOf('<id>')) {
				url = this.url.replace("<id>", part);
			}
			else {
				url = this.url+part;
			}
		}
		else {
			url = this.url+part;
		}
		return url;
	}
}

const ApiStore = new ApiStoreClass();

AppDispatcher.register((action) => {
	switch(action.type) {
		case ApiConstants.DATA_FROM_SERVER :
			ApiStore.handleDataFromServer(action);
			ApiStore.emitChange();
			break;
		case ApiConstants.GET_REQUEST :
			ApiStore.get(action.payload);
			ApiStore.emitChange();
			break;
		default :
			break;
	}
});


export default ApiStore
