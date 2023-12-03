const fs = require('fs');
data = fs.readFileSync("day01.input").asciiSlice()

part1ToAdd = []
data.split("\n").forEach(line => {
    var numbers = [];
    [...line.matchAll(/\d/g)].forEach(match => {
        numbers.push(match[0])
    }
    )
    if (numbers.length) {
        part1ToAdd.push(parseInt(`${numbers[0]}${numbers.slice(-1)}`))
    }
}
)
const initialValue = 0
const part1Sum = part1ToAdd.reduce((accumulator, currentValue) => accumulator + currentValue, initialValue)

console.log(part1Sum)

/*

Kirjava part 1:   

eval(document.body.innerText.trim().split`\n`.map(d=>(q=d.replace(/[^\d]/g,''),q[0]+q.at(-1))).join`+`)

Modified for node: 
*/
console.log(eval(data.trim().split`\n`.map(d=>(q=d.replace(/[^\d]/g,''),q[0]+q.at(-1))).join`+`))


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


var part2ToAdd = []
data.split("\n").forEach(line => {
    var numbers = [];
    // https://regex101.com/r/Z8Lwl5/1
    [...line.matchAll(/(?=(\d|one|two|three|four|five|six|seven|eight|nine))/g)].forEach(match => {
        numbers.push(match[1])
    }
    )
    var converted = []
    // numbers.forEach(number => {console.log(`Number: ${number} Converted: ${conversion[number]}`)})
    numbers.forEach(number => converted.push(conversion[number]))
    if (converted.length) {
        part2ToAdd.push(parseInt(`${converted[0]}${converted.slice(-1)}`))
    }
}
)
const part2Sum = part2ToAdd.reduce((accumulator, currentValue) => accumulator + currentValue, initialValue)

console.log(part2Sum)

    /*
     
    Kirjava part 2:
     
    (n = `_|one|two|three|four|five|six|seven|eight|nine`),
        (a = 0),
        document.body.innerText.trim().split`\n`.map(
            (t) => (
                (s = [...t].map(
                    (a, i) => (
                        (q = n.split`|`.indexOf(
                            t.match(RegExp(`^.{${i}}(${n})`))?.[1],
                        )),
                        ~q ? q : 1 / a ? a : []
                    ),
                ).join``),
                (a += +(s[0] + s.at(-1)))
            ),
        ),
        a;
    
    Modified for node:
    */

    ((n = `_|one|two|three|four|five|six|seven|eight|nine`),
        (a = 0),
        data.trim().split`\n`.map(
            (t) => (
                console.log(t),
                (s = [...t].map(
                    (a, i) => (
                        (q = n.split`|`.indexOf(
                            t.match(RegExp(`^.{${i}}(${n})`))?.[1],
                        )),
                        ~q ? q : 1 / a ? a : []
                    ),
                ).join``),
                (a += +(s[0] + s.at(-1)))
            ),
        ),
        a)