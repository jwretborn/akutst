/**
 * API-actions
 */
import AppDispatcher from '../dispatchers/app-dispatcher.js';
var ApiConstants = require('../constants/api-constants');

/**
 * Dict of available MapActions
 */
var ApiActions = {
    /**
     * @param {string} query Url to fetch
     */
     get: function(query) {
         AppDispatcher.dispatch({
             type : ApiConstants.GET_REQUEST,
             payload : query
         });
     },
};

module.exports = ApiActions;
