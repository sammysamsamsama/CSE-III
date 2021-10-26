import json
import os.path
import pickle
import time
from PIL import Image

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

from Texternet import Texternet

cwd = os.getcwd()

def sender(x):

    '''

        Used to send a message type that is prespecified. \
        The mesage will contain the inquired information taken from searching the given term.

    '''
    os.chdir(cwd)
    TN = Texternet()
    br = webdriver.PhantomJS()
    if(not os.path.isdir(x.from_)):
        Welcoming(x.from_)
    f = open(x.from_ + "/info.dat", 'r')
    stype = f.readline()
    br.get('http://www.google.com/search?as_q=' + x.body)

    string = 'Here\'s your results:'

    if(stype == "links"):
        html = bs(br.page_source, 'html.parser')
        link = html.findAll('h3', {'class':'r'})
        for y in link:
            try:
                string = string + '\n' + str(y.findAll('a')[0]).split('/url?q=')[1].split('&amp;')[0] + '\n'
            except IndexError:
                print("...")    
        TN.sendMessage(x.from_, string)

    elif(stype == "text"):
        if(not os.path.isfile(x.from_ + "/order.dat")):
            try:
                html = bs(br.page_source, 'html.parser')
                Step1(html, TN, x, x.body)
            except Exception as e:
                print(e)
        else:
            html = bs(br.page_source, 'html.parser')
            foward = False
            f = open(x.from_ + "/order.dat", 'r')
            par = [f.readline(), f.readline()]
            duh =  False
            try:
                    int(x.body)*0 == 0
                    duh = False
            except ValueError:
                duh = True
            if(not par[0] == x.body and not x.body == "more" and duh):
                par[1] = "0"
            if(x.body == "more" and int(par[1]) + 1):
                br.get("http://www.google.com/search?as_q=" + par[0] + "&lr=lang_en&hl=en")
                html = bs(br.page_source, 'html.parser')
                order = int(par[1]) + 1
                if(order == 2):
                    foward = Step2(html, TN, x, par[0][:-1])
                elif(order == 3):
                    foward = Step3(html, TN, x, par[0][:-1])
                elif(order == 4):
                    foward = Step3(html, TN, x, par[0][:-1])
            elif(int(par[1]) + 1 == 4):
                try:
                    f = open(x.from_ + "/order.dat", 'r')
                    par = [f.readline(), f.readline()]
                    br.get("http://www.google.com/search?as_q=" + par[0][:-1] + "&lr=lang_en&hl=en")
                    html = bs(br.page_source, 'html.parser')
                    counter = 0
                    while(html == None and counter < 490):
                        f = open(x.from_ + "/order.dat", 'r')
                        par = [f.readline(), f.readline()]
                        br.get("http://www.google.com/search?as_q=" + par[0][:-1] + "&lr=lang_en&hl=en")
                        html = bs(br.page_source, 'html.parser')
                        counter+=1
                    foward = Step4(html, TN, x)
                except ValueError:
                    foward = Step1(html, TN, x, x.body)
            if(not foward):
                foward = Step1(html, TN, x, x.body)
            if(not foward):
                TN.sendMessage(x.from_, "Can't find anything on your search. Pleas try again later")


    elif(stype == "image"):
        string = str(time.time())[-7:] + ".png"
        if(not os.path.isfile("/srv/texternet/html/img/" + string)):
            br.save_screenshot("/srv/texternet/html/img/" + string)
        else:
            string = string[:-4] + "y.png"
            br.save_screenshot("/srv/texternet/html/img/" + string)
        files = fixImage(string)
        TN.sendImage(x.from_, files)

    pickle.dump(x.date_sent,  open("id.in", 'wb'))
    print(x.from_ + " " + x.body)
    fw = open('test subjects.out', 'a+')
    fw.close()
    br.quit()
    return x.from_ + " " + x.body

def Welcoming(Name):
    os.makedirs(Name)
    os.chdir(Name)
    f = open("info.dat", 'w+')      
    f.write("links")
    f.close()
    os.chdir(cwd)

def fixImage(string):
    im = Image.open("/srv/texternet/html/img/" + string) 
    width, height = im.size 
    # twopics = []

    toppp = im.crop({0,0,{width,int(height/6)})
    toppp.save("/srv/texternet/html/img/" + string.split(".png")[0] + "_1.png")
    # twopics.append("https://texternet.tk/img/" + string.split(".png")[0] + "_1.png")
    toppp = im.crop({int(height/6),0,width,2*int(height/6)})
    toppp.save("/srv/texternet/html/img/" + string.split(".png")[0] + "_2.png")
    # twopics.append("https://texternet.tk/img/" + string.split(".png")[0] + "_2.png")
    toppp = im.crop({0, 2*int(height/6),width,3*int(height/6)})
    toppp.save("/srv/texternet/html/img/" + string.split(".png")[0] + "_3.png")
    # twopics.append("https://texternet.tk/img/" + string.split(".png")[0] + "_3.png")
    toppp = im.crop({0,3*int(height/6),width,4*int(height/6)})
    toppp.save("/srv/texternet/html/img/" + string.split(".png")[0] + "_4.png")
    # twopics.append("https://texternet.tk/img/" + string.split(".png")[0] + "_4.png")
    toppp = im.crop({0,4*int(height/6),width,5*int(height/6)})
    toppp.save("/srv/texternet/html/img/" + string.split(".png")[0] + "_5.png")
    # twopics.append("https://texternet.tk/img/" + string.split(".png")[0] + "5.png")
    toppp = im.crop({0,5*int(height/6),width,6*int(height/6)})
    toppp.save("/srv/texternet/html/img/" + string.split(".png")[0] + "_6.png")
    # twopics.append("https://texternet.tk/img/" + string.split(".png")[0] + "_6.png")


    return twopics 

# Retrives and sends the term wiki information in text-form
def Step1(html, TN, x, subject):
    print("Step 1: " + subject)
    # titles  = ['FSP1Dd']
    subtitles = ['F7uZG Rlw09', 'oTDgte']
    os.chdir(cwd)

    try:
            link = html.findAll('div', {'class':'FSP1Dd'})
            string = link[0].text 
            for subs in subtitles:
                try:
                    link = html.findAll('div', {'class':subs})
                    string = string + " : " + link[0].text
                except Exception as e:
                    print(e)
            link = html.findAll('div', {'class':'mraOPb'})
            string = string + "\n\n" + link[0].text
            TN.sendMessage(x.from_, string)

            os.chdir(x.from_)
            f = open("order.dat", 'w+')
            f.write(("{}\n{}").format(subject, 1))                                                                                                                                                                                                                             #easter egg
            f.close()                                   
            os.chdir(cwd)

    except IndexError as e:
        print(e)
        return Step2(html, TN, x, subject)
    return True                 
    
# Retrives and sends the term definition information, if any, in text-form
def Step2(html, TN, x, subject):
    print("Step 2 : " + subject)
    os.chdir(cwd)
    
    try:
        if 2 == len(str(html).split('''</span><span style="font:smaller 'Doulos SIL','Gentum',\
            'TITUS Cyberbit Basic','Junicode','Aborigonal Serif','Arial Unicode MS',\
            'Lucida Sans Unicode','Chrysanthi Unicode';padding-left:15px">''')):
            link = html.findAll('div', {'class':'g'})
            TN.sendMessage(x.from_, link[0].text)

            os.chdir(x.from_)
            f = open("order.dat", 'w+')
            f.write(("{}\n{}").format(subject, 2))
            f.close()
            os.chdir(cwd)
        else:
            return Step3(html, TN, x, subject)

    except IndexError as e:
        print(e)
        return Step3(html, TN, x, subject)
    return True

# Retrives and sends the term link header information, if any, in text-form
def Step3(html, TN, x,subject):
    print("Step 3 : " + subject)
    os.chdir(cwd)

    try:
        string = "Type associated number for info:"
        link = html.findAll('div', {'class':'g'})
        yz = 1

        for y in link:
            if(len(y.findAll("h3", {"class":"r"})) > 0 \
                and len(y.findAll("div", {"class":"s"})) > 0 ):
                string = string + ("\n\n{}. ").format(yz) + y.find("h3", {"class":"r"}).text
                yz+=1
        if(string == "Type associated number for info:"):
            return False
        TN.sendMessage(x.from_, string)

        os.chdir(x.from_)
        f = open("order.dat", 'w+')
        f.write(("{}\n{}").format(subject, 3))
        f.close()
        os.chdir(cwd)

    except IndexError as e:
        print(e)
        TN.sendMessage(x.from_, "We can't seem to get information for this page. \
            Plaese try again later.")
        return False
    return True          

# Retrives and sends a specified header discription information, if any, in text-form
def Step4(html, TN, x):
    print("Step 4")
    os.chdir(cwd)
    
    try:
        string = ""
        t = []
        s = []

        # Finds all the Google Links
        link = html.findAll('div', {'class':'g'})
        for y in link:
            if(len(y.findAll("h3", {"class":"r"})) > 0 \
                and len(y.findAll("div", {"class":"s"})) > 0 ):
                t.append(y.find("h3", {"class":"r"}))
                s.append(y.find("div", {"class":"s"}))

        try:
            string = t[int(x.body)-1].text + "\n\n" + s[int(x.body)-1].text\
                .split(s[int(x.body)-1].find("ul").text)[1]

        except TypeError as e:
            print(e)
            string = t[int(x.body)-1].text + "\n\n" + s[int(x.body)-1].find("span").text

        except AttributeError as e:
            print(e)
            string = t[int(x.body)-1].text + "\n\n" + s[int(x.body)-1].find("span").text
        TN.sendMessage(x.from_, string)

    except IndexError as e:
        print(e)
        TN.sendMessage(x.from_, "Please give a number within the boandaries, or type quit to quit exploring this term")
        return True
    return True
