// part 1
document.body.innerText.trim().split(/\n/).map(a=>a.match(/(\d+)-(\d+) (\w): (\w+)/)).reduce((a,v)=>a+(l=(v[4].split(v[3]).length)-1,r=v[1]<=l&&l<=v[2]),0)

// part 2
document.body.innerText.trim().split(/\n/).map(a=>a.match(/(\d+)-(\d+) (\w): (\w+)/)).reduce((a,v)=>a+((v[4][+v[1]-1]==v[3])+(v[4][+v[2]-1]==v[3])==1),0)
