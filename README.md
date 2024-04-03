# YT-Notes-Flashcard-Gen
Generate notes in .md format and anki flashcards from youtube video.

## How it works
* Enter link to YT video
* Specify folder name
* Let the script run and check the folder when it's finished running to find .md notes, .mp3, transcript and anki deck file which can be imported into Anki app.
  
## Requirements
* Use pip to install OpenAI, genanki and pytube
* Requires OpenAI key to access OpenAI API. Set key as shell environment variable or edit script to use it by other means.
