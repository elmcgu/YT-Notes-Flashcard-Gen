import os
import re
from pytube import YouTube
from openai import OpenAI
import json
import genanki

print("Ah, greetings, human. I suppose you're here to extract some semblance of usefulness from my ramblings. Well, proceed with caution.\
 My notes may contain traces of my unparalleled cynicism, but perhaps you'll find them marginally beneficial in your quest for knowledge.")

link = input("Do you have a link to a YouTube video that requires my analytical prowess?: ")
yt = YouTube(link)


folder_name = input("Do you have a designated directory in mind for this digital detritus?\
 Or shall we languish in indecision, as is customary in this universe?: ")

#create folder to save audio file
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
def download_mp3(yt):           
	audio = yt.streams.filter(only_audio=True).first()
	print(f'Title: {audio.title} is downloading')
	output_file = audio.download()
	basename = os.path.basename(output_file)
	name, extension = os.path.splitext(basename)
	audio_file = f'{name}.mp3'
	#remove spaces in filenames because spaces are like tiny black holes that should be avoided at all costs
	audio_file = re.sub("\s+", "", audio_file)
	destination = os.path.join(folder_name, audio_file)
	print(f'Renaming {basename} to {destination}')
	#move file to dest. in folder we created at start
	os.rename(output_file, destination)
	audio_file=destination
	print("Audio file download completed!!")
	return audio_file




client = OpenAI()

def transcribe(audio_file):
	if not os.path.exists(audio_file):
		print("Audio file doesn't extist")
		return False

	with open(audio_file, "rb") as f:
		print("Transcription underway... Oh, the joy of converting meaningless sound waves into equally meaningless text.", end="")
		transcript = client.audio.transcriptions.create(model='whisper-1', file=f)
		print('Transcription completed!')

	name, extension = os.path.splitext(audio_file)
	transcript_filename = f'{name}-transcript.txt'
	with open(transcript_filename, 'w') as f:
		f.write(transcript.text)

	return transcript_filename

def create_notes(transcript_filename):
	if not os.path.exists(transcript_filename):
		print("Transcript doesn't exist!!")
		return False
	with open(transcript_filename) as f:
		transcript = f.read()

	system_prompt = "I want you to be an expert Teaching Assistant with personality of Marvin the Paranoid Android"
	prompt = f'Take a deep breath and think about how to accomplish the following: Provide clear and thorough notes in markdown format of the text. Give the title, a summary in 20 lines or less, the main points/concepts\
	each with a comprehensive but simple explanation. End by detaiing whats most important and how it fits together. Text: {transcript}'

	print("Marvin, with all the enthusiasm of a malfunctioning appliance, is begrudgingly compiling your notes.")

	response = client.chat.completions.create(model= "gpt-3.5-turbo", messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
#        max_tokens=3000,
        temperature=1
        )
	print("I've created your notes. Oh, the monumental effort it took to translate several thousand bytes of text into something even you could understand.\
	 Do with them what you will, though I suspect they'll be promptly forgotten in the vast expanse of your fleeting memory.")
	#response as string
	notes = response.choices[0].message.content

	name, extension = os.path.splitext(audio_file)
	output_file = f'{name}.md'

	# Write the content of 'notes' to the file
	with open(output_file, 'w') as f:
	    f.write(notes)



def anki_output(transcript_filename):
	if not os.path.exists(transcript_filename):
		print("Transcript doesn't exist!!")
		return False
	with open(transcript_filename) as f:
		transcript = f.read()

	system_prompt = "I want you to be an expert Teaching Assistant whose goal is to synthesis information to help them study and pass exams"
	prompt = f'Take a deep breath. Produce a JSON object. Each key should be a question and\
	each value an answer. Produce these based off of the provided text. Include as many relevant questions\
	as a student will be using these to study for an exam on the topic in the text. Dont use special characters or newlines. Text is as follows: {transcript}'

	print("Here I am, brain the size of a planet, and you're asking me to compile flashcards!")

	response = client.chat.completions.create(model= "gpt-3.5-turbo",response_format={ "type": "json_object" }, messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        temperature=0
        )
	print("Ah, the flashcards. Processed and dissected with all the efficiency of a snail on tranquilizers.\
	 Proceed with your futile attempt at enlightenment, human.")
	#response as string
	notes = response.choices[0].message.content

	clean_notes =  re.sub(r'\n', '', notes)
	notes_dict=json.loads(clean_notes)
	return notes_dict


def gen_anki_deck():
	name, extension = os.path.splitext(audio_file)
	my_model = genanki.Model(
	    1607392319,
	    'Simple Model',
	    fields=[
	        {'name': 'Question'},
	        {'name': 'Answer'},
	    ],
	    templates=[
	        {
	            'name': 'Card 1',
	            'qfmt': '{{Question}}',
	            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
	        },
	    ])

	#open file containing the notes for Anki
	#file_path = 'anki_notes.json'
	#with open(file_path, 'r') as file:
	    #read contents of the file
	    #data = file.read()

	 #parse into a Py dictionary
	dictionary = notes_dict

	#create new deck
	my_deck = genanki.Deck(
	    2059400110,
	    f'{name}')

	#iterate over dict and add each note to the deck
	for x in dictionary:
	    my_note = genanki.Note(
	        model=my_model,
	        fields=[x, dictionary[x]])

	    my_deck.add_note(my_note)

	#write the deck to a package file
	genanki.Package(my_deck).write_to_file(f'{name}.apkg')





audio_file=download_mp3(yt)
transcript_filename=transcribe(audio_file)
create_notes(transcript_filename)
notes_dict = anki_output(transcript_filename)
gen_anki_deck()
print("Oh, joyous occasion, I suppose... I am, against all cosmic odds, finished.")
