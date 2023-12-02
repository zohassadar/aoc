
const fs = require('fs');
data = fs.readFileSync("day02.input").toString()


limits = {
    red: 12,
    green: 13,
    blue: 14,
}

new_data = data.trim().split`\n`.map((thing, i) => (
    bad = {
        red: [],
        blue: [],
        green: []
    },
    [...thing.matchAll(/(\d+) (red|green|blue)/g)].forEach(match => {
        value = match[1]
        color = match[2]
        if (parseInt(value) > limits[color]) { bad[color].push(value) }
    }),
    (bad['red'].length || bad['green'].length || bad['blue'].length) ? 0 : i + 1
)
)

console.log(new_data.reduce((accum, val) => accum + val, 0))
