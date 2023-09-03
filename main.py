import os
import openai
import playsound as ps
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from time import sleep


# Set up your openai API
openai.api_key = 'your openai api key'
messages = [{"role": "user", "content": "Hello GPT!"}]


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted successfully.")
    except OSError as e:
        print(f"Error occurred while deleting the file: {e}")


def generate_response(messages1):
    # Call the openai API
    response1 = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages1
    )

    return response1.choices[0].message.content


def text_to_speech(text1):
    tts = gTTS(text=text1, lang="en")
    filename1 = "gpt.mp3"
    tts.save(filename1)
    file = open(filename1)
    file.close()
    song = AudioSegment.from_mp3("./gpt.mp3")
    print('playing sound...')
    play(song)
    delete_file(filename1)


def speach_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

    text = ""
    catch = False
    while not catch:
        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            catch = True
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            print(f"Sorry, an error occurred: {e}")

    return text


# Main loop
print("Welcome to the Chatbot! Say 'exit' to end the conversation.")
while True:

    user_input = speach_to_text()
    messages.append({"role": "user", "content": user_input})
    sleep(2)

    if user_input.lower().strip() == 'exit':
        break

    # Generate a response
    response = generate_response(messages)
    messages.append({"role": "assistant", "content": response})

    print("Chatbot:", response)
    text_to_speech(response)
    sleep(2)


# in case you wanted to save the file and play it later
# if os.path.isfile("gpt.mp3"):
#     print("file exists")
# else:
#     print("doesn't exist")
#
# ps.playsound("./gpt.mp3")
# print('playing sound using pydub')
