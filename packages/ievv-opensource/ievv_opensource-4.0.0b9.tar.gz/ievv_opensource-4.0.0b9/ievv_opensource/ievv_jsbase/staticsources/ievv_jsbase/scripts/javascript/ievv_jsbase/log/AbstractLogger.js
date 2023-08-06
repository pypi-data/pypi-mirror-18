import LOGLEVEL from "./loglevel";


/**
 */
export default class AbstractLogger {
    getLogLevel() {
        throw new Error('Must be overridden in subclasses.');
    }

    _noOutput() {

    }

    /**
     * Exposes console.log. Will only print if current level is
     * higher than {@link LogLevels#DEBUG}.
     * @returns {Function} console.log
     */
    get debug() {
        if (this.getLogLevel() >= LOGLEVEL.DEBUG) {
            return console.log.bind(console);
        }
        return this._noOutput;
    }

    /**
     * Exposes console.log. Will only print if current level is
     * higher than {@link LogLevels#INFO}.
     * @returns {Function} console.log
     */
    get info() {
        if (this.getLogLevel() >= LOGLEVEL.INFO) {
            return console.log.bind(console);
        }
        return this._noOutput;
    }

    /**
     * Exposes console.warn. Will only print if current level is
     * higher than {@link LogLevels#WARNING}.
     * @returns {Function} console.warn
     */
    get warning() {
        if(this.getLogLevel() >= LOGLEVEL.WARNING) {
            return console.warn.bind(console);
        }
        return this._noOutput;
    }

    /**
     * Exposes console.error. Will only print if current level is
     * higher than {@link LogLevels#ERROR}.
     * @returns {Function} console.error
     */
    get error() {
        if (this.getLogLevel() >= LOGLEVEL.ERROR) {
            return console.error.bind(console);
        }
        return this._noOutput;
    }
}
