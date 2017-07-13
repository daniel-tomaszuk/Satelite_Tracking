function scaleX(lati, xMax){
    /**
    * Scale geographical latitude into x [px] coordinate.
    * @param {number} lati - The latitude value in degrees.
    * @param {number} xMax - The max X dimension of world map image.
    */
    var xPx = (xMax / 360) * lati + 0.5 * xMax;
    return xPx
};


function scaleY(longi, yMax){
    /**
    * Scale geographical longitude into y [px] coordinate.
    * @param {number} longi - The longitude value in degrees.
    * @param {number} yMax - The max Y dimension of map image.
    */
    var yPx = -1 * (yMax / 180) * longi + 0.5 * yMax;
    return yPx;
};


function divPoint(size, color){
    /**
    * Create point as DIV tag.
    * @param {string} size - size of the point. Same as in CSS.
    * @param {string} color - Color of the point. Same as in CSS.
    */
    var point = $('<div>');
    var size = '3px';
    $(point)
        .css('position', 'absolute')
        .css('width', size)
        .css('height', size)
        .css('background-color', color);
    return $(point)
};


function createLineElement(x, y, length, angle, color){
    /**
    * Draws line element on the image.
    * @param {number} x - Absolute x position of the line beginning.
    * @param {number} y - Absolute y position of the line beginning.
    * @param {number} length - Length of the line.
    * @param {number} angle - Angle of the line.
    * @param {string} color - Color of the line.
    */
    var line = document.createElement("div");
    var styles = 'border: 1px solid;'
               + 'width: ' + length + 'px; '
               + 'height: 0px; '
               + '-moz-transform: rotate(' + angle + 'rad); '
               + '-webkit-transform: rotate(' + angle + 'rad); '
               + '-o-transform: rotate(' + angle + 'rad); '
               + '-ms-transform: rotate(' + angle + 'rad); '
               + 'position: absolute; '
               + 'top: ' + y + 'px; '
               + 'left: ' + x + 'px; '
               + 'color:' + color +';';
    line.setAttribute('style', styles);
    return line;
};


function createLine(x1, y1, x2, y2, color) {
    /**
    * Counts parameters required for line drawing.
    * @param {number} x1 - Absolute x position of the line beginning.
    * @param {number} y1 - Absolute y position of the line beginning.
    * @param {number} x2 - Absolute x position of the line ending.
    * @param {number} y2 - Absolute y position of the line ending.
    * @param {string} color - Color of the line.
    */
    var a = x1 - x2;
    var b = y1 - y2;
    var c = Math.sqrt(a * a + b * b);

    var sx = (x1 + x2) / 2;
    var sy = (y1 + y2) / 2;

    var x = sx - c / 2;
    var y = sy;

    var alpha = Math.PI - Math.atan2(-b, a);
    return createLineElement(x, y, c, alpha, color);
};


document.addEventListener("DOMContentLoaded", function(){
    var div = document.querySelector('#box');
    // get dimensions of map image
    positionInfo = div.getBoundingClientRect();
    // loop through actual positions
    // sats_json from map view in django
    // main loop for every chosen satellite
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
                var point = divPoint('3px', color);
                $(point).appendTo($('#box'));
                // count where to put past position icon
                xPx = scaleX(sats_hist_json[j].fields.longi, positionInfo.width);
                yPx = scaleY(sats_hist_json[j].fields.lati, positionInfo.height);
                // put past position icon
                $(point).css('left', xPx+"px");
                $(point).css('top', yPx+"px");
                $(point).css('display', '');
                // push history x and y coordinates in the coordinates list
                point_list.push([xPx, yPx]);
            };
        };

        for (var k=0; k < parseInt((point_list.length)) - 1; k++){
//            console.log(point_list[k][0]);

            var x1 = parseInt(point_list[k][0])
            var y1 = parseInt(point_list[k][1])
            var x2 = parseInt(point_list[k+1][0])
            var y2 = parseInt(point_list[k+1][1])
            // count distance between two points
            var dist = Math.sqrt(Math.pow((x1 - x2), 2) +
                                 Math.pow((y1 - y2), 2));
            // draw line if the distance is close enough
            if (dist < 100){
                div.appendChild(createLine(x1, y1, x2, y2, color));
            };
        };

        // legend
        var legend = $('#legend');
        var legendText = $('<p>');
        $(legendText).text(sats_json[i].fields.name + " ");
        $(legendText).css('color', color);
        $(legendText).css('font-weight', 'bold');
        $(legendText).css('display', 'inline');
        $(legendText).appendTo($(legend));

    };

    var globalX = document.querySelector('#globalX');
    var globalY = document.querySelector('#globalY');
    var localX = document.querySelector('#localX');
    var localY = document.querySelector('#localY');

    div.addEventListener('mousemove', function(event){
       localX.innerHTML = event.clientX - div.offsetLeft;
       localY.innerHTML = event.clientY - div.offsetTop;
    });
    document.addEventListener('mousemove', function(event){
        globalX.innerHTML = event.screenX;
        globalY.innerHTML = event.screenY;
    });

});

