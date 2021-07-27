// BOJ 1000 TypeScript(node.js)
//출처: https://www.acmicpc.net/help/language 
var fs = require('fs');
var input = fs.readFileSync('/dev/stdin').toString().split(' ');
var a = parseInt(input[0]);
var b = parseInt(input[1]);
console.log(a+b);