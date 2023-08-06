import QueryString from "./QueryString";


/**
 * URL parser.
 *
 * @example
 * const urlparser = new UrlParser('http://example.com/api/people?name=Jane');
 * querystring.queryString.set('search', 'doe');
 * // urlparser.buildUrl() === 'http://example.com/api/people?name=Jane&search=doe'
 */
export class UrlParser {
    constructor(url) {
        if(typeof url !== 'string') {
            throw new TypeError('url must be a string.');
        }
        const urlSplit = url.split('?');
        this._baseUrl = urlSplit[0];

        /**
         * The query-string of the the URL.
         * @type {QueryString}
         */
        this.queryString = null;

        if(urlSplit.length > 1) {
            this.setQueryString(new QueryString(urlSplit[1]));
        } else {
            this.setQueryString(new QueryString());
        }
    }

    /**
     * Build the URL.
     * @returns {String} The built URL.
     */
    buildUrl() {
        let url = this._baseUrl;
        if(!this.queryString.isEmpty()) {
            url = `${url}?${this.queryString.urlencode()}`;
        }
        return url;
    }

    /**
     * Set/replace the query-string.
     *
     * @param {QueryString} queryStringObject The QueryString object
     *      to replace the current query-string with.
     *
     * @example
     * const urlparser = UrlParser('http://example.com/api/people');
     * const querystring = new QueryString();
     * querystring.set('search', 'doe');
     * urlparser.setQueryString(querystring);
     * // urlparser.buildUrl() === 'http://example.com/api/people?search=doe'
     */
    setQueryString(queryStringObject) {
        this.queryString = queryStringObject;
    }
}
