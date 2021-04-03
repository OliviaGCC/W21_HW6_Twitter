#########################################
##### Name: Chenchen Gao            #####
##### Uniqname: gaochenc            #####
#########################################

from requests_oauthlib import OAuth1
import json
import requests
from collections import Counter

import hw6_secrets_starter as secrets # file that contains your OAuth credentials

CACHE_FILENAME = "/Users/designurlife/Documents/Winter2021/week8/hw6/twitter_cache.json"

CACHE_DICT = {}

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)

def test_oauth():
    ''' Helper function that returns an HTTP 200 OK response code and a 
    representation of the requesting user if authentication was 
    successful; returns a 401 status code and an error message if 
    not. Only use this method to test if supplied user credentials are 
    valid. Not used to achieve the goal of this assignment.'''

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(client_key, client_secret, access_token, access_token_secret)
    authentication_state = requests.get(url, auth=auth).json()
    return authentication_state




def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params

    AUTOGRADER NOTES: To correctly test this using the autograder, use an underscore ("_") 
    to join your baseurl with the params and all the key-value pairs from params
    E.g., baseurl_key1_value1
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    #TODO Implement function
    
    params_str = []
    connector = '_'
    for d in params.keys(): 
        params_str.append(f"{d}_{params[d]}")
    params_str.sort() # sort the params based on the key alphabet order, then in defination of params, do not need to put count in front of q
    unique_key = baseurl+connector+connector.join(params_str) #join() concatenates strings
    return unique_key

    #return baseurl_key1_value1 = baseurl  + "?" + params_str


def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of 
        a dictionary
    '''
    #TODO Implement function
    response = requests.get(baseurl, params=params, auth=oauth)
    results = response.json()
    return results



def make_request_with_cache(baseurl, hashtag, count):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.

    AUTOGRADER NOTES: To test your use of caching in the autograder, please do the following:
    If the result is in your cache, print "fetching cached data"
    If you request a new result using make_request(), print "making new request"

    Do no include the print statements in your return statement. Just print them as appropriate.
    This, of course, does not ensure that you correctly retrieved that data from your cache, 
    but it will help us to see if you are appropriately attempting to use the cache.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        The hashtag to search for
    count: integer
        The number of results you request from Twitter
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''

    #TODO Implement function

    request_key = construct_unique_key(baseurl,params={'count':count,'q': hashtag})
    if request_key in CACHE_DICT.keys():
        print("fetching cached data")
        return CACHE_DICT[request_key]
        # statuslist = CACHE_DICT['statuses']


    else: 
        print("making new request")
        CACHE_DICT[request_key] = make_request(baseurl,params = {'count':count,'q': hashtag})
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]


def find_most_common_cooccurring_hashtag(tweet_data, hashtag_to_ignore):
    ''' Finds the hashtag that most commonly co-occurs with the hashtag
    queried in make_request_with_cache().

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query
    hashtag_to_ignore: string
        the same hashtag that is queried in make_request_with_cache() 
        (e.g. "#MarchMadness2021")

    Returns
    -------
    string
        the hashtag that most commonly co-occurs with the hashtag 
        queried in make_request_with_cache()

    '''
    # TODO: Implement function 
    ''' Hint: In case you're confused about the hashtag_to_ignore 
    parameter, we want to ignore the hashtag we queried because it would 
    definitely be the most occurring hashtag, and we're trying to find 
    the most commonly co-occurring hashtag with the one we queried (so 
    we're essentially looking for the second most commonly occurring 
    hashtags).'''



    statuslist = tweet_data["statuses"]
    hashtag_text_list = []
    for z in statuslist:
        hashtaglist = z['entities']["hashtags"]
        for h in hashtaglist:
            hashtag_text_list.append(h['text'])
 


    m1 = hashtag_to_ignore[1:]

    for h in hashtag_text_list : 
    #if h.find(m1) != -1 or h.find(m1.lower()) != -1 or h.find(m1.upper()) != -1 : # find() method returns the index of first occurence of the substring (if found), if not will return -1
    if h == m1 or h.lower() == m1.lower() or h.upper == m1.upper(): 
        # i used remove(), but there is a bug that some of the item could not remove, TA said it might because when each time when index increase, removing made it sometime missed remove?
        pass
    else:
        hashtag_text_list2.append(h.lower()) # lower() so when use counter() below, it will treat Vote and vote as 2 times
    

    Counter_hashtag = Counter(hashtag_text_list2) # Counter(list) return a class of collections.Counter
    m2 = Counter_hashtag.most_common(1)[0][0] #use .most_common(2)find the 2 most frequent items

    return m2
    


    

if __name__ == "__main__":
    if not client_key or not client_secret:
        print("You need to fill in CLIENT_KEY and CLIENT_SECRET in secret_data.py.")
        exit()
    if not access_token or not access_token_secret:
        print("You need to fill in ACCESS_TOKEN and ACCESS_TOKEN_SECRET in secret_data.py.")
        exit()

    CACHE_DICT = open_cache()
    

    baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    hashtag = "#MarchMadness2021"
    count = 200

    tweet_data = make_request_with_cache(baseurl, hashtag, count)
    # tweets = tweet_data['statuses']
    # for t in tweets:
    #     print(t['text'])

    most_common_cooccurring_hashtag = find_most_common_cooccurring_hashtag(tweet_data, hashtag)
    print("The most commonly cooccurring hashtag with {} is {}.".format(hashtag, most_common_cooccurring_hashtag))
