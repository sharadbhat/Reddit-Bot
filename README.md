# RedditBot

A simple call and response Reddit bot. 

Called with the phrase '!islinkdown link_name' 

It searches all comments from all subreddits to search for use phrase '!islinkdown'. 
If found, it checks the link provided along with the phrase to see if the website is up or not. 

http://downforeveryoneorjustme.com is used to check validity of the link.

Adds the comment ID to a file. Next time, it checks the file to see if the comment ID is already present.
