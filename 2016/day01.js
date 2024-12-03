//part 1
f=0;x=0;y=0;d=0;t=d=>f=(f+(d=="L"?-1:1))&0x3;a=[(n)=>y=y+n,(n)=>x=x+n,(n)=>y=y-n,(n)=>x=x-n];Array.from(document.body.innerText.matchAll(/(.)(\d+)/g)).map(m=>(t(m[1]),a[f](+m[2]))),Math.abs(x)+Math.abs(y) 
