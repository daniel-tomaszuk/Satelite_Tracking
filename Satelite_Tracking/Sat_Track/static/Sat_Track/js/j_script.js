function scaleX(lati, xMax) {
    xPx = (xMax / 360) * lati + 0.5 * xMax;
    return xPx
};


function scaleY(longi, yMax) {
    yPx = -1 * (yMax / 180) * longi + 0.5 * yMax;
    return yPx;
};


function createLineElement(x, y, length, angle) {
    var line = document.createElement("div");
    var styles = 'border: 1px solid black; '
               + 'width: ' + length + 'px; '
               + 'height: 0px; '
               + '-moz-transform: rotate(' + angle + 'rad); '
               + '-webkit-transform: rotate(' + angle + 'rad); '
               + '-o-transform: rotate(' + angle + 'rad); '
               + '-ms-transform: rotate(' + angle + 'rad); '
               + 'position: absolute; '
               + 'top: ' + y + 'px; '
               + 'left: ' + x + 'px; ';
    line.setAttribute('style', styles);
    return line;
};


function createLine(x1, y1, x2, y2) {
    var a = x1 - x2,
        b = y1 - y2,
        c = Math.sqrt(a * a + b * b);

    var sx = (x1 + x2) / 2,
        sy = (y1 + y2) / 2;

    var x = sx - c / 2,
        y = sy;

    var alpha = Math.PI - Math.atan2(-b, a);

    return createLineElement(x, y, c, alpha);
};









document.addEventListener("DOMContentLoaded", function(){
    var div = document.querySelector('#box');
    // get dimensions of map image
    positionInfo = div.getBoundingClientRect();
    // loop through actual positions
    // sats_json from map view in django
    for (var i = 0; i < sats_json.length; i++){
        var point_list = [];
        // past data points color
        var color = '#'+(Math.random()*0xFFFFFF<<0).toString(16);

        var satIcon = $('<img />');
        var dataContent = "Longi: "+ (sats_json[i].fields.longi).toFixed(2) +
                          '<br>' +
                          "Lati: " + (sats_json[i].fields.lati).toFixed(2) +
                          '<br>' +
                          "Alti: " + (sats_json[i].fields.alti.toFixed(2))

        $(satIcon).attr('id', 'SatId_'+i);
        $(satIcon).attr('src', 'static/Sat_Track/sat.png');
        $(satIcon).attr('alt', 'Sat'+i);
        $(satIcon).attr('data-toggle', 'popover');
        $(satIcon).attr('data-trigger', 'focus');
        $(satIcon).attr('data-html', true);
        $(satIcon).attr('title', sats_json[i].fields.name);
        $(satIcon).attr('data-content', dataContent);
        $(satIcon).css('display','none');
        $(satIcon).css('width', "2%");
        $(satIcon).css('height', "4%");
        $(satIcon).css('position', 'absolute');
        $(satIcon).css('top', '0px');
        $(satIcon).css('left', '0px');
        $(satIcon).appendTo($('#box'));
        // count where to put the most actual satellite position
        xPx = scaleX(sats_json[i].fields.longi, positionInfo.width);
        yPx = scaleY(sats_json[i].fields.lati, positionInfo.height);
        // put the most actual satellite position on map
        $(satIcon).css('left', xPx - 10 + "px");
        $(satIcon).css('top', yPx - 20 + "px");
        $(satIcon).css('display', '');

        $(satIcon).on('mouseover', function(event){
            setTimeout(function(){
                satIcon.popover('show');
            }, 100);

            $(satIcon).on('shown.bs.popover', function(){
                    $(document).on('click.popover', function() {
                        satIcon.popover('hide');
                    });
            });

            $(satIcon).on('hide.bs.popover', function(){
                    $(document).off('click.popover');
            });
        });


        // history points of i-th satellite
        for (var j=0; j < sats_hist_json.length; j++){
            // find history objects for actual object (i-th object)
            if (sats_hist_json[j].fields.name === sats_json[i].fields.name){
                var point = $('<div>');
                var size = '3px';
                $(point)
                    .css('position', 'absolute')
                    .css('width', size)
                    .css('height', size)
                    .css('background-color', color);

                $(point).appendTo($('#box'));
                // count where to put past position icon
                xPx = scaleX(sats_hist_json[j].fields.longi, positionInfo.width);
                yPx = scaleY(sats_hist_json[j].fields.lati, positionInfo.height);
                // put past position icon
                $(point).css('left', xPx+"px");
                $(point).css('top', yPx+"px");
                $(point).css('display', '');



                // TO DO: connect all points
                point_list.push([xPx, yPx]);
            };
        };
        console.log(point_list);
        for (var k=0; k < parseInt((point_list.length)) - 1; k++){
            console.log(point_list[k][0]);





            div.appendChild(createLine(parseInt(point_list[k][0]),
                                       parseInt(point_list[k][1]),
                                       parseInt(point_list[k+1][0]),
                                       parseInt(point_list[k+1][1])));

        };

    };


    var globalX = document.querySelector('#globalX');
    console.log(globalX);
    var globalY = document.querySelector('#globalY');

    var localX = document.querySelector('#localX');
    var localY = document.querySelector('#localY');

//    console.log(div);
//    console.log(globalX);
    div.addEventListener('mousemove', function(event){
       localX.innerHTML = event.clientX - div.offsetLeft;
       localY.innerHTML = event.clientY - div.offsetTop;
    });

    document.addEventListener('mousemove', function(event){
        globalX.innerHTML = event.screenX;
        globalY.innerHTML = event.screenY;
    });

});

