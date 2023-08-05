'use strict';

angular.module('ajenti.augeas', ['core']);


'use strict';

angular.module('ajenti.augeas').service('augeas', function ($http, $q, AugeasConfig) {
    this.get = function (endpoint) {
        return $http.get('/api/augeas/endpoint/get/' + endpoint).then(function (response) {
            return AugeasConfig.get(response.data);
        });
    };

    this.set = function (endpoint, config) {
        return $http.post('/api/augeas/endpoint/set/' + endpoint, config.serialize()).then(function (response) {
            return response.data;
        });
    };

    return this;
});


'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

angular.module('ajenti.augeas').service('AugeasConfig', function () {
    var AugeasNode = function () {
        function AugeasNode() {
            _classCallCheck(this, AugeasNode);

            this.children = [];
        }

        _createClass(AugeasNode, [{
            key: 'fullPath',
            value: function fullPath() {
                if (this.path) {
                    return this.path;
                }

                var total = 0;
                var index = null;
                for (var i = 0; i < this.parent.children.length; i++) {
                    var child = this.parent.children[i];
                    if (child.name === this.name) {
                        total += 1;
                    }
                    if (child === this) {
                        index = total;
                    }
                }
                if (total > 1) {
                    return this.parent.fullPath() + '/' + this.name + '[' + index + ']';
                } else {
                    return this.parent.fullPath() + '/' + this.name;
                }
            }
        }]);

        return AugeasNode;
    }();

    var AugeasConfig = function () {
        function AugeasConfig(data) {
            _classCallCheck(this, AugeasConfig);

            this.root = this.__construct(data);
            this.root.path = data.path;
        }

        _createClass(AugeasConfig, [{
            key: 'serialize',
            value: function serialize(node) {
                var _this = this;

                if (typeof node === 'undefined' || node === null) {
                    node = this.root;
                }
                var data = {};
                data.path = node.fullPath();
                data.name = node.name;
                data.value = node.value;
                data.children = node.children.map(function (c) {
                    return _this.serialize(c);
                });
                return data;
            }
        }, {
            key: '__construct',
            value: function __construct(data, parent) {
                var node = new AugeasNode();
                node.name = data.name;
                node.value = data.value;
                node.parent = parent;
                for (var i = 0; i < data.children.length; i++) {
                    var c = data.children[i];
                    node.children.push(this.__construct(c, node));
                }
                return node;
            }
        }, {
            key: 'relativize',
            value: function relativize(path) {
                return path.substring(this.root.path.length + 1);
            }
        }, {
            key: 'getNode',
            value: function getNode(path) {
                var matches = this.matchNodes(path);
                if (matches.length === 0) {
                    return null;
                }
                return matches[0];
            }
        }, {
            key: 'get',
            value: function get(path) {
                var node = this.getNode(path);
                if (!node) {
                    return null;
                }
                return node.value;
            }
        }, {
            key: 'set',
            value: function set(path, value, node) {
                if (!node) {
                    node = this.root;
                    if (path[0] === '/') {
                        path = this.relativize(path);
                    }
                }

                if (!path) {
                    node.value = value;
                    return;
                }

                if (path.indexOf('/') === -1) {
                    var q = path;
                    var remainder = null;
                } else {
                    var q = path.substring(0, path.indexOf('/'));
                    var remainder = path.substring(path.indexOf('/') + 1);
                }

                var child = this.matchNodes(q, node)[0];
                if (!child) {
                    child = new AugeasNode();
                    child.parent = node;
                    child.name = q;
                    node.children.push(child);
                }

                return this.set(remainder, value, child);
            }
        }, {
            key: 'setd',
            value: function setd(path, value) {
                if (!value) {
                    return this.remove(path);
                } else {
                    return this.set(path, value);
                }
            }
        }, {
            key: 'model',
            value: function model(path, setd) {
                var _this2 = this;

                var setfx = function setfx(p, v) {
                    return setd ? _this2.setd(p, v) : _this2.set(p, v);
                };
                var fx = function fx(value) {
                    if (angular.isDefined(value)) {
                        setfx(path, value);
                    }
                    return _this2.get(path);
                };

                return fx;
            }
        }, {
            key: 'insert',
            value: function insert(path, value, index) {
                var matches = this.matchNodes(path);
                if (matches.length === 0) {
                    this.set(path, value);
                    return path;
                } else {
                    var node = matches[0].parent;
                    if (typeof index === 'undefined' || index === null) {
                        index = node.children.indexOf(matches[matches.length - 1]) + 1;
                    }
                    var child = new AugeasNode();
                    child.parent = node;
                    child.name = path.substring(path.lastIndexOf('/') + 1);
                    child.value = value;
                    node.children.splice(index, 0, child);
                    return child.fullPath();
                }
            }
        }, {
            key: 'remove',
            value: function remove(path) {
                return this.matchNodes(path).map(function (node) {
                    return node.parent.children.remove(node);
                });
            }
        }, {
            key: 'match',
            value: function match(path, node) {
                return this.matchNodes(path, node).map(function (x) {
                    return x.fullPath();
                });
            }
        }, {
            key: 'matchNodes',
            value: function matchNodes(path, node) {
                if (!node) {
                    node = this.root;
                    if (path[0] === '/') {
                        path = this.relativize(path);
                    }
                }

                if (path.indexOf('/') === -1) {
                    var q = path;
                    var remainder = null;
                } else {
                    var q = path.substring(0, path.indexOf('/'));
                    var remainder = path.substring(path.indexOf('/') + 1);
                }

                if (q.indexOf('[') === -1) {
                    var index = null;
                } else {
                    var index = parseInt(q.substring(q.indexOf('[') + 1, q.indexOf(']'))) - 1;
                    var q = q.substring(0, q.indexOf('['));
                }

                var matches = [];
                var rx = new RegExp('^' + q + '$');
                for (var i = 0; i < node.children.length; i++) {
                    var child = node.children[i];
                    if (rx.test(child.name)) {
                        matches.push(child);
                    }
                }

                if (index !== null) {
                    if (matches.length <= index) {
                        matches = [];
                    } else {
                        matches = [matches[index]];
                    }
                }

                if (!remainder) {
                    return matches;
                }

                var deepMatches = [];
                for (var j = 0; j < matches.length; j++) {
                    var match = matches[j];
                    var iterable = this.matchNodes(remainder, match);
                    for (var k = 0; k < iterable.length; k++) {
                        var sm = iterable[k];
                        deepMatches.push(sm);
                    }
                }

                return deepMatches;
            }
        }]);

        return AugeasConfig;
    }();

    this.get = function (data) {
        return new AugeasConfig(data);
    };

    return this;
});


