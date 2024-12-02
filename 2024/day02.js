// part 1
document.body.innerText.trim().split('\n').map(l=>l.split(/\s+/).map(d=>+d)).map((l,i)=>{for(j=0;j<l.length-2;j++){d1=l[j]-l[j+1];d2=l[j+1]-l[j+2];if(!d1||!d2||!(d1>0==d2>0)||Math.abs(d1)>3||Math.abs(d2)>3){return 0}};return 1}).reduce((a,v)=>a+v,0)

// part 2
function testSafety(layer) {
    for (i = 0; i < layer.length - 2; i++) {
        diff1 = layer[i] - layer[i + 1];
        diff2 = layer[i + 1] - layer[i + 2];
        if (!diff1) return 0;
        if (!diff2) return 0;
        if (!(diff1 > 0 == diff2 > 0)) return 0;
        if (Math.abs(diff1) > 3) return 0;
        if (Math.abs(diff2) > 3) return 0;
    }
    return 1;
}

document.body.innerText
    .trim()
    .split('\n')
    .map((l) => l.split(/\s+/).map((d) => +d))
    .map((l, i) => {
        if (testSafety(l)) {
            return 1;
        } else {
            for (j = 0; j < l.length; j++) {
                without = [...l.slice(0, j), ...l.slice(j + 1)];
                if (testSafety(without)) return 1;
            }
            return 0
        }
    })
    .reduce((a, v) => a + v, 0);

