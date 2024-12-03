//part 1
f=0;x=0;y=0;d=0;t=d=>f=(f+(d=="L"?-1:1))&0x3;a=[(n)=>y=y+n,(n)=>x=x+n,(n)=>y=y-n,(n)=>x=x-n];Array.from(document.body.innerText.matchAll(/(.)(\d+)/g)).map(m=>(t(m[1]),a[f](+m[2]))),Math.abs(x)+Math.abs(y) 


//part 2

h = [];
f = 0;
x = 0;
y = 0;
d = 0;
z = 1;
t = (d) => (f = (f + (d == 'L' ? -1 : 1)) & 0x3);
a = [() => y++, () => x++, () => y--, () => x--];
Array.from(document.body.innerText.matchAll(/(.)(\d+)/g)).every(
    (m) => (
        console.log(x, y),
        t(m[1]),
        [...Array(+m[2])]
            .map(
                () =>
                    h.filter((s) => s == x + ',' + y).length < 2 &&
                    (a[f](), h.push(x + ',' + y)),
            )
            .pop()
    ),
),
    Math.abs(x) + Math.abs(y);

