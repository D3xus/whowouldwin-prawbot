from datetime import datetime

def update_stylesheet(subreddit):
    # Grab the subreddit's stylesheet
    stylesheet = subreddit.stylesheet
    
    # Read the file from the built CSS
    newCSS = ""
    with open('../reddit/reddit.css', 'r') as reddit_css:
        newCSS=reddit_css.read().replace('\n', '')

    # Update the CSS on the subreddit with the built css
    now=datetime.today().strftime("%c")
    stylesheet.update(newCSS, "Automated CSS update at " + now)
    print("CSS updated at " + now + "!")

    return True