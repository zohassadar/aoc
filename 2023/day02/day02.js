
const fs = require('fs');
data = fs.readFileSync("day02.input").toString()


limits = {
    red: 12,
    green: 13,
    blue: 14,
}

part1 = [];
part2 = [];

data.trim().split`\n`.forEach((thing, i) => (
    bad = {
        red: [],
        blue: [],
        green: []
    },
    maxes = {
        red: 0,
        blue: 0,
        green: 0
    },
    [...thing.matchAll(/(\d+) (red|green|blue)/g)].forEach(match => {
        value = match[1]
        color = match[2]
        if (parseInt(value) > limits[color]) { bad[color].push(value) }
        if (parseInt(value) > maxes[color]) { maxes[color] = value }
    }),
    part1.push((bad['red'].length || bad['green'].length || bad['blue'].length) ? 0 : i + 1),
    part2.push(maxes['red'] * maxes['green'] * maxes['blue'])
)
)

console.log(part1.reduce((accum, val) => accum + val, 0))
console.log(part2.reduce((accum, val) => accum + val, 0))


/*

import re; lim=dict(r=12,g=13,b=14); sum( i+1 if 0 not in (int(m[0]) <= lim[m[1]] for m in re.findall(r'(\d+) (\w)', l)) else 0 for i,l in enumerate(open('day02.input').read().splitlines())) 

import re;p=re.compile(r'(\d+) g|(\d+) r|(\d+) b').findall;m=lambda n,l: max(int(i[n]) if i[n] else 0 for i in l);sum(m(0,p(l))*m(1,p(l))*m(2,p(l)) for l in open('day02.input').read().splitlines())

*/


/*

Kirjava part 1:

document.body.innerText.trim``.split`\n`.reduce((e,n,r)=>e+=n.replace(/.+: /,[]).split`;`.every(e=>!e.replace(/ ?(\d+) (\w+),? ?/g,(_,n,[r])=>({r:13,g:14,b:15}[r]>n&&[])))?r+1:0,0)

*/
console.log(data.trim``.split`\n`.reduce((e,n,r)=>e+=n.replace(/.+: /,[]).split`;`.every(e=>!e.replace(/ ?(\d+) (\w+),? ?/g,(_,n,[r])=>({r:13,g:14,b:15}[r]>n&&[])))?r+1:0,0))


/*

Kirjava part 2:

document.body.innerText.trim().split`\n`.reduce((e,n)=>(x={r:0,g:0,b:0},n.replace(/(\d+) (\w)/g,(_,n,r)=>{x[r]=Math.max(n,x[r])}),e+x.r*x.g*x.b),0)


*/