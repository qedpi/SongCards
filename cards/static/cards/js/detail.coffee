shift = (s) ->
  s.toUpperCase()


$ ->
  #alert('all ready')

  temp = $('#test-case').text()
  $('#lyrics').text (temp.split '\n').join('+')

  ###

  $('#toggle-favorite').on 'Submit', (e) ->
    e.preventDefault()
    alert 'Favorited!'
    toggle_favorite
  ###


  $('#is_sharable').change ->
    disable_status = if ($(@).prop 'checked') then 'enable' else 'disable'
    $('#share_with').bootstrapToggle disable_status
    $('#share_link').prop('disabled', not $('#share_link').prop 'disabled')

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

