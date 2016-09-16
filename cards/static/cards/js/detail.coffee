### QEDPI's Latte ###

$ ->
  # testing
  
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

  animate_body = ->
    #$('select').val('') # clear selected
    $('html, body').animate(
      scrollTop: $('html, body').get(0).scrollHeight,
      scroll_speed
    )

  stop_animation = ->
    $('html, body').stop()


  scroll_state_off = 'fa fa-arrow-down'
  scroll_state_on = 'fa fa-pause'

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

  $('#transpose-up').click ->
    lyrics_text = $('#lyrics').text()
    $('#lyrics').html transpose('A B C').fromKey('A').up(1).text

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

