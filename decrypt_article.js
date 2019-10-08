
const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({
		input: fs.createReadStream('out/en_articles.dat'),
		crlfDelay: Infinity
	});

function processArticle(line) {
	var e_data = JSON.parse(line);
	var d_data = decrypt_data(e_data.data, e_data.aid);
	//console.log(d_data);
	fs.appendFile('out/de_articles.dat', d_data + '\n', function (err) {
		if (err) {
			console.log(e_data.aid + ' failed.')
		} else {
			console.log(e_data.aid + ' succeeded.');
		}
	});
};

rl.on('line', processArticle);

function test(aid) {
	//return decrypt_data(encrypt_data, aid);
	return aid;
};

function decrypt_data(data, aid) {
	var o = ["A", "b", "H", "P", "Q", "X", "V", "p", "r", "I", "$", "7", "F", "z", "o", "K", "_", "S", "6", "a", "T", "C", "t", "j", "5", "n", "D", "e", "x", "U", "R", "y", "4", "N", "Y", "9", "v", "0", "3", "W", "l", "u", "1", "i", "q", "s", "O", "J", "G", "E", "w", "f", "B", "m", "L", "2", "d", "h", "k", "8", "c", "g", "Z", "M"];

	var result = (function (t, e) {
		return function (t, e, i) {
			var o = {},
			s = String.fromCharCode("}".charCodeAt(0) + 1),
			r = e.length;
			e = function (t, e, i) {
				var n = function n(t) {
					return function (t) {
						if (Array.isArray(t)) {
							for (var e = 0, i = new Array(t.length); e < t.length; e++)
								i[e] = t[e];
							return i
						}
					}
					(t) || function (t) {
						if (Symbol.iterator in Object(t) || "[object Arguments]" === Object.prototype.toString.call(t))
							return Array.from(t)
					}
					(t) || function () {
						throw new TypeError("Invalid attempt to spread non-iterable instance")
					}
					()
				};
				return e ? (t = t.slice(),
					e.split("").forEach(function (e) {
						var o = e.charCodeAt(0) % i;
						t = [].concat(n(t.slice(o)), n(t.slice(0, o)))
					}),
					t) : t
			}
			(e, i, r);
			for (var a = 0; a < r; ++a)
				o[e[a]] = a;
			for (var h, l, c, u, d = [], f = 0, p = 0; f < t.length; )
				h = o[t[f++]],
				l = o[t[f++]],
				c = o[t[f++]],
				u = o[t[f++]],
				d[p++] = h << 2 | l >> 4,
				d[p++] = (15 & l) << 4 | c >> 2,
				d[p++] = (3 & c) << 6 | u;
			var g = t.slice(-2);
			return g[0] === s ? d.length = d.length - 2 : g[1] === s && (d.length = d.length - 1),
			function (t) {
				for (var e = "", i = 0; i < t.length; ++i) {
					var n = t[i];
					e += String.fromCharCode(256 * n + t[++i])
				}
				return e
			}
			(d)
		}
		(t, o, e)
	})(data, (function (t) {
			return parseInt(("" + t).slice(0, 10), 36).toString().slice(0, 5)
		}
			(aid)));
	return result;
};

function ƒ(t) {
	return parseInt(("" + t).slice(0, 10), 36).toString().slice(0, 5)
};

function a(t, e) {
	return function (t, e, i) {
		var o = {},
		s = String.fromCharCode("}".charCodeAt(0) + 1),
		r = e.length;
		e = function (t, e, i) {
			return e ? (t = t.slice(),
				e.split("").forEach(function (e) {
					var o = e.charCodeAt(0) % i;
					t = [].concat(n(t.slice(o)), n(t.slice(0, o)))
				}),
				t) : t
		}
		(e, i, r);
		for (var a = 0; a < r; ++a)
			o[e[a]] = a;
		for (var h, l, c, u, d = [], f = 0, p = 0; f < t.length; )
			h = o[t[f++]],
			l = o[t[f++]],
			c = o[t[f++]],
			u = o[t[f++]],
			d[p++] = h << 2 | l >> 4,
			d[p++] = (15 & l) << 4 | c >> 2,
			d[p++] = (3 & c) << 6 | u;
		var g = t.slice(-2);
		return g[0] === s ? d.length = d.length - 2 : g[1] === s && (d.length = d.length - 1),
		function (t) {
			for (var e = "", i = 0; i < t.length; ++i) {
				var n = t[i];
				e += String.fromCharCode(256 * n + t[++i])
			}
			return e
		}
		(d)
	}
	(t, o, e)
};
