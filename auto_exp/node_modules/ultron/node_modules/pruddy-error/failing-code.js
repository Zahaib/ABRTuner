var isNode = !!(typeof process != 'undefined' && process.versions && process.versions.node);
var failingLine = require('./failing-line');

var fs;
var nodeRequire;

if (isNode) {
  nodeRequire = require;
  fs = nodeRequire('fs');
  nodeRequire = null;
}

module.exports = function failingCode (error, doc, shift) {
  var ln = failingLine(error, shift);

  if (!ln) return;

  if (!doc && fs) {
    try {
      doc = fs.readFileSync(ln.filename).toString();
    } catch (readError) {
      return undefined;
    }
  }

  if (!doc) return undefined;

  var result = [];
  var lines = doc.split('\n');

  var i = ln.line - 3;
  while (++i < ln.line + 1) {
    if (i + 1 != ln.line) {
      result.push({
        line: ln.line - (ln.line - i -1),
        code: lines[i]
      });
      continue;
    }

    result.push({
      line: ln.line,
      col: ln.col,
      fn: ln.fn,
      filename: ln.filename,
      code: lines[i],
      failed: true
    });
  }

  return result;
};
