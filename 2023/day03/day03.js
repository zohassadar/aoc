
const fs = require('fs');
data = fs.readFileSync("day03.input", "utf-8")

// dunno that i'll get to this one.  See 6502 asm instead
// https://github.com/zohassadar/NESHelloWorld/blob/main/aoc2023/day03.asm

// Kirjava part 1:
// I=document.body.innerText,A=0,I.replace(/\d+/g,(n,e)=>{for(i=a=0;3>i;a+=I.substring(e-=[1,-141,282][i++],e+([]+n).length+2));/[^\d\.\n]/.test(a)&&(A+=+n)}),A


// Kirjava part 2:
// A=128;I=document.body.innerText.replace(/\*/g,_=>String.fromCharCode(A++))
// A=0;G={};I.replace(/\d+/g,(n,e)=>{
//    for(i=a=0;3>i;a+=I.substring(e-=[1,-141,282][i++],e+([]+n).length+2))
//    (V=a.match(/[\u0080-\u03FF]/)?.[0])&&(G[V]?A+=G[V]*n:G[V]=n)
// }),A
