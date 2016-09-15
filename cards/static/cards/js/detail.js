/**
 * Created by qedpi on 9/15/2016.
 */

$(document).ready(() => {

    var semitonesOffset = 0;

    $('#reset').click(() => {
        $('#lyrics').html('');
    });

    $('#transpose-up').click(function () {
        alert('doing cool stuff');
        var currentKey = 'C'; //$("#current-key").val();
        if (false && currentKey == "auto") {
            currentKey = null;
        }
        // var semitones = parseInt($("#semitones").val());
        semitonesOffset++;
        var result = transposeSemitones($("#lyrics").val(), semitonesOffset, {
            currentKey: currentKey,
            formatter: chordSpanFormatter
        });
        //var newText = result.text;
        $('#output').html(result.text.replace(/(?:\r\n|\r|\n)/g, '<br />'));
        $('#new-key').val(result.key);
    });
});

