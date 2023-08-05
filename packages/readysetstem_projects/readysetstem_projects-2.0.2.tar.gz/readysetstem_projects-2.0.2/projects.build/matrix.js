function circle(svg, x, y, r, color, strokeWidth) {
    colormap = {
        '-' : 'transparent',
        '0' : 'hsl(360,100%,100%)',
        '1' : 'hsl(360,100%,97%)',
        '2' : 'hsl(360,100%,93%)',
        '3' : 'hsl(360,100%,90%)',
        '4' : 'hsl(360,100%,87%)',
        '5' : 'hsl(360,100%,83%)',
        '6' : 'hsl(360,100%,80%)',
        '7' : 'hsl(360,100%,77%)',
        '8' : 'hsl(360,100%,73%)',
        '9' : 'hsl(360,100%,70%)',
        'A' : 'hsl(360,100%,67%)',
        'B' : 'hsl(360,100%,63%)',
        'C' : 'hsl(360,100%,60%)',
        'D' : 'hsl(360,100%,57%)',
        'E' : 'hsl(360,100%,53%)',
        'F' : 'hsl(360,100%,50%)',
    };

    var circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', x.toString());
    circle.setAttribute('cy', y.toString());
    circle.setAttribute('r', (r).toString());
    circle.setAttribute('fill', colormap[color]);
    circle.setAttribute('stroke', 'black');
    circle.setAttribute('stroke-width', strokeWidth);
    svg.appendChild(circle);
    console.log(x, y, r-4, colormap[color]);
}

chainedOnload(function() {
    var R = 6;
    var W = 1;
    var matrixes = document.getElementsByClassName('matrix');
    for (i = 0; i < matrixes.length; i++) {
        var div = document.createElement('div');
        var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('height', String(R*16+2*W));
        svg.setAttribute('width', String(R*16+2*W));

        var bitmap = matrixes[i].innerHTML;
        var lines = bitmap.split('\n');
        for (y = 0; y < lines.length; y++) {
            if (lines[y].length == 0) continue;
            for (x = 0; x < lines[y].length; x++) {
                circle(svg, W+2*x*R+R, W+2*y*R+R, R, lines[y][x], W);
            }
        }
        div.appendChild(svg);
        matrixes[i].parentNode.insertBefore(div, matrixes[i]);
    }
    /*
     * ASCII matrixes must be removed in a separate loop - if they are remove
     * while processing them, the will not be all removed.
     */
    for (i = matrixes.length - 1; i >= 0; i--) {
        matrixes[i].parentNode.removeChild(matrixes[i]);
    }

});


