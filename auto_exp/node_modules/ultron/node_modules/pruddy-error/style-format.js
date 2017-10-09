var ansi = require('./ansi-codes.json');
var format = require('./format-text');

module.exports = styleFormat;

function styleFormat (text) {
  return format(text, ansi);
}
