a=[];b=[];document.body.innerText.trim().split('\n').map(c=>c.split(/\s+/)).map(d=>(a.push(+d[0]),b.push(+d[1])));a.sort();b.sort();a.map((e,i)=>[e,b[i]]).reduce((a,v)=>a+Math.abs(v[0]-v[1]),0)

a=[];b=[];document.body.innerText.trim().split('\n').map(c=>c.split(/\s+/)).map(d=>(a.push(+d[0]),b.push(+d[1])));a.reduce((a,z)=>a+b.filter(c=>c==z).length*z,0)
