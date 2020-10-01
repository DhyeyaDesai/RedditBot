import praw
import smtplib
import datetime

SCHEDULED_TIME = 100
UPVOTES_REQUIRED = 0
keywords = ['invest']
client_id = '9Lcntf9Gu5D3tQ'
client_secret = '4Nn0yXerVDMv0mZqVDjkTkIKWy8'
user_agent = 'wallstreetbets bot'

def getPostTime(postTime):
    return round((datetime.datetime.now().timestamp() - postTime)/60)

def getPosts():
    posts = []
    reddit = praw.Reddit(client_id = client_id , client_secret = client_secret, user_agent = user_agent)
    all_posts = reddit.subreddit('wallstreetbets').new(limit=10)
    for post in all_posts:
        postTime = getPostTime(post.created_utc)
        if(postTime < SCHEDULED_TIME):
            if post.score > UPVOTES_REQUIRED:
                for keyword in keywords:
                    if keyword in post.title.lower() or keyword in post.selftext.lower():
                        p = {'Title': post.title, 'Duration': postTime, 'Upvotes': post.score, 'URL': post.url}
                        posts.append(p)
    return posts

def emailPosts(posts):
    if posts:
        for post in posts:
            message = f"Hey! A post got {post['Upvotes']} upvotes in {post['Duration']} minutes. You might wanna take a look:\n\"{post['Title']}\"\n{post['URL']}"

            if post['Upvotes'] == 1:
                message = message.replace("upvotes", "upvote")
            if post['Duration'] == 1:
                message = message.replace("minutes", "minute")
            
            subject = f"[RedditBot] \"{post['Title']}\""
            
            print(subject)
            # print()
            # print(message)
            # print()

            msg = f"Subject: {subject}\n\n{message}"

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login("rahuldesai1999@gmail.com", "icmdwcnsjzlsluni")

            server.sendmail(
                "rahuldesai1999@gmail.com",
                "rahuldesai1999@gmail.com",
                msg 
            )


def main():
    posts = getPosts()
    emailPosts(posts)

main()

# schedule.every().day.do(main)
# while 1:
# 	schedule.run_pending()
# 	time.sleep(1)