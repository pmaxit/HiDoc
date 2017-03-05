# Hi Doc, Chatbot

Flask base python chat bot designed to make diagnosing illness easier. This conversational bot is named "Chappie" and comes with in-build state-of-art machine learning algorithms to detect diagnosis from symptoms. It also allows users to contact doctors, book appointments, and ask questions with the chatbot intended to speed up this process.


## Initial installation
Fork this repository and clone.

## Launch Server in heroku
create heroku project and push to heroku:
```bash
heroku create
git push heroku master
```

## Further Configuration
  * Setup your Facebook Webhook callback to the heroku app you deployed.
  * Set the following in your HEroku Config Variables:
 
 ```
 WIT_TOKEN = "your wit.ai token"
 FB_PAGE_TOKEN = "your facebook page token"
 FB_VERIFY_TOKEN = "your webhook verification token"
```
## Documentation
 
 Within the repository you'll find the following directories and files:
 
 ```
 Wit-Facebook-Weather-Py
         ├── setup needed as Heroku pip doesn't find this.
         ├── app.json
         ├── Procfile
         └── README.md
         └── server.py
         └── requirements.txt
 ```
