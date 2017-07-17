var scaleX = function(lati, xMax){
    /**
    * Scale geographical latitude into x [px] coordinate.
    * @param {number} lati - The latitude value in degrees.
    * @param {number} xMax - The max X dimension of world map image.
    */
    var xPx = (xMax / 360) * lati + 0.5 * xMax;
    return xPx
};

var scaleY = function(longi, yMax){
    /**
    * Scale geographical longitude into y [px] coordinate.
    * @param {number} longi - The longitude value in degrees.
    * @param {number} yMax - The max Y dimension of map image.
    */
    var yPx = -1 * (yMax / 180) * longi + 0.5 * yMax;
    return yPx;
};

var mapDivPoint = function(size, color){
    /**
    * Create point as mapDiv tag.
    * @param {string} size - size of the point. Same as in CSS.
    * @param {string} color - Color of the point. Same as in CSS.
    */
    var point = $('<mapDiv>');
    var size = '3px';
    $(point)
        .css('position', 'absolute')
        .css('width', size)
        .css('height', size)
        .css('background-color', color);
    return $(point)
};

var createLineElement = function(x, y, length, angle, color){
    /**
    * Draws line element on the image.
    * @param {number} x - Absolute x position of the line beginning.
    * @param {number} y - Absolute y position of the line beginning.
    * @param {number} length - Length of the line.
    * @param {number} angle - Angle of the line.
    * @param {string} color - Color of the line.
    */
    var line = document.createElement('div');
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

var createLine = function(x1, y1, x2, y2, color) {
    /**
    * Counts parameters required for line drawing.
    * https://stackoverflow.com/questions/4270485/drawing-lines-on-html-page
    * @param {number} x1 - Absolute x position of the line beginning.
    * @param {number} y1 - Absolute y position of the line beginning.
    * @param {number} x2 - Absolute x position of the line ending.
    * @param {number} y2 - Absolute y position of the line ending.
    * @param {string} color - Color of the line.
    */
    // a^2 + b^2 = c^2
    var a = x1 - x2;
    var b = y1 - y2;
    var c = Math.sqrt(a * a + b * b);
    // coordinate of the middle point in c line
    var sx = (x1 + x2) / 2;
    var sy = (y1 + y2) / 2;

    var x = sx - c / 2;
    var y = sy;

    var alpha = Math.PI - Math.atan2(-b, a);
    return createLineElement(x, y, c, alpha, color);
};


// one ajax to rule them all
var modifyDB = function(myType, myData, url, successFunction){
    /**
    * ajax function for DB modifications.
    * @myType {string} myType - type of action that ajax should do: GET only
    * @myData {string} myData  - json data to send, only for POST action
    * @url {string} url - string which determines where to connect in REST API
    * @mapDiv {object} mapDiv - map div tag from map.html
    * @successFunction {object} successFunction - function to fire when ajax
                                                  successfully finish given
                                                  action
    */

    $.ajax({
        url: url,
        data: myData, // data to send to the server
        type: myType, // GET, POST, DELETE, PUT
        crossDomain: false,
        dataType: 'json',
        async: true, // TO DO: working with true
        success: function(response){
            successFunction(response);  // function to fire when success
        },
        error: function(response){
            console.log('Ajax Fail!\n' + response);
        }
    });
};

// ajax success function for past positions
var ajaxGetPast = function(response){
    /**
    * Takes satellites past positions form response and draws trajectory of sat
    * @response {string} response - json with DB server response
    */
    var mapDiv = document.querySelector('#box');
    console.log('Success data download!');
    var positionInfo = mapDiv.getBoundingClientRect();

    // find how many unique satellite names is in the response
    var unique_names = [];
    for (var i = 0; i < response.length; i++){
        // if no name in unique names list, add name to list
        if (!(unique_names.includes(response[i].name))){
            unique_names.push(response[i].name);
        };
    };

    // main loop for every chosen satellite
    for (var i = 0; i < unique_names.length; i++){
        var point_list = [];
        // past data points color
        var color = '#' + (Math.random()*0xFFFFFF<<0).toString(16);
        // history points of i-th satellite
        for (var j = 0; j < response.length; j++){
        // find history objects for satellite with name i-th unique name
            if (response[j].name === unique_names[i]){
                var point = mapDivPoint('3px', color);
                $(point).appendTo($('#box'));
                // count where to put past position icon
                var xPx = scaleX(response[j].longi,
                                 positionInfo.width);
                var yPx = scaleY(response[j].lati,
                                 positionInfo.height);
                // put past position icon
                $(point).css('left', xPx + "px");
                $(point).css('top', yPx + "px");
                $(point).css('display', '');
                // push history x and y coordinates in the coordinates list
                point_list.push([xPx, yPx]);
            };
        };

        for (var k =0 ; k < parseInt((point_list.length)) - 1; k++){
        //console.log(point_list[k][0]);

            var x1 = parseInt(point_list[k][0])
            var y1 = parseInt(point_list[k][1])
            var x2 = parseInt(point_list[k+1][0])
            var y2 = parseInt(point_list[k+1][1])
            // count distance between two points
            var dist = Math.sqrt(Math.pow((x1 - x2), 2) +
                                 Math.pow((y1 - y2), 2));
            // draw line if the distance is close enough
            if (dist < 100){
                mapDiv.appendChild(createLine(x1, y1, x2, y2, color));
            };
        };
        // legend
        var legend = $('#legend');
        var legendText = $('<p>');
        $(legendText).text(unique_names[i] + " ");
        $(legendText).css('color', color);
        $(legendText).css('font-weight', 'bold');
        $(legendText).css('display', 'inline');
        $(legendText).appendTo($(legend));
    };
};

// ajax success functions for most recent (actual) positions
var ajaxGetPresent = function(response){
    /**
    * Gets most recent satellites positions and puts sat icon in that position
    * success function for ajax GET action
    * @response {string} response - json with DB server response
    */
    var mapDiv = document.querySelector('#box');
    console.log('Success data download!');
    var positionInfo = mapDiv.getBoundingClientRect();

    // find how many unique satellite names there is in the response
    var unique_names = [];
    for (var i = 0; i < response.length; i++){
        // if no name in unique names list, add name to list
        if (!(unique_names.includes(response[i].name))){
            unique_names.push(response[i].name);
        };
    };

    var point_list = [];
    // main loop for every chosen satellite
        for (var l = 0; l < response.length; l++){
            var satIcon = $('<img />');
            var dataContent = "Longi: "+ (response[l].longi).toFixed(2) +
                              '<br>' +
                              "Lati: " + (response[l].lati).toFixed(2) +
                              '<br>' +
                              "Alti: " + (response[l].alti.toFixed(2))

            $(satIcon).attr('class', 'pop');
            $(satIcon).attr('id', 'SatId_' + i);
            $(satIcon).attr('src', 'static/Sat_Track/sat.png');
            $(satIcon).attr('alt', 'Sat' + i);
            $(satIcon).attr('data-toggle', 'popover');
            $(satIcon).attr('data-trigger', 'focus');
            $(satIcon).attr('data-html', true);
            $(satIcon).attr('title', response[l].name);
            $(satIcon).attr('data-content', dataContent);
            $(satIcon).css('display','none');
            $(satIcon).css('width', "2%");
            $(satIcon).css('height', "4%");
            $(satIcon).css('position', 'absolute');
            $(satIcon).css('top', '0px');
            $(satIcon).css('left', '0px');

            // put the most actual satellite position on map
            // count where to put the most actual satellite position
            xPx = scaleX(response[l].longi, positionInfo.width);
            yPx = scaleY(response[l].lati, positionInfo.height);
            $(satIcon).css('left', xPx - 10 + "px");
            $(satIcon).css('top', yPx - 20 + "px");
            $(satIcon).css('display', '');
            $(satIcon).css('z-index', '10');
            $(satIcon).appendTo($('#box'));
        };

    // popovers
    $(".pop").each(function() {
        $(this).on('mouseover', function(event){
            $(this).popover('show');
        });

        $(this).on('mouseout', function(){
            $(this).popover('hide');
        });

        $(this).on('hide.bs.popover', function(){
            $(document).off('click.popover');
        });
    });
};


// GET data from DB by means of asynchronous ways ..
// 18ms < 50%; 25ms -> 100% for localhost
var getSatHistory = function(url){
    // url base to GET REST API past points + url (for sats and dates)
    var urlBase = 'http://localhost:8000/history/';
    modifyDB('GET', '{}', urlBase + url, ajaxGetPast);
};


// GET data from DB by means of asynchronous ways ..
// 18ms < 50%; 25ms -> 100% for localhost
var getSatPresent = function(url){
    // urlBase to GET REST API present points)
    var urlBase = 'http://localhost:8000/satellites_list/';
    modifyDB('GET', '{}', urlBase + url, ajaxGetPresent);
};


document.addEventListener("DOMContentLoaded", function(){
    var url = '';
    var mapDiv = document.querySelector('#box');
    var satForm = $('#satellite_form');
    $(satForm).on('submit', function(event){
        // get required information from satellites.html for API GET prepare
//         event.preventDefault();
        // var for GET request
        var selectDate = $('#select_date');
        var selectSat = $(':checkbox');
        var satCheckList = [];
        url = '';
        $(selectSat).each(function(){
            if ($(this).prop('checked')){
                satCheckList.push(($(this).val()));
            };
        });
        console.log($(selectDate).val())
        console.log(satCheckList);
        url += '?the_date=';
        url += $(selectDate).val();
        for (var m = 0; m < satCheckList.length; m++){
        // replace spaces with "+" and concatenate GET request for API
            url += '&' + satCheckList[m].replace(/ /g,"+") +
                   '=' + satCheckList[m].replace(/ /g,"+");
        };
        // create a cookie to store url for later use in /map page
        var date = new Date();
        // lifetime: 1h
        date.setTime(date.getTime() + (3600 * 1000));
        Cookies.set('url', url, { expires: date });
    });

    url = Cookies.get('url');
//    Cookies.remove('url');
    if (mapDiv){
        // GET present point from REST API
        getSatPresent(url);
        // GET past point from REST API
        getSatHistory(url);

        var globalX = document.querySelector('#globalX');
        var globalY = document.querySelector('#globalY');
        var localX = document.querySelector('#localX');
        var localY = document.querySelector('#localY');

        mapDiv.addEventListener('mousemove', function(event){
           localX.innerHTML = event.clientX - mapDiv.offsetLeft;
           localY.innerHTML = event.clientY - mapDiv.offsetTop;
        });
        document.addEventListener('mousemove', function(event){
            globalX.innerHTML = event.screenX;
            globalY.innerHTML = event.screenY;
        });
    };
});

