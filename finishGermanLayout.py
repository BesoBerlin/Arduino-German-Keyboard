#!/usr/bin/env python
# coding: utf-8

#danke, dass du BesoBerlins Finish zur konvertierung fuer charaktere, die AltGr benoetigen benutzt!


#################### funktion zum mappen ####################

def mappen(s):		#hier werden charaktere gemappt, fuer deren verwendung das druecken von AltGr notwendig ist 
	
	###### liste mit zu ersetzenden charakteren ######
	deu = ("~",
	"@",
	"{",
	"}",
	"[",
	"]",
	"|",
	"\\")	

	###### liste mit zu drueckenden AltGr + charakteren ######
	altGr = ("+",
	"q",
	"7",
	"0",
	"8",
	"9",
	"<",
	"ß")

	if s.count(r"\\") > 0:	
		#position ausfindig machen fuer ersetzen
		charPos = s.find(r"\\")
		#zeile bis zum charakter kopieren  + stringuebergabe beenden + AltGr druecken + erstezen durch taste drueck bzw. char schreiben + rest der zeile kopieren
		s = s[:charPos] + "\");\n" + "/*EINRUECKEN*/	Keyboard.press(KEY_RIGHT_ALT);\n" + "/*EINRUECKEN*/   Keyboard.print(\"" + (r"\\") + "\");\n" + "/*EINRUECKEN*/   Keyboard.release(KEY_RIGHT_ALT);\n" + "Keyboard.print(\"" + s[charPos+1:]

	for i in range(len(deu)):		
	###### Schleife fuer Mehrfachvorfachkommen ######
		while s.count(deu[i]) > 0:	
			#position ausfindig machen fuer ersetzen
			charPos = s.find(deu[i])
			#zeile bis zum charakter kopieren  + stringuebergabe beenden + AltGr druecken + erstezen durch taste drueck bzw. char schreiben + rest der zeile kopieren
			s = s[:charPos] + "\");\n" + "/*EINRUECKEN*/	Keyboard.press(KEY_RIGHT_ALT);\n" + "/*EINRUECKEN*/   Keyboard.print(\"" + (altGr[i]) + "\");\n" + "/*EINRUECKEN*/   Keyboard.release(KEY_RIGHT_ALT);\n" + "Keyboard.print(\"" + s[charPos+1:]
	return s



#################### datei einlesen ####################
inputFile = open("input.ino")
linesList = inputFile.readlines()
inputFile.close()
#################### datei bearbeiten ####################
lineNumber = 0
prntlnFlag = False
commentFlag = False

for line in linesList:
    
    if (linesList[lineNumber].find("/*")!=(-1)):
        commentFlag = True
        
    if (linesList[lineNumber].find("*/")!=(-1)):
        commentFlag = False
        
    if commentFlag == False:

        if ((linesList[lineNumber].find("//")==(-1))and(linesList[lineNumber].find("//")<linesList[lineNumber].find("Keyboard.print"))):     #check ob keyboard-anweisung innerhalb eines einzeiligen Kommentars ist  

            if (linesList[lineNumber].find("Keyboard.println")!=(-1)):	                                                                     #check ob es println statt print ist
                prntlnFlag = True                                                                                                            #Flag setzen um am Ende wieder ein \n-Enter einzufuegen
                lnStart = (linesList[lineNumber].find("Keyboard.println"))+len("Keyboard.print")	                                         #beginn des zu mappenden strings innerhalb des dokumentenstrings ermitteln
                linesList[lineNumber] = linesList[lineNumber][:lnStart] + linesList[lineNumber][lnStart+2:]                                  #println zu print umwandeln
        
            if (linesList[lineNumber].find("Keyboard.print")!=(-1)):	                                                                     #check ob es strings in  Keayboard.print gibt
                stringStart = (linesList[lineNumber].find("Keyboard.print(\""))+len("Keyboard.print(\"")	                                 #beginn des zu mappenden strings innerhalb von print ermitteln
                linesList[lineNumber] = linesList[lineNumber][:stringStart] + mappen(linesList[lineNumber][stringStart:])	                 #ALT.GR charaktere mappen
            
            if prntlnFlag == True:
                linesList[lineNumber] = linesList[lineNumber] + "/*EINRUECKEN*/	Keyboard.press(KEY_RETURN);\n/*EINRUECKEN*/	Keyboard.release(KEY_RETURN);\n" #\n-Enter einfuegen weil println die gewuenschte Funktion war. 
                prntlnFlag = False

	lineNumber=lineNumber+1



#################### bearbeitete datei speichern ####################
outputFile = open('finish.ino', 'w')
linesList.insert(0,"\n\n\n//Thank You for using BESOBERLINs GermanKeyboardFinish!\n\n\n")
outputFile.writelines(linesList)
outputFile.close()


