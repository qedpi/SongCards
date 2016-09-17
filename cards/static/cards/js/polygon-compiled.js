'use strict';

/**
 * Created by qedpi on 9/17/2016.
 */

var drawdodo = function drawdodo(x) {
    var canvas = document.getElementById('shapes');
    var ctx = canvas.getContext('2d');

    //var poly = [5, 5, 100, 50, 50, 100, 10, 90];
    var halfx = Math.floor(x / 2);
    var poly = [halfx, 0, halfx + 1, 1, halfx + 2, 2, x, halfx, x - 1, halfx - 1, x - 2, halfx - 2, halfx, x];

    //var poly = [5, 5, 100, 50, 50, 100, 10, 90];

    // copy array
    var shape = poly.slice(0);

    ctx.fillStyle = '#f00';
    ctx.beginPath();
    ctx.moveTo(shape.shift(), shape.shift());
    while (shape.length) {
        ctx.lineTo(shape.shift(), shape.shift());
    }
    ctx.closePath();
    ctx.fill();
};

drawdodo(50);

/*
var canvas = $('shapes');
var context = canvas.getContext('2d');
context.fillStyle = '#f00';
context.beginPath();
context.moveTo(0, 0);
context.lineTo(100, 50);
context.lineTo(50, 100);
context.lineTo(100, 90);
context.lineTo(0, 90);
context.closePath();
context.fill();*/

/*
alert('ready');
var context = $("#polypoly");
var context = context.getContext("2d");

context.fillStyle = "FF0000";
context.fillRect(0,0,150,75);
*/
//context.width = window.innerWidth;
//context.height = window.innerHeight;

//alert('done');

/*
$( () => {

    /*context.fillStyle = '#f00';

    context.fillRect(10, 10, 1000, 1000);
    context.save();

    context.beginPath();
    context.moveTo(0, 0);
    context.lineTo(100, 50);
    context.lineTo(50, 100);
    context.lineTo(100, 90);
    context.lineTo(0, 90);
    context.closePath();
    context.fill();
});
*/

//# sourceMappingURL=polygon-compiled.js.map