//part 1
Array.from(document.body.innerText.matchAll(/mul\((\d+),(\d+)\)/g), m=>m[1]*m[2]).reduce((a,v)=>a+v,0)

// part 2
f=1;Array.from(document.body.innerText.matchAll(/mul\((\d+),(\d+)\)|do(?:n't)?\(\)/g),m=>m[0][0]=="d"?m[0][2]=="n"?f=0:(f=1,0):f?m[1]*m[2]:0).reduce((a,v)=>a+v,0)
