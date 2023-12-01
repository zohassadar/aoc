const fs = require('fs');
data = fs.readFileSync("day01.input").asciiSlice()

to_add = []
data.split("\n").forEach(line => {
    var numbers = [];
    [...line.matchAll(/\d/g)].forEach(match => {
        numbers.push(match[0])
    }
    )
    if (numbers.length) {
        to_add.push(parseInt(`${numbers[0]}${numbers.slice(-1)}`))
    }
}
)
const initialValue = 0
const sum = to_add.reduce((accumulator, currentValue) => accumulator + currentValue, initialValue)

console.log(sum)

const conversion = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}


var part2_to_add = []
data.split("\n").forEach(line => {
    var numbers = [];
    [...line.matchAll(/(?=(\d|one|two|three|four|five|six|seven|eight|nine))/g)].forEach(match => {
        numbers.push(match[1])
    }
    )
    var converted = []
    numbers.forEach(number => {console.log(`Number: ${number} Converted: ${conversion[number]}`)})
    numbers.forEach(number => converted.push(conversion[number]))
    if (converted.length) {
        part2_to_add.push(parseInt(`${converted[0]}${converted.slice(-1)}`))
    }
}
)
const part2_sum = part2_to_add.reduce((accumulator, currentValue) => accumulator + currentValue, initialValue)

console.log(part2_sum)
