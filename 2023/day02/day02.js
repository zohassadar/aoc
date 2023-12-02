
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
