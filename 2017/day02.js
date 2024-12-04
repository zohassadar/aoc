//part 1
document.body.innerText.trim().split(/\n/).reduce((a,v)=>(n=v.split(/\s+/),a+Math.max(...n)-Math.min(...n)),0) 

// part 2
t = 0;
document.body.innerText
    .trim()
    .split(/\n/)
    .map(
        (v) => (
            (n = v.split(/\s+/).sort((a, b) => b - a)),
            n.forEach((o, i) =>
                n.slice(i + 1).forEach((p) => !(o % p) && (t += o / p)),
            )
        ),
    );
t;

