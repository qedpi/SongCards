settings = ['again', 'easy', 'medium', 'hard']
modifiers = [.1, 2, 1.3, 1]
multipliers = dict(zip(settings, modifiers))


used_fields = ['topic', 'front', 'back', 'card_audio', 'card_score', 'card_pic',
               'is_favorite', 'is_pinned']


interaction_relations = ['I share with', 'Shares with me', 'Other users']
interaction_msg = ['', 'Browse Songs', '']
interaction_tooltip = ['Stop Sharing', '', 'Start Sharing']
interaction_button = ['danger', 'primary', 'success']
interaction_icon = ['glyphicon glyphicon-minus', 'glyphicon glyphicon-camera', 'glyphicon glyphicon-plus']
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