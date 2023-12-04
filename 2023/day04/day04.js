
const fs = require('fs');
data = fs.readFileSync("day04.input", "utf-8")

pullNumbers = function (str) {
    return str.trim().split(/\s+/).map((d) => +d)
}

total = 0
cardCount = data.trim().split('\n').map(() => 1)

for ([index, line] of Object.entries(data.split('\n'))) {
    info = line.match(/(?<=:)([\d ]+)\|([\d ]+)/)
    winners = pullNumbers(info[1])
    mine = pullNumbers(info[2])
    points = -1
    mine.forEach((m) => { if (winners.includes(m)) points += 1 })
    if (points >= 0) {
        total += 2 ** points
        idx = +index
        first = idx + 1
        if (idx<cardCount.length){
            last = first + points + 1
            last = last < cardCount.length ? last : cardCount.length
            // console.log(`i: ${idx+1} f:${first} l: ${last}`)
            for (i=first;i<last;i+=1){
                cardCount[i]+=(1*cardCount[idx])
                }
        }
    }
}

console.log(total)
console.log(cardCount.reduce((a,v)=>a+v,0))



