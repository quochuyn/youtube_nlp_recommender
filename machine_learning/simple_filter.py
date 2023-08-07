#This file is only for offline testing purposes currently.

#Instead of machine learning
#this will be a baseline approach of using a simple filter to recommend videos
#of exact word matches between the filter and any video title

#Pro: A video title may be long but a few word exact or close match should always be filtered out

#Con: This will have limitations as sports can refer to a lot of things, but the exact
#word may not be present in the title, transcript, tag, description, etc.
#Con: Won't capture alternate spellings, abbreviations, etc.

filter_sent = "Russia"
list_of_videos = ["Who'se Really Supporting Russia","The Perfect Hillary Clinton Analogy","The Evolution of Alex Jones",\
                  "Patrick Bet David on The Breakfast Club","The Truth About The 2020 Election","Kobe Bryant’s Last Great Interview"]
def filter_out_simple(filter_sent,list_of_videos):
    results = []
    #Compute embedding for both lists
    for i in list_of_videos:
        if filter_sent not in i:
            print(i)
            results.append(i)
    return results
test_case_1 = filter_out_simple(filter_sent,list_of_videos)
assert("Who'se Really Supporting Russia" not in test_case_1)
