import QueryString from "../../http/QueryString";
import {UrlParser} from "../../http/UrlParser";


describe('UrlParser', () => {
    it('setQueryString', () => {
        const urlparser = new UrlParser('http://example.com/');
        expect(urlparser.queryString.isEmpty()).toBe(true);
        const querystring = new QueryString();
        querystring.set('name', 'Jane');
        urlparser.setQueryString(querystring);
        expect(urlparser.queryString.urlencode()).toBe('name=Jane');
    });

    it('buildUrl() no querystring', () => {
        const urlparser = new UrlParser('http://example.com/api/people');
        expect(urlparser.buildUrl()).toBe('http://example.com/api/people');
    });

    it('buildUrl() with querystring', () => {
        const urlparser = new UrlParser('http://example.com/api/people');
        urlparser.queryString = new QueryString('name=Jane');
        expect(urlparser.buildUrl()).toBe('http://example.com/api/people?name=Jane');
    });
});
