$ ->
  # toggle practice vs browse
  # TODO make global property
  $('#toggle-practice-browse').change ->
    if not $(@).prop 'checked' # Practice
      window.location.href = '/cards/public'
      $(@).bootstrapToggle 'off'
