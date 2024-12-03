//part 1
document.body.innerText.trim().split(/\n/).reduce((a,v)=>(n=v.split(/\s+/),a+Math.max(...n)-Math.min(...n)),0) 
