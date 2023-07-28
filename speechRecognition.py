from pynput import keyboard
import os
import speech_recognition as sr
import pygame

# Get the directory path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the sound file paths relative to the current script's directory
start_sound_file = os.path.join(current_dir, "start.mp3")
stop_sound_file = os.path.join(current_dir, "stop.mp3")
stop1_sound_file = os.path.join(current_dir, "stop1.mp3")
go_sound_file = os.path.join(current_dir, "go.mp3")

# Use the sound file paths in your code
# ...


# Initialize website shortcuts dictionary
website_shortcuts = {
    "openai": "https://www.openai.com/",
    "github": "https://github.com/",
    "gmail": "https://mail.google.com/",
    "stackoverflow": "https://stackoverflow.com/",
    # Add more shortcuts here
}

# Initialize recognizer
r = sr.Recognizer()

# Initialize Pygame mixer
pygame.mixer.init()

def play_sound(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
        pygame.time.Clock().tick(10)  # wait and let the music play for 10 ms

def on_press(key):
    try:
        if key is keyboard.Key.shift:
            # Play start sound
            play_sound(start_sound_file)
            
            try:
                with sr.Microphone() as source:
                    print("Talk")
                    try:
                        # Here we've set the timeout to 15 seconds
                        audio_text = r.listen(source)
                    except sr.WaitTimeoutError:
                        print("Timeout error: Didn't hear any audio input for 15 seconds")
                        return
                    print("Time over, thanks")

                    try:
                        text = r.recognize_google(audio_text)
                        print("Text: " + text)
                        
                        if text.lower().startswith("open the website"):
                            website_shortcut = text.split()[-1].lower()  # Get the last word
                            if website_shortcut in website_shortcuts:
                                os.system(f'open "{website_shortcuts[website_shortcut]}"')
                                play_sound(go_sound_file)  # Play "go" sound
                        elif text.lower() == "stop listening":
                            print("Ending the program...")
                            play_sound(stop1_sound_file)  # Play "stop" sound
                            return False
                    except:
                        # Play stop sound
                        play_sound(stop_sound_file)
                        print("Sorry, I did not get that")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
            except Exception as e:
                print(f"An error occurred: {e}")

            
    except AttributeError:
        print('Unknown key {0}'.format(key))

# Listen for keyboard input
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
