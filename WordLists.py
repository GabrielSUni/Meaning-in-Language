import pickle

# create dale chall word list
with open('daleChallList.txt', 'r') as file:
    DaleChallList = file.read().replace("\n", " ").split(" ")
    while "" in DaleChallList: DaleChallList.remove("")


# create dictionary with word lists
Wordlists = {
    "Dale_Chall" : DaleChallList,
}
