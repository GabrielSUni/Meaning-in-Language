from WordLists import Wordlists
import re
import pickle
import yaml


class Tests:
    def __init__(self, speech):
        speech = re.sub("\(.*?\)", "", speech)
        self.speech = speech

    
    
    @property
    def ListOfWords(self):
        # replace regex
        speech = self.speech.replace("\n", " ")
        speech = speech.replace("\r", "")
        speech = speech.replace("-", " ")
        # speech = speech.replace("\u", " ")
        # speech = speech.replace("\t", "")

        # separate into words
        liste = speech.split(" ")

        # remove unnecessary stuff
        while " " in liste: liste.remove(" ") 
        while "" in liste: liste.remove("") 
        while "-" in liste: liste.remove("-") 
        while "—" in liste: liste.remove("—") 
        for word in liste:
            if len(word) == 0:
                liste.remove(word)
        
        return liste


    @property
    def NumberOfWords(self):
        return len(self.ListOfWords)
    
    @property
    def NumberOfSentences(self):
        # replace signs
        speech = self.speech.replace("!", ".")
        speech = speech.replace("?", ".")
        speech = speech.replace(";", ".")
        speech = speech.replace(" - ", ".")
        speech = speech.replace(" — ", ".")
        # add more

        liste = speech.split(".")
        return len(liste) -1
    
    @property
    def NumberOfSyllabels(self):
        NumSyl = 0
        for word in self.ListOfWords:
            NumSyl += Tests.SyllableEstimator(word)
        return NumSyl
    
    @property
    def NumberOfLetters(self):
    # note: strokes not letter, punctuation marks count as well!
        NumLet = 0
        for word in self.ListOfWords:
            NumLet += len(word)
        return NumLet
    
    
    def SyllableEstimator(word):
        vowels = ["a", "e", "i", "o", "u", "y"]
        counter = 0
        for letter in word:
            if letter in vowels:
                counter += 1
        
        if word[-1] == "e":
            counter -= 1
        
        for i in range(len(word)-1):
            if word[i] in vowels and word[i+1] in vowels:
                counter -= 1

        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            counter += 1

        if word.endswith('ed') and len(word) > 2 and word[-3] not in vowels:
            counter -= 1

        if counter == 0:
            counter = 1

        return counter
    
    def CountHardWords(self, test):
        NumHardWords = 0

        if test == "FogCount":
            for word in self.ListOfWords:
                if Tests.SyllableEstimator(word) >= 3:
                    NumHardWords += 1
                  
        else:   
            pass

        if NumHardWords < 0:
            NumHardWords = 0

        return NumHardWords

    def CountEasyWords(self, test):
        NumEasyWords = 0

        if test == "FogCount":
            # for word in self.ListOfWords:
            #     if Tests.SyllableEstimator(word) < 3:
            #         NumEasyWords += 1
            pass

        elif test == "DaleChall":
            endings = ["ied", "ies", "ing", "est", "s", "es", "ed", "er", "ly", "n"]
            for i in range(len(self.ListOfWords)):
                # remove puncutation from words
                word = self.ListOfWords[i]
                if word.endswith((".", ",", "!", "?")): 
                    word = word[:-1]

                # check if in word list
                if word.lower() in set(Wordlists["Dale_Chall"]):
                    NumEasyWords += 1
                else:
                    # check if word-ending in word list
                    for ending in endings:
                        if word.endswith(ending):
                            if word.lower()[:-len(ending)] in set(Wordlists["Dale_Chall"]):
                                NumEasyWords += 1
                        else:
                            # proper names
                            if word[0].isupper():
                                NumEasyWords += 1
                                
        elif test == "DaleChall2":   
            counter = 0
            endings = ["ied", "ies", "ing", "est", "s", "es", "ed", "er", "ly", "n"]

            # make set from list of words
            self.SetOfWords = set(self.ListOfWords)  

            # load dict
            # with open('DaleChallDict.yaml', 'r') as file:
            #     DaleChallDict = yaml.safe_load(file)
            DaleChallDict = {}

            # loop through Set of words to fill the dict
            for word in self.SetOfWords:
                if not re.search('[a-zA-Z]', word):
                    continue
                while not re.search(r"\A[a-z]", word.lower()) and len(word) > 0:
                    word = word[1:]
                while not re.search(r"[a-z]\Z", word.lower()) and len(word) > 0:
                    word = word[:-1]
            
                # remove punctuation and ending
                if word.endswith((".", ",", "!", "?")): 
                    word = word[:-1]


                if word.lower() not in DaleChallDict.keys():
                    # easy word
                    if word.lower() in Wordlists["Dale_Chall"]:
                        DaleChallDict[word.lower()] = True
                    
                    else:
                        # proper names
                        if word[0].isupper():
                            DaleChallDict[word.lower()] = True
                        else:
                            # easy words + ending
                            for end in endings:
                                if word.endswith(end):
                                    word_stripped = word[:-len(end)]
                                    if word_stripped.lower() in Wordlists["Dale_Chall"]:
                                        DaleChallDict[word.lower()] = True
                                else:
                                    # difficult words
                                    DaleChallDict[word.lower()] = False
                        

            
            # with open('DaleChallDict.yaml', 'w') as file:
            #     yaml.dump(DaleChallDict, file)
            


            # look up in dict ob diffucult oder easy
            for word in self.ListOfWords:
                
                while not re.search(r"\A[a-z]", word.lower()) and len(word) > 0:
                    word = word[1:]

                
                while not re.search(r"[a-z]\Z", word.lower()) and len(word) > 0:
                    word = word[:-1]
                

                # if word.endswith((".",",", "!", "?")): 
                #     word = word[:-1]
                

                if word.lower() in DaleChallDict.keys():
                    if DaleChallDict[word.lower()] == True:
                        counter += 1
                    else:
                        if word[0].isupper():
                            counter += 1
                        else: 
                            pass
                else:
                    for end in endings:
                        if word.endswith(end):
                            word = word[:-len(end)]
                            if DaleChallDict[word.lower()] == True:
                                counter += 1
                        else:
                            pass
            
            NumEasyWords = counter

        else:
            pass

        return NumEasyWords
    
    def PercentageHardWords(self):
        return (self.NumberOfWords-Tests.CountEasyWords(self, test="DaleChall"))/self.NumberOfWords

    
    def DaleChall(self):
        DC = (0.1579*100*((self.NumberOfWords-Tests.CountEasyWords(self, test="DaleChall2"))/self.NumberOfWords)\
        ) + (0.0496*(self.NumberOfWords/self.NumberOfSentences)) + 3.6365

        return round(DC, 2)
         

    def CLI(self):
        CLI = 0.0588*(100*self.NumberOfLetters/self.NumberOfWords)-0.296*(100*self.NumberOfSentences/self.NumberOfWords)-15.8
        return round(CLI, 2)



    def FOGC(self):
        FOGC = (0.4*((self.NumberOfWords/self.NumberOfSentences)+100*(Tests.CountHardWords(self, test="FogCount")/self.NumberOfWords)))
        
        return round(FOGC, 2)
