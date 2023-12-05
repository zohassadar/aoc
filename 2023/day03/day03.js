
const fs = require('fs');
data = fs.readFileSync("day03.input", "utf-8")

chars_seen = new Set()

// 2d table
convert_to_numbers = (c) => (chars_seen.add(c), isNaN(c) ? c : +c)
convert_lines = (line) => [...line].map(convert_to_numbers)
table = data.trim().split('\n').map(convert_lines)

// identify what's not a digit or dot
special_chars = [...chars_seen].filter((c) => c != "." && isNaN(c))

// when number is found, use this to get actual value
numbers_by_index = {};
[...data.replace(/\s+/g, '').matchAll(/\d+/g)].map((m) => numbers_by_index[m.index] = +m[0])

part1 = 0
for (y = 0; y < table.length; y += 1) {
    for (x = 0; x < table[0].length; x += 1) {
        is_special = false
        index = y * table[0].length + x
        if (isNaN(table[y][x])) continue
        value = numbers_by_index[index.toString()]
        length = value.toString().length
        // check above first
        if (y > 0) {
            for (aboveX = x; aboveX < x + length; aboveX += 1) {
                if (special_chars.includes(table[y - 1][aboveX])) is_special = true
            }
            if (x > 0) {
                if (special_chars.includes(table[y - 1][x - 1])) is_special = true
            }
            if (x + length < table[0].length - 1) {
                if (special_chars.includes(table[y - 1][x + length])) is_special = true
            }
        }
        // check below next
        if (y < table.length - 1) {
            for (belowX = x; belowX < x + length; belowX += 1) {
                if (special_chars.includes(table[y + 1][belowX])) is_special = true
            }
            if (x > 0){
                if (special_chars.includes(table[y+1][x-1])) is_special = true
            }
            if (x + length < table[0].length - 1){
                if (special_chars.includes(table[y+1][x+length])) is_special = true
            }
        }

        // check left and right next
        if (x > 0){
            if (special_chars.includes(table[y][x-1])) is_special = true
        }
        if (x + length < table[0].length - 1){
            if (special_chars.includes(table[y][x+length])) is_special = true
        }
        // console.log(`table[${y}][${x}]=${table[y][x]} value is ${value} special: ${is_special}`)
        if (is_special) part1 += value

        // kick pointer ahead
        x += value.toString().length
    }
}

console.log(part1)



// Kirjava part 1:
// I=document.body.innerText,A=0,I.replace(/\d+/g,(n,e)=>{for(i=a=0;3>i;a+=I.substring(e-=[1,-141,282][i++],e+([]+n).length+2));/[^\d\.\n]/.test(a)&&(A+=+n)}),A


// Kirjava part 2:
// A=128;I=document.body.innerText.replace(/\*/g,_=>String.fromCharCode(A++))
// A=0;G={};I.replace(/\d+/g,(n,e)=>{
//    for(i=a=0;3>i;a+=I.substring(e-=[1,-141,282][i++],e+([]+n).length+2))
//    (V=a.match(/[\u0080-\u03FF]/)?.[0])&&(G[V]?A+=G[V]*n:G[V]=n)
// }),A
