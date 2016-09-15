settings = ['again', 'easy', 'medium', 'hard']
modifiers = [0, 1, 2, 3]
multipliers = dict(zip(settings, modifiers))


used_fields = ['topic', 'front', 'back', 'card_audio', 'card_score', 'card_pic']

interaction_relations = ['I share with', 'Shares with me', 'Other users']
interaction_msg = ['', '', '']
interaction_tooltip = ['Stop Sharing', 'Browse Songs', 'Start Sharing']
interaction_button = ['danger', 'primary', 'success']
interaction_icon = ['glyphicon glyphicon-remove', 'glyphicon glyphicon-eye-open', 'glyphicon glyphicon-plus']
interaction_view = ['cards:unfriend', 'cards:friend_index', 'cards:befriend']
interaction_arg = ['shared_with', 'shares_with_me', 'unrelated_users']

interaction_table = [interaction_relations, interaction_msg, interaction_tooltip, interaction_button,
                     interaction_icon, interaction_view, interaction_arg]
interaction_tags = ['relation', 'msg', 'tooltip', 'button', 'icon', 'view_link', 'arg']
interactions = [dict(), dict(), dict()]

for i in range(3):
    for tag, vals in zip(interaction_tags, interaction_table):
        interactions[i][tag] = vals[i]
interactions[1], interactions[0] = interactions[0], interactions[1]


KEYS_MAJOR_MINOR = 'A/F#m Bb/Dm B/G#m C/Am Db/Bbm D/Bm Eb/Cm E/C#m F/Dm F#/D#m G/Em Ab/Fm'.split()