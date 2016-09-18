# MusicCards
FlashCards for lyrics and tablatures (Django, JS)

A prototype is on heroku at https://songcards.herokuapp.com/

I find flash-card programs with spaced-repetition useful for exploring a large repertoire of music. 
However, unlike flash-cards for learning, it's desirable to give feedback on how much we like a song,
to influence the frequency that it's presented to us.

This project seeks to become a hybrid of guitar/ukulele/tablature/lyrics sites and online flash-card sites. 
The long-term aim is to include: A repertoire of pieces that users can add to their own collection of cards. 
Automated transposition of pieces considering users' vocal ranges and simplicity of tablature. 
Social / User feedback to improve existing repository of cards.

## Practice Songs (Ordered by review time, filtered by search)
![Screenshot](screenshots/screenshot_songs.jpg)
Search: for my cards
Pin: always at the front
Favorite: appears more frequently for practice
New cards have red border, cards not due for review are grayed out

## Add Songs
![Screenshot](screenshots/screenshot_add_song.jpg)
Autogenerate: lyrics, tempo, youtube video, tablature site from title and artist

## Browse Public Songs
![Screenshot](screenshots/screenshot_browse_public.jpg)
Can add to collection

## Song Screen, Spaced-Repetition and Details (+ Debugging Info)
![Screenshot](screenshots/screenshot_details.jpg)
Transposition: to any key of the same type (major, minor), reset to original key
Autoscroll: adjust speed with controls
Privacy options: private, share with friends, or public
Feedback: for spaced rpetition
Colors: for chord symbol corresponds to relative position. (circle of fifths, using rainbow colors)
Manage card: edit, delete, share

## Tabs appear as tooltip on hover
![Screenshot](screenshots/screenshot_tab_tooltip.jpg)

## Generate share-link
![Screenshot](screenshots/screenshot_share_link.jpg)
Allows copy to clipboard

## Sharing, Following, Friending
![Screenshot](screenshots/screenshot_friends.jpg)

## View other users' profiles
![Screenshot](screenshots/screenshot_user_profile.jpg)

## View other users' cards
![Screenshot](screenshots/screenshot_friends_cards.jpg)
Can add to own collection

## User management (Register, Login, Logout)
![Screenshot](screenshots/screenshot_user_management.jpg)