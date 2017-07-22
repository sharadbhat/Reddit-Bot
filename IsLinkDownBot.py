import praw
from praw.exceptions import APIException
import requests
import bs4
import time

reddit = praw.Reddit(client_id = '**********',
                    client_secret = '*********************',
                    username = 'IsLinkDownBot',
                    password = '**********',
                    user_agent = 'IsLinkDown v1.0')

subreddit = reddit.subreddit('all')



def is_link_down(link):
    """
    Checks downforeveryoneorjustme.com to find out if the link is down or not.
    If an error occurs, waits for 2 minutes and tries again.
    Takes the link as input.
    Returns message as output.
    """
    link = link.lower()
    url = "http://www.downforeveryoneorjustme.com/{}".format(link)
    try:
        if not link.startswith('http://') or not link.startswith('https://'):
            link2 = link
            link = 'https://' + link
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        for p_tag in soup.find_all('p'):
            result = str(p_tag.contents[0]).strip()
            if result == "It's just you.":
                result += "\n\n[" + link2 + "](" + link + ")" + " is up for everybody else.\n\n[Developer](https://reddit.com/u/sharadbhat7) | [Code](https://github.com/sharadbhat/RedditBot) | [Feedback](https://www.reddit.com/message/compose?to=sharadbhat7&subject=Feedback)"
            elif result == "It's not just you!":
                result += "\n\n[" + link2 + "](" + link + ")" + " is down for everybody else.\n\n[Developer](https://reddit.com/u/sharadbhat7) | [Code](https://github.com/sharadbhat/RedditBot) | [Feedback](https://www.reddit.com/message/compose?to=sharadbhat7&subject=Feedback)"
            break
        return result
    except:
        time.sleep(120)
        is_link_down(link)



while True:
    """
    If !islinkdown has been mentioned in any comment, it replies with the message.
    """
     try:
        for comment in subreddit.stream.comments():
            comment_text = str(comment.body.lower()) #!islinkdown google.com
            if "!islinkdown" in comment_text.split():
                with open("comments_replied_to.txt", "r") as f:
                    comments_replied_to = f.read()
                    comments_replied_to = comments_replied_to.split("\n")
                    comments_replied_to = list(filter(None, comments_replied_to))
                    if comment.id not in comments_replied_to:
                        comment_text = comment_text.replace("!islinkdown", "") # google.com
                        comment_text = comment_text.strip() #google.com
                        url = comment_text
                        reply_text = is_link_down(url)
                        try:
                            comment.reply(reply_text)
                            comments_replied_to.append(comment.id)
                        except APIException as ae:
                            if (str(ae).split())[0].replace(":", "") == "RATELIMIT":
                                time_to_wait = int(str((str(ae).split())[10]))
                                print("Waiting for " + str(time_to_wait),end="\r")
                                time.sleep(time_to_wait * 60)
                            break #Unable to reply. RateLimitExceeded might have occured.
                with open("comments_replied_to.txt", "w") as f:
                    for comment_ID in comments_replied_to:
                        f.write(comment_ID + "\n")
    except:
        continue
