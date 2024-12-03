// part 1
x=0;y=0;document.body.innerText.trim().split(/\n/).map(l=>(d={},[...Array(l.length)].map((c,i)=>(j=d[l[i]],d[l[i]]=j?j+1:1,l[i])),(Object.values(d).includes(2)&&x++),Object.values(d).includes(3)&&y++));x*y 
