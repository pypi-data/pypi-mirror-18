(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.SentSignalInfo = exports.ReceivedSignalInfo = exports.DuplicateReceiverNameForSignal = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _makeCustomError = require("./makeCustomError");

var _makeCustomError2 = _interopRequireDefault(_makeCustomError);

var _PrettyFormat = require("./utils/PrettyFormat");

var _PrettyFormat2 = _interopRequireDefault(_PrettyFormat);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Exception raised by {@link HttpCookies#getStrict} when the cookie is not found.
 *
 * @type {Error}
 */
var DuplicateReceiverNameForSignal = exports.DuplicateReceiverNameForSignal = (0, _makeCustomError2.default)('DuplicateReceiverNameForSignal');

/**
 * Represents information about the received signal.
 *
 * An object of this class is sent to the ``callback``
 * of all signal receivers.
 *
 * The data sent by the signal is available in
 * {@link ReceivedSignalInfo.data}.
 */

var ReceivedSignalInfo = exports.ReceivedSignalInfo = function () {
    function ReceivedSignalInfo(data, signalName, receiverName) {
        _classCallCheck(this, ReceivedSignalInfo);

        /**
         * The data sent by {@link SignalHandlerSingleton#send}.
         */
        this.data = data;

        /**
         * The signal name.
         *
         * @type {string}
         */
        this.signalName = signalName;

        /**
         * The receiver name.
         *
         * @type {string}
         */
        this.receiverName = receiverName;
    }

    /**
     * Get a string with debug information about the received signal.
     */


    _createClass(ReceivedSignalInfo, [{
        key: "toString",
        value: function toString() {
            var prettyData = new _PrettyFormat2.default(this.data).toString(2);
            return "signalName=\"" + this.signalName + "\", " + ("receiverName=\"" + this.receiverName + "\", ") + ("data=" + prettyData);
        }
    }]);

    return ReceivedSignalInfo;
}();

/**
 * Private class used by {@link _SignalReceivers} to represent
 * a single receiver listening for a single signal.
 */


var _SignalReceiver = function () {
    function _SignalReceiver(signal, name, callback) {
        _classCallCheck(this, _SignalReceiver);

        this.signal = signal;
        this.name = name;
        this.callback = callback;
    }

    /**
     * Asynchronously trigger the receiver callback.
     * @param data The signal data (the data argument provided for
     *    {@link SignalHandlerSingleton#send}.
     */


    _createClass(_SignalReceiver, [{
        key: "trigger",
        value: function trigger(data) {
            var _this = this;

            setTimeout(function () {
                _this.callback(new ReceivedSignalInfo(data, _this.signal.name, _this.name));
            }, 0);
        }
    }]);

    return _SignalReceiver;
}();

/**
 * Object containing debugging information about a sent
 * signal.
 */


var SentSignalInfo = exports.SentSignalInfo = function () {
    function SentSignalInfo(signalName) {
        _classCallCheck(this, SentSignalInfo);

        /**
         * The signal name.
         *
         * @type {string}
         */
        this.signalName = signalName;

        /**
         * Array of triggered receiver names.
         *
         * @type {Array}
         */
        this.triggeredReceiverNames = [];
    }

    _createClass(SentSignalInfo, [{
        key: "_addReceiverName",
        value: function _addReceiverName(receiverName) {
            this.triggeredReceiverNames.push(receiverName);
        }

        /**
         * Get a string representation of the sent signal info.
         *
         * @returns {string}
         */

    }, {
        key: "toString",
        value: function toString() {
            var receivers = this.triggeredReceiverNames.join(', ');
            if (receivers === '') {
                receivers = 'NO RECEIVERS';
            }
            return "Signal: " + this.signalName + " was sent do: " + receivers;
        }
    }]);

    return SentSignalInfo;
}();

/**
 * Private class used by {@link SignalHandlerSingleton}
 * to represent all receivers for a single signal.
 */


var _SignalReceivers = function () {
    function _SignalReceivers(name) {
        _classCallCheck(this, _SignalReceivers);

        this.name = name;
        this.receiverMap = new Map();
    }

    /**
     * Add a receiver.
     *
     * @throw DuplicateReceiverNameForSignal If the receiver is already registered for the signal.
     */


    _createClass(_SignalReceivers, [{
        key: "addReceiver",
        value: function addReceiver(receiverName, callback) {
            if (this.receiverMap.has(receiverName)) {
                throw new DuplicateReceiverNameForSignal("The \"" + receiverName + "\" receiver is already registered for the \"" + this.name + "\" signal");
            }
            this.receiverMap.set(receiverName, new _SignalReceiver(this, receiverName, callback));
        }

        /**
         * Remove a receiver.
         *
         * If the receiver is not registered for the signal,
         * nothing happens.
         */

    }, {
        key: "removeReceiver",
        value: function removeReceiver(receiverName) {
            if (this.receiverMap.has(receiverName)) {
                this.receiverMap.delete(receiverName);
            }
        }

        /**
         * Check if we have a specific receiver for this signal.
         */

    }, {
        key: "hasReceiver",
        value: function hasReceiver(receiverName) {
            return this.receiverMap.has(receiverName);
        }

        /**
         * Get the number of receivers registered for the signal.
         */

    }, {
        key: "receiverCount",
        value: function receiverCount() {
            return this.receiverMap.size;
        }

        /**
         * Send the signal.
         *
         * @param data The data sent with the signal. Forwarded to
         *      the signal receiver callback.
         * @param {SentSignalInfo} info If this is provided, we add the
         *      name of all receivers the signal was sent to.
         */

    }, {
        key: "send",
        value: function send(data, info) {
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = this.receiverMap.values()[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var receiver = _step.value;

                    receiver.trigger(data);
                    if (info) {
                        info._addReceiverName(receiver.name);
                    }
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }
        }
    }]);

    return _SignalReceivers;
}();

/**
 * The instance of the {@link SignalHandlerSingleton}.
 */


var _instance = null;

/**
 * Signal handler singleton for global communication.
 *
 * @example <caption>Basic example</caption>
 * let signalHandler = new SignalHandlerSingleton();
 * signalHandler.addReceiver('myapp.mysignal', 'myotherapp.MyReceiver', (receivedSignalInfo) => {
 *     console.log('Signal received. Data:', receivedSignalInfo.data);
 * });
 * signalHandler.send('myapp.mysignal', {'the': 'data'});
 *
 *
 * @example <caption>Recommended signal and receiver naming</caption>
 *
 * // In myapp/menu/MenuComponent.js
 * class MenuComponent {
 *     constructor(menuName) {
 *         this.menuName = menuName;
 *         let signalHandler = new SignalHandlerSingleton();
 *         signalHandler.addReceiver(
 *             `toggleMenu#${this.menuName}`,
 *             'myapp.menu.MenuComponent',
 *             (receivedSignalInfo) => {
 *                  this.toggle();
 *             }
 *         );
 *     }
 *     toggle() {
 *         // Toggle the menu
 *     }
 * }
 *
 * // In myotherapp/widgets/MenuToggle.js
 * class MenuToggle {
 *     constructor(menuName) {
 *         this.menuName = menuName;
 *     }
 *     toggle() {
 *         let signalHandler = new SignalHandlerSingleton();
 *         signalHandler.send(`toggleMenu#${this.menuName}`);
 *     }
 * }
 *
 * @example <caption>Multiple receivers</caption>
 * let signalHandler = new SignalHandlerSingleton();
 * signalHandler.addReceiver('myapp.mysignal', 'myotherapp.MyFirstReceiver', (receivedSignalInfo) => {
 *     console.log('Signal received by receiver 1!');
 * });
 * signalHandler.addReceiver('myapp.mysignal', 'myotherapp.MySecondReceiver', (receivedSignalInfo) => {
 *     console.log('Signal received by receiver 1!');
 * });
 * signalHandler.send('myapp.mysignal', {'the': 'data'});
 *
 *
 * @example <caption>Debugging</caption>
 * let signalHandler = new SignalHandlerSingleton();
 * signalHandler.addReceiver('mysignal', 'MyReceiver', (receivedSignalInfo) => {
 *     console.log('received signal:', receivedSignalInfo.toString());
 * });
 * signalHandler.send('myapp.mysignal', {'the': 'data'}, (sentSignalInfo) => {
 *     console.log('sent signal info:', sentSignalInfo.toString());
 * });
 *
 */

var SignalHandlerSingleton = function () {
    function SignalHandlerSingleton() {
        _classCallCheck(this, SignalHandlerSingleton);

        if (!_instance) {
            _instance = this;
            this._signalMap = new Map();
        }
        return _instance;
    }

    /**
     * Remove all receivers for all signals.
     *
     * Useful for debugging and tests, but should not be
     * used for production code.
     */


    _createClass(SignalHandlerSingleton, [{
        key: "clearAllReceiversForAllSignals",
        value: function clearAllReceiversForAllSignals() {
            this._signalMap.clear();
        }

        /**
         * Add a receiver for a specific signal.
         *
         * @param {string} signalName The name of the signal.
         *      Typically something like ``toggleMenu`` or ``myapp.toggleMenu``.
         *
         *      What if we have multiple objects listening for this ``toggleMenu``
         *      signal, and we only want to toggle a specific menu? You need
         *      to ensure the signalName is unique for each menu. We recommend
         *      that you do this by adding ``#<context>``. For example
         *      ``toggleMenu#mainmenu``. This is shown in one of the examples
         *      above.
         * @param {string} receiverName The name of the receiver.
         *      Must be unique for the signal.
         *      We recommend that you use a very explicit name for your signals.
         *      It should normally be the full path to the method or function receiving
         *      the signal. So if you have a class named ``myapp/menu/MenuComponent.js``
         *      that receives a signal to toggle the menu, the receiverName should be
         *      ``myapp.menu.MenuComponent``.
         * @param callback The callback to call when the signal is sent.
         *      The callback is called with a single argument - a
         *      {@link ReceivedSignalInfo} object.
         */

    }, {
        key: "addReceiver",
        value: function addReceiver(signalName, receiverName, callback) {
            if (typeof callback === 'undefined') {
                throw new TypeError('The callback argument for addReceiver() is required.');
            }
            if (!this._signalMap.has(signalName)) {
                this._signalMap.set(signalName, new _SignalReceivers(signalName));
            }
            var signal = this._signalMap.get(signalName);
            signal.addReceiver(receiverName, callback);
        }

        /**
         * Remove a receiver for a signal added with {@link SignalHandlerSingleton#addReceiver}.
         *
         * @param {string} signalName The name of the signal.
         * @param {string} receiverName The name of the receiver.
         */

    }, {
        key: "removeReceiver",
        value: function removeReceiver(signalName, receiverName) {
            if (this._signalMap.has(signalName)) {
                var signal = this._signalMap.get(signalName);
                signal.removeReceiver(receiverName);
                if (signal.receiverCount() === 0) {
                    this._signalMap.delete(signalName);
                }
            }
        }

        /**
         * Check if a signal has a specific receiver.
         *
         * @param {string} signalName The name of the signal.
         * @param {string} receiverName The name of the receiver.
         */

    }, {
        key: "hasReceiver",
        value: function hasReceiver(signalName, receiverName) {
            if (this._signalMap.has(signalName)) {
                var signal = this._signalMap.get(signalName);
                return signal.hasReceiver(receiverName);
            } else {
                return false;
            }
        }

        /**
         * Remove all receivers for a specific signal.
         *
         * @param {string} signalName The name of the signal to remove.
         */

    }, {
        key: "clearAllReceiversForSignal",
        value: function clearAllReceiversForSignal(signalName) {
            if (this._signalMap.has(signalName)) {
                this._signalMap.delete(signalName);
            }
        }

        /**
         * Send a signal.
         *
         * @param {string} signalName The name of the signal to send.
         * @param data Data to send to the callback of all receivers registered
         *      for the signal.
         * @param infoCallback An optional callback that receives information
         *      about the signal. Useful for debugging what actually received
         *      the signal. The ``infoCallback`` is called with a single
         *      argument - a {@link SentSignalInfo} object.
         */

    }, {
        key: "send",
        value: function send(signalName, data, infoCallback) {
            var info = null;
            if (infoCallback) {
                info = new SentSignalInfo(signalName);
            }
            if (this._signalMap.has(signalName)) {
                var signal = this._signalMap.get(signalName);
                signal.send(data, info);
            }
            if (infoCallback) {
                infoCallback(info);
            }
        }
    }]);

    return SignalHandlerSingleton;
}();

exports.default = SignalHandlerSingleton;

},{"./makeCustomError":7,"./utils/PrettyFormat":8}],2:[function(require,module,exports){
"use strict";

var _SignalHandlerSingleton = require("./SignalHandlerSingleton");

var _SignalHandlerSingleton2 = _interopRequireDefault(_SignalHandlerSingleton);

var _WidgetRegistrySingleton = require("./widget/WidgetRegistrySingleton");

var _WidgetRegistrySingleton2 = _interopRequireDefault(_WidgetRegistrySingleton);

var _LoggerSingleton = require("./log/LoggerSingleton");

var _LoggerSingleton2 = _interopRequireDefault(_LoggerSingleton);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

window.ievv_jsbase_core = {
    SignalHandlerSingleton: _SignalHandlerSingleton2.default,
    WidgetRegistrySingleton: _WidgetRegistrySingleton2.default,
    LoggerSingleton: _LoggerSingleton2.default
};

},{"./SignalHandlerSingleton":1,"./log/LoggerSingleton":5,"./widget/WidgetRegistrySingleton":10}],3:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _loglevel = require("./loglevel");

var _loglevel2 = _interopRequireDefault(_loglevel);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 */
var AbstractLogger = function () {
    function AbstractLogger() {
        _classCallCheck(this, AbstractLogger);
    }

    _createClass(AbstractLogger, [{
        key: "getLogLevel",
        value: function getLogLevel() {
            throw new Error('Must be overridden in subclasses.');
        }
    }, {
        key: "_noOutput",
        value: function _noOutput() {}

        /**
         * Exposes console.log. Will only print if current level is
         * higher than {@link LogLevels#DEBUG}.
         * @returns {Function} console.log
         */

    }, {
        key: "debug",
        get: function get() {
            if (this.getLogLevel() >= _loglevel2.default.DEBUG) {
                return console.log.bind(console);
            }
            return this._noOutput;
        }

        /**
         * Exposes console.log. Will only print if current level is
         * higher than {@link LogLevels#INFO}.
         * @returns {Function} console.log
         */

    }, {
        key: "info",
        get: function get() {
            if (this.getLogLevel() >= _loglevel2.default.INFO) {
                return console.log.bind(console);
            }
            return this._noOutput;
        }

        /**
         * Exposes console.warn. Will only print if current level is
         * higher than {@link LogLevels#WARNING}.
         * @returns {Function} console.warn
         */

    }, {
        key: "warning",
        get: function get() {
            if (this.getLogLevel() >= _loglevel2.default.WARNING) {
                return console.warn.bind(console);
            }
            return this._noOutput;
        }

        /**
         * Exposes console.error. Will only print if current level is
         * higher than {@link LogLevels#ERROR}.
         * @returns {Function} console.error
         */

    }, {
        key: "error",
        get: function get() {
            if (this.getLogLevel() >= _loglevel2.default.ERROR) {
                return console.error.bind(console);
            }
            return this._noOutput;
        }
    }]);

    return AbstractLogger;
}();

exports.default = AbstractLogger;

},{"./loglevel":6}],4:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _AbstractLogger2 = require("./AbstractLogger");

var _AbstractLogger3 = _interopRequireDefault(_AbstractLogger2);

var _loglevel = require("./loglevel");

var _loglevel2 = _interopRequireDefault(_loglevel);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Logger = function (_AbstractLogger) {
    _inherits(Logger, _AbstractLogger);

    /**
     *
     * @param {string} name The name of the logger.
     * @param {LoggerSingleton} loggerSingleton The logger singleton
     *      this logger belongs to.
     */
    function Logger(name, loggerSingleton) {
        _classCallCheck(this, Logger);

        var _this = _possibleConstructorReturn(this, (Logger.__proto__ || Object.getPrototypeOf(Logger)).call(this));

        _this._name = name;
        _this._logLevel = null;
        _this._loggerSingleton = loggerSingleton;
        return _this;
    }

    /**
     * Get the name of this logger.
     * @returns {string}
     */


    _createClass(Logger, [{
        key: "setLogLevel",


        /**
         * Set the loglevel for this logger.
         *
         * @param {int} logLevel The log level. Must be one of the loglevels
         *      defined in {@link LogLevels}.
         * @throws {RangeError} if {@link LogLevels#validateLogLevel} fails.
         */
        value: function setLogLevel(logLevel) {
            _loglevel2.default.validateLogLevel(logLevel);
            this._logLevel = logLevel;
        }

        /**
         * Get the log level.
         *
         * If no log level has been set with {@link Logger#setLogLevel},
         * this returns {@link LoggerSingleton#getDefaultLogLevel}.
         *
         * @returns {int}
         */

    }, {
        key: "getLogLevel",
        value: function getLogLevel() {
            if (this._logLevel == null) {
                return this._loggerSingleton.getDefaultLogLevel();
            }
            return this._logLevel;
        }

        /**
         * Get textual name for the log level. If the logger
         * does not have a logLevel (if it inherits it from the LoggerSingleton)
         * a string with information about this and the default logLevel for the
         * LoggerSingleton is returned.
         *
         * Intended for debugging. The format of the string may change.
         *
         * @returns {string}
         */

    }, {
        key: "getTextualNameForLogLevel",
        value: function getTextualNameForLogLevel() {
            if (this._logLevel == null) {
                return '[default for LoggerSingleton - ' + (this._loggerSingleton.getTextualNameForDefaultLogLevel() + "]");
            }
            return _loglevel2.default.getTextualNameForLogLevel(this.getLogLevel());
        }
    }, {
        key: "getDebugInfoString",
        value: function getDebugInfoString() {
            return this.name + ": " + this.getTextualNameForLogLevel();
        }
    }, {
        key: "name",
        get: function get() {
            return this._name;
        }
    }]);

    return Logger;
}(_AbstractLogger3.default);

exports.default = Logger;

},{"./AbstractLogger":3,"./loglevel":6}],5:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _Logger = require("./Logger");

var _Logger2 = _interopRequireDefault(_Logger);

var _loglevel = require("./loglevel");

var _loglevel2 = _interopRequireDefault(_loglevel);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var _instance = null;

/**
 * A logging system.
 *
 * @example <caption>Create and use a logger</caption>
 * import LoggerSingleton from 'ievv_jsbase/log/LoggerSingleton';
 * let mylogger = new LoggerSingleton().loggerSingleton.getLogger('myproject.MyClass');
 * mylogger.debug('Hello debug world');
 * mylogger.info('Hello info world');
 * mylogger.warning('Hello warning world');
 * mylogger.error('Hello error world');
 *
 * @example <caption>Set a default loglevel for all loggers</caption>
 * import LOGLEVEL from 'ievv_jsbase/log/loglevel';
 * new LoggerSingleton().setDefaultLogLevel(LOGLEVEL.DEBUG);
 *
 * @example <caption>Set a custom loglevel for a single logger</caption>
 * import LOGLEVEL from 'ievv_jsbase/log/loglevel';
 * new LoggerSingleton().getLogger('mylogger').setLoglevel(LOGLEVEL.DEBUG);
 */

var LoggerSingleton = function () {
    /**
     * Get an instance of the singleton.
     *
     * The first time this is called, we create a new instance.
     * For all subsequent calls, we return the instance that was
     * created on the first call.
     */
    function LoggerSingleton() {
        _classCallCheck(this, LoggerSingleton);

        if (!_instance) {
            _instance = this;
        }
        this._loggerMap = new Map();
        this.reset();
        return _instance;
    }

    /**
     * Get the number of loggers registered using
     * {@link getLogger}.
     *
     * @returns {number} The number of loggers.
     */


    _createClass(LoggerSingleton, [{
        key: "getLoggerCount",
        value: function getLoggerCount() {
            return this._loggerMap.size;
        }

        /**
         * Reset to default log level, and clear all
         * custom loggers.
         */

    }, {
        key: "reset",
        value: function reset() {
            this._logLevel = _loglevel2.default.WARNING;
            this._loggerMap.clear();
        }

        /**
         * Get the default log level.
         *
         * Defaults to {@link LogLevels#WARNING} if not overridden
         * with {@LoggerSingleton#setDefaultLogLevel}.
         *
         * @returns {int} One of the loglevels defined in {@link LogLevels}
         */

    }, {
        key: "getDefaultLogLevel",
        value: function getDefaultLogLevel() {
            return this._logLevel;
        }

        /**
         * Set the default loglevel.
         *
         * All loggers use this by default unless
         * you override their loglevel.
         *
         * @example <caption>Override loglevel of a specific logger</caption>
         * import LoggerSingleton from 'ievv_jsbase/log/LoggerSingleton';
         * import LOGLEVEL from 'ievv_jsbase/log/loglevel';
         * let loggerSingleton = new LoggerSingleton();
         * loggerSingleton.getLogger('mylogger').setLogLevel(LOGLEVEL.DEBUG);
         *
         * @param logLevel The log level. Must be one of the loglevels
         *      defined in {@link LogLevels}.
         * @throws {RangeError} if {@link LogLevels#validateLogLevel} fails.
         */

    }, {
        key: "setDefaultLogLevel",
        value: function setDefaultLogLevel(logLevel) {
            _loglevel2.default.validateLogLevel(logLevel);
            this._logLevel = logLevel;
        }

        /**
         * Get a logger.
         *
         * @param {string} name A name for the logger. Should be a unique name,
         *      so typically the full import path of the class/function using
         *      the logger.
         * @returns {Logger}
         */

    }, {
        key: "getLogger",
        value: function getLogger(name) {
            if (!this._loggerMap.has(name)) {
                this._loggerMap.set(name, new _Logger2.default(name, this));
            }
            return this._loggerMap.get(name);
        }

        /**
         * Get the names of all the registered loggers.
         *
         * @returns {Array} Sorted array with the same of the loggers.
         */

    }, {
        key: "getLoggerNameArray",
        value: function getLoggerNameArray() {
            var loggerNames = Array.from(this._loggerMap.keys());
            loggerNames.sort();
            return loggerNames;
        }

        /**
         * Get textual name for the default log level.
         *
         * Intended for debugging. The format of the string may change.
         *
         * @returns {string}
         */

    }, {
        key: "getTextualNameForDefaultLogLevel",
        value: function getTextualNameForDefaultLogLevel() {
            return _loglevel2.default.getTextualNameForLogLevel(this.getDefaultLogLevel());
        }

        /**
         * Get a string that summarize information about all the
         * loggers. The string has a list of loglevels with
         * their loglevel. Perfect for debugging.
         *
         * Intended for debugging. The format of the string may change.
         *
         * @returns {string}
         */

    }, {
        key: "getDebugInfoString",
        value: function getDebugInfoString() {
            var loggerInfoString = "Default logLevel: " + (this.getTextualNameForDefaultLogLevel() + "\n") + "Loggers:\n";
            if (this.getLoggerCount() === 0) {
                loggerInfoString += '(no loggers)\n';
            } else {
                var _iteratorNormalCompletion = true;
                var _didIteratorError = false;
                var _iteratorError = undefined;

                try {
                    for (var _iterator = this.getLoggerNameArray()[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                        var loggerName = _step.value;

                        var logger = this.getLogger(loggerName);
                        loggerInfoString += " - " + logger.getDebugInfoString() + "\n";
                    }
                } catch (err) {
                    _didIteratorError = true;
                    _iteratorError = err;
                } finally {
                    try {
                        if (!_iteratorNormalCompletion && _iterator.return) {
                            _iterator.return();
                        }
                    } finally {
                        if (_didIteratorError) {
                            throw _iteratorError;
                        }
                    }
                }
            }
            return loggerInfoString;
        }
    }]);

    return LoggerSingleton;
}();

exports.default = LoggerSingleton;

},{"./Logger":4,"./loglevel":6}],6:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Defines valid log levels.
 *
 * Not used directly, but instead via the LOGLEVEL
 * constant exported as default by this module.
 *
 * @example
 * import LOGLEVEL from 'ievv_jsbase/log/loglevel';
 * console.log('The debug loglevel is:', LOGLEVEL.DEBUG);
 * LOGLEVEL.validateLogLevel(10);
 */
var LogLevels = exports.LogLevels = function () {
    function LogLevels() {
        _classCallCheck(this, LogLevels);

        this._prettyLogLevelNames = {};
        this._prettyLogLevelNames[this.DEBUG] = 'DEBUG';
        this._prettyLogLevelNames[this.INFO] = 'INFO';
        this._prettyLogLevelNames[this.WARNING] = 'WARNING';
        this._prettyLogLevelNames[this.ERROR] = 'ERROR';
        this._prettyLogLevelNames[this.SILENT] = 'SILENT';
    }

    /**
     * Get the number for log level DEBUG.
     * @returns {number}
     */


    _createClass(LogLevels, [{
        key: 'validateLogLevel',


        /**
         * Validate a log level.
         *
         * Should be used by all functions/methods that set a log level.
         *
         * @param logLevel The loglevel.
         * @throws {RangeError} If ``logLevel`` is not one
         *   of:
         *
         *   - {@link LogLevels#DEBUG}
         *   - {@link LogLevels#INFO}
         *   - {@link LogLevels#WARNING}
         *   - {@link LogLevels#ERROR}
         *   - {@link LogLevels#SILENT}
         */
        value: function validateLogLevel(logLevel) {
            if (logLevel > this.DEBUG || logLevel < this.SILENT) {
                throw new RangeError('Invalid log level: ' + logLevel + ', must be between ' + (this.SILENT + ' (SILENT) and ' + this.DEBUG + ' (DEBUG)'));
            }
        }

        /**
         * Get the textual name for a log level.
         *
         * @param {number} logLevel The log level to get a textual name for.
         * @returns {string}
         *
         * @example
         * const infoText = LOGLEVEL.getTextualNameForLogLevel(LOGLEVEL.INFO);
         * // infoText === 'INFO'
         */

    }, {
        key: 'getTextualNameForLogLevel',
        value: function getTextualNameForLogLevel(logLevel) {
            return this._prettyLogLevelNames[logLevel];
        }
    }, {
        key: 'DEBUG',
        get: function get() {
            return 4;
        }

        /**
         * Get the number for log level INFO.
         * @returns {number}
         */

    }, {
        key: 'INFO',
        get: function get() {
            return 3;
        }

        /**
         * Get the number for log level WARNING.
         * @returns {number}
         */

    }, {
        key: 'WARNING',
        get: function get() {
            return 2;
        }

        /**
         * Get the number for log level ERROR.
         * @returns {number}
         */

    }, {
        key: 'ERROR',
        get: function get() {
            return 1;
        }

        /**
         * Get the number for log level SILENT.
         * @returns {number}
         */

    }, {
        key: 'SILENT',
        get: function get() {
            return 0;
        }
    }]);

    return LogLevels;
}();

var LOGLEVEL = new LogLevels();
exports.default = LOGLEVEL;

},{}],7:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.default = makeCustomError;
/**
 * Make a custom error "class".
 *
 * Makes an old style prototype based error class.
 *
 * @example
 * export let NotFoundError = makeCustomError('NotFoundError');
 *
 * @param name The name of the error class.
 * @returns {Error} The created error class.
 */
function makeCustomError(name) {
    var CustomError = function CustomError(message) {
        this.message = message;
        var last_part = new Error().stack.match(/[^\s]+$/);
        this.stack = this.name + " at " + last_part;
    };
    Object.setPrototypeOf(CustomError, Error);
    CustomError.prototype = Object.create(Error.prototype);
    CustomError.prototype.name = name;
    CustomError.prototype.message = "";
    CustomError.prototype.constructor = CustomError;
    return CustomError;
}

},{}],8:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _typeDetect = require('./typeDetect');

var _typeDetect2 = _interopRequireDefault(_typeDetect);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * Pretty format any javascript object.
 *
 * Handles the following types:
 *
 * - null
 * - undefined
 * - Number
 * - Boolean
 * - String
 * - Array
 * - Map
 * - Set
 * - Function
 * - Class (detected as a Function, so pretty formatted just like a function)
 * - Object
 *
 * @example <caption>Without indentation</caption>
 * new PrettyFormat([1, 2]).toString();
 *
 * @example <caption>With indentation (indent by 2 spaces)</caption>
 * new PrettyFormat([1, 2]).toString(2);
 *
 * @example <caption>Simple examples</caption>
 * new PrettyFormat(true).toString() === 'true';
 * new PrettyFormat(null).toString() === 'null';
 * new PrettyFormat([1, 2]).toString() === '[1, 2]';
 * new PrettyFormat({name: "John", age: 29}).toString() === '{"age": 29, "name": John}';
 *
 * @example <caption>Complex example</caption>
 * let map = new Map();
 * map.set('a', [10, 20]);
 * map.set('b', [30, 40, 50]);
 * function testFunction() {}
 * let obj = {
 *     theMap: map,
 *     aSet: new Set(['one', 'two']),
 *     theFunction: testFunction
 * };
 * const prettyFormatted = new PrettyFormat(obj).toString(2);
 */
var PrettyFormat = function () {
    function PrettyFormat(obj) {
        _classCallCheck(this, PrettyFormat);

        this._obj = obj;
    }

    _createClass(PrettyFormat, [{
        key: '_indentString',
        value: function _indentString(str, indent, indentLevel) {
            if (indent === 0) {
                return str;
            }
            return '' + ' '.repeat(indent * indentLevel) + str;
        }
    }, {
        key: '_objectToMap',
        value: function _objectToMap(obj) {
            var map = new Map();
            var sortedKeys = Array.from(Object.keys(obj));
            sortedKeys.sort();
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = sortedKeys[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var key = _step.value;

                    map.set(key, obj[key]);
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }

            return map;
        }
    }, {
        key: '_prettyFormatFlatIterable',
        value: function _prettyFormatFlatIterable(flatIterable, size, indent, indentLevel, prefix, suffix) {
            var output = prefix;
            var itemSuffix = ', ';
            if (indent) {
                output = prefix + '\n';
                itemSuffix = ',';
            }
            var index = 1;
            var _iteratorNormalCompletion2 = true;
            var _didIteratorError2 = false;
            var _iteratorError2 = undefined;

            try {
                for (var _iterator2 = flatIterable[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                    var item = _step2.value;

                    var prettyItem = this._prettyFormat(item, indent, indentLevel + 1);
                    if (index !== size) {
                        prettyItem += itemSuffix;
                    }
                    output += this._indentString(prettyItem, indent, indentLevel + 1);
                    if (indent) {
                        output += '\n';
                    }
                    index++;
                }
            } catch (err) {
                _didIteratorError2 = true;
                _iteratorError2 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion2 && _iterator2.return) {
                        _iterator2.return();
                    }
                } finally {
                    if (_didIteratorError2) {
                        throw _iteratorError2;
                    }
                }
            }

            output += this._indentString('' + suffix, indent, indentLevel);
            return output;
        }
    }, {
        key: '_prettyFormatMap',
        value: function _prettyFormatMap(map, indent, indentLevel, prefix, suffix, keyValueSeparator) {
            var output = prefix;
            var itemSuffix = ', ';
            if (indent) {
                output = prefix + '\n';
                itemSuffix = ',';
            }
            var index = 1;
            var _iteratorNormalCompletion3 = true;
            var _didIteratorError3 = false;
            var _iteratorError3 = undefined;

            try {
                for (var _iterator3 = map[Symbol.iterator](), _step3; !(_iteratorNormalCompletion3 = (_step3 = _iterator3.next()).done); _iteratorNormalCompletion3 = true) {
                    var _step3$value = _slicedToArray(_step3.value, 2);

                    var key = _step3$value[0];
                    var value = _step3$value[1];

                    var prettyKey = this._prettyFormat(key, indent, indentLevel + 1);
                    var prettyValue = this._prettyFormat(value, indent, indentLevel + 1);
                    var prettyItem = '' + prettyKey + keyValueSeparator + prettyValue;
                    if (index !== map.size) {
                        prettyItem += itemSuffix;
                    }
                    output += this._indentString(prettyItem, indent, indentLevel + 1);
                    if (indent) {
                        output += '\n';
                    }
                    index++;
                }
            } catch (err) {
                _didIteratorError3 = true;
                _iteratorError3 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion3 && _iterator3.return) {
                        _iterator3.return();
                    }
                } finally {
                    if (_didIteratorError3) {
                        throw _iteratorError3;
                    }
                }
            }

            output += this._indentString('' + suffix, indent, indentLevel);
            return output;
        }
    }, {
        key: '_prettyFormatFunction',
        value: function _prettyFormatFunction(fn) {
            return '[Function: ' + fn.name + ']';
        }
    }, {
        key: '_prettyFormat',
        value: function _prettyFormat(obj, indent, indentLevel) {
            var typeString = (0, _typeDetect2.default)(obj);
            var output = '';
            if (typeString === 'string') {
                output = '"' + obj + '"';
            } else if (typeString === 'number' || typeString === 'boolean' || typeString === 'undefined' || typeString === 'null') {
                output = '' + obj;
            } else if (typeString === 'array') {
                output = this._prettyFormatFlatIterable(obj, obj.length, indent, indentLevel, '[', ']');
            } else if (typeString === 'set') {
                output = this._prettyFormatFlatIterable(obj, obj.size, indent, indentLevel, 'Set(', ')');
            } else if (typeString === 'map') {
                output = this._prettyFormatMap(obj, indent, indentLevel, 'Map(', ')', ' => ');
            } else if (typeString === 'function') {
                output = this._prettyFormatFunction(obj);
            } else {
                output = this._prettyFormatMap(this._objectToMap(obj), indent, indentLevel, '{', '}', ': ');
            }
            return output;
        }

        /**
         * Get the results as a string, optionally indented.
         *
         * @param {number} indent The number of spaces to indent by. Only
         *    child objects are indented, and they are indented recursively.
         * @returns {string}
         */

    }, {
        key: 'toString',
        value: function toString(indent) {
            indent = indent || 0;
            return this._prettyFormat(this._obj, indent, 0);
        }
    }]);

    return PrettyFormat;
}();

exports.default = PrettyFormat;

},{"./typeDetect":9}],9:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

exports.default = typeDetect;
/**
 * Detect the type of an object and return the
 * result as a string.
 *
 * Handles the following types:
 *
 * - null  (returned as ``"null"``).
 * - undefined  (returned as ``"undefined"``).
 * - Number  (returned as ``"number"``).
 * - Boolean  (returned as ``"boolean"``).
 * - String  (returned as ``"string"``).
 * - Array  (returned as ``"array"``).
 * - Map  (returned as ``"map"``).
 * - Set  (returned as ``"set"``).
 * - Function  (returned as ``"function"``).
 * - Object  (returned as ``"object"``).
 *
 * We do not handle classes - they are returned as ``"function"``.
 * We could handle classes, but for Babel classes that will require
 * a fairly expensive and error prone regex.
 *
 * @param obj An object to detect the type for.
 * @returns {string}
 */
function typeDetect(obj) {
    if (obj === null) {
        return 'null';
    }
    var typeOf = typeof obj === 'undefined' ? 'undefined' : _typeof(obj);
    if (typeOf === 'undefined') {
        return 'undefined';
    }
    if (typeOf === 'number') {
        return 'number';
    }
    if (typeOf === 'boolean') {
        return 'boolean';
    }
    if (typeOf === 'string') {
        return 'string';
    }
    if (typeOf === 'function') {
        return 'function';
    }
    if (Array.isArray(obj)) {
        return 'array';
    }
    if (obj instanceof Map) {
        return 'map';
    }
    if (obj instanceof Set) {
        return 'set';
    }
    return 'object';
}

},{}],10:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.ElementIsNotInitializedAsWidget = exports.InvalidWidgetAliasError = exports.ElementIsNotWidgetError = exports.ElementHasNoWidgetInstanceIdError = undefined;

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _makeCustomError = require('../makeCustomError');

var _makeCustomError2 = _interopRequireDefault(_makeCustomError);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * The instance of the {@link WidgetRegistrySingleton}.
 */
var _instance = null;

/**
 * Exception thrown when an element where we expect the
 * ``data-ievv-jsbase-widget-instanceid`` attribute does
 * not have this attribute.
 *
 * @type {Error}
 */
var ElementHasNoWidgetInstanceIdError = exports.ElementHasNoWidgetInstanceIdError = (0, _makeCustomError2.default)('ElementHasNoWidgetInstanceIdError');

/**
 * Exception thrown when an element that we expect to have
 * the ``data-ievv-jsbase-widget`` attribute does not have
 * this attribute.
 *
 * @type {Error}
 */
var ElementIsNotWidgetError = exports.ElementIsNotWidgetError = (0, _makeCustomError2.default)('ElementIsNotWidgetError');

/**
 * Exception thrown when an element has a
 * ``data-ievv-jsbase-widget`` with a value that
 * is not an alias registered in the {@link WidgetRegistrySingleton}.
 *
 * @type {Error}
 */
var InvalidWidgetAliasError = exports.InvalidWidgetAliasError = (0, _makeCustomError2.default)('InvalidWidgetAliasError');

/**
 * Exception thrown when an element with the
 * ``data-ievv-jsbase-widget-instanceid=<widgetInstanceId>`` attribute is not in
 * the {@link WidgetRegistrySingleton} with ``<widgetInstanceId>``.
 *
 * @type {Error}
 */
var ElementIsNotInitializedAsWidget = exports.ElementIsNotInitializedAsWidget = (0, _makeCustomError2.default)('ElementIsNotInitializedAsWidget');

/**
 * A very lightweight widget system.
 *
 * Basic example below - see {@link AbstractWidget} for more examples.
 *
 * @example <caption>Create a very simple widget</caption>
 * export default class OpenMenuWidget extends AbstractWidget {
 *     constructor(element) {
 *          super(element);
 *          this._onClickBound = (...args) => {
 *              this._onClick(...args);
 *          };
 *          this.element.addEventListener('click', this._onClickBound);
 *     }
 *
 *     _onClick = (e) => {
 *          e.preventDefault();
 *          console.log('I should have opened the menu here');
 *     }
 *
 *     destroy() {
 *          this.element.removeEventListener('click', this._onClickBound);
 *     }
 * }
 *
 * @example <caption>Use the widget</caption>
 * <button data-ievv-jsbase-widget="open-menu-button" type="button">
 *     Open menu
 * </button>
 *
 * @example <caption>Register and load widgets</caption>
 * // Somewhere that is called after all the widgets are rendered
 * // - typically at the end of the <body>
 * import WidgetRegistrySingleton from 'ievv_jsbase/widget/WidgetRegistrySingleton';
 * import OpenMenuWidget from 'path/to/OpenMenuWidget';
 * const widgetRegistry = new WidgetRegistrySingleton();
 * widgetRegistry.registerWidgetClass('open-menu-button', OpenMenuWidget);
 * widgetRegistry.initializeAllWidgetsWithinElement(document.body);
 *
 */

var WidgetRegistrySingleton = function () {
    function WidgetRegistrySingleton() {
        _classCallCheck(this, WidgetRegistrySingleton);

        if (!_instance) {
            _instance = this;
            this._initialize();
        }
        return _instance;
    }

    _createClass(WidgetRegistrySingleton, [{
        key: '_initialize',
        value: function _initialize() {
            this._widgetAttribute = 'data-ievv-jsbase-widget';
            this._widgetInstanceIdAttribute = 'data-ievv-jsbase-widget-instanceid';
            this._widgetClassMap = new Map();
            this._widgetInstanceMap = new Map();
            this._widgetInstanceCounter = 0;
        }
    }, {
        key: 'clear',
        value: function clear() {
            // TODO: Call destroyAllWidgetsWithinDocumentBody()
            this._widgetClassMap.clear();
            this._widgetInstanceMap.clear();
            this._widgetInstanceCounter = 0;
        }

        /**
         * Register a widget class in the registry.
         *
         * @param {string} alias The alias for the widget. This is the string that
         *      is used as the attribute value with the ``data-ievv-jsbase-widget``
         *      DOM element attribute.
         * @param {AbstractWidget} WidgetClass The widget class.
         */

    }, {
        key: 'registerWidgetClass',
        value: function registerWidgetClass(alias, WidgetClass) {
            this._widgetClassMap.set(alias, WidgetClass);
        }

        /**
         * Remove widget class from registry.
         *
         * @param alias The alias that the widget class was registered with
         *      by using {@link WidgetRegistrySingleton#registerWidgetClass}.
         */

    }, {
        key: 'removeWidgetClass',
        value: function removeWidgetClass(alias) {
            this._widgetClassMap.delete(alias);
        }

        /**
         * Initialize the provided element as a widget.
         *
         * @param {Element} element The DOM element to initalize as a widget.
         *
         * @throws {ElementIsNotWidgetError} If the element does not have
         *      the ``data-ievv-jsbase-widget`` attribute.
         * @throws {InvalidWidgetAliasError} If the widget alias is not in this registry.
         */

    }, {
        key: 'initializeWidget',
        value: function initializeWidget(element) {
            var alias = element.getAttribute(this._widgetAttribute);
            if (!alias) {
                throw new ElementIsNotWidgetError('The\n\n' + element.outerHTML + '\n\nelement has no or empty' + (this._widgetAttribute + ' attribute.'));
            }
            if (!this._widgetClassMap.has(alias)) {
                throw new InvalidWidgetAliasError('No WidgetClass registered with the "' + alias + '" alias.');
            }
            var WidgetClass = this._widgetClassMap.get(alias);
            var widget = new WidgetClass(element);
            this._widgetInstanceCounter++;
            var widgetInstanceId = this._widgetInstanceCounter.toString();
            this._widgetInstanceMap.set(widgetInstanceId, widget);
            element.setAttribute(this._widgetInstanceIdAttribute, widgetInstanceId);
            return widget;
        }
    }, {
        key: '_getAllWidgetElementsWithinElement',
        value: function _getAllWidgetElementsWithinElement(element) {
            return element.querySelectorAll('[' + this._widgetAttribute + ']');
        }

        /**
         * Initialize all widgets within the provided element.
         *
         * @param {Element} element A DOM element.
         */

    }, {
        key: 'initializeAllWidgetsWithinElement',
        value: function initializeAllWidgetsWithinElement(element) {
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = this._getAllWidgetElementsWithinElement(element)[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var widgetElement = _step.value;

                    this.initializeWidget(widgetElement);
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }
        }

        /**
         * Get the value of the ``data-ievv-jsbase-widget-instanceid`` attribute
         * of the provided element.
         *
         * @param {Element} element A DOM element.
         * @returns {null|string}
         */

    }, {
        key: 'getWidgetInstanceIdFromElement',
        value: function getWidgetInstanceIdFromElement(element) {
            return element.getAttribute(this._widgetInstanceIdAttribute);
        }

        /**
         * Get a widget instance by its widget instance id.
         *
         * @param widgetInstanceId A widget instance id.
         * @returns {AbstractWidget} A widget instance or ``null``.
         */

    }, {
        key: 'getWidgetInstanceByInstanceId',
        value: function getWidgetInstanceByInstanceId(widgetInstanceId) {
            return this._widgetInstanceMap.get(widgetInstanceId);
        }

        /**
         * Destroy the widget on the provided element.
         *
         * @param {Element} element A DOM element that has been initialized by
         *      {@link WidgetRegistrySingleton#initializeWidget}.
         *
         * @throws {ElementHasNoWidgetInstanceIdError} If the element has
         *      no ``data-ievv-jsbase-widget-instanceid`` attribute or the
         *      attribute value is empty. This normally means that
         *      the element is not a widget, or that the widget
         *      is not initialized.
         * @throws {ElementIsNotInitializedAsWidget} If the element
         *      has the ``data-ievv-jsbase-widget-instanceid`` attribute
         *      but the value of the attribute is not a valid widget instance
         *      id. This should not happen unless you manipulate the
         *      attribute manually or use the private members of this registry.
         */

    }, {
        key: 'destroyWidget',
        value: function destroyWidget(element) {
            var widgetInstanceId = this.getWidgetInstanceIdFromElement(element);
            if (widgetInstanceId) {
                var widgetInstance = this.getWidgetInstanceByInstanceId(widgetInstanceId);
                if (widgetInstance) {
                    widgetInstance.destroy();
                    this._widgetInstanceMap.delete(widgetInstanceId);
                    element.removeAttribute(this._widgetInstanceIdAttribute);
                } else {
                    throw new ElementIsNotInitializedAsWidget('Element\n\n' + element.outerHTML + '\n\nhas the ' + (this._widgetInstanceIdAttribute + ' attribute, but the id is ') + 'not in the widget registry.');
                }
            } else {
                throw new ElementHasNoWidgetInstanceIdError('Element\n\n' + element.outerHTML + '\n\nhas no or empty ' + (this._widgetInstanceIdAttribute + ' attribute.'));
            }
        }
    }, {
        key: '_getAllInstanciatedWidgetElementsWithinElement',
        value: function _getAllInstanciatedWidgetElementsWithinElement(element) {
            return element.querySelectorAll('[' + this._widgetInstanceIdAttribute + ']');
        }

        /**
         * Destroy all widgets within the provided element.
         * Only destroys widgets on elements that is a child of the element.
         *
         * @param {Element} element The DOM Element.
         */

    }, {
        key: 'destroyAllWidgetsWithinElement',
        value: function destroyAllWidgetsWithinElement(element) {
            var _iteratorNormalCompletion2 = true;
            var _didIteratorError2 = false;
            var _iteratorError2 = undefined;

            try {
                for (var _iterator2 = this._getAllInstanciatedWidgetElementsWithinElement(element)[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                    var widgetElement = _step2.value;

                    this.destroyWidget(widgetElement);
                }
            } catch (err) {
                _didIteratorError2 = true;
                _iteratorError2 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion2 && _iterator2.return) {
                        _iterator2.return();
                    }
                } finally {
                    if (_didIteratorError2) {
                        throw _iteratorError2;
                    }
                }
            }
        }
    }]);

    return WidgetRegistrySingleton;
}();

exports.default = WidgetRegistrySingleton;

},{"../makeCustomError":7}]},{},[2])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJzY3JpcHRzL2phdmFzY3JpcHQvaWV2dl9qc2Jhc2UvU2lnbmFsSGFuZGxlclNpbmdsZXRvbi5qcyIsInNjcmlwdHMvamF2YXNjcmlwdC9pZXZ2X2pzYmFzZS9pZXZ2X2pzYmFzZV9jb3JlLmpzIiwic2NyaXB0cy9qYXZhc2NyaXB0L2lldnZfanNiYXNlL2xvZy9BYnN0cmFjdExvZ2dlci5qcyIsInNjcmlwdHMvamF2YXNjcmlwdC9pZXZ2X2pzYmFzZS9sb2cvTG9nZ2VyLmpzIiwic2NyaXB0cy9qYXZhc2NyaXB0L2lldnZfanNiYXNlL2xvZy9Mb2dnZXJTaW5nbGV0b24uanMiLCJzY3JpcHRzL2phdmFzY3JpcHQvaWV2dl9qc2Jhc2UvbG9nL2xvZ2xldmVsLmpzIiwic2NyaXB0cy9qYXZhc2NyaXB0L2lldnZfanNiYXNlL21ha2VDdXN0b21FcnJvci5qcyIsInNjcmlwdHMvamF2YXNjcmlwdC9pZXZ2X2pzYmFzZS91dGlscy9QcmV0dHlGb3JtYXQuanMiLCJzY3JpcHRzL2phdmFzY3JpcHQvaWV2dl9qc2Jhc2UvdXRpbHMvdHlwZURldGVjdC5qcyIsInNjcmlwdHMvamF2YXNjcmlwdC9pZXZ2X2pzYmFzZS93aWRnZXQvV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24uanMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7Ozs7Ozs7Ozs7QUNBQTs7OztBQUNBOzs7Ozs7OztBQUVBOzs7OztBQUtPLElBQUksMEVBQWlDLCtCQUFnQixnQ0FBaEIsQ0FBckM7O0FBR1A7Ozs7Ozs7Ozs7SUFTYSxrQixXQUFBLGtCO0FBQ1QsZ0NBQVksSUFBWixFQUFrQixVQUFsQixFQUE4QixZQUE5QixFQUE0QztBQUFBOztBQUN4Qzs7O0FBR0EsYUFBSyxJQUFMLEdBQVksSUFBWjs7QUFFQTs7Ozs7QUFLQSxhQUFLLFVBQUwsR0FBa0IsVUFBbEI7O0FBRUE7Ozs7O0FBS0EsYUFBSyxZQUFMLEdBQW9CLFlB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RCxNQUlPO0FBQ0gsMEJBQU0sSUFBSSwrQkFBSixDQUNGLGdCQUFjLFFBQVEsU0FBdEIscUJBQ0csS0FBSywwQkFEUixnRUFERSxDQUFOO0FBSUM7QUFDUixhQVpELE1BWU87QUFDSCxzQkFBTSxJQUFJLGlDQUFKLENBQ0YsZ0JBQWMsUUFBUSxTQUF0Qiw2QkFDRyxLQUFLLDBCQURSLGlCQURFLENBQU47QUFHSDtBQUNKOzs7dUVBRThDLE8sRUFBUztBQUNwRCxtQkFBTyxRQUFRLGdCQUFSLE9BQTZCLEtBQUssMEJBQWxDLE9BQVA7QUFDSDs7QUFFRDs7Ozs7Ozs7O3VEQU0rQixPLEVBQVM7QUFBQTtBQUFBO0FBQUE7O0FBQUE7QUFDcEMsc0NBQXlCLEtBQUssOENBQUwsQ0FBb0QsT0FBcEQsQ0FBekIsbUlBQXVGO0FBQUEsd0JBQS9FLGFBQStFOztBQUNuRix5QkFBSyxhQUFMLENBQW1CLGFBQW5CO0FBQ0g7QUFIbUM7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUl2Qzs7Ozs7O2tCQWxLZ0IsdUIiLCJmaWxlIjoiZ2VuZXJhdGVkLmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiBlKHQsbixyKXtmdW5jdGlvbiBzKG8sdSl7aWYoIW5bb10pe2lmKCF0W29dKXt2YXIgYT10eXBlb2YgcmVxdWlyZT09XCJmdW5jdGlvblwiJiZyZXF1aXJlO2lmKCF1JiZhKXJldHVybiBhKG8sITApO2lmKGkpcmV0dXJuIGkobywhMCk7dmFyIGY9bmV3IEVycm9yKFwiQ2Fubm90IGZpbmQgbW9kdWxlICdcIitvK1wiJ1wiKTt0aHJvdyBmLmNvZGU9XCJNT0RVTEVfTk9UX0ZPVU5EXCIsZn12YXIgbD1uW29dPXtleHBvcnRzOnt9fTt0W29dWzBdLmNhbGwobC5leHBvcnRzLGZ1bmN0aW9uKGUpe3ZhciBuPXRbb11bMV1bZV07cmV0dXJuIHMobj9uOmUpfSxsLGwuZXhwb3J0cyxlLHQsbixyKX1yZXR1cm4gbltvXS5leHBvcnRzfXZhciBpPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7Zm9yKHZhciBvPTA7bzxyLmxlbmd0aDtvKyspcyhyW29dKTtyZXR1cm4gc30pIiwiaW1wb3J0IG1ha2VDdXN0b21FcnJvciBmcm9tIFwiLi9tYWtlQ3VzdG9tRXJyb3JcIjtcbmltcG9ydCBQcmV0dHlGb3JtYXQgZnJvbSBcIi4vdXRpbHMvUHJldHR5Rm9ybWF0XCI7XG5cbi8qKlxuICogRXhjZXB0aW9uIHJhaXNlZCBieSB7QGxpbmsgSHR0cENvb2tpZXMjZ2V0U3RyaWN0fSB3aGVuIHRoZSBjb29raWUgaXMgbm90IGZvdW5kLlxuICpcbiAqIEB0eXBlIHtFcnJvcn1cbiAqL1xuZXhwb3J0IGxldCBEdXBsaWNhdGVSZWNlaXZlck5hbWVGb3JTaWduYWwgPSBtYWtlQ3VzdG9tRXJyb3IoJ0R1cGxpY2F0ZVJlY2VpdmVyTmFtZUZvclNpZ25hbCcpO1xuXG5cbi8qKlxuICogUmVwcmVzZW50cyBpbmZvcm1hdGlvbiBhYm91dCB0aGUgcmVjZWl2ZWQgc2lnbmFsLlxuICpcbiAqIEFuIG9iamVjdCBvZiB0aGlzIGNsYXNzIGlzIHNlbnQgdG8gdGhlIGBgY2FsbGJhY2tgYFxuICogb2YgYWxsIHNpZ25hbCByZWNlaXZlcnMuXG4gKlxuICogVGhlIGRhdGEgc2VudCBieSB0aGUgc2lnbmFsIGlzIGF2YWlsYWJsZSBpblxuICoge0BsaW5rIFJlY2VpdmVkU2lnbmFsSW5mby5kYXRhfS5cbiAqL1xuZXhwb3J0IGNsYXNzIFJlY2VpdmVkU2lnbmFsSW5mbyB7XG4gICAgY29uc3RydWN0b3IoZGF0YSwgc2lnbmFsTmFtZSwgcmVjZWl2ZXJOYW1lKSB7XG4gICAgICAgIC8qKlxuICAgICAgICAgKiBUaGUgZGF0YSBzZW50IGJ5IHtAbGluayBTaWduYWxIYW5kbGVyU2luZ2xldG9uI3NlbmR9LlxuICAgICAgICAgKi9cbiAgICAgICAgdGhpcy5kYXRhID0gZGF0YTtcblxuICAgICAgICAvKipcbiAgICAgICAgICogVGhlIHNpZ25hbCBuYW1lLlxuICAgICAgICAgKlxuICAgICAgICAgKiBAdHlwZSB7c3RyaW5nfVxuICAgICAgICAgKi9cbiAgICAgICAgdGhpcy5zaWduYWxOYW1lID0gc2lnbmFsTmFtZTtcblxuICAgICAgICAvKipcbiAgICAgICAgICogVGhlIHJlY2VpdmVyIG5hbWUuXG4gICAgICAgICAqXG4gICAgICAgICAqIEB0eXBlIHtzdHJpbmd9XG4gICAgICAgICAqL1xuICAgICAgICB0aGlzLnJlY2VpdmVyTmFtZSA9IHJlY2VpdmVyTmFtZTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgYSBzdHJpbmcgd2l0aCBkZWJ1ZyBpbmZvcm1hdGlvbiBhYm91dCB0aGUgcmVjZWl2ZWQgc2lnbmFsLlxuICAgICAqL1xuICAgIHRvU3RyaW5nKCkge1xuICAgICAgICBsZXQgcHJldHR5RGF0YSA9IG5ldyBQcmV0dHlGb3JtYXQodGhpcy5kYXRhKS50b1N0cmluZygyKTtcbiAgICAgICAgcmV0dXJuIGBzaWduYWxOYW1lPVwiJHt0aGlzLnNpZ25hbE5hbWV9XCIsIGAgK1xuICAgICAgICAgICAgYHJlY2VpdmVyTmFtZT1cIiR7dGhpcy5yZWNlaXZlck5hbWV9XCIsIGAgK1xuICAgICAgICAgICAgYGRhdGE9JHtwcmV0dHlEYXRhfWA7XG4gICAgfVxufVxuXG5cbi8qKlxuICogUHJpdmF0ZSBjbGFzcyB1c2VkIGJ5IHtAbGluayBfU2lnbmFsUmVjZWl2ZXJzfSB0byByZXByZXNlbnRcbiAqIGEgc2luZ2xlIHJlY2VpdmVyIGxpc3RlbmluZyBmb3IgYSBzaW5nbGUgc2lnbmFsLlxuICovXG5jbGFzcyBfU2lnbmFsUmVjZWl2ZXIge1xuICAgIGNvbnN0cnVjdG9yKHNpZ25hbCwgbmFtZSwgY2FsbGJhY2spIHtcbiAgICAgICAgdGhpcy5zaWduYWwgPSBzaWduYWw7XG4gICAgICAgIHRoaXMubmFtZSA9IG5hbWU7XG4gICAgICAgIHRoaXMuY2FsbGJhY2sgPSBjYWxsYmFjaztcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBBc3luY2hyb25vdXNseSB0cmlnZ2VyIHRoZSByZWNlaXZlciBjYWxsYmFjay5cbiAgICAgKiBAcGFyYW0gZGF0YSBUaGUgc2lnbmFsIGRhdGEgKHRoZSBkYXRhIGFyZ3VtZW50IHByb3ZpZGVkIGZvclxuICAgICAqICAgIHtAbGluayBTaWduYWxIYW5kbGVyU2luZ2xldG9uI3NlbmR9LlxuICAgICAqL1xuICAgIHRyaWdnZXIoZGF0YSkge1xuICAgICAgICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgICAgIHRoaXMuY2FsbGJhY2sobmV3IFJlY2VpdmVkU2lnbmFsSW5mbyhkYXRhLCB0aGlzLnNpZ25hbC5uYW1lLCB0aGlzLm5hbWUpKTtcbiAgICAgICAgfSwgMCk7XG4gICAgfVxufVxuXG5cbi8qKlxuICogT2JqZWN0IGNvbnRhaW5pbmcgZGVidWdnaW5nIGluZm9ybWF0aW9uIGFib3V0IGEgc2VudFxuICogc2lnbmFsLlxuICovXG5leHBvcnQgY2xhc3MgU2VudFNpZ25hbEluZm8ge1xuICAgIGNvbnN0cnVjdG9yKHNpZ25hbE5hbWUpIHtcbiAgICAgICAgLyoqXG4gICAgICAgICAqIFRoZSBzaWduYWwgbmFtZS5cbiAgICAgICAgICpcbiAgICAgICAgICogQHR5cGUge3N0cmluZ31cbiAgICAgICAgICovXG4gICAgICAgIHRoaXMuc2lnbmFsTmFtZSA9IHNpZ25hbE5hbWU7XG5cbiAgICAgICAgLyoqXG4gICAgICAgICAqIEFycmF5IG9mIHRyaWdnZXJlZCByZWNlaXZlciBuYW1lcy5cbiAgICAgICAgICpcbiAgICAgICAgICogQHR5cGUge0FycmF5fVxuICAgICAgICAgKi9cbiAgICAgICAgdGhpcy50cmlnZ2VyZWRSZWNlaXZlck5hbWVzID0gW107XG4gICAgfVxuXG4gICAgX2FkZFJlY2VpdmVyTmFtZShyZWNlaXZlck5hbWUpIHtcbiAgICAgICAgdGhpcy50cmlnZ2VyZWRSZWNlaXZlck5hbWVzLnB1c2gocmVjZWl2ZXJOYW1lKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgYSBzdHJpbmcgcmVwcmVzZW50YXRpb24gb2YgdGhlIHNlbnQgc2lnbmFsIGluZm8uXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyB7c3RyaW5nfVxuICAgICAqL1xuICAgIHRvU3RyaW5nKCkge1xuICAgICAgICBsZXQgcmVjZWl2ZXJzID0gdGhpcy50cmlnZ2VyZWRSZWNlaXZlck5hbWVzLmpvaW4oJywgJyk7XG4gICAgICAgIGlmKHJlY2VpdmVycyA9PT0gJycpIHtcbiAgICAgICAgICAgIHJlY2VpdmVycyA9ICdOTyBSRUNFSVZFUlMnO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBgU2lnbmFsOiAke3RoaXMuc2lnbmFsTmFtZX0gd2FzIHNlbnQgZG86ICR7cmVjZWl2ZXJzfWA7XG4gICAgfVxufVxuXG5cbi8qKlxuICogUHJpdmF0ZSBjbGFzcyB1c2VkIGJ5IHtAbGluayBTaWduYWxIYW5kbGVyU2luZ2xldG9ufVxuICogdG8gcmVwcmVzZW50IGFsbCByZWNlaXZlcnMgZm9yIGEgc2luZ2xlIHNpZ25hbC5cbiAqL1xuY2xhc3MgX1NpZ25hbFJlY2VpdmVycyB7XG4gICAgY29uc3RydWN0b3IobmFtZSkge1xuICAgICAgICB0aGlzLm5hbWUgPSBuYW1lO1xuICAgICAgICB0aGlzLnJlY2VpdmVyTWFwID0gbmV3IE1hcCgpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEFkZCBhIHJlY2VpdmVyLlxuICAgICAqXG4gICAgICogQHRocm93IER1cGxpY2F0ZVJlY2VpdmVyTmFtZUZvclNpZ25hbCBJZiB0aGUgcmVjZWl2ZXIgaXMgYWxyZWFkeSByZWdpc3RlcmVkIGZvciB0aGUgc2lnbmFsLlxuICAgICAqL1xuICAgIGFkZFJlY2VpdmVyKHJlY2VpdmVyTmFtZSwgY2FsbGJhY2spIHtcbiAgICAgICAgaWYodGhpcy5yZWNlaXZlck1hcC5oYXMocmVjZWl2ZXJOYW1lKSkge1xuICAgICAgICAgICAgdGhyb3cgbmV3IER1cGxpY2F0ZVJlY2VpdmVyTmFtZUZvclNpZ25hbChcbiAgICAgICAgICAgICAgICBgVGhlIFwiJHtyZWNlaXZlck5hbWV9XCIgcmVjZWl2ZXIgaXMgYWxyZWFkeSByZWdpc3RlcmVkIGZvciB0aGUgXCIke3RoaXMubmFtZX1cIiBzaWduYWxgKTtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLnJlY2VpdmVyTWFwLnNldChcbiAgICAgICAgICAgIHJlY2VpdmVyTmFtZSxcbiAgICAgICAgICAgIG5ldyBfU2lnbmFsUmVjZWl2ZXIodGhpcywgcmVjZWl2ZXJOYW1lLCBjYWxsYmFjaykpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlbW92ZSBhIHJlY2VpdmVyLlxuICAgICAqXG4gICAgICogSWYgdGhlIHJlY2VpdmVyIGlzIG5vdCByZWdpc3RlcmVkIGZvciB0aGUgc2lnbmFsLFxuICAgICAqIG5vdGhpbmcgaGFwcGVucy5cbiAgICAgKi9cbiAgICByZW1vdmVSZWNlaXZlcihyZWNlaXZlck5hbWUpIHtcbiAgICAgICAgaWYodGhpcy5yZWNlaXZlck1hcC5oYXMocmVjZWl2ZXJOYW1lKSkge1xuICAgICAgICAgICAgdGhpcy5yZWNlaXZlck1hcC5kZWxldGUocmVjZWl2ZXJOYW1lKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIENoZWNrIGlmIHdlIGhhdmUgYSBzcGVjaWZpYyByZWNlaXZlciBmb3IgdGhpcyBzaWduYWwuXG4gICAgICovXG4gICAgaGFzUmVjZWl2ZXIocmVjZWl2ZXJOYW1lKSB7XG4gICAgICAgIHJldHVybiB0aGlzLnJlY2VpdmVyTWFwLmhhcyhyZWNlaXZlck5hbWUpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgbnVtYmVyIG9mIHJlY2VpdmVycyByZWdpc3RlcmVkIGZvciB0aGUgc2lnbmFsLlxuICAgICAqL1xuICAgIHJlY2VpdmVyQ291bnQoKSB7XG4gICAgICAgIHJldHVybiB0aGlzLnJlY2VpdmVyTWFwLnNpemU7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogU2VuZCB0aGUgc2lnbmFsLlxuICAgICAqXG4gICAgICogQHBhcmFtIGRhdGEgVGhlIGRhdGEgc2VudCB3aXRoIHRoZSBzaWduYWwuIEZvcndhcmRlZCB0b1xuICAgICAqICAgICAgdGhlIHNpZ25hbCByZWNlaXZlciBjYWxsYmFjay5cbiAgICAgKiBAcGFyYW0ge1NlbnRTaWduYWxJbmZvfSBpbmZvIElmIHRoaXMgaXMgcHJvdmlkZWQsIHdlIGFkZCB0aGVcbiAgICAgKiAgICAgIG5hbWUgb2YgYWxsIHJlY2VpdmVycyB0aGUgc2lnbmFsIHdhcyBzZW50IHRvLlxuICAgICAqL1xuICAgIHNlbmQoZGF0YSwgaW5mbykge1xuICAgICAgICBmb3IobGV0IHJlY2VpdmVyIG9mIHRoaXMucmVjZWl2ZXJNYXAudmFsdWVzKCkpIHtcbiAgICAgICAgICAgIHJlY2VpdmVyLnRyaWdnZXIoZGF0YSk7XG4gICAgICAgICAgICBpZihpbmZvKSB7XG4gICAgICAgICAgICAgICAgaW5mby5fYWRkUmVjZWl2ZXJOYW1lKHJlY2VpdmVyLm5hbWUpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxufVxuXG5cbi8qKlxuICogVGhlIGluc3RhbmNlIG9mIHRoZSB7QGxpbmsgU2lnbmFsSGFuZGxlclNpbmdsZXRvbn0uXG4gKi9cbmxldCBfaW5zdGFuY2UgPSBudWxsO1xuXG4vKipcbiAqIFNpZ25hbCBoYW5kbGVyIHNpbmdsZXRvbiBmb3IgZ2xvYmFsIGNvbW11bmljYXRpb24uXG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+QmFzaWMgZXhhbXBsZTwvY2FwdGlvbj5cbiAqIGxldCBzaWduYWxIYW5kbGVyID0gbmV3IFNpZ25hbEhhbmRsZXJTaW5nbGV0b24oKTtcbiAqIHNpZ25hbEhhbmRsZXIuYWRkUmVjZWl2ZXIoJ215YXBwLm15c2lnbmFsJywgJ215b3RoZXJhcHAuTXlSZWNlaXZlcicsIChyZWNlaXZlZFNpZ25hbEluZm8pID0+IHtcbiAqICAgICBjb25zb2xlLmxvZygnU2lnbmFsIHJlY2VpdmVkLiBEYXRhOicsIHJlY2VpdmVkU2lnbmFsSW5mby5kYXRhKTtcbiAqIH0pO1xuICogc2lnbmFsSGFuZGxlci5zZW5kKCdteWFwcC5teXNpZ25hbCcsIHsndGhlJzogJ2RhdGEnfSk7XG4gKlxuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPlJlY29tbWVuZGVkIHNpZ25hbCBhbmQgcmVjZWl2ZXIgbmFtaW5nPC9jYXB0aW9uPlxuICpcbiAqIC8vIEluIG15YXBwL21lbnUvTWVudUNvbXBvbmVudC5qc1xuICogY2xhc3MgTWVudUNvbXBvbmVudCB7XG4gKiAgICAgY29uc3RydWN0b3IobWVudU5hbWUpIHtcbiAqICAgICAgICAgdGhpcy5tZW51TmFtZSA9IG1lbnVOYW1lO1xuICogICAgICAgICBsZXQgc2lnbmFsSGFuZGxlciA9IG5ldyBTaWduYWxIYW5kbGVyU2luZ2xldG9uKCk7XG4gKiAgICAgICAgIHNpZ25hbEhhbmRsZXIuYWRkUmVjZWl2ZXIoXG4gKiAgICAgICAgICAgICBgdG9nZ2xlTWVudSMke3RoaXMubWVudU5hbWV9YCxcbiAqICAgICAgICAgICAgICdteWFwcC5tZW51Lk1lbnVDb21wb25lbnQnLFxuICogICAgICAgICAgICAgKHJlY2VpdmVkU2lnbmFsSW5mbykgPT4ge1xuICogICAgICAgICAgICAgICAgICB0aGlzLnRvZ2dsZSgpO1xuICogICAgICAgICAgICAgfVxuICogICAgICAgICApO1xuICogICAgIH1cbiAqICAgICB0b2dnbGUoKSB7XG4gKiAgICAgICAgIC8vIFRvZ2dsZSB0aGUgbWVudVxuICogICAgIH1cbiAqIH1cbiAqXG4gKiAvLyBJbiBteW90aGVyYXBwL3dpZGdldHMvTWVudVRvZ2dsZS5qc1xuICogY2xhc3MgTWVudVRvZ2dsZSB7XG4gKiAgICAgY29uc3RydWN0b3IobWVudU5hbWUpIHtcbiAqICAgICAgICAgdGhpcy5tZW51TmFtZSA9IG1lbnVOYW1lO1xuICogICAgIH1cbiAqICAgICB0b2dnbGUoKSB7XG4gKiAgICAgICAgIGxldCBzaWduYWxIYW5kbGVyID0gbmV3IFNpZ25hbEhhbmRsZXJTaW5nbGV0b24oKTtcbiAqICAgICAgICAgc2lnbmFsSGFuZGxlci5zZW5kKGB0b2dnbGVNZW51IyR7dGhpcy5tZW51TmFtZX1gKTtcbiAqICAgICB9XG4gKiB9XG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+TXVsdGlwbGUgcmVjZWl2ZXJzPC9jYXB0aW9uPlxuICogbGV0IHNpZ25hbEhhbmRsZXIgPSBuZXcgU2lnbmFsSGFuZGxlclNpbmdsZXRvbigpO1xuICogc2lnbmFsSGFuZGxlci5hZGRSZWNlaXZlcignbXlhcHAubXlzaWduYWwnLCAnbXlvdGhlcmFwcC5NeUZpcnN0UmVjZWl2ZXInLCAocmVjZWl2ZWRTaWduYWxJbmZvKSA9PiB7XG4gKiAgICAgY29uc29sZS5sb2coJ1NpZ25hbCByZWNlaXZlZCBieSByZWNlaXZlciAxIScpO1xuICogfSk7XG4gKiBzaWduYWxIYW5kbGVyLmFkZFJlY2VpdmVyKCdteWFwcC5teXNpZ25hbCcsICdteW90aGVyYXBwLk15U2Vjb25kUmVjZWl2ZXInLCAocmVjZWl2ZWRTaWduYWxJbmZvKSA9PiB7XG4gKiAgICAgY29uc29sZS5sb2coJ1NpZ25hbCByZWNlaXZlZCBieSByZWNlaXZlciAxIScpO1xuICogfSk7XG4gKiBzaWduYWxIYW5kbGVyLnNlbmQoJ215YXBwLm15c2lnbmFsJywgeyd0aGUnOiAnZGF0YSd9KTtcbiAqXG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+RGVidWdnaW5nPC9jYXB0aW9uPlxuICogbGV0IHNpZ25hbEhhbmRsZXIgPSBuZXcgU2lnbmFsSGFuZGxlclNpbmdsZXRvbigpO1xuICogc2lnbmFsSGFuZGxlci5hZGRSZWNlaXZlcignbXlzaWduYWwnLCAnTXlSZWNlaXZlcicsIChyZWNlaXZlZFNpZ25hbEluZm8pID0+IHtcbiAqICAgICBjb25zb2xlLmxvZygncmVjZWl2ZWQgc2lnbmFsOicsIHJlY2VpdmVkU2lnbmFsSW5mby50b1N0cmluZygpKTtcbiAqIH0pO1xuICogc2lnbmFsSGFuZGxlci5zZW5kKCdteWFwcC5teXNpZ25hbCcsIHsndGhlJzogJ2RhdGEnfSwgKHNlbnRTaWduYWxJbmZvKSA9PiB7XG4gKiAgICAgY29uc29sZS5sb2coJ3NlbnQgc2lnbmFsIGluZm86Jywgc2VudFNpZ25hbEluZm8udG9TdHJpbmcoKSk7XG4gKiB9KTtcbiAqXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFNpZ25hbEhhbmRsZXJTaW5nbGV0b24ge1xuXG4gICAgY29uc3RydWN0b3IoKSB7XG4gICAgICAgIGlmKCFfaW5zdGFuY2UpIHtcbiAgICAgICAgICAgIF9pbnN0YW5jZSA9IHRoaXM7XG4gICAgICAgICAgICB0aGlzLl9zaWduYWxNYXAgPSBuZXcgTWFwKCk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIF9pbnN0YW5jZTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW1vdmUgYWxsIHJlY2VpdmVycyBmb3IgYWxsIHNpZ25hbHMuXG4gICAgICpcbiAgICAgKiBVc2VmdWwgZm9yIGRlYnVnZ2luZyBhbmQgdGVzdHMsIGJ1dCBzaG91bGQgbm90IGJlXG4gICAgICogdXNlZCBmb3IgcHJvZHVjdGlvbiBjb2RlLlxuICAgICAqL1xuICAgIGNsZWFyQWxsUmVjZWl2ZXJzRm9yQWxsU2lnbmFscygpIHtcbiAgICAgICAgdGhpcy5fc2lnbmFsTWFwLmNsZWFyKCk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQWRkIGEgcmVjZWl2ZXIgZm9yIGEgc3BlY2lmaWMgc2lnbmFsLlxuICAgICAqXG4gICAgICogQHBhcmFtIHtzdHJpbmd9IHNpZ25hbE5hbWUgVGhlIG5hbWUgb2YgdGhlIHNpZ25hbC5cbiAgICAgKiAgICAgIFR5cGljYWxseSBzb21ldGhpbmcgbGlrZSBgYHRvZ2dsZU1lbnVgYCBvciBgYG15YXBwLnRvZ2dsZU1lbnVgYC5cbiAgICAgKlxuICAgICAqICAgICAgV2hhdCBpZiB3ZSBoYXZlIG11bHRpcGxlIG9iamVjdHMgbGlzdGVuaW5nIGZvciB0aGlzIGBgdG9nZ2xlTWVudWBgXG4gICAgICogICAgICBzaWduYWwsIGFuZCB3ZSBvbmx5IHdhbnQgdG8gdG9nZ2xlIGEgc3BlY2lmaWMgbWVudT8gWW91IG5lZWRcbiAgICAgKiAgICAgIHRvIGVuc3VyZSB0aGUgc2lnbmFsTmFtZSBpcyB1bmlxdWUgZm9yIGVhY2ggbWVudS4gV2UgcmVjb21tZW5kXG4gICAgICogICAgICB0aGF0IHlvdSBkbyB0aGlzIGJ5IGFkZGluZyBgYCM8Y29udGV4dD5gYC4gRm9yIGV4YW1wbGVcbiAgICAgKiAgICAgIGBgdG9nZ2xlTWVudSNtYWlubWVudWBgLiBUaGlzIGlzIHNob3duIGluIG9uZSBvZiB0aGUgZXhhbXBsZXNcbiAgICAgKiAgICAgIGFib3ZlLlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfSByZWNlaXZlck5hbWUgVGhlIG5hbWUgb2YgdGhlIHJlY2VpdmVyLlxuICAgICAqICAgICAgTXVzdCBiZSB1bmlxdWUgZm9yIHRoZSBzaWduYWwuXG4gICAgICogICAgICBXZSByZWNvbW1lbmQgdGhhdCB5b3UgdXNlIGEgdmVyeSBleHBsaWNpdCBuYW1lIGZvciB5b3VyIHNpZ25hbHMuXG4gICAgICogICAgICBJdCBzaG91bGQgbm9ybWFsbHkgYmUgdGhlIGZ1bGwgcGF0aCB0byB0aGUgbWV0aG9kIG9yIGZ1bmN0aW9uIHJlY2VpdmluZ1xuICAgICAqICAgICAgdGhlIHNpZ25hbC4gU28gaWYgeW91IGhhdmUgYSBjbGFzcyBuYW1lZCBgYG15YXBwL21lbnUvTWVudUNvbXBvbmVudC5qc2BgXG4gICAgICogICAgICB0aGF0IHJlY2VpdmVzIGEgc2lnbmFsIHRvIHRvZ2dsZSB0aGUgbWVudSwgdGhlIHJlY2VpdmVyTmFtZSBzaG91bGQgYmVcbiAgICAgKiAgICAgIGBgbXlhcHAubWVudS5NZW51Q29tcG9uZW50YGAuXG4gICAgICogQHBhcmFtIGNhbGxiYWNrIFRoZSBjYWxsYmFjayB0byBjYWxsIHdoZW4gdGhlIHNpZ25hbCBpcyBzZW50LlxuICAgICAqICAgICAgVGhlIGNhbGxiYWNrIGlzIGNhbGxlZCB3aXRoIGEgc2luZ2xlIGFyZ3VtZW50IC0gYVxuICAgICAqICAgICAge0BsaW5rIFJlY2VpdmVkU2lnbmFsSW5mb30gb2JqZWN0LlxuICAgICAqL1xuICAgIGFkZFJlY2VpdmVyKHNpZ25hbE5hbWUsIHJlY2VpdmVyTmFtZSwgY2FsbGJhY2spIHtcbiAgICAgICAgaWYodHlwZW9mIGNhbGxiYWNrID09PSAndW5kZWZpbmVkJykge1xuICAgICAgICAgICAgdGhyb3cgbmV3IFR5cGVFcnJvcignVGhlIGNhbGxiYWNrIGFyZ3VtZW50IGZvciBhZGRSZWNlaXZlcigpIGlzIHJlcXVpcmVkLicpO1xuICAgICAgICB9XG4gICAgICAgIGlmKCF0aGlzLl9zaWduYWxNYXAuaGFzKHNpZ25hbE5hbWUpKSB7XG4gICAgICAgICAgICB0aGlzLl9zaWduYWxNYXAuc2V0KHNpZ25hbE5hbWUsIG5ldyBfU2lnbmFsUmVjZWl2ZXJzKHNpZ25hbE5hbWUpKTtcbiAgICAgICAgfVxuICAgICAgICBsZXQgc2lnbmFsID0gdGhpcy5fc2lnbmFsTWFwLmdldChzaWduYWxOYW1lKTtcbiAgICAgICAgc2lnbmFsLmFkZFJlY2VpdmVyKHJlY2VpdmVyTmFtZSwgY2FsbGJhY2spXG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVtb3ZlIGEgcmVjZWl2ZXIgZm9yIGEgc2lnbmFsIGFkZGVkIHdpdGgge0BsaW5rIFNpZ25hbEhhbmRsZXJTaW5nbGV0b24jYWRkUmVjZWl2ZXJ9LlxuICAgICAqXG4gICAgICogQHBhcmFtIHtzdHJpbmd9IHNpZ25hbE5hbWUgVGhlIG5hbWUgb2YgdGhlIHNpZ25hbC5cbiAgICAgKiBAcGFyYW0ge3N0cmluZ30gcmVjZWl2ZXJOYW1lIFRoZSBuYW1lIG9mIHRoZSByZWNlaXZlci5cbiAgICAgKi9cbiAgICByZW1vdmVSZWNlaXZlcihzaWduYWxOYW1lLCByZWNlaXZlck5hbWUpIHtcbiAgICAgICAgaWYodGhpcy5fc2lnbmFsTWFwLmhhcyhzaWduYWxOYW1lKSkge1xuICAgICAgICAgICAgbGV0IHNpZ25hbCA9IHRoaXMuX3NpZ25hbE1hcC5nZXQoc2lnbmFsTmFtZSk7XG4gICAgICAgICAgICBzaWduYWwucmVtb3ZlUmVjZWl2ZXIocmVjZWl2ZXJOYW1lKTtcbiAgICAgICAgICAgIGlmKHNpZ25hbC5yZWNlaXZlckNvdW50KCkgPT09IDApIHtcbiAgICAgICAgICAgICAgICB0aGlzLl9zaWduYWxNYXAuZGVsZXRlKHNpZ25hbE5hbWUpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQ2hlY2sgaWYgYSBzaWduYWwgaGFzIGEgc3BlY2lmaWMgcmVjZWl2ZXIuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge3N0cmluZ30gc2lnbmFsTmFtZSBUaGUgbmFtZSBvZiB0aGUgc2lnbmFsLlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfSByZWNlaXZlck5hbWUgVGhlIG5hbWUgb2YgdGhlIHJlY2VpdmVyLlxuICAgICAqL1xuICAgIGhhc1JlY2VpdmVyKHNpZ25hbE5hbWUsIHJlY2VpdmVyTmFtZSkge1xuICAgICAgICBpZih0aGlzLl9zaWduYWxNYXAuaGFzKHNpZ25hbE5hbWUpKSB7XG4gICAgICAgICAgICBsZXQgc2lnbmFsID0gdGhpcy5fc2lnbmFsTWFwLmdldChzaWduYWxOYW1lKTtcbiAgICAgICAgICAgIHJldHVybiBzaWduYWwuaGFzUmVjZWl2ZXIocmVjZWl2ZXJOYW1lKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgICAgfVxuICAgIH1cblxuXG4gICAgLyoqXG4gICAgICogUmVtb3ZlIGFsbCByZWNlaXZlcnMgZm9yIGEgc3BlY2lmaWMgc2lnbmFsLlxuICAgICAqXG4gICAgICogQHBhcmFtIHtzdHJpbmd9IHNpZ25hbE5hbWUgVGhlIG5hbWUgb2YgdGhlIHNpZ25hbCB0byByZW1vdmUuXG4gICAgICovXG4gICAgY2xlYXJBbGxSZWNlaXZlcnNGb3JTaWduYWwoc2lnbmFsTmFtZSkge1xuICAgICAgICBpZih0aGlzLl9zaWduYWxNYXAuaGFzKHNpZ25hbE5hbWUpKSB7XG4gICAgICAgICAgICB0aGlzLl9zaWduYWxNYXAuZGVsZXRlKHNpZ25hbE5hbWUpO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogU2VuZCBhIHNpZ25hbC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfSBzaWduYWxOYW1lIFRoZSBuYW1lIG9mIHRoZSBzaWduYWwgdG8gc2VuZC5cbiAgICAgKiBAcGFyYW0gZGF0YSBEYXRhIHRvIHNlbmQgdG8gdGhlIGNhbGxiYWNrIG9mIGFsbCByZWNlaXZlcnMgcmVnaXN0ZXJlZFxuICAgICAqICAgICAgZm9yIHRoZSBzaWduYWwuXG4gICAgICogQHBhcmFtIGluZm9DYWxsYmFjayBBbiBvcHRpb25hbCBjYWxsYmFjayB0aGF0IHJlY2VpdmVzIGluZm9ybWF0aW9uXG4gICAgICogICAgICBhYm91dCB0aGUgc2lnbmFsLiBVc2VmdWwgZm9yIGRlYnVnZ2luZyB3aGF0IGFjdHVhbGx5IHJlY2VpdmVkXG4gICAgICogICAgICB0aGUgc2lnbmFsLiBUaGUgYGBpbmZvQ2FsbGJhY2tgYCBpcyBjYWxsZWQgd2l0aCBhIHNpbmdsZVxuICAgICAqICAgICAgYXJndW1lbnQgLSBhIHtAbGluayBTZW50U2lnbmFsSW5mb30gb2JqZWN0LlxuICAgICAqL1xuICAgIHNlbmQoc2lnbmFsTmFtZSwgZGF0YSwgaW5mb0NhbGxiYWNrKSB7XG4gICAgICAgIGxldCBpbmZvID0gbnVsbDtcbiAgICAgICAgaWYoaW5mb0NhbGxiYWNrKSB7XG4gICAgICAgICAgICBpbmZvID0gbmV3IFNlbnRTaWduYWxJbmZvKHNpZ25hbE5hbWUpO1xuICAgICAgICB9XG4gICAgICAgIGlmKHRoaXMuX3NpZ25hbE1hcC5oYXMoc2lnbmFsTmFtZSkpIHtcbiAgICAgICAgICAgIGxldCBzaWduYWwgPSB0aGlzLl9zaWduYWxNYXAuZ2V0KHNpZ25hbE5hbWUpO1xuICAgICAgICAgICAgc2lnbmFsLnNlbmQoZGF0YSwgaW5mbyk7XG4gICAgICAgIH1cbiAgICAgICAgaWYoaW5mb0NhbGxiYWNrKSB7XG4gICAgICAgICAgICBpbmZvQ2FsbGJhY2soaW5mbyk7XG4gICAgICAgIH1cbiAgICB9XG59XG4iLCJpbXBvcnQgU2lnbmFsSGFuZGxlclNpbmdsZXRvbiBmcm9tIFwiLi9TaWduYWxIYW5kbGVyU2luZ2xldG9uXCI7XG5pbXBvcnQgV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24gZnJvbSBcIi4vd2lkZ2V0L1dpZGdldFJlZ2lzdHJ5U2luZ2xldG9uXCI7XG5pbXBvcnQgTG9nZ2VyU2luZ2xldG9uIGZyb20gXCIuL2xvZy9Mb2dnZXJTaW5nbGV0b25cIjtcblxud2luZG93LmlldnZfanNiYXNlX2NvcmUgPSB7XG4gICAgU2lnbmFsSGFuZGxlclNpbmdsZXRvbjogU2lnbmFsSGFuZGxlclNpbmdsZXRvbixcbiAgICBXaWRnZXRSZWdpc3RyeVNpbmdsZXRvbjogV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24sXG4gICAgTG9nZ2VyU2luZ2xldG9uOiBMb2dnZXJTaW5nbGV0b25cbn07XG4iLCJpbXBvcnQgTE9HTEVWRUwgZnJvbSBcIi4vbG9nbGV2ZWxcIjtcblxuXG4vKipcbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgQWJzdHJhY3RMb2dnZXIge1xuICAgIGdldExvZ0xldmVsKCkge1xuICAgICAgICB0aHJvdyBuZXcgRXJyb3IoJ011c3QgYmUgb3ZlcnJpZGRlbiBpbiBzdWJjbGFzc2VzLicpO1xuICAgIH1cblxuICAgIF9ub091dHB1dCgpIHtcblxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEV4cG9zZXMgY29uc29sZS5sb2cuIFdpbGwgb25seSBwcmludCBpZiBjdXJyZW50IGxldmVsIGlzXG4gICAgICogaGlnaGVyIHRoYW4ge0BsaW5rIExvZ0xldmVscyNERUJVR30uXG4gICAgICogQHJldHVybnMge0Z1bmN0aW9ufSBjb25zb2xlLmxvZ1xuICAgICAqL1xuICAgIGdldCBkZWJ1ZygpIHtcbiAgICAgICAgaWYgKHRoaXMuZ2V0TG9nTGV2ZWwoKSA+PSBMT0dMRVZFTC5ERUJVRykge1xuICAgICAgICAgICAgcmV0dXJuIGNvbnNvbGUubG9nLmJpbmQoY29uc29sZSk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHRoaXMuX25vT3V0cHV0O1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEV4cG9zZXMgY29uc29sZS5sb2cuIFdpbGwgb25seSBwcmludCBpZiBjdXJyZW50IGxldmVsIGlzXG4gICAgICogaGlnaGVyIHRoYW4ge0BsaW5rIExvZ0xldmVscyNJTkZPfS5cbiAgICAgKiBAcmV0dXJucyB7RnVuY3Rpb259IGNvbnNvbGUubG9nXG4gICAgICovXG4gICAgZ2V0IGluZm8oKSB7XG4gICAgICAgIGlmICh0aGlzLmdldExvZ0xldmVsKCkgPj0gTE9HTEVWRUwuSU5GTykge1xuICAgICAgICAgICAgcmV0dXJuIGNvbnNvbGUubG9nLmJpbmQoY29uc29sZSk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHRoaXMuX25vT3V0cHV0O1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEV4cG9zZXMgY29uc29sZS53YXJuLiBXaWxsIG9ubHkgcHJpbnQgaWYgY3VycmVudCBsZXZlbCBpc1xuICAgICAqIGhpZ2hlciB0aGFuIHtAbGluayBMb2dMZXZlbHMjV0FSTklOR30uXG4gICAgICogQHJldHVybnMge0Z1bmN0aW9ufSBjb25zb2xlLndhcm5cbiAgICAgKi9cbiAgICBnZXQgd2FybmluZygpIHtcbiAgICAgICAgaWYodGhpcy5nZXRMb2dMZXZlbCgpID49IExPR0xFVkVMLldBUk5JTkcpIHtcbiAgICAgICAgICAgIHJldHVybiBjb25zb2xlLndhcm4uYmluZChjb25zb2xlKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdGhpcy5fbm9PdXRwdXQ7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogRXhwb3NlcyBjb25zb2xlLmVycm9yLiBXaWxsIG9ubHkgcHJpbnQgaWYgY3VycmVudCBsZXZlbCBpc1xuICAgICAqIGhpZ2hlciB0aGFuIHtAbGluayBMb2dMZXZlbHMjRVJST1J9LlxuICAgICAqIEByZXR1cm5zIHtGdW5jdGlvbn0gY29uc29sZS5lcnJvclxuICAgICAqL1xuICAgIGdldCBlcnJvcigpIHtcbiAgICAgICAgaWYgKHRoaXMuZ2V0TG9nTGV2ZWwoKSA+PSBMT0dMRVZFTC5FUlJPUikge1xuICAgICAgICAgICAgcmV0dXJuIGNvbnNvbGUuZXJyb3IuYmluZChjb25zb2xlKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdGhpcy5fbm9PdXRwdXQ7XG4gICAgfVxufVxuIiwiaW1wb3J0IEFic3RyYWN0TG9nZ2VyIGZyb20gXCIuL0Fic3RyYWN0TG9nZ2VyXCI7XG5pbXBvcnQgTE9HTEVWRUwgZnJvbSBcIi4vbG9nbGV2ZWxcIjtcblxuXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBMb2dnZXIgZXh0ZW5kcyBBYnN0cmFjdExvZ2dlciB7XG4gICAgLyoqXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge3N0cmluZ30gbmFtZSBUaGUgbmFtZSBvZiB0aGUgbG9nZ2VyLlxuICAgICAqIEBwYXJhbSB7TG9nZ2VyU2luZ2xldG9ufSBsb2dnZXJTaW5nbGV0b24gVGhlIGxvZ2dlciBzaW5nbGV0b25cbiAgICAgKiAgICAgIHRoaXMgbG9nZ2VyIGJlbG9uZ3MgdG8uXG4gICAgICovXG4gICAgY29uc3RydWN0b3IobmFtZSwgbG9nZ2VyU2luZ2xldG9uKSB7XG4gICAgICAgIHN1cGVyKCk7XG4gICAgICAgIHRoaXMuX25hbWUgPSBuYW1lO1xuICAgICAgICB0aGlzLl9sb2dMZXZlbCA9IG51bGw7XG4gICAgICAgIHRoaXMuX2xvZ2dlclNpbmdsZXRvbiA9IGxvZ2dlclNpbmdsZXRvbjtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIG5hbWUgb2YgdGhpcyBsb2dnZXIuXG4gICAgICogQHJldHVybnMge3N0cmluZ31cbiAgICAgKi9cbiAgICBnZXQgbmFtZSgpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuX25hbWU7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogU2V0IHRoZSBsb2dsZXZlbCBmb3IgdGhpcyBsb2dnZXIuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge2ludH0gbG9nTGV2ZWwgVGhlIGxvZyBsZXZlbC4gTXVzdCBiZSBvbmUgb2YgdGhlIGxvZ2xldmVsc1xuICAgICAqICAgICAgZGVmaW5lZCBpbiB7QGxpbmsgTG9nTGV2ZWxzfS5cbiAgICAgKiBAdGhyb3dzIHtSYW5nZUVycm9yfSBpZiB7QGxpbmsgTG9nTGV2ZWxzI3ZhbGlkYXRlTG9nTGV2ZWx9IGZhaWxzLlxuICAgICAqL1xuICAgIHNldExvZ0xldmVsKGxvZ0xldmVsKSB7XG4gICAgICAgIExPR0xFVkVMLnZhbGlkYXRlTG9nTGV2ZWwobG9nTGV2ZWwpO1xuICAgICAgICB0aGlzLl9sb2dMZXZlbCA9IGxvZ0xldmVsO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgbG9nIGxldmVsLlxuICAgICAqXG4gICAgICogSWYgbm8gbG9nIGxldmVsIGhhcyBiZWVuIHNldCB3aXRoIHtAbGluayBMb2dnZXIjc2V0TG9nTGV2ZWx9LFxuICAgICAqIHRoaXMgcmV0dXJucyB7QGxpbmsgTG9nZ2VyU2luZ2xldG9uI2dldERlZmF1bHRMb2dMZXZlbH0uXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyB7aW50fVxuICAgICAqL1xuICAgIGdldExvZ0xldmVsKCkge1xuICAgICAgICBpZih0aGlzLl9sb2dMZXZlbCA9PSBudWxsKSB7XG4gICAgICAgICAgICByZXR1cm4gdGhpcy5fbG9nZ2VyU2luZ2xldG9uLmdldERlZmF1bHRMb2dMZXZlbCgpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB0aGlzLl9sb2dMZXZlbDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGV4dHVhbCBuYW1lIGZvciB0aGUgbG9nIGxldmVsLiBJZiB0aGUgbG9nZ2VyXG4gICAgICogZG9lcyBub3QgaGF2ZSBhIGxvZ0xldmVsIChpZiBpdCBpbmhlcml0cyBpdCBmcm9tIHRoZSBMb2dnZXJTaW5nbGV0b24pXG4gICAgICogYSBzdHJpbmcgd2l0aCBpbmZvcm1hdGlvbiBhYm91dCB0aGlzIGFuZCB0aGUgZGVmYXVsdCBsb2dMZXZlbCBmb3IgdGhlXG4gICAgICogTG9nZ2VyU2luZ2xldG9uIGlzIHJldHVybmVkLlxuICAgICAqXG4gICAgICogSW50ZW5kZWQgZm9yIGRlYnVnZ2luZy4gVGhlIGZvcm1hdCBvZiB0aGUgc3RyaW5nIG1heSBjaGFuZ2UuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyB7c3RyaW5nfVxuICAgICAqL1xuXG4gICAgZ2V0VGV4dHVhbE5hbWVGb3JMb2dMZXZlbCgpIHtcbiAgICAgICAgaWYodGhpcy5fbG9nTGV2ZWwgPT0gbnVsbCkge1xuICAgICAgICAgICAgcmV0dXJuICdbZGVmYXVsdCBmb3IgTG9nZ2VyU2luZ2xldG9uIC0gJyArXG4gICAgICAgICAgICAgICAgYCR7dGhpcy5fbG9nZ2VyU2luZ2xldG9uLmdldFRleHR1YWxOYW1lRm9yRGVmYXVsdExvZ0xldmVsKCl9XWA7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIExPR0xFVkVMLmdldFRleHR1YWxOYW1lRm9yTG9nTGV2ZWwodGhpcy5nZXRMb2dMZXZlbCgpKTtcbiAgICB9XG5cbiAgICBnZXREZWJ1Z0luZm9TdHJpbmcoKSB7XG4gICAgICAgIHJldHVybiBgJHt0aGlzLm5hbWV9OiAke3RoaXMuZ2V0VGV4dHVhbE5hbWVGb3JMb2dMZXZlbCgpfWA7XG4gICAgfVxufVxuIiwiaW1wb3J0IExvZ2dlciBmcm9tIFwiLi9Mb2dnZXJcIjtcbmltcG9ydCBMT0dMRVZFTCBmcm9tIFwiLi9sb2dsZXZlbFwiO1xuXG5sZXQgX2luc3RhbmNlID0gbnVsbDtcblxuXG4vKipcbiAqIEEgbG9nZ2luZyBzeXN0ZW0uXG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+Q3JlYXRlIGFuZCB1c2UgYSBsb2dnZXI8L2NhcHRpb24+XG4gKiBpbXBvcnQgTG9nZ2VyU2luZ2xldG9uIGZyb20gJ2lldnZfanNiYXNlL2xvZy9Mb2dnZXJTaW5nbGV0b24nO1xuICogbGV0IG15bG9nZ2VyID0gbmV3IExvZ2dlclNpbmdsZXRvbigpLmxvZ2dlclNpbmdsZXRvbi5nZXRMb2dnZXIoJ215cHJvamVjdC5NeUNsYXNzJyk7XG4gKiBteWxvZ2dlci5kZWJ1ZygnSGVsbG8gZGVidWcgd29ybGQnKTtcbiAqIG15bG9nZ2VyLmluZm8oJ0hlbGxvIGluZm8gd29ybGQnKTtcbiAqIG15bG9nZ2VyLndhcm5pbmcoJ0hlbGxvIHdhcm5pbmcgd29ybGQnKTtcbiAqIG15bG9nZ2VyLmVycm9yKCdIZWxsbyBlcnJvciB3b3JsZCcpO1xuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPlNldCBhIGRlZmF1bHQgbG9nbGV2ZWwgZm9yIGFsbCBsb2dnZXJzPC9jYXB0aW9uPlxuICogaW1wb3J0IExPR0xFVkVMIGZyb20gJ2lldnZfanNiYXNlL2xvZy9sb2dsZXZlbCc7XG4gKiBuZXcgTG9nZ2VyU2luZ2xldG9uKCkuc2V0RGVmYXVsdExvZ0xldmVsKExPR0xFVkVMLkRFQlVHKTtcbiAqXG4gKiBAZXhhbXBsZSA8Y2FwdGlvbj5TZXQgYSBjdXN0b20gbG9nbGV2ZWwgZm9yIGEgc2luZ2xlIGxvZ2dlcjwvY2FwdGlvbj5cbiAqIGltcG9ydCBMT0dMRVZFTCBmcm9tICdpZXZ2X2pzYmFzZS9sb2cvbG9nbGV2ZWwnO1xuICogbmV3IExvZ2dlclNpbmdsZXRvbigpLmdldExvZ2dlcignbXlsb2dnZXInKS5zZXRMb2dsZXZlbChMT0dMRVZFTC5ERUJVRyk7XG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIExvZ2dlclNpbmdsZXRvbiB7XG4gICAgLyoqXG4gICAgICogR2V0IGFuIGluc3RhbmNlIG9mIHRoZSBzaW5nbGV0b24uXG4gICAgICpcbiAgICAgKiBUaGUgZmlyc3QgdGltZSB0aGlzIGlzIGNhbGxlZCwgd2UgY3JlYXRlIGEgbmV3IGluc3RhbmNlLlxuICAgICAqIEZvciBhbGwgc3Vic2VxdWVudCBjYWxscywgd2UgcmV0dXJuIHRoZSBpbnN0YW5jZSB0aGF0IHdhc1xuICAgICAqIGNyZWF0ZWQgb24gdGhlIGZpcnN0IGNhbGwuXG4gICAgICovXG4gICAgY29uc3RydWN0b3IoKSB7XG4gICAgICAgIGlmKCFfaW5zdGFuY2UpIHtcbiAgICAgICAgICAgIF9pbnN0YW5jZSA9IHRoaXM7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy5fbG9nZ2VyTWFwID0gbmV3IE1hcCgpO1xuICAgICAgICB0aGlzLnJlc2V0KCk7XG4gICAgICAgIHJldHVybiBfaW5zdGFuY2U7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSBudW1iZXIgb2YgbG9nZ2VycyByZWdpc3RlcmVkIHVzaW5nXG4gICAgICoge0BsaW5rIGdldExvZ2dlcn0uXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyB7bnVtYmVyfSBUaGUgbnVtYmVyIG9mIGxvZ2dlcnMuXG4gICAgICovXG4gICAgZ2V0TG9nZ2VyQ291bnQoKSB7XG4gICAgICAgIHJldHVybiB0aGlzLl9sb2dnZXJNYXAuc2l6ZTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZXNldCB0byBkZWZhdWx0IGxvZyBsZXZlbCwgYW5kIGNsZWFyIGFsbFxuICAgICAqIGN1c3RvbSBsb2dnZXJzLlxuICAgICAqL1xuICAgIHJlc2V0KCkge1xuICAgICAgICB0aGlzLl9sb2dMZXZlbCA9IExPR0xFVkVMLldBUk5JTkc7XG4gICAgICAgIHRoaXMuX2xvZ2dlck1hcC5jbGVhcigpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgZGVmYXVsdCBsb2cgbGV2ZWwuXG4gICAgICpcbiAgICAgKiBEZWZhdWx0cyB0byB7QGxpbmsgTG9nTGV2ZWxzI1dBUk5JTkd9IGlmIG5vdCBvdmVycmlkZGVuXG4gICAgICogd2l0aCB7QExvZ2dlclNpbmdsZXRvbiNzZXREZWZhdWx0TG9nTGV2ZWx9LlxuICAgICAqXG4gICAgICogQHJldHVybnMge2ludH0gT25lIG9mIHRoZSBsb2dsZXZlbHMgZGVmaW5lZCBpbiB7QGxpbmsgTG9nTGV2ZWxzfVxuICAgICAqL1xuICAgIGdldERlZmF1bHRMb2dMZXZlbCgpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuX2xvZ0xldmVsO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFNldCB0aGUgZGVmYXVsdCBsb2dsZXZlbC5cbiAgICAgKlxuICAgICAqIEFsbCBsb2dnZXJzIHVzZSB0aGlzIGJ5IGRlZmF1bHQgdW5sZXNzXG4gICAgICogeW91IG92ZXJyaWRlIHRoZWlyIGxvZ2xldmVsLlxuICAgICAqXG4gICAgICogQGV4YW1wbGUgPGNhcHRpb24+T3ZlcnJpZGUgbG9nbGV2ZWwgb2YgYSBzcGVjaWZpYyBsb2dnZXI8L2NhcHRpb24+XG4gICAgICogaW1wb3J0IExvZ2dlclNpbmdsZXRvbiBmcm9tICdpZXZ2X2pzYmFzZS9sb2cvTG9nZ2VyU2luZ2xldG9uJztcbiAgICAgKiBpbXBvcnQgTE9HTEVWRUwgZnJvbSAnaWV2dl9qc2Jhc2UvbG9nL2xvZ2xldmVsJztcbiAgICAgKiBsZXQgbG9nZ2VyU2luZ2xldG9uID0gbmV3IExvZ2dlclNpbmdsZXRvbigpO1xuICAgICAqIGxvZ2dlclNpbmdsZXRvbi5nZXRMb2dnZXIoJ215bG9nZ2VyJykuc2V0TG9nTGV2ZWwoTE9HTEVWRUwuREVCVUcpO1xuICAgICAqXG4gICAgICogQHBhcmFtIGxvZ0xldmVsIFRoZSBsb2cgbGV2ZWwuIE11c3QgYmUgb25lIG9mIHRoZSBsb2dsZXZlbHNcbiAgICAgKiAgICAgIGRlZmluZWQgaW4ge0BsaW5rIExvZ0xldmVsc30uXG4gICAgICogQHRocm93cyB7UmFuZ2VFcnJvcn0gaWYge0BsaW5rIExvZ0xldmVscyN2YWxpZGF0ZUxvZ0xldmVsfSBmYWlscy5cbiAgICAgKi9cbiAgICBzZXREZWZhdWx0TG9nTGV2ZWwobG9nTGV2ZWwpIHtcbiAgICAgICAgTE9HTEVWRUwudmFsaWRhdGVMb2dMZXZlbChsb2dMZXZlbCk7XG4gICAgICAgIHRoaXMuX2xvZ0xldmVsID0gbG9nTGV2ZWw7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IGEgbG9nZ2VyLlxuICAgICAqXG4gICAgICogQHBhcmFtIHtzdHJpbmd9IG5hbWUgQSBuYW1lIGZvciB0aGUgbG9nZ2VyLiBTaG91bGQgYmUgYSB1bmlxdWUgbmFtZSxcbiAgICAgKiAgICAgIHNvIHR5cGljYWxseSB0aGUgZnVsbCBpbXBvcnQgcGF0aCBvZiB0aGUgY2xhc3MvZnVuY3Rpb24gdXNpbmdcbiAgICAgKiAgICAgIHRoZSBsb2dnZXIuXG4gICAgICogQHJldHVybnMge0xvZ2dlcn1cbiAgICAgKi9cbiAgICBnZXRMb2dnZXIobmFtZSkge1xuICAgICAgICBpZighdGhpcy5fbG9nZ2VyTWFwLmhhcyhuYW1lKSkge1xuICAgICAgICAgICAgdGhpcy5fbG9nZ2VyTWFwLnNldChuYW1lLCBuZXcgTG9nZ2VyKG5hbWUsIHRoaXMpKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdGhpcy5fbG9nZ2VyTWFwLmdldChuYW1lKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIG5hbWVzIG9mIGFsbCB0aGUgcmVnaXN0ZXJlZCBsb2dnZXJzLlxuICAgICAqXG4gICAgICogQHJldHVybnMge0FycmF5fSBTb3J0ZWQgYXJyYXkgd2l0aCB0aGUgc2FtZSBvZiB0aGUgbG9nZ2Vycy5cbiAgICAgKi9cbiAgICBnZXRMb2dnZXJOYW1lQXJyYXkoKSB7XG4gICAgICAgIGxldCBsb2dnZXJOYW1lcyA9IEFycmF5LmZyb20odGhpcy5fbG9nZ2VyTWFwLmtleXMoKSk7XG4gICAgICAgIGxvZ2dlck5hbWVzLnNvcnQoKTtcbiAgICAgICAgcmV0dXJuIGxvZ2dlck5hbWVzO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0ZXh0dWFsIG5hbWUgZm9yIHRoZSBkZWZhdWx0IGxvZyBsZXZlbC5cbiAgICAgKlxuICAgICAqIEludGVuZGVkIGZvciBkZWJ1Z2dpbmcuIFRoZSBmb3JtYXQgb2YgdGhlIHN0cmluZyBtYXkgY2hhbmdlLlxuICAgICAqXG4gICAgICogQHJldHVybnMge3N0cmluZ31cbiAgICAgKi9cbiAgICBnZXRUZXh0dWFsTmFtZUZvckRlZmF1bHRMb2dMZXZlbCgpIHtcbiAgICAgICAgcmV0dXJuIExPR0xFVkVMLmdldFRleHR1YWxOYW1lRm9yTG9nTGV2ZWwodGhpcy5nZXREZWZhdWx0TG9nTGV2ZWwoKSk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IGEgc3RyaW5nIHRoYXQgc3VtbWFyaXplIGluZm9ybWF0aW9uIGFib3V0IGFsbCB0aGVcbiAgICAgKiBsb2dnZXJzLiBUaGUgc3RyaW5nIGhhcyBhIGxpc3Qgb2YgbG9nbGV2ZWxzIHdpdGhcbiAgICAgKiB0aGVpciBsb2dsZXZlbC4gUGVyZmVjdCBmb3IgZGVidWdnaW5nLlxuICAgICAqXG4gICAgICogSW50ZW5kZWQgZm9yIGRlYnVnZ2luZy4gVGhlIGZvcm1hdCBvZiB0aGUgc3RyaW5nIG1heSBjaGFuZ2UuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyB7c3RyaW5nfVxuICAgICAqL1xuICAgIGdldERlYnVnSW5mb1N0cmluZygpIHtcbiAgICAgICAgbGV0IGxvZ2dlckluZm9TdHJpbmcgPSBgRGVmYXVsdCBsb2dMZXZlbDogYCArXG4gICAgICAgICAgICBgJHt0aGlzLmdldFRleHR1YWxOYW1lRm9yRGVmYXVsdExvZ0xldmVsKCl9XFxuYCArXG4gICAgICAgICAgICBgTG9nZ2VyczpcXG5gO1xuICAgICAgICBpZih0aGlzLmdldExvZ2dlckNvdW50KCkgPT09IDApIHtcbiAgICAgICAgICAgIGxvZ2dlckluZm9TdHJpbmcgKz0gJyhubyBsb2dnZXJzKVxcbic7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBmb3IgKGxldCBsb2dnZXJOYW1lIG9mIHRoaXMuZ2V0TG9nZ2VyTmFtZUFycmF5KCkpIHtcbiAgICAgICAgICAgICAgICBsZXQgbG9nZ2VyID0gdGhpcy5nZXRMb2dnZXIobG9nZ2VyTmFtZSk7XG4gICAgICAgICAgICAgICAgbG9nZ2VySW5mb1N0cmluZyArPVxuICAgICAgICAgICAgICAgICAgICBgIC0gJHtsb2dnZXIuZ2V0RGVidWdJbmZvU3RyaW5nKCl9XFxuYDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gbG9nZ2VySW5mb1N0cmluZztcbiAgICB9XG59XG4iLCIvKipcbiAqIERlZmluZXMgdmFsaWQgbG9nIGxldmVscy5cbiAqXG4gKiBOb3QgdXNlZCBkaXJlY3RseSwgYnV0IGluc3RlYWQgdmlhIHRoZSBMT0dMRVZFTFxuICogY29uc3RhbnQgZXhwb3J0ZWQgYXMgZGVmYXVsdCBieSB0aGlzIG1vZHVsZS5cbiAqXG4gKiBAZXhhbXBsZVxuICogaW1wb3J0IExPR0xFVkVMIGZyb20gJ2lldnZfanNiYXNlL2xvZy9sb2dsZXZlbCc7XG4gKiBjb25zb2xlLmxvZygnVGhlIGRlYnVnIGxvZ2xldmVsIGlzOicsIExPR0xFVkVMLkRFQlVHKTtcbiAqIExPR0xFVkVMLnZhbGlkYXRlTG9nTGV2ZWwoMTApO1xuICovXG5leHBvcnQgY2xhc3MgTG9nTGV2ZWxzIHtcbiAgICBjb25zdHJ1Y3RvcigpIHtcbiAgICAgICAgdGhpcy5fcHJldHR5TG9nTGV2ZWxOYW1lcyA9IHt9O1xuICAgICAgICB0aGlzLl9wcmV0dHlMb2dMZXZlbE5hbWVzW3RoaXMuREVCVUddID0gJ0RFQlVHJztcbiAgICAgICAgdGhpcy5fcHJldHR5TG9nTGV2ZWxOYW1lc1t0aGlzLklORk9dID0gJ0lORk8nO1xuICAgICAgICB0aGlzLl9wcmV0dHlMb2dMZXZlbE5hbWVzW3RoaXMuV0FSTklOR10gPSAnV0FSTklORyc7XG4gICAgICAgIHRoaXMuX3ByZXR0eUxvZ0xldmVsTmFtZXNbdGhpcy5FUlJPUl0gPSAnRVJST1InO1xuICAgICAgICB0aGlzLl9wcmV0dHlMb2dMZXZlbE5hbWVzW3RoaXMuU0lMRU5UXSA9ICdTSUxFTlQnO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgbnVtYmVyIGZvciBsb2cgbGV2ZWwgREVCVUcuXG4gICAgICogQHJldHVybnMge251bWJlcn1cbiAgICAgKi9cbiAgICBnZXQgREVCVUcoKSB7XG4gICAgICAgIHJldHVybiA0O1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgbnVtYmVyIGZvciBsb2cgbGV2ZWwgSU5GTy5cbiAgICAgKiBAcmV0dXJucyB7bnVtYmVyfVxuICAgICAqL1xuICAgIGdldCBJTkZPKCkge1xuICAgICAgICByZXR1cm4gMztcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIG51bWJlciBmb3IgbG9nIGxldmVsIFdBUk5JTkcuXG4gICAgICogQHJldHVybnMge251bWJlcn1cbiAgICAgKi9cbiAgICBnZXQgV0FSTklORygpIHtcbiAgICAgICAgcmV0dXJuIDI7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSBudW1iZXIgZm9yIGxvZyBsZXZlbCBFUlJPUi5cbiAgICAgKiBAcmV0dXJucyB7bnVtYmVyfVxuICAgICAqL1xuICAgIGdldCBFUlJPUigpIHtcbiAgICAgICAgcmV0dXJuIDE7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSBudW1iZXIgZm9yIGxvZyBsZXZlbCBTSUxFTlQuXG4gICAgICogQHJldHVybnMge251bWJlcn1cbiAgICAgKi9cbiAgICBnZXQgU0lMRU5UKCkge1xuICAgICAgICByZXR1cm4gMDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBWYWxpZGF0ZSBhIGxvZyBsZXZlbC5cbiAgICAgKlxuICAgICAqIFNob3VsZCBiZSB1c2VkIGJ5IGFsbCBmdW5jdGlvbnMvbWV0aG9kcyB0aGF0IHNldCBhIGxvZyBsZXZlbC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBsb2dMZXZlbCBUaGUgbG9nbGV2ZWwuXG4gICAgICogQHRocm93cyB7UmFuZ2VFcnJvcn0gSWYgYGBsb2dMZXZlbGBgIGlzIG5vdCBvbmVcbiAgICAgKiAgIG9mOlxuICAgICAqXG4gICAgICogICAtIHtAbGluayBMb2dMZXZlbHMjREVCVUd9XG4gICAgICogICAtIHtAbGluayBMb2dMZXZlbHMjSU5GT31cbiAgICAgKiAgIC0ge0BsaW5rIExvZ0xldmVscyNXQVJOSU5HfVxuICAgICAqICAgLSB7QGxpbmsgTG9nTGV2ZWxzI0VSUk9SfVxuICAgICAqICAgLSB7QGxpbmsgTG9nTGV2ZWxzI1NJTEVOVH1cbiAgICAgKi9cbiAgICB2YWxpZGF0ZUxvZ0xldmVsKGxvZ0xldmVsKSB7XG4gICAgICAgIGlmIChsb2dMZXZlbCA+IHRoaXMuREVCVUcgfHwgbG9nTGV2ZWwgPCB0aGlzLlNJTEVOVCkge1xuICAgICAgICAgICAgdGhyb3cgbmV3IFJhbmdlRXJyb3IoXG4gICAgICAgICAgICAgICAgYEludmFsaWQgbG9nIGxldmVsOiAke2xvZ0xldmVsfSwgbXVzdCBiZSBiZXR3ZWVuIGAgK1xuICAgICAgICAgICAgICAgIGAke3RoaXMuU0lMRU5UfSAoU0lMRU5UKSBhbmQgJHt0aGlzLkRFQlVHfSAoREVCVUcpYCk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIHRleHR1YWwgbmFtZSBmb3IgYSBsb2cgbGV2ZWwuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge251bWJlcn0gbG9nTGV2ZWwgVGhlIGxvZyBsZXZlbCB0byBnZXQgYSB0ZXh0dWFsIG5hbWUgZm9yLlxuICAgICAqIEByZXR1cm5zIHtzdHJpbmd9XG4gICAgICpcbiAgICAgKiBAZXhhbXBsZVxuICAgICAqIGNvbnN0IGluZm9UZXh0ID0gTE9HTEVWRUwuZ2V0VGV4dHVhbE5hbWVGb3JMb2dMZXZlbChMT0dMRVZFTC5JTkZPKTtcbiAgICAgKiAvLyBpbmZvVGV4dCA9PT0gJ0lORk8nXG4gICAgICovXG4gICAgZ2V0VGV4dHVhbE5hbWVGb3JMb2dMZXZlbChsb2dMZXZlbCkge1xuICAgICAgICByZXR1cm4gdGhpcy5fcHJldHR5TG9nTGV2ZWxOYW1lc1tsb2dMZXZlbF07XG4gICAgfVxufVxuXG5jb25zdCBMT0dMRVZFTCA9IG5ldyBMb2dMZXZlbHMoKTtcbmV4cG9ydCBkZWZhdWx0IExPR0xFVkVMO1xuIiwiLyoqXG4gKiBNYWtlIGEgY3VzdG9tIGVycm9yIFwiY2xhc3NcIi5cbiAqXG4gKiBNYWtlcyBhbiBvbGQgc3R5bGUgcHJvdG90eXBlIGJhc2VkIGVycm9yIGNsYXNzLlxuICpcbiAqIEBleGFtcGxlXG4gKiBleHBvcnQgbGV0IE5vdEZvdW5kRXJyb3IgPSBtYWtlQ3VzdG9tRXJyb3IoJ05vdEZvdW5kRXJyb3InKTtcbiAqXG4gKiBAcGFyYW0gbmFtZSBUaGUgbmFtZSBvZiB0aGUgZXJyb3IgY2xhc3MuXG4gKiBAcmV0dXJucyB7RXJyb3J9IFRoZSBjcmVhdGVkIGVycm9yIGNsYXNzLlxuICovXG5leHBvcnQgZGVmYXVsdCBmdW5jdGlvbiBtYWtlQ3VzdG9tRXJyb3IobmFtZSkge1xuICAgIGxldCBDdXN0b21FcnJvciA9IGZ1bmN0aW9uKG1lc3NhZ2UpIHtcbiAgICAgICAgdGhpcy5tZXNzYWdlID0gbWVzc2FnZTtcbiAgICAgICAgdmFyIGxhc3RfcGFydCA9IG5ldyBFcnJvcigpLnN0YWNrLm1hdGNoKC9bXlxcc10rJC8pO1xuICAgICAgICB0aGlzLnN0YWNrID0gYCR7dGhpcy5uYW1lfSBhdCAke2xhc3RfcGFydH1gO1xuICAgIH07XG4gICAgT2JqZWN0LnNldFByb3RvdHlwZU9mKEN1c3RvbUVycm9yLCBFcnJvcik7XG4gICAgQ3VzdG9tRXJyb3IucHJvdG90eXBlID0gT2JqZWN0LmNyZWF0ZShFcnJvci5wcm90b3R5cGUpO1xuICAgIEN1c3RvbUVycm9yLnByb3RvdHlwZS5uYW1lID0gbmFtZTtcbiAgICBDdXN0b21FcnJvci5wcm90b3R5cGUubWVzc2FnZSA9IFwiXCI7XG4gICAgQ3VzdG9tRXJyb3IucHJvdG90eXBlLmNvbnN0cnVjdG9yID0gQ3VzdG9tRXJyb3I7XG4gICAgcmV0dXJuIEN1c3RvbUVycm9yO1xufVxuIiwiaW1wb3J0IHR5cGVEZXRlY3QgZnJvbSBcIi4vdHlwZURldGVjdFwiO1xuXG4vKipcbiAqIFByZXR0eSBmb3JtYXQgYW55IGphdmFzY3JpcHQgb2JqZWN0LlxuICpcbiAqIEhhbmRsZXMgdGhlIGZvbGxvd2luZyB0eXBlczpcbiAqXG4gKiAtIG51bGxcbiAqIC0gdW5kZWZpbmVkXG4gKiAtIE51bWJlclxuICogLSBCb29sZWFuXG4gKiAtIFN0cmluZ1xuICogLSBBcnJheVxuICogLSBNYXBcbiAqIC0gU2V0XG4gKiAtIEZ1bmN0aW9uXG4gKiAtIENsYXNzIChkZXRlY3RlZCBhcyBhIEZ1bmN0aW9uLCBzbyBwcmV0dHkgZm9ybWF0dGVkIGp1c3QgbGlrZSBhIGZ1bmN0aW9uKVxuICogLSBPYmplY3RcbiAqXG4gKiBAZXhhbXBsZSA8Y2FwdGlvbj5XaXRob3V0IGluZGVudGF0aW9uPC9jYXB0aW9uPlxuICogbmV3IFByZXR0eUZvcm1hdChbMSwgMl0pLnRvU3RyaW5nKCk7XG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+V2l0aCBpbmRlbnRhdGlvbiAoaW5kZW50IGJ5IDIgc3BhY2VzKTwvY2FwdGlvbj5cbiAqIG5ldyBQcmV0dHlGb3JtYXQoWzEsIDJdKS50b1N0cmluZygyKTtcbiAqXG4gKiBAZXhhbXBsZSA8Y2FwdGlvbj5TaW1wbGUgZXhhbXBsZXM8L2NhcHRpb24+XG4gKiBuZXcgUHJldHR5Rm9ybWF0KHRydWUpLnRvU3RyaW5nKCkgPT09ICd0cnVlJztcbiAqIG5ldyBQcmV0dHlGb3JtYXQobnVsbCkudG9TdHJpbmcoKSA9PT0gJ251bGwnO1xuICogbmV3IFByZXR0eUZvcm1hdChbMSwgMl0pLnRvU3RyaW5nKCkgPT09ICdbMSwgMl0nO1xuICogbmV3IFByZXR0eUZvcm1hdCh7bmFtZTogXCJKb2huXCIsIGFnZTogMjl9KS50b1N0cmluZygpID09PSAne1wiYWdlXCI6IDI5LCBcIm5hbWVcIjogSm9obn0nO1xuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPkNvbXBsZXggZXhhbXBsZTwvY2FwdGlvbj5cbiAqIGxldCBtYXAgPSBuZXcgTWFwKCk7XG4gKiBtYXAuc2V0KCdhJywgWzEwLCAyMF0pO1xuICogbWFwLnNldCgnYicsIFszMCwgNDAsIDUwXSk7XG4gKiBmdW5jdGlvbiB0ZXN0RnVuY3Rpb24oKSB7fVxuICogbGV0IG9iaiA9IHtcbiAqICAgICB0aGVNYXA6IG1hcCxcbiAqICAgICBhU2V0OiBuZXcgU2V0KFsnb25lJywgJ3R3byddKSxcbiAqICAgICB0aGVGdW5jdGlvbjogdGVzdEZ1bmN0aW9uXG4gKiB9O1xuICogY29uc3QgcHJldHR5Rm9ybWF0dGVkID0gbmV3IFByZXR0eUZvcm1hdChvYmopLnRvU3RyaW5nKDIpO1xuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBQcmV0dHlGb3JtYXQge1xuICAgIGNvbnN0cnVjdG9yKG9iaikge1xuICAgICAgICB0aGlzLl9vYmogPSBvYmo7XG4gICAgfVxuXG4gICAgX2luZGVudFN0cmluZyhzdHIsIGluZGVudCwgaW5kZW50TGV2ZWwpIHtcbiAgICAgICAgaWYoaW5kZW50ID09PSAwKSB7XG4gICAgICAgICAgICByZXR1cm4gc3RyO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBgJHsnICcucmVwZWF0KGluZGVudCAqIGluZGVudExldmVsKX0ke3N0cn1gO1xuICAgIH1cblxuICAgIF9vYmplY3RUb01hcChvYmopIHtcbiAgICAgICAgbGV0IG1hcCA9IG5ldyBNYXAoKTtcbiAgICAgICAgbGV0IHNvcnRlZEtleXMgPSBBcnJheS5mcm9tKE9iamVjdC5rZXlzKG9iaikpO1xuICAgICAgICBzb3J0ZWRLZXlzLnNvcnQoKTtcbiAgICAgICAgZm9yKGxldCBrZXkgb2Ygc29ydGVkS2V5cykge1xuICAgICAgICAgICAgbWFwLnNldChrZXksIG9ialtrZXldKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gbWFwO1xuICAgIH1cblxuICAgIF9wcmV0dHlGb3JtYXRGbGF0SXRlcmFibGUoZmxhdEl0ZXJhYmxlLCBzaXplLCBpbmRlbnQsIGluZGVudExldmVsLCBwcmVmaXgsIHN1ZmZpeCkge1xuICAgICAgICBsZXQgb3V0cHV0ID0gcHJlZml4O1xuICAgICAgICBsZXQgaXRlbVN1ZmZpeCA9ICcsICc7XG4gICAgICAgIGlmKGluZGVudCkge1xuICAgICAgICAgICAgb3V0cHV0ID0gYCR7cHJlZml4fVxcbmA7XG4gICAgICAgICAgICBpdGVtU3VmZml4ID0gJywnO1xuICAgICAgICB9XG4gICAgICAgIGxldCBpbmRleCA9IDE7XG4gICAgICAgIGZvcihsZXQgaXRlbSBvZiBmbGF0SXRlcmFibGUpIHtcbiAgICAgICAgICAgIGxldCBwcmV0dHlJdGVtID0gdGhpcy5fcHJldHR5Rm9ybWF0KGl0ZW0sIGluZGVudCwgaW5kZW50TGV2ZWwgKyAxKTtcbiAgICAgICAgICAgIGlmKGluZGV4ICE9PSBzaXplKSB7XG4gICAgICAgICAgICAgICAgcHJldHR5SXRlbSArPSBpdGVtU3VmZml4O1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgb3V0cHV0ICs9IHRoaXMuX2luZGVudFN0cmluZyhwcmV0dHlJdGVtLCBpbmRlbnQsIGluZGVudExldmVsICsgMSk7XG4gICAgICAgICAgICBpZihpbmRlbnQpIHtcbiAgICAgICAgICAgICAgICBvdXRwdXQgKz0gJ1xcbic7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBpbmRleCArKztcbiAgICAgICAgfVxuICAgICAgICBvdXRwdXQgKz0gdGhpcy5faW5kZW50U3RyaW5nKGAke3N1ZmZpeH1gLCBpbmRlbnQsIGluZGVudExldmVsKTtcbiAgICAgICAgcmV0dXJuIG91dHB1dDtcbiAgICB9XG5cbiAgICBfcHJldHR5Rm9ybWF0TWFwKG1hcCwgaW5kZW50LCBpbmRlbnRMZXZlbCwgcHJlZml4LCBzdWZmaXgsIGtleVZhbHVlU2VwYXJhdG9yKSB7XG4gICAgICAgIGxldCBvdXRwdXQgPSBwcmVmaXg7XG4gICAgICAgIGxldCBpdGVtU3VmZml4ID0gJywgJztcbiAgICAgICAgaWYoaW5kZW50KSB7XG4gICAgICAgICAgICBvdXRwdXQgPSBgJHtwcmVmaXh9XFxuYDtcbiAgICAgICAgICAgIGl0ZW1TdWZmaXggPSAnLCc7XG4gICAgICAgIH1cbiAgICAgICAgbGV0IGluZGV4ID0gMTtcbiAgICAgICAgZm9yKGxldCBba2V5LCB2YWx1ZV0gb2YgbWFwKSB7XG4gICAgICAgICAgICBsZXQgcHJldHR5S2V5ID0gdGhpcy5fcHJldHR5Rm9ybWF0KGtleSwgaW5kZW50LCBpbmRlbnRMZXZlbCArIDEpO1xuICAgICAgICAgICAgbGV0IHByZXR0eVZhbHVlID0gdGhpcy5fcHJldHR5Rm9ybWF0KHZhbHVlLCBpbmRlbnQsIGluZGVudExldmVsICsgMSk7XG4gICAgICAgICAgICBsZXQgcHJldHR5SXRlbSA9IGAke3ByZXR0eUtleX0ke2tleVZhbHVlU2VwYXJhdG9yfSR7cHJldHR5VmFsdWV9YDtcbiAgICAgICAgICAgIGlmKGluZGV4ICE9PSBtYXAuc2l6ZSkge1xuICAgICAgICAgICAgICAgIHByZXR0eUl0ZW0gKz0gaXRlbVN1ZmZpeDtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIG91dHB1dCArPSB0aGlzLl9pbmRlbnRTdHJpbmcocHJldHR5SXRlbSwgaW5kZW50LCBpbmRlbnRMZXZlbCArIDEpO1xuICAgICAgICAgICAgaWYoaW5kZW50KSB7XG4gICAgICAgICAgICAgICAgb3V0cHV0ICs9ICdcXG4nO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaW5kZXggKys7XG4gICAgICAgIH1cbiAgICAgICAgb3V0cHV0ICs9IHRoaXMuX2luZGVudFN0cmluZyhgJHtzdWZmaXh9YCwgaW5kZW50LCBpbmRlbnRMZXZlbCk7XG4gICAgICAgIHJldHVybiBvdXRwdXQ7XG4gICAgfVxuXG4gICAgX3ByZXR0eUZvcm1hdEZ1bmN0aW9uKGZuKSB7XG4gICAgICAgIHJldHVybiBgW0Z1bmN0aW9uOiAke2ZuLm5hbWV9XWA7XG4gICAgfVxuXG4gICAgX3ByZXR0eUZvcm1hdChvYmosIGluZGVudCwgaW5kZW50TGV2ZWwpIHtcbiAgICAgICAgY29uc3QgdHlwZVN0cmluZyA9IHR5cGVEZXRlY3Qob2JqKTtcbiAgICAgICAgbGV0IG91dHB1dCA9ICcnO1xuICAgICAgICBpZih0eXBlU3RyaW5nID09PSAnc3RyaW5nJykge1xuICAgICAgICAgICAgb3V0cHV0ID0gYFwiJHtvYmp9XCJgO1xuICAgICAgICB9IGVsc2UgaWYodHlwZVN0cmluZyA9PT0gJ251bWJlcicgfHwgdHlwZVN0cmluZyA9PT0gJ2Jvb2xlYW4nIHx8XG4gICAgICAgICAgICAgICAgdHlwZVN0cmluZyA9PT0gJ3VuZGVmaW5lZCcgfHwgdHlwZVN0cmluZyA9PT0gJ251bGwnKSB7XG4gICAgICAgICAgICBvdXRwdXQgPSBgJHtvYmp9YDtcbiAgICAgICAgfSBlbHNlIGlmKHR5cGVTdHJpbmcgPT09ICdhcnJheScpIHtcbiAgICAgICAgICAgIG91dHB1dCA9IHRoaXMuX3ByZXR0eUZvcm1hdEZsYXRJdGVyYWJsZShvYmosIG9iai5sZW5ndGgsIGluZGVudCwgaW5kZW50TGV2ZWwsICdbJywgJ10nKTtcbiAgICAgICAgfSBlbHNlIGlmKHR5cGVTdHJpbmcgPT09ICdzZXQnKSB7XG4gICAgICAgICAgICBvdXRwdXQgPSB0aGlzLl9wcmV0dHlGb3JtYXRGbGF0SXRlcmFibGUob2JqLCBvYmouc2l6ZSwgaW5kZW50LCBpbmRlbnRMZXZlbCwgJ1NldCgnLCAnKScpO1xuICAgICAgICB9IGVsc2UgaWYodHlwZVN0cmluZyA9PT0gJ21hcCcpIHtcbiAgICAgICAgICAgIG91dHB1dCA9IHRoaXMuX3ByZXR0eUZvcm1hdE1hcChvYmosIGluZGVudCwgaW5kZW50TGV2ZWwsICdNYXAoJywgJyknLCAnID0+ICcpO1xuICAgICAgICB9IGVsc2UgaWYodHlwZVN0cmluZyA9PT0gJ2Z1bmN0aW9uJykge1xuICAgICAgICAgICAgb3V0cHV0ID0gdGhpcy5fcHJldHR5Rm9ybWF0RnVuY3Rpb24ob2JqKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIG91dHB1dCA9IHRoaXMuX3ByZXR0eUZvcm1hdE1hcCh0aGlzLl9vYmplY3RUb01hcChvYmopLCBpbmRlbnQsIGluZGVudExldmVsLCAneycsICd9JywgJzogJyk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIG91dHB1dDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIHJlc3VsdHMgYXMgYSBzdHJpbmcsIG9wdGlvbmFsbHkgaW5kZW50ZWQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge251bWJlcn0gaW5kZW50IFRoZSBudW1iZXIgb2Ygc3BhY2VzIHRvIGluZGVudCBieS4gT25seVxuICAgICAqICAgIGNoaWxkIG9iamVjdHMgYXJlIGluZGVudGVkLCBhbmQgdGhleSBhcmUgaW5kZW50ZWQgcmVjdXJzaXZlbHkuXG4gICAgICogQHJldHVybnMge3N0cmluZ31cbiAgICAgKi9cbiAgICB0b1N0cmluZyhpbmRlbnQpIHtcbiAgICAgICAgaW5kZW50ID0gaW5kZW50IHx8IDA7XG4gICAgICAgIHJldHVybiB0aGlzLl9wcmV0dHlGb3JtYXQodGhpcy5fb2JqLCBpbmRlbnQsIDApO1xuICAgIH1cbn1cbiIsIi8qKlxuICogRGV0ZWN0IHRoZSB0eXBlIG9mIGFuIG9iamVjdCBhbmQgcmV0dXJuIHRoZVxuICogcmVzdWx0IGFzIGEgc3RyaW5nLlxuICpcbiAqIEhhbmRsZXMgdGhlIGZvbGxvd2luZyB0eXBlczpcbiAqXG4gKiAtIG51bGwgIChyZXR1cm5lZCBhcyBgYFwibnVsbFwiYGApLlxuICogLSB1bmRlZmluZWQgIChyZXR1cm5lZCBhcyBgYFwidW5kZWZpbmVkXCJgYCkuXG4gKiAtIE51bWJlciAgKHJldHVybmVkIGFzIGBgXCJudW1iZXJcImBgKS5cbiAqIC0gQm9vbGVhbiAgKHJldHVybmVkIGFzIGBgXCJib29sZWFuXCJgYCkuXG4gKiAtIFN0cmluZyAgKHJldHVybmVkIGFzIGBgXCJzdHJpbmdcImBgKS5cbiAqIC0gQXJyYXkgIChyZXR1cm5lZCBhcyBgYFwiYXJyYXlcImBgKS5cbiAqIC0gTWFwICAocmV0dXJuZWQgYXMgYGBcIm1hcFwiYGApLlxuICogLSBTZXQgIChyZXR1cm5lZCBhcyBgYFwic2V0XCJgYCkuXG4gKiAtIEZ1bmN0aW9uICAocmV0dXJuZWQgYXMgYGBcImZ1bmN0aW9uXCJgYCkuXG4gKiAtIE9iamVjdCAgKHJldHVybmVkIGFzIGBgXCJvYmplY3RcImBgKS5cbiAqXG4gKiBXZSBkbyBub3QgaGFuZGxlIGNsYXNzZXMgLSB0aGV5IGFyZSByZXR1cm5lZCBhcyBgYFwiZnVuY3Rpb25cImBgLlxuICogV2UgY291bGQgaGFuZGxlIGNsYXNzZXMsIGJ1dCBmb3IgQmFiZWwgY2xhc3NlcyB0aGF0IHdpbGwgcmVxdWlyZVxuICogYSBmYWlybHkgZXhwZW5zaXZlIGFuZCBlcnJvciBwcm9uZSByZWdleC5cbiAqXG4gKiBAcGFyYW0gb2JqIEFuIG9iamVjdCB0byBkZXRlY3QgdGhlIHR5cGUgZm9yLlxuICogQHJldHVybnMge3N0cmluZ31cbiAqL1xuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gdHlwZURldGVjdChvYmopIHtcbiAgICBpZihvYmogPT09IG51bGwpIHtcbiAgICAgICAgcmV0dXJuICdudWxsJztcbiAgICB9XG4gICAgY29uc3QgdHlwZU9mID0gdHlwZW9mIG9iajtcbiAgICBpZih0eXBlT2YgPT09ICd1bmRlZmluZWQnKSB7XG4gICAgICAgIHJldHVybiAndW5kZWZpbmVkJztcbiAgICB9XG4gICAgaWYodHlwZU9mID09PSAnbnVtYmVyJykge1xuICAgICAgICByZXR1cm4gJ251bWJlcic7XG4gICAgfVxuICAgIGlmKHR5cGVPZiA9PT0gJ2Jvb2xlYW4nKSB7XG4gICAgICAgIHJldHVybiAnYm9vbGVhbic7XG4gICAgfVxuICAgIGlmKHR5cGVPZiA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgcmV0dXJuICdzdHJpbmcnO1xuICAgIH1cbiAgICBpZih0eXBlT2YgPT09ICdmdW5jdGlvbicpIHtcbiAgICAgICAgcmV0dXJuICdmdW5jdGlvbic7XG4gICAgfVxuICAgIGlmKEFycmF5LmlzQXJyYXkob2JqKSkge1xuICAgICAgICByZXR1cm4gJ2FycmF5JztcbiAgICB9XG4gICAgaWYob2JqIGluc3RhbmNlb2YgTWFwKSB7XG4gICAgICAgIHJldHVybiAnbWFwJztcbiAgICB9XG4gICAgaWYob2JqIGluc3RhbmNlb2YgU2V0KSB7XG4gICAgICAgIHJldHVybiAnc2V0JztcbiAgICB9XG4gICAgcmV0dXJuICdvYmplY3QnO1xufVxuIiwiaW1wb3J0IG1ha2VDdXN0b21FcnJvciBmcm9tIFwiLi4vbWFrZUN1c3RvbUVycm9yXCI7XG5cbi8qKlxuICogVGhlIGluc3RhbmNlIG9mIHRoZSB7QGxpbmsgV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b259LlxuICovXG5sZXQgX2luc3RhbmNlID0gbnVsbDtcblxuXG4vKipcbiAqIEV4Y2VwdGlvbiB0aHJvd24gd2hlbiBhbiBlbGVtZW50IHdoZXJlIHdlIGV4cGVjdCB0aGVcbiAqIGBgZGF0YS1pZXZ2LWpzYmFzZS13aWRnZXQtaW5zdGFuY2VpZGBgIGF0dHJpYnV0ZSBkb2VzXG4gKiBub3QgaGF2ZSB0aGlzIGF0dHJpYnV0ZS5cbiAqXG4gKiBAdHlwZSB7RXJyb3J9XG4gKi9cbmV4cG9ydCBsZXQgRWxlbWVudEhhc05vV2lkZ2V0SW5zdGFuY2VJZEVycm9yID0gbWFrZUN1c3RvbUVycm9yKCdFbGVtZW50SGFzTm9XaWRnZXRJbnN0YW5jZUlkRXJyb3InKTtcblxuXG4vKipcbiAqIEV4Y2VwdGlvbiB0aHJvd24gd2hlbiBhbiBlbGVtZW50IHRoYXQgd2UgZXhwZWN0IHRvIGhhdmVcbiAqIHRoZSBgYGRhdGEtaWV2di1qc2Jhc2Utd2lkZ2V0YGAgYXR0cmlidXRlIGRvZXMgbm90IGhhdmVcbiAqIHRoaXMgYXR0cmlidXRlLlxuICpcbiAqIEB0eXBlIHtFcnJvcn1cbiAqL1xuZXhwb3J0IGxldCBFbGVtZW50SXNOb3RXaWRnZXRFcnJvciA9IG1ha2VDdXN0b21FcnJvcignRWxlbWVudElzTm90V2lkZ2V0RXJyb3InKTtcblxuXG4vKipcbiAqIEV4Y2VwdGlvbiB0aHJvd24gd2hlbiBhbiBlbGVtZW50IGhhcyBhXG4gKiBgYGRhdGEtaWV2di1qc2Jhc2Utd2lkZ2V0YGAgd2l0aCBhIHZhbHVlIHRoYXRcbiAqIGlzIG5vdCBhbiBhbGlhcyByZWdpc3RlcmVkIGluIHRoZSB7QGxpbmsgV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b259LlxuICpcbiAqIEB0eXBlIHtFcnJvcn1cbiAqL1xuZXhwb3J0IGxldCBJbnZhbGlkV2lkZ2V0QWxpYXNFcnJvciA9IG1ha2VDdXN0b21FcnJvcignSW52YWxpZFdpZGdldEFsaWFzRXJyb3InKTtcblxuXG4vKipcbiAqIEV4Y2VwdGlvbiB0aHJvd24gd2hlbiBhbiBlbGVtZW50IHdpdGggdGhlXG4gKiBgYGRhdGEtaWV2di1qc2Jhc2Utd2lkZ2V0LWluc3RhbmNlaWQ9PHdpZGdldEluc3RhbmNlSWQ+YGAgYXR0cmlidXRlIGlzIG5vdCBpblxuICogdGhlIHtAbGluayBXaWRnZXRSZWdpc3RyeVNpbmdsZXRvbn0gd2l0aCBgYDx3aWRnZXRJbnN0YW5jZUlkPmBgLlxuICpcbiAqIEB0eXBlIHtFcnJvcn1cbiAqL1xuZXhwb3J0IGxldCBFbGVtZW50SXNOb3RJbml0aWFsaXplZEFzV2lkZ2V0ID0gbWFrZUN1c3RvbUVycm9yKCdFbGVtZW50SXNOb3RJbml0aWFsaXplZEFzV2lkZ2V0Jyk7XG5cblxuLyoqXG4gKiBBIHZlcnkgbGlnaHR3ZWlnaHQgd2lkZ2V0IHN5c3RlbS5cbiAqXG4gKiBCYXNpYyBleGFtcGxlIGJlbG93IC0gc2VlIHtAbGluayBBYnN0cmFjdFdpZGdldH0gZm9yIG1vcmUgZXhhbXBsZXMuXG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+Q3JlYXRlIGEgdmVyeSBzaW1wbGUgd2lkZ2V0PC9jYXB0aW9uPlxuICogZXhwb3J0IGRlZmF1bHQgY2xhc3MgT3Blbk1lbnVXaWRnZXQgZXh0ZW5kcyBBYnN0cmFjdFdpZGdldCB7XG4gKiAgICAgY29uc3RydWN0b3IoZWxlbWVudCkge1xuICogICAgICAgICAgc3VwZXIoZWxlbWVudCk7XG4gKiAgICAgICAgICB0aGlzLl9vbkNsaWNrQm91bmQgPSAoLi4uYXJncykgPT4ge1xuICogICAgICAgICAgICAgIHRoaXMuX29uQ2xpY2soLi4uYXJncyk7XG4gKiAgICAgICAgICB9O1xuICogICAgICAgICAgdGhpcy5lbGVtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcy5fb25DbGlja0JvdW5kKTtcbiAqICAgICB9XG4gKlxuICogICAgIF9vbkNsaWNrID0gKGUpID0+IHtcbiAqICAgICAgICAgIGUucHJldmVudERlZmF1bHQoKTtcbiAqICAgICAgICAgIGNvbnNvbGUubG9nKCdJIHNob3VsZCBoYXZlIG9wZW5lZCB0aGUgbWVudSBoZXJlJyk7XG4gKiAgICAgfVxuICpcbiAqICAgICBkZXN0cm95KCkge1xuICogICAgICAgICAgdGhpcy5lbGVtZW50LnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcy5fb25DbGlja0JvdW5kKTtcbiAqICAgICB9XG4gKiB9XG4gKlxuICogQGV4YW1wbGUgPGNhcHRpb24+VXNlIHRoZSB3aWRnZXQ8L2NhcHRpb24+XG4gKiA8YnV0dG9uIGRhdGEtaWV2di1qc2Jhc2Utd2lkZ2V0PVwib3Blbi1tZW51LWJ1dHRvblwiIHR5cGU9XCJidXR0b25cIj5cbiAqICAgICBPcGVuIG1lbnVcbiAqIDwvYnV0dG9uPlxuICpcbiAqIEBleGFtcGxlIDxjYXB0aW9uPlJlZ2lzdGVyIGFuZCBsb2FkIHdpZGdldHM8L2NhcHRpb24+XG4gKiAvLyBTb21ld2hlcmUgdGhhdCBpcyBjYWxsZWQgYWZ0ZXIgYWxsIHRoZSB3aWRnZXRzIGFyZSByZW5kZXJlZFxuICogLy8gLSB0eXBpY2FsbHkgYXQgdGhlIGVuZCBvZiB0aGUgPGJvZHk+XG4gKiBpbXBvcnQgV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24gZnJvbSAnaWV2dl9qc2Jhc2Uvd2lkZ2V0L1dpZGdldFJlZ2lzdHJ5U2luZ2xldG9uJztcbiAqIGltcG9ydCBPcGVuTWVudVdpZGdldCBmcm9tICdwYXRoL3RvL09wZW5NZW51V2lkZ2V0JztcbiAqIGNvbnN0IHdpZGdldFJlZ2lzdHJ5ID0gbmV3IFdpZGdldFJlZ2lzdHJ5U2luZ2xldG9uKCk7XG4gKiB3aWRnZXRSZWdpc3RyeS5yZWdpc3RlcldpZGdldENsYXNzKCdvcGVuLW1lbnUtYnV0dG9uJywgT3Blbk1lbnVXaWRnZXQpO1xuICogd2lkZ2V0UmVnaXN0cnkuaW5pdGlhbGl6ZUFsbFdpZGdldHNXaXRoaW5FbGVtZW50KGRvY3VtZW50LmJvZHkpO1xuICpcbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24ge1xuICAgIGNvbnN0cnVjdG9yKCkge1xuICAgICAgICBpZiAoIV9pbnN0YW5jZSkge1xuICAgICAgICAgICAgX2luc3RhbmNlID0gdGhpcztcbiAgICAgICAgICAgIHRoaXMuX2luaXRpYWxpemUoKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gX2luc3RhbmNlO1xuICAgIH1cblxuICAgIF9pbml0aWFsaXplKCkge1xuICAgICAgICB0aGlzLl93aWRnZXRBdHRyaWJ1dGUgPSAnZGF0YS1pZXZ2LWpzYmFzZS13aWRnZXQnO1xuICAgICAgICB0aGlzLl93aWRnZXRJbnN0YW5jZUlkQXR0cmlidXRlID0gJ2RhdGEtaWV2di1qc2Jhc2Utd2lkZ2V0LWluc3RhbmNlaWQnO1xuICAgICAgICB0aGlzLl93aWRnZXRDbGFzc01hcCA9IG5ldyBNYXAoKTtcbiAgICAgICAgdGhpcy5fd2lkZ2V0SW5zdGFuY2VNYXAgPSBuZXcgTWFwKCk7XG4gICAgICAgIHRoaXMuX3dpZGdldEluc3RhbmNlQ291bnRlciA9IDA7XG4gICAgfVxuXG4gICAgY2xlYXIoKSB7XG4gICAgICAgIC8vIFRPRE86IENhbGwgZGVzdHJveUFsbFdpZGdldHNXaXRoaW5Eb2N1bWVudEJvZHkoKVxuICAgICAgICB0aGlzLl93aWRnZXRDbGFzc01hcC5jbGVhcigpO1xuICAgICAgICB0aGlzLl93aWRnZXRJbnN0YW5jZU1hcC5jbGVhcigpO1xuICAgICAgICB0aGlzLl93aWRnZXRJbnN0YW5jZUNvdW50ZXIgPSAwO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlZ2lzdGVyIGEgd2lkZ2V0IGNsYXNzIGluIHRoZSByZWdpc3RyeS5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfSBhbGlhcyBUaGUgYWxpYXMgZm9yIHRoZSB3aWRnZXQuIFRoaXMgaXMgdGhlIHN0cmluZyB0aGF0XG4gICAgICogICAgICBpcyB1c2VkIGFzIHRoZSBhdHRyaWJ1dGUgdmFsdWUgd2l0aCB0aGUgYGBkYXRhLWlldnYtanNiYXNlLXdpZGdldGBgXG4gICAgICogICAgICBET00gZWxlbWVudCBhdHRyaWJ1dGUuXG4gICAgICogQHBhcmFtIHtBYnN0cmFjdFdpZGdldH0gV2lkZ2V0Q2xhc3MgVGhlIHdpZGdldCBjbGFzcy5cbiAgICAgKi9cbiAgICByZWdpc3RlcldpZGdldENsYXNzKGFsaWFzLCBXaWRnZXRDbGFzcykge1xuICAgICAgICB0aGlzLl93aWRnZXRDbGFzc01hcC5zZXQoYWxpYXMsIFdpZGdldENsYXNzKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW1vdmUgd2lkZ2V0IGNsYXNzIGZyb20gcmVnaXN0cnkuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gYWxpYXMgVGhlIGFsaWFzIHRoYXQgdGhlIHdpZGdldCBjbGFzcyB3YXMgcmVnaXN0ZXJlZCB3aXRoXG4gICAgICogICAgICBieSB1c2luZyB7QGxpbmsgV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24jcmVnaXN0ZXJXaWRnZXRDbGFzc30uXG4gICAgICovXG4gICAgcmVtb3ZlV2lkZ2V0Q2xhc3MoYWxpYXMpIHtcbiAgICAgICAgdGhpcy5fd2lkZ2V0Q2xhc3NNYXAuZGVsZXRlKGFsaWFzKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBJbml0aWFsaXplIHRoZSBwcm92aWRlZCBlbGVtZW50IGFzIGEgd2lkZ2V0LlxuICAgICAqXG4gICAgICogQHBhcmFtIHtFbGVtZW50fSBlbGVtZW50IFRoZSBET00gZWxlbWVudCB0byBpbml0YWxpemUgYXMgYSB3aWRnZXQuXG4gICAgICpcbiAgICAgKiBAdGhyb3dzIHtFbGVtZW50SXNOb3RXaWRnZXRFcnJvcn0gSWYgdGhlIGVsZW1lbnQgZG9lcyBub3QgaGF2ZVxuICAgICAqICAgICAgdGhlIGBgZGF0YS1pZXZ2LWpzYmFzZS13aWRnZXRgYCBhdHRyaWJ1dGUuXG4gICAgICogQHRocm93cyB7SW52YWxpZFdpZGdldEFsaWFzRXJyb3J9IElmIHRoZSB3aWRnZXQgYWxpYXMgaXMgbm90IGluIHRoaXMgcmVnaXN0cnkuXG4gICAgICovXG4gICAgaW5pdGlhbGl6ZVdpZGdldChlbGVtZW50KSB7XG4gICAgICAgIGxldCBhbGlhcyA9IGVsZW1lbnQuZ2V0QXR0cmlidXRlKHRoaXMuX3dpZGdldEF0dHJpYnV0ZSk7XG4gICAgICAgIGlmKCFhbGlhcykge1xuICAgICAgICAgICAgdGhyb3cgbmV3IEVsZW1lbnRJc05vdFdpZGdldEVycm9yKFxuICAgICAgICAgICAgICAgIGBUaGVcXG5cXG4ke2VsZW1lbnQub3V0ZXJIVE1MfVxcblxcbmVsZW1lbnQgaGFzIG5vIG9yIGVtcHR5YCArXG4gICAgICAgICAgICAgICAgYCR7dGhpcy5fd2lkZ2V0QXR0cmlidXRlfSBhdHRyaWJ1dGUuYCk7XG4gICAgICAgIH1cbiAgICAgICAgaWYoIXRoaXMuX3dpZGdldENsYXNzTWFwLmhhcyhhbGlhcykpIHtcbiAgICAgICAgICAgIHRocm93IG5ldyBJbnZhbGlkV2lkZ2V0QWxpYXNFcnJvcihgTm8gV2lkZ2V0Q2xhc3MgcmVnaXN0ZXJlZCB3aXRoIHRoZSBcIiR7YWxpYXN9XCIgYWxpYXMuYCk7XG4gICAgICAgIH1cbiAgICAgICAgbGV0IFdpZGdldENsYXNzID0gdGhpcy5fd2lkZ2V0Q2xhc3NNYXAuZ2V0KGFsaWFzKTtcbiAgICAgICAgbGV0IHdpZGdldCA9IG5ldyBXaWRnZXRDbGFzcyhlbGVtZW50KTtcbiAgICAgICAgdGhpcy5fd2lkZ2V0SW5zdGFuY2VDb3VudGVyICsrO1xuICAgICAgICBsZXQgd2lkZ2V0SW5zdGFuY2VJZCA9IHRoaXMuX3dpZGdldEluc3RhbmNlQ291bnRlci50b1N0cmluZygpO1xuICAgICAgICB0aGlzLl93aWRnZXRJbnN0YW5jZU1hcC5zZXQod2lkZ2V0SW5zdGFuY2VJZCwgd2lkZ2V0KTtcbiAgICAgICAgZWxlbWVudC5zZXRBdHRyaWJ1dGUodGhpcy5fd2lkZ2V0SW5zdGFuY2VJZEF0dHJpYnV0ZSwgd2lkZ2V0SW5zdGFuY2VJZCk7XG4gICAgICAgIHJldHVybiB3aWRnZXQ7XG4gICAgfVxuXG4gICAgX2dldEFsbFdpZGdldEVsZW1lbnRzV2l0aGluRWxlbWVudChlbGVtZW50KSB7XG4gICAgICAgIHJldHVybiBlbGVtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoYFske3RoaXMuX3dpZGdldEF0dHJpYnV0ZX1dYCk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogSW5pdGlhbGl6ZSBhbGwgd2lkZ2V0cyB3aXRoaW4gdGhlIHByb3ZpZGVkIGVsZW1lbnQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge0VsZW1lbnR9IGVsZW1lbnQgQSBET00gZWxlbWVudC5cbiAgICAgKi9cbiAgICBpbml0aWFsaXplQWxsV2lkZ2V0c1dpdGhpbkVsZW1lbnQoZWxlbWVudCkge1xuICAgICAgICBmb3IobGV0IHdpZGdldEVsZW1lbnQgb2YgdGhpcy5fZ2V0QWxsV2lkZ2V0RWxlbWVudHNXaXRoaW5FbGVtZW50KGVsZW1lbnQpKSB7XG4gICAgICAgICAgICB0aGlzLmluaXRpYWxpemVXaWRnZXQod2lkZ2V0RWxlbWVudCk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIHZhbHVlIG9mIHRoZSBgYGRhdGEtaWV2di1qc2Jhc2Utd2lkZ2V0LWluc3RhbmNlaWRgYCBhdHRyaWJ1dGVcbiAgICAgKiBvZiB0aGUgcHJvdmlkZWQgZWxlbWVudC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7RWxlbWVudH0gZWxlbWVudCBBIERPTSBlbGVtZW50LlxuICAgICAqIEByZXR1cm5zIHtudWxsfHN0cmluZ31cbiAgICAgKi9cbiAgICBnZXRXaWRnZXRJbnN0YW5jZUlkRnJvbUVsZW1lbnQoZWxlbWVudCkge1xuICAgICAgICByZXR1cm4gZWxlbWVudC5nZXRBdHRyaWJ1dGUodGhpcy5fd2lkZ2V0SW5zdGFuY2VJZEF0dHJpYnV0ZSk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IGEgd2lkZ2V0IGluc3RhbmNlIGJ5IGl0cyB3aWRnZXQgaW5zdGFuY2UgaWQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gd2lkZ2V0SW5zdGFuY2VJZCBBIHdpZGdldCBpbnN0YW5jZSBpZC5cbiAgICAgKiBAcmV0dXJucyB7QWJzdHJhY3RXaWRnZXR9IEEgd2lkZ2V0IGluc3RhbmNlIG9yIGBgbnVsbGBgLlxuICAgICAqL1xuICAgIGdldFdpZGdldEluc3RhbmNlQnlJbnN0YW5jZUlkKHdpZGdldEluc3RhbmNlSWQpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuX3dpZGdldEluc3RhbmNlTWFwLmdldCh3aWRnZXRJbnN0YW5jZUlkKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBEZXN0cm95IHRoZSB3aWRnZXQgb24gdGhlIHByb3ZpZGVkIGVsZW1lbnQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge0VsZW1lbnR9IGVsZW1lbnQgQSBET00gZWxlbWVudCB0aGF0IGhhcyBiZWVuIGluaXRpYWxpemVkIGJ5XG4gICAgICogICAgICB7QGxpbmsgV2lkZ2V0UmVnaXN0cnlTaW5nbGV0b24jaW5pdGlhbGl6ZVdpZGdldH0uXG4gICAgICpcbiAgICAgKiBAdGhyb3dzIHtFbGVtZW50SGFzTm9XaWRnZXRJbnN0YW5jZUlkRXJyb3J9IElmIHRoZSBlbGVtZW50IGhhc1xuICAgICAqICAgICAgbm8gYGBkYXRhLWlldnYtanNiYXNlLXdpZGdldC1pbnN0YW5jZWlkYGAgYXR0cmlidXRlIG9yIHRoZVxuICAgICAqICAgICAgYXR0cmlidXRlIHZhbHVlIGlzIGVtcHR5LiBUaGlzIG5vcm1hbGx5IG1lYW5zIHRoYXRcbiAgICAgKiAgICAgIHRoZSBlbGVtZW50IGlzIG5vdCBhIHdpZGdldCwgb3IgdGhhdCB0aGUgd2lkZ2V0XG4gICAgICogICAgICBpcyBub3QgaW5pdGlhbGl6ZWQuXG4gICAgICogQHRocm93cyB7RWxlbWVudElzTm90SW5pdGlhbGl6ZWRBc1dpZGdldH0gSWYgdGhlIGVsZW1lbnRcbiAgICAgKiAgICAgIGhhcyB0aGUgYGBkYXRhLWlldnYtanNiYXNlLXdpZGdldC1pbnN0YW5jZWlkYGAgYXR0cmlidXRlXG4gICAgICogICAgICBidXQgdGhlIHZhbHVlIG9mIHRoZSBhdHRyaWJ1dGUgaXMgbm90IGEgdmFsaWQgd2lkZ2V0IGluc3RhbmNlXG4gICAgICogICAgICBpZC4gVGhpcyBzaG91bGQgbm90IGhhcHBlbiB1bmxlc3MgeW91IG1hbmlwdWxhdGUgdGhlXG4gICAgICogICAgICBhdHRyaWJ1dGUgbWFudWFsbHkgb3IgdXNlIHRoZSBwcml2YXRlIG1lbWJlcnMgb2YgdGhpcyByZWdpc3RyeS5cbiAgICAgKi9cbiAgICBkZXN0cm95V2lkZ2V0KGVsZW1lbnQpIHtcbiAgICAgICAgbGV0IHdpZGdldEluc3RhbmNlSWQgPSB0aGlzLmdldFdpZGdldEluc3RhbmNlSWRGcm9tRWxlbWVudChlbGVtZW50KTtcbiAgICAgICAgaWYod2lkZ2V0SW5zdGFuY2VJZCkge1xuICAgICAgICAgICAgbGV0IHdpZGdldEluc3RhbmNlID0gdGhpcy5nZXRXaWRnZXRJbnN0YW5jZUJ5SW5zdGFuY2VJZCh3aWRnZXRJbnN0YW5jZUlkKTtcbiAgICAgICAgICAgIGlmKHdpZGdldEluc3RhbmNlKSB7XG4gICAgICAgICAgICAgICAgd2lkZ2V0SW5zdGFuY2UuZGVzdHJveSgpO1xuICAgICAgICAgICAgICAgIHRoaXMuX3dpZGdldEluc3RhbmNlTWFwLmRlbGV0ZSh3aWRnZXRJbnN0YW5jZUlkKTtcbiAgICAgICAgICAgICAgICBlbGVtZW50LnJlbW92ZUF0dHJpYnV0ZSh0aGlzLl93aWRnZXRJbnN0YW5jZUlkQXR0cmlidXRlKTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgdGhyb3cgbmV3IEVsZW1lbnRJc05vdEluaXRpYWxpemVkQXNXaWRnZXQoXG4gICAgICAgICAgICAgICAgICAgIGBFbGVtZW50XFxuXFxuJHtlbGVtZW50Lm91dGVySFRNTH1cXG5cXG5oYXMgdGhlIGAgK1xuICAgICAgICAgICAgICAgICAgICBgJHt0aGlzLl93aWRnZXRJbnN0YW5jZUlkQXR0cmlidXRlfSBhdHRyaWJ1dGUsIGJ1dCB0aGUgaWQgaXMgYCArXG4gICAgICAgICAgICAgICAgICAgIGBub3QgaW4gdGhlIHdpZGdldCByZWdpc3RyeS5gKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aHJvdyBuZXcgRWxlbWVudEhhc05vV2lkZ2V0SW5zdGFuY2VJZEVycm9yKFxuICAgICAgICAgICAgICAgIGBFbGVtZW50XFxuXFxuJHtlbGVtZW50Lm91dGVySFRNTH1cXG5cXG5oYXMgbm8gb3IgZW1wdHkgYCArXG4gICAgICAgICAgICAgICAgYCR7dGhpcy5fd2lkZ2V0SW5zdGFuY2VJZEF0dHJpYnV0ZX0gYXR0cmlidXRlLmApO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgX2dldEFsbEluc3RhbmNpYXRlZFdpZGdldEVsZW1lbnRzV2l0aGluRWxlbWVudChlbGVtZW50KSB7XG4gICAgICAgIHJldHVybiBlbGVtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoYFske3RoaXMuX3dpZGdldEluc3RhbmNlSWRBdHRyaWJ1dGV9XWApO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIERlc3Ryb3kgYWxsIHdpZGdldHMgd2l0aGluIHRoZSBwcm92aWRlZCBlbGVtZW50LlxuICAgICAqIE9ubHkgZGVzdHJveXMgd2lkZ2V0cyBvbiBlbGVtZW50cyB0aGF0IGlzIGEgY2hpbGQgb2YgdGhlIGVsZW1lbnQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge0VsZW1lbnR9IGVsZW1lbnQgVGhlIERPTSBFbGVtZW50LlxuICAgICAqL1xuICAgIGRlc3Ryb3lBbGxXaWRnZXRzV2l0aGluRWxlbWVudChlbGVtZW50KSB7XG4gICAgICAgIGZvcihsZXQgd2lkZ2V0RWxlbWVudCBvZiB0aGlzLl9nZXRBbGxJbnN0YW5jaWF0ZWRXaWRnZXRFbGVtZW50c1dpdGhpbkVsZW1lbnQoZWxlbWVudCkpIHtcbiAgICAgICAgICAgIHRoaXMuZGVzdHJveVdpZGdldCh3aWRnZXRFbGVtZW50KTtcbiAgICAgICAgfVxuICAgIH1cbn1cbiJdfQ==
