import pickle
import threading

import client
from Texternet import Texternet

TN = Texternet()

'''
    This is the file that stores all the methods of Texternet used to change user settings.
'''

def theSlash(x):

    '''
        Used to determine which command is being called if any.
    '''
    # If message is equal to links, change message type sent to links
    if x.body == "/links":
        changeLinks(x)

    # If message is equal to image, change message type sent to image
    elif x.body == "/image":
        changeImage(x)

    # If message is equal to text, change message type sent to text
    elif x.body == "/text":
        changeText(x)

    elif x.body == "/assistant":
        changeAssistant(x)

    # If message is equal to clear, it will erase the term being served from memory
    elif x.body == "/clear":
        quit(x)
    
    # If message is equal to help, it will send a list of helpful commands
    elif x.body == "/help":
        help(x)

    # If message is equal to exit, close program
    elif x.body == "/exit":
        exit(0)

    # Else run search protocol in seperate process
    else:
        # Passing message to separate process
        t = threading.Thread(name="child procs", target=client.sender, args=(x,))
        t.setDaemon(True)
        t.start()

    print(x.from_ + " " + x.body)
    return x.from_ + " " + x.body

def changeLinks(x):

    '''
    Switches the type of search results given to URL results.
    '''

    try:
        f = open(x.from_ + "/info.dat", "w+")
        f.write("links")
        f.close()
        TN.sendMessage(x.from_, "Sucessfully changed to links!")
        pickle.dump(x.date_sent, open("id.in", "wb"))
    except Exception as e:
        TN.sendMessage(x.from_, "Change failed: Try searching something first")
        pickle.dump(x.date_sent, open("id.in", "wb"))
        print(e)

def changeImage(x):

    '''
    Switches the type of search results given to images of search page results.
    '''

    try:
        f = open(x.from_ + "/info.dat", "w+")
        f.write("image")
        f.close()
        TN.sendMessage(x.from_, "Sucessfully changed to image!")
        pickle.dump(x.date_sent, open("id.in", "wb"))
    except Exception as e:
        TN.sendMessage(x.from_, "Change failed: Try searching something first")
        pickle.dump(x.date_sent, open("id.in", "wb"))
        print(e)

def changeAssistant(x):

    '''
    Switches the type of search results given to images of search page results.
    '''

    try:
        f = open(x.from_ + "/info.dat", "w+")
        f.write("assistant")
        f.close()
        TN.sendMessage(x.from_, "Sucessfully changed to assistant!")
        pickle.dump(x.date_sent, open("id.in", "wb"))
    except Exception as e:
        TN.sendMessage(x.from_, "Change failed: Try searching something first")
        pickle.dump(x.date_sent, open("id.in", "wb"))
        print(e)

def changeText(x):

    '''
    Switches the type of search results given to text-understandable results.
    '''

    try:
        f = open(x.from_ + "/info.dat", "w+")
        f.write("text")
        f.close()
        TN.sendMessage(x.from_, "Sucessfully changed to text!")
        pickle.dump(x.date_sent, open("id.in", "wb"))
    except Exception as e:
        TN.sendMessage(x.from_, "Change failed: Try searching something first")
        pickle.dump(x.date_sent, open("id.in", "wb"))
        print(e)

def quit(x):

    '''
    Terminates the current search term saved to memory.
    '''

    try:
        f = open(x.from_ + "/order.dat", "w+")
        f.write("")
        f.close()
        TN.sendMessage(x.from_, "Last search term has been cleared from memory!")
        pickle.dump(x.date_sent, open("id.in", "wb"))
    except Exception as e:
        TN.sendMessage(x.from_, "Quit failed: Try searching something first")
        pickle.dump(x.date_sent, open("id.in", "wb"))
        print(e)

def help(x):
    try:
        TN.sendMessage(x.from_, '''Texternet.tk
        This is the center for the Texternet service.
        We make your life easier by saving you data when you search on our platform.
        Thank you so much for using our service, below we have a list of commands to use
        in our service, and we also have surveys to learn more about our user base,
        if you ever feel like helping to make a better Texternet.tk.

        Disclaimer: This service is meant to help with searching for quick information when
        data is at risk. We use a browser on our end, but Texternet.tk is not a browser.
    

Commands
 
        /links
        If message is equal to links, change message type sent to links

        /image
        If message is equal to image, change message type sent to image

        /text
        If message is equal to text, change message type sent to text

        /clear
        If message is equal to clear, it will erase the term being served from memory
        
        /help
        If message is equal to help, it will send a list of helpful commands''')
        pickle.dump(x.date_sent, open("id.in", "wb"))
    except Exception as e:
        TN.sendMessage(x.from_, "Help failed: Try searching something first")
        pickle.dump(x.date_sent, open("id.in", "wb"))
        print(e)