
const fs = require('fs');
data = fs.readFileSync("day05.input", "utf-8")

const mapperFinder = {
    things: [],
    crunch: function (num) {
        for ([trans, start, range] of this.things) {
            if (num >= start && num < start + range){
                return trans + (num-start)
            }
        }
        return num
    },
  };
  
get_finder = (mapper) => Object.create(mapperFinder, { things: { value: mapper} });

chunks = data.split('map:')
seeds = [...chunks[0].matchAll(/\d+/g)].map((d) => +d)
maps = chunks.slice(1,).map((chunk) => ([...chunk.matchAll(/^(\d+) (\d+) (\d+)$/mg)].map((m) => [+m[1], +m[2], +m[3]]))).map((m) => get_finder(m))


console.log(Math.min(...seeds.map((seed) => maps.reduce((a, m) => m.crunch(a), seed))))


