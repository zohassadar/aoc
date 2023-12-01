const fs = require("fs");

var number = parseInt(process.argv[2])
if (!number || number === NaN) {
    console.log("Give number")
    process.exit(1)
}

day = `day${number.toString().padStart(2, "0")}`

code = `
const fs = require('fs');
data = fs.readFileSync("${day}.input", "utf-8")

`
try {
    fs.mkdirSync(`2023/${day}`, true)
} catch (e) { }

fs.writeFileSync(`2023/${day}/${day}.js`, code)

console.log("Give input:")

// found stdin in example as 0, but this looks better
var data = fs.readFileSync(process.stdin.fd, "utf-8");

fs.writeFileSync(`2023/${day}/${day}.input`, data.trim())
