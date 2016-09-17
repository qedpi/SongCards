### QEDPI's Latte ###

Transposer = require('chord-transposer')

$ ->

  major_to_minor =
    "Eb": "C",
    "E": "C#",
    "F": "D",
    "Gb": "Eb",
    "G": "E",
    "Ab": "F",
    "A": "F#",
    "Bb": "G",
    "B": "G#",
    "C": "A",
    "Db": "Bb",
    "D": "B"


  into_lines = (text) ->
    text.split('\n')

  words = (line) ->
    line.split(' ')

  #alert 'hello'
  # testing

  major_to_both = (key) ->
    key + '/' + major_to_minor[key] + 'm'

  set_key_to = (result) ->
    $('#lyrics').html music_format result.text
    #alert major_to_both (result.key)
    $('#new-key').val major_to_both (result.key)

  #replace_all = String.prototype.replaceAll

  music_format = (text) ->
    text.replace(/#/g, '♯').replace(/b/g, '♭')

  music_unformat = (text) ->
    text.replace(/♯/g, '#').replace(/♭/g, 'b')

  music_formatter = (sym, id) ->
    sym.replace('#', '♯').replace('b', '♭')

  transpose_by = (steps) ->
    lyrics_text = music_unformat $('#lyrics').text()
    #$('#lyrics').html Transposer.transpose(lyrics_text).fromKey('Em').up(steps)['text']
    set_key_to Transposer.transpose(lyrics_text).up(steps)

  transpose_to = (key) ->
    lyrics_text = music_unformat $('#lyrics').text()
    set_key_to Transposer.transpose(lyrics_text).toKey(key)

  # get original key
  original_key = major_to_both Transposer.transpose($('#lyrics').text()).up(0).key
  #$('#new-key').val original_key
  #$('#lyrics').
  transpose_by(0)

  $('#transpose-up').click ->
    # todo maybe have default key stored somewhere  
    transpose_by(1)

  $('#transpose-down').click ->
    transpose_by(-1)

  $('#transpose-reset').click ->
    #alert original_key.split('/')[1]
    transpose_to(original_key.split('/')[0])


  shareClipboard = new Clipboard('#share_link_passcode')


  temp = $('#test-case').text()
  #$('#lyrics').text (temp.split '\n').join('+')


  pretty =
    val: 2

  ###*
  #my docstring
  #
  ###

  ###
  scroll_lyrics = $('div.autoscrolling')
  setInterval ->
    pos = scroll_lyrics.scrollTop
    scroll_lyrics.scrollTop(++pos)
  , 100
  ###

  scroll_speed_fast = 100000
  scroll_speed_medium = 200000
  scroll_speed_slow = 400000
  scroll_speed = scroll_speed_medium

  scroll_state_off = 'fa fa-arrow-down'
  scroll_state_on = 'fa fa-pause'

  stop_animation = ->
    $('html, body').stop()

  # todo http://stackoverflow.com/questions/12164263/jquery-auto-scroll-vertically-in-a-div
  # todo make scrolling constant pace and stop at bottom
  # todo make button go to top of page if scrolled to bottom
  animate_body = ->
    #$('select').val('') # clear selected
    $('html, body').animate(
      scrollTop: $('html, body').get(0).scrollHeight,
      scroll_speed
    )

    scrollable = $('html, body')
    #if ($(scrollable).scrollTop() + $(scrollable).innerHeight()) * 1.1 >= $(scrollable).scrollHeight
    ###
    if ($(scrollable).scrollTop() + $(scrollable).innerHeight()) * .1 >= $(scrollable).scrollHeight
      $('#autoscroll-button').removeClass(scroll_state_on).addClass(scroll_state_off)
      stop_animation()
      alert 'done scrolling'
    ###
      #clearInterval(scroller);

  $('#autoscroll-button').click ->
    current = $('#autoscroll-button')
    if current.hasClass(scroll_state_off) # start autoscroll
      $('#autoscroll-button').removeClass(scroll_state_off).addClass(scroll_state_on)
      animate_body()
    else
      $('#autoscroll-button').removeClass(scroll_state_on).addClass(scroll_state_off)
      stop_animation()

  $('#autoscroll-faster').click ->
    stop_animation()
    scroll_speed *= .75
    animate_body()

  $('#autoscroll-slower').click ->
    stop_animation()
    scroll_speed *= 1.3
    animate_body()


  # toggle sharing
  $('#is_sharable').change ->
    disable_status = if ($(@).prop 'checked') then 'enable' else 'disable'
    $('#share_with').bootstrapToggle disable_status
    $('#share_link').prop('disabled', not $('#share_link').prop 'disabled')


  share_link = ''

  $('#share_link').click ->
    #alert $('#share_link_passcode').text()
    share_link = $('#share_link_passcode').text()


  $('#copy_sharelink_clipboard').click ->
    link_new = window.location.href.split('/')[0..-3].join('/') + '/' + share_link
    #alert link_new
    $('#share_link_passcode').val(window.location.href.split('/')[0..-3].join('/') + '/' + $('#share_link_passcode').val())
    $('#share_link_passcode').select()

    #$('#share_link_passcode').select()
    #alert 'copied'
    #window.clipboardData.setData("Text", share_link);
    #$temp = $('<input>')
    #$('body').append($temp)
    #$temp.val('123').select()

    document.execCommand('copy')
    #$temp.remove()
    #alert 'copied!'


  ###
  $('#toggle-favorite').on 'Submit', (e) ->
    e.preventDefault()
    alert 'Favorited!'
    toggle_favorite
  ###

#first coffeescript comment!
###first multiline coment!
###
###
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

###

