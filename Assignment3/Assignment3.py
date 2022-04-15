"""
Assignment 3:
In this Assignment I'm creating a movie analytics tools that allows user to search for a movie of
their choice and obtain further information about it using online data and text analytics.
"""

# Uncomment the below line if using google collab
# !pip install xmltodict
import json
import matplotlib.pyplot as plt
import nltk
import requests
import skimage.io
import textblob
import wordcloud
import xmltodict

nltk.download("punkt")


# Below function is defined to create wordcloud of review text.
def word_cloud(data):
    text = ""
    for line in data:
        review = line["Review text"]
        text = text + review + " "
    # print(text)
    # Generating word cloud using WordCloud method.
    cloud = wordcloud.WordCloud(width=1000, height=1000, background_color="white", colormap="rainbow")
    cloud.generate(text)

    # Saving poster figure in directory by the ame of "poster.png".
    cloud.to_file("yelp_wordcloud.png")

    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")

    # Uncomment the below code to show the wordcloud figure

    # plt.show(block=False)
    # plt.pause(0.1)
    # plt.close()


# Below function is defined to print the background details, Reception details, displaying and saving the movie poster.
# movie_data() will display movie details according to user input. There are 3 conditions for printing movie background
# details, Reception details and movie poster.
def movie_data(data, choice):

    if choice == "background":
        year = data['root']['movie']['@year']
        rating = data['root']['movie']['@rated']
        runtime = data['root']['movie']['@runtime']
        genre = data['root']['movie']['@genre']
        actors = data['root']['movie']['@actors']
        plot = data['root']['movie']['@plot']
        print("Year :", year)
        print("Rating :", rating)
        print("Runtime :", runtime)
        print("Genre :", genre)
        print("Actors :", actors)
        print("Plot :", plot)

    elif option == "reception":
        awards = data['root']['movie']['@awards']
        score = data['root']['movie']['@metascore']
        imdb = data['root']['movie']['@imdbRating']
        print("Awards :", awards)
        print("Metascore :", score)
        print("IMDb rating :", imdb)

    elif option == "poster":
        poster = data['root']['movie']['@poster']
        image = skimage.io.imread(poster)

        plt.imshow(image, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("poster.png")         # Saving poster figure in directory by the ame of "poster.png".
        # Uncomment the below code to show the wordcloud figure

        # plt.show(block=False)
        # plt.pause(0.1)
        # plt.close()


# Entry message
print("Welcome to the movie analytics tool! \n")
repeat = "yes"
while repeat == 'yes':       # Loop to  allow the user to run as many analyses as desired.

    # below asking user to enter the movie name and kind of analysis.
    movie = input("What movie would you like to analyze?").lower()
    option = input("What would you like to see \n (background/reception/poster/wordcloud/sentiment)? ").lower()
    word = textblob.TextBlob(option).correct()
    # print(word)

    # if below condition will true then response1 will get active otherwise response2 will get active.
    if word in ["background", "reception", "poster"]:

        response1 = requests.get("https://www.omdbapi.com/?r=xml&apikey=86cadd95&t=" + movie)
        if response1:
            data = xmltodict.parse(response1.text)
            # print(data)
            movie_data(data, word)
        else:
            print("Sorry, the tool could not successfully load movie details")

    elif word in ["wordcloud", "sentiment"]:
        response2 = requests.get("https://dgoldberg.sdsu.edu/515/imdb/" + movie + ".json")
        if response2:
            if word == "wordcloud":
                data = json.loads(response2.text)
                word_cloud(data)
            elif word == "sentiment":
                blob = textblob.TextBlob(response2.text)
                print("Average IMDb review polarity:", blob.polarity)
                print("Average IMDb review subjectivity", blob.subjectivity)

        else:
            print("Sorry, the tool could not successfully load any IMDb reviews for this movie. Please try another "
                  "analysis or movie. ")
    else:
        print("Sorry, that analysis is not supported. Please try again.")

    repeat = input("Do you want to repeat. (yes/No) ?").lower()
    repeat = textblob.TextBlob(repeat).correct()

print("Thank you for using movie analytic tool")
