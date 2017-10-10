```
This is a clone of the `prettify-error` module which was unpublished by the
author. All dependencies have been inlined to prevent future conflicts.
```

## pruddy-error

Prettify given error objects for console outputs

![](https://i.cloudup.com/Vt6PAM3yDA.png)

## Install

``bash
$ npm install pruddy-error
``

## Usage

```js
var pruddy = require('pruddy-error');
var error = new Error('lorem ipsum');

console.error(pruddy(error) || error);
```

If you'd like to skip some lines from the stack:

```js
pruddy(error, 2) // Will start reading the stack from the third line.
```
