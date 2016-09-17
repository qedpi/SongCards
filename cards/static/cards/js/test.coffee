into_lines = (text) ->
  text.split('\n')

words = (line) ->
  line.split(' ')

input = "C            F         G \n
here are my lyrics yay!"

lines = into_lines input


console.log (lines)