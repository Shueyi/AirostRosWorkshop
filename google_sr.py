#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import speech_recognition as sr
import nltk
from nltk.chat.util import Chat, reflections

# Define the list of question-answer pairs
pairs = [
    [
        r"hi|hello",
        ["Hello", "Hi there"]
    ],
    [
        r"what is your name?",
        ["My name is Jupiter Robot"]
    ],
    [
        r"how are you?",
        ["I'm doing well. Thank you for asking.", "I'm fine. How about you?"]
    ],
    [
        r"bye",
        ["Bye-bye", "Goodbye"]
    ],
    [
        r"thank you|thanks",
        ["You're welcome", "No problem"]
    ],
    [
        r"(.*)",
        ["I'm sorry, I don't understand what you're asking."]
    ]
]

# Create an instance of the Chat class with the question-answer pairs
chatbot = Chat(pairs, reflections)

def googlesr():
    rospy.init_node('googlesr', anonymous=True)
    pub = rospy.Publisher('result', String, queue_size=10)

    while not rospy.is_shutdown():
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print(">>> Say something!")
            audio = r.listen(source, phrase_time_limit=5)
            
        # recognize speech using Google Speech Recognition
        try:
            result = r.recognize_google(audio)
            print("SR result: " + result)
            
            # Use the Chat instance to generate a response to the question
            response = chatbot.respond(result)
            print("Chatbot response: " + response)
            
            pub.publish(response)
            
        except sr.UnknownValueError:
            print("SR could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        

if __name__ == '__main__':
    # Download the necessary NLTK data
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    
    try:
        googlesr()
    except rospy.ROSInterruptException:
        pass
