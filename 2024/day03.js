//part 1
Array.from(document.body.innerText.matchAll(/mul\((\d+),(\d+)\)/g), m=>m[1]*m[2]).reduce((a,v)=>a+v,0)
