const fs = require('fs');
data = fs.readFileSync("day01.input").asciiSlice()

to_add = []
let variable
data.split("\n").forEach(line => {
    var numbers = [];
    [...line.matchAll(/\d/g)].forEach(match => {
        numbers.push(match[0])
    }
    )
    if (numbers.length){
        to_add.push(parseInt(`${numbers[0]}${numbers.slice(-1)}`))
        }
}
)
const initialValue = 0
const sum = to_add.reduce((accumulator, currentValue) => accumulator + currentValue, initialValue)

console.log(sum)
