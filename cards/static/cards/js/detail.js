// Generated by CoffeeScript 1.10.0

/* QEDPI's Latte */

(function() {
  $(function() {
    var pretty, temp;
    temp = $('#test-case').text();
    pretty = {
      val: 2
    };

    /**
    #my docstring
     *
     */
    $('#transpose-up').click(function() {
      var lyrics_text;
      lyrics_text = $('#lyrics').text();
      return $('#lyrics').html(transpose('A B C').fromKey('A').up(1).text);
    });
    return $('#is_sharable').change(function() {
      var disable_status;
      disable_status = $(this).prop('checked') ? 'enable' : 'disable';
      $('#share_with').bootstrapToggle(disable_status);
      return $('#share_link').prop('disabled', !$('#share_link').prop('disabled'));
    });

    /*
    $('#toggle-favorite').on 'Submit', (e) ->
      e.preventDefault()
      alert 'Favorited!'
      toggle_favorite
     */
  });


  /*first multiline coment!
   */


  /*
  name = 'hello bye'
  
  coffee = ->
    console.log 'coffee'
  
  double = (x) ->
    x * 2
  
  console.log name
  console.log double 5
  
  makeitdouble = (msg) ->
    answer = confirm msg
    "your answer is #{answer}"
  
  alert makeitdouble('apple')
   */

}).call(this);

//# sourceMappingURL=detail.js.map
