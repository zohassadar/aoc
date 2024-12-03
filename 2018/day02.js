// part 1
x=0;y=0;document.body.innerText.trim().split(/\n/).map(l=>(d={},[...Array(l.length)].map((c,i)=>(j=d[l[i]],d[l[i]]=j?j+1:1,l[i])),(Object.values(d).includes(2)&&x++),Object.values(d).includes(3)&&y++));x*y 


//part 2
l = document.body.innerText.trim().split(/\n/);
for (i = 0; i < l.length - 1; i++) {
    for (j = i + 1; j < l.length; j++) {
        c = 0;
        m = Math.max(l[i].length, l[j].length);
        w = -1;
        for (k = 0; k < m; k++) {
            r = l[i][k] == l[j][k];
            c += r;
            r || (w = k);
        }
        m - c == 1 && console.log(l[i].slice(0, w) + l[i].slice(w + 1));
    }
}

