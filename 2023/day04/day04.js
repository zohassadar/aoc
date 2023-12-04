
const fs = require('fs');
data = fs.readFileSync("day04.input", "utf-8")

pullNumbers = function (str) {
    return str.trim().split(/\s+/).map((d) => +d)
}

total = 0

for (line of data.split('\n')) {
    info = line.match(/(?<=:)([\d ]+)\|([\d ]+)/)
    winners = pullNumbers(info[1])
    mine = pullNumbers(info[2])
    points = -1
    mine.forEach((m) => {if (winners.includes(m))points+=1})
    if (points >= 0) total+=2**points
    }

console.log(total)
