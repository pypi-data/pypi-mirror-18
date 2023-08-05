(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol ? "symbol" : typeof obj; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var WebSocket = void 0;
if (typeof WebSocket === 'undefined') {
  WebSocket = require('websocket').w3cwebsocket; // eslint-disable-line
}

/**
 * Connection to the backend.
 *
 * The standard template is to create a connection first, then use it to
 * wire all UI elements, to add custom callback functions and at last to run
 * {@link Connection#connect|connect()} to create a WebSocket connection to the backend
 * server (see example below).
 *
 * The other two essential functions to know about are
 * {@link Connection#on|on()} and {@link Connection#emit|emit()}.
 *
 * @example
 * var d = new Databench.Connection();
 * Databench.ui.wire(d);
 * // put custom d.on() methods here
 * d.connect();
 */

var Connection = function () {
  /**
   * @param  {String} [analysisId=null]  Specify an analysis id or null to have one generated.
   *                                     The connection will try to connect to a previously created
   *                                     analysis with that id.
   * @param  {String} [wsUrl=null]       URL of WebSocket endpoint or null to guess it.
   * @param  {String} [requestArgs=null] `search` part of request url or null to take from
   *                                     `window.location.search`.
   */

  function Connection() {
    var analysisId = arguments.length <= 0 || arguments[0] === undefined ? null : arguments[0];
    var wsUrl = arguments.length <= 1 || arguments[1] === undefined ? null : arguments[1];
    var requestArgs = arguments.length <= 2 || arguments[2] === undefined ? null : arguments[2];

    _classCallCheck(this, Connection);

    this.analysisId = analysisId;
    this.wsUrl = wsUrl || Connection.guessWSUrl();
    this.requestArgs = requestArgs == null && typeof window !== 'undefined' ? window.location.search : requestArgs;

    if (!this.wsUrl) {
      throw Error('Need a wsUrl.');
    }

    this.errorCB = function (msg) {
      return msg != null ? console.log('connection error: ' + msg) : null;
    };
    this.onCallbacks = [];
    this._onCallbacksOptimized = null;
    this.onProcessCallbacks = {};

    this.wsReconnectAttempt = 0;
    this.wsReconnectDelay = 100.0;

    this.socket = null;
    this.socketCheckOpen = null;
  }

  _createClass(Connection, [{
    key: 'connect',


    /** initialize connection */
    value: function connect() {
      this.socket = new WebSocket(this.wsUrl);

      this.socketCheckOpen = setInterval(this.wsCheckOpen.bind(this), 2000);
      this.socket.onopen = this.wsOnOpen.bind(this);
      this.socket.onclose = this.wsOnClose.bind(this);
      this.socket.onmessage = this.wsOnMessage.bind(this);
      return this;
    }

    /** close connection */

  }, {
    key: 'disconnect',
    value: function disconnect() {
      this.socket.onclose = null;
      this.socket.close();
      this.socket = null;
    }
  }, {
    key: 'wsCheckOpen',
    value: function wsCheckOpen() {
      if (this.socket.readyState === this.socket.CONNECTING) {
        return;
      }
      if (this.socket.readyState !== this.socket.OPEN) {
        this.errorCB('Connection could not be opened. ' + 'Please <a href="javascript:location.reload(true);" ' + 'class="alert-link">reload</a> this page to try again.');
      }
      clearInterval(this.socketCheckOpen);
    }
  }, {
    key: 'wsOnOpen',
    value: function wsOnOpen() {
      this.wsReconnectAttempt = 0;
      this.wsReconnectDelay = 100.0;
      this.errorCB(); // clear errors
      this.socket.send(JSON.stringify({
        __connect: this.analysisId,
        __request_args: this.requestArgs }));
    }
  }, {
    key: 'wsOnClose',
    // eslint-disable-line camelcase
    value: function wsOnClose() {
      clearInterval(this.socketCheckOpen);

      this.wsReconnectAttempt += 1;
      this.wsReconnectDelay *= 2;

      if (this.wsReconnectAttempt > 3) {
        this.errorCB('Connection closed. ' + 'Please <a href="javascript:location.reload(true);" ' + 'class="alert-link">reload</a> this page to reconnect.');
        return;
      }

      var actualDelay = 0.7 * this.wsReconnectDelay + 0.3 * Math.random() * this.wsReconnectDelay;
      console.log('WebSocket reconnect attempt ' + this.wsReconnectAttempt + ' ' + ('in ' + actualDelay.toFixed(0) + 'ms.'));
      setTimeout(this.connect.bind(this), actualDelay);
    }
  }, {
    key: 'wsOnMessage',
    value: function wsOnMessage(event) {
      var _this = this;

      var message = JSON.parse(event.data);

      // connect response
      if (message.signal === '__connect') {
        this.analysisId = message.load.analysis_id;
      }

      // processes
      if (message.signal === '__process') {
        (function () {
          var id = message.load.id;
          var status = message.load.status;
          _this.onProcessCallbacks[id].map(function (cb) {
            return cb(status);
          });
        })();
      }

      // normal message
      if (this._onCallbacksOptimized === null) this.optimizeOnCallbacks();
      if (message.signal in this._onCallbacksOptimized) {
        this._onCallbacksOptimized[message.signal].map(function (cb) {
          return cb(message.load);
        });
      }
    }
  }, {
    key: 'optimizeOnCallbacks',
    value: function optimizeOnCallbacks() {
      var _this2 = this;

      this._onCallbacksOptimized = {};
      this.onCallbacks.forEach(function (_ref) {
        var signal = _ref.signal;
        var callback = _ref.callback;

        if (typeof signal === 'string') {
          if (!(signal in _this2._onCallbacksOptimized)) {
            _this2._onCallbacksOptimized[signal] = [];
          }
          _this2._onCallbacksOptimized[signal].push(callback);
        } else if ((typeof signal === 'undefined' ? 'undefined' : _typeof(signal)) === 'object') {
          Object.keys(signal).forEach(function (signalName) {
            var entryName = signal[signalName];
            var filteredCallback = function filteredCallback(data) {
              if (data.hasOwnProperty(entryName)) {
                callback(data[entryName]);
              }
            };

            if (!(signalName in _this2._onCallbacksOptimized)) {
              _this2._onCallbacksOptimized[signalName] = [];
            }

            // only use the filtered callback if the entry was not empty
            if (entryName) {
              _this2._onCallbacksOptimized[signalName].push(filteredCallback);
            } else {
              _this2._onCallbacksOptimized[signalName].push(callback);
            }
          });
        }
      });
    }

    /**
     * Register a callback that listens for a signal.
     *
     * The signal can be a simple string (the name for a signal/action), but it
     * can also be an Object of the form `{data: 'current_value'}` which would
     * trigger on `data` actions that are sending a JSON dictionary that contains
     * the key `current_value`. In this case, the value that is
     * given to the callback function is the value assigned to `current_value`.
     *
     * @example
     * d.on('data', value => { console.log(value); });
     * // If the backend sends an action called 'data' with a message
     * // {current_value: 3.0}, this function would log `{current_value: 3.0}`.
     *
     * @example
     * d.on({data: 'current_value'}, value => { console.log(value); });
     * // If the backend sends an action called 'data' with a
     * // message {current_value: 3.0}, this function would log `3.0`.
     * // This callback is not triggered when the message does not contain a
     * // `current_value` key.
     *
     * @param  {string|Object}   signal   Signal name to listen for.
     * @param  {Function}        callback A callback function that takes the attached data.
     * @return {Connection}      this
     */

  }, {
    key: 'on',
    value: function on(signal, callback) {
      this.onCallbacks.push({ signal: signal, callback: callback });
      this._onCallbacksOptimized = null;
      return this;
    }

    /**
     * Emit a signal/action to the backend.
     * @param  {string}                   signalName A signal name. Usually an action name.
     * @param  {string|Object|Array|null} message    Payload attached to the action.
     * @return {Connection}                          this
     */

  }, {
    key: 'emit',
    value: function emit(signalName, message) {
      var _this3 = this;

      if (this.socket == null || this.socket.readyState !== this.socket.OPEN) {
        setTimeout(function () {
          return _this3.emit(signalName, message);
        }, 5);
        return this;
      }
      this.socket.send(JSON.stringify({ signal: signalName, load: message }));
      return this;
    }
  }, {
    key: 'onProcess',
    value: function onProcess(processID, callback) {
      if (!(processID in this.onProcessCallbacks)) {
        this.onProcessCallbacks[processID] = [];
      }
      this.onProcessCallbacks[processID].push(callback);
      return this;
    }
  }], [{
    key: 'guessWSUrl',
    value: function guessWSUrl() {
      if (typeof location === 'undefined') return null;
      var WSProtocol = location.origin.startsWith('https://') ? 'wss' : 'ws';
      var path = location.pathname.substring(0, location.pathname.lastIndexOf('/'));
      return WSProtocol + '://' + document.domain + ':' + location.port + path + '/ws';
    }
  }]);

  return Connection;
}();

exports.Connection = Connection;

},{"websocket":4}],2:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.Connection = exports.ui = undefined;

var _ui = require('./ui');

var ui = _interopRequireWildcard(_ui);

var _connection = require('./connection');

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

// create a public interface
/**
 * Databench
 */

if (typeof window !== 'undefined') {
  window.Databench = { ui: ui, Connection: _connection.Connection };
}
exports.ui = ui;
exports.Connection = _connection.Connection;

},{"./connection":1,"./ui":3}],3:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * This is a basic set of UI elements to create analyses without having to add
 * frontend frameworks like Angular or React.
 *
 * @module ui
 */

/**
 * Abstract class for user interface elements which provides general helpers
 * to determine the action name from an HTML tag and a way to modify the message
 * that is sent with actions of wired elements.
 *
 * The constructor adds the variables `actionName` and `wireSignal` using
 * {@link module:ui~UIElement.determineActionName|determineActionName()} and
 * {@link module:ui~UIElement.determineWireSignal|determineWireSignal()}
 * respectively.
 * It also adds `this` UI element to the DOM node at `databenchUI`.
 */

var UIElement = function () {
  /**
   * @param  {HTMLElement} node An HTML element.
   */

  function UIElement(node) {
    _classCallCheck(this, UIElement);

    this.node = node;
    this.node.databenchUI = this;

    this.actionName = UIElement.determineActionName(node);
    this.wireSignal = UIElement.determineWireSignal(node);
  }

  /**
   * Formats the payload of an action.
   * @param  {any} value Original payload.
   * @return {any}       Modified payload.
   */


  _createClass(UIElement, [{
    key: 'actionFormat',
    value: function actionFormat(value) {
      return value;
    }

    /**
     * Determine the name of the action that should be associated with the node.
     *
     * This can be forced to be `null` by adding a `data-skipwire=true` attribute
     * to the HTML tag. If that is not found, the action name is determined from
     * the tag's `data-action`, `name` or `id` attribute (in that order).
     *
     * @param  {HTMLElement} node A HTML element.
     * @return {string}      Name of action or null.
     */

  }], [{
    key: 'determineActionName',
    value: function determineActionName(node) {
      // determine action name from HTML DOM
      var action = null;

      if (node.dataset.skipwire === 'true' || node.dataset.skipwire === 'TRUE' || node.dataset.skipwire === '1') {
        return null;
      }

      if (node.dataset.action) {
        action = node.dataset.action;
      } else if (node.getAttribute('name')) {
        action = node.getAttribute('name');
      } else if (node.getAttribute('id')) {
        action = node.getAttribute('id');
      }

      return action;
    }

    /**
     * Determine the name of the signal that should be listened to from the backend.
     *
     * If the HTML tag as a `data-skipwire=true` attribute, this is forced to be
     * null. Otherwise the signal name is determined from the `data-signal`,
     * `data-action`, `name` or `id` attribute (in that order.)
     * For all attributes apart from `data-signal`, the value is wrapped in an
     * object like `{ data: value-of-attribute }`. The `data-signal` value
     * can contain a `:` which will be used to create an object as well. That means
     * that `data-signal="data:myvalue"` gives the same result as `data-action="myvalue"`.
     *
     * @param  {HTMLElement} node A HTML element.
     * @return {string}           Name of a signal or null.
     */

  }, {
    key: 'determineWireSignal',
    value: function determineWireSignal(node) {
      // determine signal name from HTML DOM
      var signal = null;

      if (node.dataset.skipwire === 'true' || node.dataset.skipwire === 'TRUE' || node.dataset.skipwire === '1') {
        return null;
      }

      if (node.dataset.signal) {
        signal = node.dataset.signal;
        if (signal.indexOf(':') >= 1) {
          var _signal$split = signal.split(':', 2);

          var _signal$split2 = _slicedToArray(_signal$split, 2);

          var key = _signal$split2[0];
          var value = _signal$split2[1];

          signal = _defineProperty({}, key, value);
        }
      } else if (node.dataset.action) {
        signal = { data: node.dataset.action };
      } else if (node.getAttribute('name')) {
        signal = { data: node.getAttribute('name') };
      } else if (node.getAttribute('id')) {
        signal = { data: node.getAttribute('id') };
      }

      return signal;
    }
  }]);

  return UIElement;
}();

/**
 * Shows all `console.log()` messages and `log` actions from backend.
 *
 * Usually wired to a `<pre id="log">` element.
 */


var Log = function (_UIElement) {
  _inherits(Log, _UIElement);

  /**
   * @param  {HTMLElement} node     Primary node.
   * @param  {String} [consoleFnName='log'] Name of console method to replace.
   * @param  {Number} [limitNumber=20]      Maximum number of messages to show.
   * @param  {Number} [limitLength=250]     Maximum length of a message.
   */

  function Log(node) {
    var consoleFnName = arguments.length <= 1 || arguments[1] === undefined ? 'log' : arguments[1];
    var limitNumber = arguments.length <= 2 || arguments[2] === undefined ? 20 : arguments[2];
    var limitLength = arguments.length <= 3 || arguments[3] === undefined ? 250 : arguments[3];

    _classCallCheck(this, Log);

    var _this = _possibleConstructorReturn(this, Object.getPrototypeOf(Log).call(this, node));

    _this.consoleFnName = consoleFnName;
    _this.limitNumber = limitNumber;
    _this.limitLength = limitLength;
    _this._messages = [];

    // more sensible default for this case
    _this.wireSignal = { log: null };

    // capture events from frontend
    var _consoleFnOriginal = console[consoleFnName];
    console[consoleFnName] = function (message) {
      _this.add(message, 'frontend');
      _consoleFnOriginal.apply(console, [message]);
    };
    return _this;
  }

  _createClass(Log, [{
    key: 'render',
    value: function render() {
      var _this2 = this;

      while (this._messages.length > this.limitNumber) {
        this._messages.shift();
      }this.node.innerText = this._messages.map(function (m) {
        return m.join('');
      }).map(function (m) {
        return m.length > _this2.limitLength ? m.substr(0, _this2.limitLength) + ' ...' : m;
      }).join('\n');

      return this;
    }
  }, {
    key: 'add',
    value: function add(message) {
      var source = arguments.length <= 1 || arguments[1] === undefined ? 'unknown' : arguments[1];

      var msg = typeof message === 'string' ? message : JSON.stringify(message);
      var paddedSource = ' '.repeat(Math.max(0, 8 - source.length)) + source;
      this._messages.push([paddedSource + ': ' + msg]);
      this.render();
      return this;
    }

    /** Wire all logs. */

  }], [{
    key: 'wire',
    value: function wire(conn) {
      var id = arguments.length <= 1 || arguments[1] === undefined ? 'log' : arguments[1];
      var source = arguments.length <= 2 || arguments[2] === undefined ? 'backend' : arguments[2];
      var consoleFnName = arguments.length <= 3 || arguments[3] === undefined ? 'log' : arguments[3];
      var limitNumber = arguments.length <= 4 || arguments[4] === undefined ? 20 : arguments[4];
      var limitLength = arguments.length <= 5 || arguments[5] === undefined ? 250 : arguments[5];

      var node = document.getElementById(id);
      if (node == null) return;
      if (UIElement.determineActionName(node) == null) return;

      console.log('Wiring log to ', node, 'with id=' + id + '.');
      var l = new Log(node, consoleFnName, limitNumber, limitLength);
      conn.on(l.wireSignal, function (message) {
        return l.add(message, source);
      });
      return;
    }
  }]);

  return Log;
}(UIElement);

/**
 * Visual representation of alerts like connection failures.
 *
 * Usually wired to a `<div id="ws-alerts">` element.
 */


var StatusLog = function (_UIElement2) {
  _inherits(StatusLog, _UIElement2);

  /**
   * @param  {HTMLElement} node      HTML node.
   * @param  {function}    formatter Formats a message and a count to a string.
   */

  function StatusLog(node) {
    var formatter = arguments.length <= 1 || arguments[1] === undefined ? StatusLog.defaultAlert : arguments[1];

    _classCallCheck(this, StatusLog);

    var _this3 = _possibleConstructorReturn(this, Object.getPrototypeOf(StatusLog).call(this, node));

    _this3.formatter = formatter;
    _this3._messages = new Map();

    // to avoid confusion, void meaningless parent variable
    _this3.wireSignal = null;
    return _this3;
  }

  /**
   * The default formatter function
   * @param  {string} msg   A message.
   * @param  {number} count Count of the message.
   * @return {string}       HTML formatted version of the inputs.
   */


  _createClass(StatusLog, [{
    key: 'render',
    value: function render() {
      var _this4 = this;

      var formatted = [].concat(_toConsumableArray(this._messages)).map(function (_ref) {
        var _ref2 = _slicedToArray(_ref, 2);

        var m = _ref2[0];
        var c = _ref2[1];
        return _this4.formatter(m, c);
      });
      this.node.innerHTML = formatted.join('\n');
      return this;
    }
  }, {
    key: 'add',
    value: function add(message) {
      if (message == null) {
        this._messages.clear();
        return this;
      }
      var msg = typeof message === 'string' ? message : JSON.stringify(message);

      if (this._messages.has(msg)) {
        this._messages.set(msg, this._messages.get(msg) + 1);
      } else {
        this._messages.set(msg, 1);
      }
      this.render();
      return this;
    }

    /** Wire all status logs. */

  }], [{
    key: 'defaultAlert',
    value: function defaultAlert(msg, count) {
      var countFormat = count <= 1 ? '' : '<b>(' + count + ')</b> ';
      return '<div class="alert alert-danger">' + countFormat + msg + '</div>';
    }
  }, {
    key: 'wire',
    value: function wire(conn) {
      var id = arguments.length <= 1 || arguments[1] === undefined ? 'ws-alerts' : arguments[1];
      var formatter = arguments.length <= 2 || arguments[2] === undefined ? StatusLog.defaultAlert : arguments[2];

      var node = document.getElementById(id);
      if (node == null) return;
      if (UIElement.determineActionName(node) == null) return;

      console.log('Wiring status log', node, 'to element with id=' + id + '.');
      var l = new StatusLog(node, formatter);
      conn.errorCB = l.add.bind(l);
    }
  }]);

  return StatusLog;
}(UIElement);

/**
 * A button, and usually wired to any `<button>` with an action name.
 *
 * This button also binds to process IDs of the backend. That means
 * that the button is disabled (using the CSS class `disabled`) while the
 * backend is processing the action that got started when it was clicked.
 * A simple example is below.
 *
 * @example
 * // in index.html, add:
 * <button data-action="run">Run</button>
 *
 * // in analysis.py, add:
 * def on_run(self):
 *     """Run when button is pressed."""
 *     pass
 *
 * // In this form, Databench finds the button automatically and connects it
 * // to the backend. No additional JavaScript code is required.
 */


var Button = function (_UIElement3) {
  _inherits(Button, _UIElement3);

  /**
   * @param  {HTMLElement} node DOM node to connect.
   */

  function Button(node) {
    _classCallCheck(this, Button);

    var _this5 = _possibleConstructorReturn(this, Object.getPrototypeOf(Button).call(this, node));

    _this5.IDLE = 0;
    _this5.ACTIVE = 2;
    _this5._state = _this5.IDLE;

    _this5.node.addEventListener('click', _this5.click.bind(_this5), false);
    return _this5;
  }

  /**
   * Called on click events. When a button is wired, this function is overwritten
   * with the actual function that is triggered on click events.
   * @param  {int} processID a random id for the process that could be started
   */


  _createClass(Button, [{
    key: 'clickCB',
    value: function clickCB(processID) {
      return console.log('click on ' + this.node + ' with ' + processID);
    }
  }, {
    key: 'render',
    value: function render() {
      switch (this._state) {
        case this.ACTIVE:
          this.node.classList.add('disabled');
          break;
        default:
          this.node.classList.remove('disabled');
      }
      return this;
    }
  }, {
    key: 'click',
    value: function click() {
      if (this._state !== this.IDLE) return this;

      var processID = Math.floor(Math.random() * 0x100000);
      this.clickCB(processID);
      return this;
    }
  }, {
    key: 'state',
    value: function state(s) {
      if (s !== this.IDLE && s !== this.ACTIVE) return this;

      this._state = s;
      this.render();
      return this;
    }

    /** Wire all buttons. */

  }], [{
    key: 'wire',
    value: function wire(conn) {
      Array.from(document.getElementsByTagName('BUTTON')).filter(function (node) {
        return node.databenchUI === undefined;
      }).filter(function (node) {
        return UIElement.determineActionName(node) !== null;
      }).forEach(function (node) {
        var b = new Button(node);
        console.log('Wiring button', node, 'to action ' + b.actionName + '.');

        // set up click callback
        b.clickCB = function (processID) {
          // set up process callback
          conn.onProcess(processID, function (status) {
            return b.state(
            // map process status to state
            { start: b.ACTIVE, end: b.IDLE }[status]);
          });

          conn.emit(b.actionName, b.actionFormat({
            __process_id: processID }));
        };
      });
    }
  }]);

  return Button;
}(UIElement);

/**
 * Data bound text elements.
 *
 * Wired to ``<span>``, ``<p>``, ``<div>``, ``<i>`` and ``<b>`` tags with a
 * ``data-action`` attribute specifying the action name.
 */


// eslint-disable-line camelcase

var Text = function (_UIElement4) {
  _inherits(Text, _UIElement4);

  function Text() {
    _classCallCheck(this, Text);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(Text).apply(this, arguments));
  }

  _createClass(Text, [{
    key: 'formatFn',

    /**
     * Format the value.
     * @param  {any} value Value as represented in the backend.
     * @return {string}       Formatted representation of the value.
     */
    value: function formatFn(value) {
      return value;
    }

    /** Reads and sets the value. */

  }, {
    key: 'value',
    value: function value(v) {
      if (v === undefined) return this.node.innerHTML;

      this.node.innerHTML = this.formatFn(v || '');
      return this;
    }

    /**
     * Wire all text.
     * @param  {Connection} conn Connection to use.
     */

  }], [{
    key: 'wire',
    value: function wire(conn) {
      [].concat(_toConsumableArray(Array.from(document.getElementsByTagName('SPAN'))), _toConsumableArray(Array.from(document.getElementsByTagName('P'))), _toConsumableArray(Array.from(document.getElementsByTagName('DIV'))), _toConsumableArray(Array.from(document.getElementsByTagName('I'))), _toConsumableArray(Array.from(document.getElementsByTagName('B')))).filter(function (node) {
        return node.databenchUI === undefined;
      }).filter(function (node) {
        return node.dataset.action !== undefined;
      }).filter(function (node) {
        return UIElement.determineActionName(node) !== null;
      }).forEach(function (node) {
        var t = new Text(node);
        console.log('Wiring text', node, 'to action ' + t.actionName + '.');

        // handle events from backend
        conn.on(t.wireSignal, function (message) {
          return t.value(message);
        });
      });
    }
  }]);

  return Text;
}(UIElement);

/** Make an `<input[type='text']>` with an action name interactive. */


var TextInput = function (_UIElement5) {
  _inherits(TextInput, _UIElement5);

  /**
   * @param {HTMLElement} node The node to connect.
   */

  function TextInput(node) {
    _classCallCheck(this, TextInput);

    var _this7 = _possibleConstructorReturn(this, Object.getPrototypeOf(TextInput).call(this, node));

    _this7._triggerOnKeyUp = false;

    _this7.node.addEventListener('change', _this7.change.bind(_this7), false);
    return _this7;
  }

  /**
   * Format the value.
   * @param  {any}    value Value as represented in the backend.
   * @return {string}       Formatted representation of the value.
   */


  _createClass(TextInput, [{
    key: 'formatFn',
    value: function formatFn(value) {
      return value;
    }

    /**
     * Callback that is triggered on frontend changes.
     * @param  {any} value A formatted action.
     */

  }, {
    key: 'changeCB',
    value: function changeCB(value) {
      return console.log('change of ' + this.node + ': ' + value);
    }
  }, {
    key: 'change',
    value: function change() {
      return this.changeCB(this.actionFormat(this.value()));
    }

    /**
     * The default is `false`, which means that the callback is only triggered on
     * `change` events (i.e. pressing enter or unfocusing the element).
     * Setting this to true will trigger on every `keyup` event of this element.
     *
     * @param  {boolean}   v Whether to trigger on `keyup` events. Default is true.
     * @return {TextInput}   self
     */

  }, {
    key: 'triggerOnKeyUp',
    value: function triggerOnKeyUp(v) {
      if (v !== false && !this._triggerOnKeyUp) {
        this.node.addEventListener('keyup', this.change.bind(this), false);
        this._triggerOnKeyUp = true;
      }

      if (v === false && this._triggerOnKeyUp) {
        this.node.removeEventListener('keyup', this.change.bind(this), false);
        this._triggerOnKeyUp = false;
      }

      return this;
    }

    /** Reads and sets the value. */

  }, {
    key: 'value',
    value: function value(v) {
      if (v === undefined) return this.node.value;

      this.node.value = this.formatFn(v || '');
      return this;
    }

    /** Wire all text inputs. */

  }], [{
    key: 'wire',
    value: function wire(conn) {
      Array.from(document.getElementsByTagName('INPUT')).filter(function (node) {
        return node.databenchUI === undefined;
      }).filter(function (node) {
        return node.getAttribute('type') === 'text';
      }).filter(function (node) {
        return UIElement.determineActionName(node) !== null;
      }).forEach(function (node) {
        var t = new TextInput(node);
        console.log('Wiring text input', node, 'to action ' + t.actionName + '.');

        // handle events from frontend
        t.changeCB = function (message) {
          return conn.emit(t.actionName, message);
        };

        // handle events from backend
        conn.on(t.wireSignal, function (message) {
          return t.value(message);
        });
      });
    }
  }]);

  return TextInput;
}(UIElement);

/**
 * Make all `<input[type='range']>` with an action name interactive.
 *
 * @example
 * // in index.html, add:
 * <label for="samples">Samples:</label>
 * <input type="range" id="samples" value="1000" min="100" max="10000" step="100" />
 *
 * // in analysis.py, add:
 * def on_samples(self, value):
 *     """Sets the number of samples to generate per run."""
 *     self.data['samples'] = value
 *
 * // The Python code is for illustration only and can be left out as this is
 * // the default behavior.
 */


var Slider = function (_UIElement6) {
  _inherits(Slider, _UIElement6);

  /**
   * @param  {HTMLElement}  node      DOM node to bind.
   * @param  {HTMLElement?} labelNode DOM node label that corresponds to the slider.
   */

  function Slider(node, labelNode) {
    _classCallCheck(this, Slider);

    var _this8 = _possibleConstructorReturn(this, Object.getPrototypeOf(Slider).call(this, node));

    _this8.labelNode = labelNode;
    _this8.labelHtml = labelNode ? labelNode.innerHTML : null;

    _this8.node.addEventListener('input', _this8.render.bind(_this8), false);
    _this8.node.addEventListener('change', _this8.change.bind(_this8), false);
    _this8.render();
    return _this8;
  }

  /**
   * Callback with changes to the slider value.
   * @param  {Number} value   Value from a sliderToValue() transform.
   */


  _createClass(Slider, [{
    key: 'changeCB',
    value: function changeCB(value) {
      return console.log('slider value change: ' + value);
    }

    /**
     * Transform a backend value to a slider value.
     * @param  {number} value Value as stored in backend.
     * @return {int}          Value for the HTML range element.
     */

  }, {
    key: 'valueToSlider',
    value: function valueToSlider(value) {
      return value;
    }

    /**
     * Transform a value from the HTML range element to a value that should be stored.
     * @param  {int}    s Value from HTML range element.
     * @return {number}   Value to store.
     */

  }, {
    key: 'sliderToValue',
    value: function sliderToValue(s) {
      return s;
    }

    /**
     * How a value should be represented.
     * For example, this can add units or convert from radians to degrees.
     * @param  {number}         value Input value as it is stored in the backend.
     * @return {string|number}        Representation of a value.
     */

  }, {
    key: 'formatFn',
    value: function formatFn(value) {
      return value;
    }
  }, {
    key: 'render',
    value: function render() {
      var v = this.value();
      if (this.labelNode) {
        this.labelNode.innerHTML = this.labelHtml + ' ' + this.formatFn(v);
      }
      return this;
    }

    /** Reads and sets the value. */

  }, {
    key: 'value',
    value: function value(v) {
      if (v === undefined) {
        return this.sliderToValue(parseFloat(this.node.value));
      }

      var newSliderValue = this.valueToSlider(v);
      if (this.node.value === newSliderValue) return this;

      this.node.value = newSliderValue;
      this.render();
      return this;
    }
  }, {
    key: 'change',
    value: function change() {
      return this.changeCB(this.actionFormat(this.value()));
    }

    /** Preprocess labels before wiring. */

  }], [{
    key: 'preprocessLabels',
    value: function preprocessLabels() {
      Array.from(document.getElementsByTagName('LABEL')).filter(function (label) {
        return label.htmlFor;
      }).forEach(function (label) {
        var node = document.getElementById(label.htmlFor);
        if (node) node.label = label;
      });
    }

    /** Wire all sliders. */

  }, {
    key: 'wire',
    value: function wire(conn) {
      this.preprocessLabels();

      Array.from(document.getElementsByTagName('INPUT')).filter(function (node) {
        return node.databenchUI === undefined;
      }).filter(function (node) {
        return node.getAttribute('type') === 'range';
      }).filter(function (node) {
        return UIElement.determineActionName(node) !== null;
      }).forEach(function (node) {
        var slider = new Slider(node, node.label);
        console.log('Wiring slider', node, 'to action ' + slider.actionName + '.');

        // handle events from frontend
        slider.changeCB = function (message) {
          return conn.emit(slider.actionName, message);
        };

        // handle events from backend
        conn.on(slider.wireSignal, function (message) {
          return slider.value(message);
        });
      });
    }
  }]);

  return Slider;
}(UIElement);

/**
 * Connect an `<img>` with a signal name to the backend.
 *
 * The signal message is placed directly into the `src` attribute of the image
 * tag. For matplotlib, that formatting can be done with the utility function
 * `fig_to_src()` (see example below).
 *
 * @example
 * // in index.html, add
 * <img alt="my plot" data-signal="mpl" />
 *
 * // in analysis.py, add
 * import matplotlib.pyplot as plt
 * ...
 * fig = plt.figure()
 * ...
 * self.emit('mpl', databench.fig_to_src(fig))
 */


var Image = function (_UIElement7) {
  _inherits(Image, _UIElement7);

  function Image() {
    _classCallCheck(this, Image);

    return _possibleConstructorReturn(this, Object.getPrototypeOf(Image).apply(this, arguments));
  }

  _createClass(Image, [{
    key: 'value',

    /** Reads and sets the value. */
    value: function value(v) {
      if (v === undefined) return this.node.src;

      this.node.src = v || '';
      return this;
    }

    /** Wire all text inputs. */

  }], [{
    key: 'wire',
    value: function wire(conn) {
      Array.from(document.getElementsByTagName('IMG')).filter(function (node) {
        return node.databenchUI === undefined;
      }).filter(function (node) {
        return node.dataset.signal !== undefined;
      }).filter(function (node) {
        return UIElement.determineWireSignal(node) !== null;
      }).forEach(function (node) {
        var img = new Image(node);
        console.log('Wiring image', node, 'to signal ' + img.wireSignal + '.');

        // handle events from backend
        conn.on(img.wireSignal, function (message) {
          return img.value(message);
        });
      });
    }
  }]);

  return Image;
}(UIElement);

/**
 * Wire all the UI elements to the backend. The action name is determined by
 * {@link module:ui~UIElement.determineActionName|UIElement.determineActionName()}
 * and the action message can be modified by overwriting
 * {@link module:ui~UIElement#actionFormat|UIElement.actionFormat()}. The signal
 * name is determined by
 * {@link module:ui~UIElement.determineWireSignal|UIElement.determineWireSignal()}.
 *
 * @param  {Connection} connection A Databench.Connection instance.
 * @return {Connection}            The same connection.
 */


function wire(connection) {
  StatusLog.wire(connection);
  Button.wire(connection);
  TextInput.wire(connection);
  Text.wire(connection);
  Slider.wire(connection);
  Image.wire(connection);
  Log.wire(connection);
  return connection;
}

exports.StatusLog = StatusLog;
exports.Log = Log;
exports.Button = Button;
exports.TextInput = TextInput;
exports.Text = Text;
exports.Slider = Slider;
exports.Image = Image;
exports.wire = wire;

},{}],4:[function(require,module,exports){
var _global = (function() { return this; })();
var nativeWebSocket = _global.WebSocket || _global.MozWebSocket;
var websocket_version = require('./version');


/**
 * Expose a W3C WebSocket class with just one or two arguments.
 */
function W3CWebSocket(uri, protocols) {
	var native_instance;

	if (protocols) {
		native_instance = new nativeWebSocket(uri, protocols);
	}
	else {
		native_instance = new nativeWebSocket(uri);
	}

	/**
	 * 'native_instance' is an instance of nativeWebSocket (the browser's WebSocket
	 * class). Since it is an Object it will be returned as it is when creating an
	 * instance of W3CWebSocket via 'new W3CWebSocket()'.
	 *
	 * ECMAScript 5: http://bclary.com/2004/11/07/#a-13.2.2
	 */
	return native_instance;
}


/**
 * Module exports.
 */
module.exports = {
    'w3cwebsocket' : nativeWebSocket ? W3CWebSocket : null,
    'version'      : websocket_version
};

},{"./version":5}],5:[function(require,module,exports){
module.exports = require('../package.json').version;

},{"../package.json":6}],6:[function(require,module,exports){
module.exports={
  "_args": [
    [
      "websocket@^1.0.22",
      "/Users/svenkreiss/tech/databench"
    ]
  ],
  "_from": "websocket@>=1.0.22 <2.0.0",
  "_id": "websocket@1.0.23",
  "_inCache": true,
  "_installable": true,
  "_location": "/websocket",
  "_nodeVersion": "0.10.45",
  "_npmOperationalInternal": {
    "host": "packages-16-east.internal.npmjs.com",
    "tmp": "tmp/websocket-1.0.23.tgz_1463625793005_0.4532310354989022"
  },
  "_npmUser": {
    "email": "brian@worlize.com",
    "name": "theturtle32"
  },
  "_npmVersion": "2.15.1",
  "_phantomChildren": {},
  "_requested": {
    "name": "websocket",
    "raw": "websocket@^1.0.22",
    "rawSpec": "^1.0.22",
    "scope": null,
    "spec": ">=1.0.22 <2.0.0",
    "type": "range"
  },
  "_requiredBy": [
    "/"
  ],
  "_resolved": "https://registry.npmjs.org/websocket/-/websocket-1.0.23.tgz",
  "_shasum": "20de8ec4a7126b09465578cd5dbb29a9c296aac6",
  "_shrinkwrap": null,
  "_spec": "websocket@^1.0.22",
  "_where": "/Users/svenkreiss/tech/databench",
  "author": {
    "email": "brian@worlize.com",
    "name": "Brian McKelvey",
    "url": "https://www.worlize.com/"
  },
  "browser": "lib/browser.js",
  "bugs": {
    "url": "https://github.com/theturtle32/WebSocket-Node/issues"
  },
  "config": {
    "verbose": false
  },
  "contributors": [
    {
      "email": "ibc@aliax.net",
      "name": "Iñaki Baz Castillo",
      "url": "http://dev.sipdoc.net"
    }
  ],
  "dependencies": {
    "debug": "^2.2.0",
    "nan": "^2.3.3",
    "typedarray-to-buffer": "^3.1.2",
    "yaeti": "^0.0.4"
  },
  "description": "Websocket Client & Server Library implementing the WebSocket protocol as specified in RFC 6455.",
  "devDependencies": {
    "buffer-equal": "^0.0.1",
    "faucet": "^0.0.1",
    "gulp": "git+https://github.com/gulpjs/gulp.git#4.0",
    "gulp-jshint": "^1.11.2",
    "jshint-stylish": "^1.0.2",
    "tape": "^4.0.1"
  },
  "directories": {
    "lib": "./lib"
  },
  "dist": {
    "shasum": "20de8ec4a7126b09465578cd5dbb29a9c296aac6",
    "tarball": "https://registry.npmjs.org/websocket/-/websocket-1.0.23.tgz"
  },
  "engines": {
    "node": ">=0.8.0"
  },
  "gitHead": "ba2fa7e9676c456bcfb12ad160655319af66faed",
  "homepage": "https://github.com/theturtle32/WebSocket-Node",
  "keywords": [
    "websocket",
    "websockets",
    "socket",
    "networking",
    "comet",
    "push",
    "RFC-6455",
    "realtime",
    "server",
    "client"
  ],
  "license": "Apache-2.0",
  "main": "index",
  "maintainers": [
    {
      "email": "brian@worlize.com",
      "name": "theturtle32"
    }
  ],
  "name": "websocket",
  "optionalDependencies": {},
  "readme": "ERROR: No README data found!",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/theturtle32/WebSocket-Node.git"
  },
  "scripts": {
    "gulp": "gulp",
    "install": "(node-gyp rebuild 2> builderror.log) || (exit 0)",
    "test": "faucet test/unit"
  },
  "version": "1.0.23"
}

},{}]},{},[2])


//# sourceMappingURL=databench.js.map
