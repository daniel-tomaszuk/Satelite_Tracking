function scaleX(lati, xMax) {
    xPx = (xMax / 360) * lati + 0.5 * xMax;
    return xPx
};

function scaleY(longi, yMax) {
    yPx = -1 * (yMax / 180) * longi + 0.5 * yMax;
    return yPx;
};

document.addEventListener("DOMContentLoaded", function(){
    var div = document.querySelector('#box');


    positionInfo = div.getBoundingClientRect();

    console.log(sats_json);
    // loop through actual positions
    for (var i = 0; i < sats_json.length; i++){
        var satIcon = $('<img />', {
          id: 'SatId'+i,
          src: 'static/Sat_Track/sat.png',
          alt: 'MySat'+i,
        });
        satIcon.css('display','none');

        satIcon.css('width', "2%");
        satIcon.css('height', "4%");
        satIcon.css('position','absolute');
        satIcon.css('top','0px');
        satIcon.css('left','0px');

        satIcon.appendTo($('#box'));

        xPx = scaleX(sats_json[i].fields.longi, positionInfo.width);
        yPx = scaleY(sats_json[i].fields.lati, positionInfo.height);
        satIcon.css('left', xPx+"px");
        satIcon.css('top', yPx+"px");
        satIcon.css('display', '');


        for (var j=0; j < sats_hist_json.length; j++){
            // find history objects for actual object (i-th object)
            if (sats_hist_json[j].fields.name === sats_json[i].fields.name){
                var satHistIcon = $('<img />', {
                    id: 'SatHistId'+ sats_json[i].fields.name + j,
                    src: 'static/Sat_Track/square.png',
                    alt: 'MySatHist'+sats_json[i].fields.name + j,
                });

                satHistIcon.css('width', "0.25%");
                satHistIcon.css('height', "0.5%");
                satHistIcon.css('position','absolute');
                satHistIcon.css('top','0px');
                satHistIcon.css('left','0px');
                satHistIcon.appendTo($('#box'));

                xPx = scaleX(sats_hist_json[j].fields.longi, positionInfo.width);
                yPx = scaleY(sats_hist_json[j].fields.lati, positionInfo.height);
                satHistIcon.css('left', xPx+"px");
                satHistIcon.css('top', yPx+"px");
                satHistIcon.css('display', '');

            };

        };
    };

    console.log("SATS HIST JSON");
    console.log(sats_hist_json);









//    console.log("Map size");
////  Y - dlugosc geograficzna:
//    console.log("height Y:")
//    console.log(positionInfo.height);
////  X - szerokosc geograficzna
//    console.log("width X:")
//    console.log(positionInfo.width);
//
//    console.log(sats_json);
//
//    console.log(sats_json[0].fields.name);
//    console.log("Y:")
//    console.log(sats_json[0].fields.lati);  // szerokosc geograficzna y
//    console.log("X:")
//    console.log(sats_json[0].fields.longi); // dlugosc geograficzna x
//    console.log(sats_json[0].fields.alti);
//





//
//    console.log("Xpx");
//    console.log(xPx);
//    console.log("Ypx");
//    console.log(yPx);
//    console.log("X_max:")
//    console.log(positionInfo.width)
//    console.log("Y_max:")
//    console.log(positionInfo.height)



//    console.log(satIcon)






//#################################################################
    console.log();
    console.log(div.offsetTop);

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

