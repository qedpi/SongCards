$ ->
  local_pathname = window.location.pathname

  #if local_pathname == '/cards/public/'

  #$('#toggle-practice-browse').attr('data-on', 'hey') #bootstrapToggle({on: 'browse me', off: 'bah'}

  $('#toggle-practice-browse').change ->
    goto = '/cards/practice/'
    if local_pathname == '/cards/practice/'
      goto = '/cards/public/'
    #else if local_pathname == '/cards/public/'

    window.location.href = goto

###
$ ->
  practice_browse_state = sessionStorage.getItem('practice_browse')

    if practice_browse_state == 'false' # browse mode: turn button off
      $('#toggle-practice-browse').change ->
        sessionStorage.setItem('practice_browse', 'true')
        window.location.href = '/cards/practice'
    else
      $(@).bootstrapToggle 'toggle'
      $('#toggle-practice-browse').change ->
        sessionStorage.setItem('practice_browse', 'false')
        window.location.href = '/cards/public'
###

###
$ ->
  practice_browse_state = sessionStorage.getItem('practice_browse')
  alert practice_browse_state
  unchanged = true
  if practice_browse_state == 'false'
    $('#toggle-practice-browse').bootstrapToggle 'off'
    alert 'swithed off'
    unchanged = false


  # toggle practice vs browse
  $('#toggle-practice-browse-href').click ->

    if unchanged
      sessionStorage.setItem('practice_browse', (if practice_browse_state then 'false' else 'true'))
      alert 'changed by function'
      if ($(@).prop 'checked') == 'false' # Practice
        window.location.href = '/cards/public'
      else
        window.location.href = '/cards/practice'
    else
      unchanged = true

        #$(@).bootstrapToggle 'off'
        #$(@).attr(class, 'white fa fa-')
###

