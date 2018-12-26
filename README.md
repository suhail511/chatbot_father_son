# Father-Son-Chatbot

The Father-Son chatbot that I trained to talk. This is following a clone of [this repository](https://github.com/adeshpande3/Facebook-Messenger-Bot) and [this blog-post](https://adeshpande3.github.io/adeshpande3.github.io/How-I-Used-Deep-Learning-to-Train-a-Chatbot-to-Talk-Like-Me)

## Overview

For this project, I wanted to train a Sequence To Sequence model on some conversation logs of Father-Son conversation dataset. Let me explain how you can train the chatbot.

## Requirements and Installation
In order to run these scripts, you'll need the following libraries.

* **[TensorFlow](https://www.tensorflow.org/install/) version 1.0 or later**
* [NumPy](https://docs.scipy.org/doc/numpy/user/install.html)
* [Pandas](https://pandas.pydata.org/pandas-docs/stable/install.html)
* [Sklearn](http://scikit-learn.org/stable/install.html)

## How You Can Train

1. Download and unzip [this entire repository from GitHub](https://github.com/Pphhaaaddd/chatbot_father_son), either interactively, or by entering the following in your Terminal.
    ```bash
    git clone https://github.com/Pphhaaaddd/chatbot_father_son
    ```

2. Navigate into the top directory of the repo on your machine
    ```bash
    cd chatbot_father_son
    ```
3. The first job is to get Chat Data samples from different sources and put them in '''files''' folder. Make sure the txt files are in the following format:

  ![](Images/sample01.jpg)

### If you don't have any Chat Data samples, use our pre-trained model. Skip to step 7.
4. Now that we have all our conversation logs, we can go ahead and create our dataset. In our directory, let's run:
    ```bash
    python createDataset.py
    ```
    This will create Conversation Data for both Father and Son. This script will create a files named **sonConversationDictionary.npy** and **fatherConversationDictionary.npy** which are Numpy objects that contains pairs in the form of (MESSAGE, RESPONSE). File named **sonConversationData.txt** and **fatherConversationData.txt** will also be created. These are simply large text files the dictionary data in a unified form.

5. Now that we have these files, we can start creating our word vectors through a Word2Vec model. This step is a little different from the others. The Tensorflow function we see later on (in SonSeq2seq.py and FatherSeq2Seq.py) actually also handles the embedding part.
    ```bash
    python SonWord2Vec.py
    python FatherWord2Vec.py
    ```
    If you run word2vec.py in its entirety, this will create different wordlist files for Father and Son. **SonWordList.txt** and **FatherWordList.txt**, which simply contains all of the unique words in our corpus.

6. Now, we can use create and train our Seq2Seq model.
    ```bash
    python SonSeq2Seq.py
    python FatherSeq2Seq.py
    ```
    This will create more different files. **SonSeq2SeqXTrain.npy**, **SonSeq2SeqYTrain.npy**, **FatherSeq2SeqXTrain.npy** and **FatherSeq2SeqYTrain.npy** are the training matrices that Seq2Seq will use. Again, we save these just in case we want to make changes to our model architecture, and we don't want to recompute our training set. The last file(s) will be .ckpt files which holds our saved Seq2Seq model. Models will be saved at different time periods in the training loop. These will be used and deployed once we've created our chatbot.
<!--
7. Now that we have a saved model, let's now create our Facebook chatbot. To do so, I'd recommend following this [tutorial](https://github.com/jw84/messenger-bot-tutorial). You don't need to read anything beneath the "Customize what the bot says" section. Our Seq2Seq model will handle that part. **IMPORTANT - The tutorial will tell you to create a new folder where the Node project will lie.** Keep in mind this folder will be different from our folder. You can think of this folder as being where our data preprocessing and model training lie, while the other folder is strictly reserved for the Express app (EDIT: I believe you can follow the tutorial's steps inside of our folder and just create the Node project, Procfile, and index.js files in here if you want). The tutorial itself should be sufficient, but here's a summary of the steps.

    - Build the server, and host on Heroku.
    - Create a Facebook App/Page, set up the webhook, get page token, and trigger the app.
    - Add an API endpoint to **index.js** so that the bot can respond with messages.

    After following the steps correctly, you should be able to message the chatbot, and get responses back.

    ![](Images/DefaultChatbotResponse.png)

8. Ah, you're almost done! Now, we have to create a Flask server where we can deploy our saved Seq2Seq model. I have the code for that server [here](https://github.com/adeshpande3/Chatbot-Flask-Server). Let's talk about the general structure. Flask servers normally have one main .py file where you define all of the endpoints. This will be [app.py](https://github.com/adeshpande3/Chatbot-Flask-Server/blob/master/app.py) in our case. This whill be where we load in our model. You should create a folder called 'models', and fill it with 4 files (a checkpoint file, a data file, an index file, and a meta file). These are the files that get created when you save a Tensorflow model.

![](Images/Models.png)

In this app.py file, we want to create a route (/prediction in my case) where the input to the route will be fed into our saved model, and the decoder output is the string that is returned. Go ahead and take a closer look at app.py if that's still a bit confusing. Now that you have your app.py and your models (and other helper files if you need them), you can deploy your server. We'll be using Heroku again. There are a lot of different tutorials on deploying Flask servers to Heroku, but I like [this one](https://coderwall.com/p/pstm1w/deploying-a-flask-app-at-heroku) in particular (Don't need the Foreman and Logging sections).

9. Once you have your Flask server deployed, you'll need to edit your index.js file so that the Express app can communicate with your Flask server. Basically, you'll need to send a POST request to the Flask server with the input message that your chatbot receives, receive the output, and then use the sendTextMessage function to have the chatbot respond to the message. If you've cloned my repository, all you really need to do is replace the URL of the request function call with the URL of your own server.

There ya go. You should be able to send messages to the chatbot, and see some interesting responses that (hopefully) resemble yourelf in some way.

## Samples

![](Images/Samples.png)

**Please let me know if you have any issues or if you have any suggestions for making this README better. If you thought a certain step was unclear, let me know and I'll try my best to edit the README and make any clarifications.** -->
