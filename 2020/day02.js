// part 1
document.body.innerText.trim().split(/\n/).map(a=>a.match(/(\d+)-(\d+) (\w): (\w+)/)).reduce((a,v)=>a+(l=(v[4].split(v[3]).length)-1,r=v[1]<=l&&l<=v[2]),0)
