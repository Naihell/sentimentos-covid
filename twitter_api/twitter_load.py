import csv
import sys
import os
import tweepy

# Substituir pelos valores vinculados ao dev user do twitter.
auth = tweepy.AppAuthHandler('API_KEY', 'API_SECRET')
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

query = ['pandemia']  # Termos a serem procurados nas mensagens.
total_tweets = 5000000 # Qualquer valor desejado para que a api tente buscar.
tweets_by_request = 100  # A API tem a limitação de 100 tweets por requisição.
file_name = 'nome.csv' # Nome do arquivo gerado.
# Deixando None a API vai varrer todos os resultados possíveis. Caso tenha algum ID definido ele irá buscar a partir do valor informado.
since_id = None

# Variável auxilia em todo o controle do laço para chamar a API.
max_id = -1
tweet_count = 0
print("Downloading max {0} tweets".format(total_tweets))

with open(file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["tweet_id", "time_stamp", "coordinates", "retweets_count", "user_id", "user_screen_name", "message"])

    while tweet_count < total_tweets:
        try:
            if (max_id <= 0):
                if (not since_id):
                    new_tweets = api.search(q=query, lang='pt', locale="pt-br", count=tweets_by_request, tweet_mode='extended')
                else:
                    new_tweets = api.search(q=query, lang='pt', locale="pt-br", count=tweets_by_request, since_id=since_id, tweet_mode='extended')
            else:
                if (not since_id):
                    new_tweets = api.search(q=query, lang='pt', locale="pt-br", count=tweets_by_request, max_id=str(max_id - 1), tweet_mode='extended')
                else:
                    new_tweets = api.search(q=query, lang='pt', locale="pt-br", count=tweets_by_request, max_id=str(max_id - 1), since_id=since_id, tweet_mode='extended')
            if not new_tweets:
                print("No more tweets found")
                break

            for tweet in new_tweets:
                try:
                    writer.writerow([tweet.id, tweet.created_at, tweet.coordinates, tweet.retweet_count, tweet.user.id, tweet.user.screen_name, tweet.full_text])
                    print(counter, tweet.id, tweet.created_at, tweet.coordinates, tweet.retweet_count, tweet.user.id, tweet.user.screen_name, tweet.full_text)
                except AttributeError:  # Not a Retweet
                    writer.writerow([tweet.id, tweet.created_at, tweet.coordinates, tweet.retweet_count, tweet.user.id, tweet.user.screen_name, tweet.text])
                    print(counter, tweet.id, tweet.created_at, tweet.coordinates, tweet.retweet_count, tweet.user.id, tweet.user.screen_name, tweet.full_text)
            tweet_count += len(new_tweets)

            print("Downloaded {0} tweets".format(tweet_count))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweet_count, file_name))
