djmessenger
===========

.. image:: https://badge.fury.io/py/djmessenger.svg
   :target: https://badge.fury.io/py/djmessenger

.. image:: https://img.shields.io/badge/python-3.4-brightgreen.svg

djmessenger provides a simple way to build a Facebook Messenger BOT

Download
--------

Get the latest version of ``djmessenger`` from 
https://pypi.python.org/pypi/djmessenger

::

    $ pip install djmessenger
    
To get the git version

::

    $ git clone git://github.com/ifanchu/djmessenger.git


Overview
--------

.. image:: https://www.lucidchart.com/publicSegments/view/b4bee311-d2f0-4757-bccf-04d73eefb14d/image.png

**djmessenger** is essentially a REST API. djmessenger simply exposes a REST API
endpoint for Facebook Messenger webhook so that Facebook will send a 
request to **djmessenger** endpoint when subscribed events happen. 

Here is how **djmessenger** works (roughly, though)

1. Upon receiving message relayed by Facebook (Facebook call this a 
   **callback**), ``receiving`` module kicks in and determines what's 
   the ``ReceivingType`` (defined by **djmessenger**) of the message
2. Because each **callback** could contain multiple messages, we loop 
   them one by one.
   this could happen if your BOT was somehow not responding for a while, 
   and when the BOT just comes online, it will get all the messages that 
   were failed to deliver previously at once
   
3. From `routing policy <https://github.com/ifanchu/djmessenger/wiki/Routing-Policy>`_, 
   we got corresponding **Rule** for this type of **Callback**, then 
   we apply each **Rule** to each **Messaging** (within **Callback**)
4. Each **Rule** contains 

   4.1 Multiple **Filter**: Takes a **Messaging** and determines 
       whether it should pass and continue further, if all filters 
       pass, proceed with **Handler**
   4.2 Multiple **Handler**: Takes a **Messaging** and performs internal
       operation such like saving something into database, and etc. 
   4.3 Multiple **Replier**: Takes a **Messaging** and reply something 
       back to the Facebook user


Features
--------

* For each message sent, record sender's PSID (page-scoped ID) so that
  we can send something back to the sender
* Save user basic info into database
* If the user sends a location, save it into database
* If the user sends a simple text, filter it with regex and send back 
  something
* Send Quick Replies and handle its postback
* Send Buttons and handle its postback
* Easy to `setup <https://github.com/ifanchu/djmessenger/wiki/Minimal-BOT-Setup>`_
* Flexible to extend
* Flexible `routing policy <https://github.com/ifanchu/djmessenger/wiki/Routing-Policy>`_
* `i18n support <https://github.com/ifanchu/djmessenger/wiki/i18n-Support>`_

Current Receiving Types
-----------------------

::

    ReceivingType.SIMPLE_TEXT
    ReceivingType.QUICK_REPLY
    ReceivingType.IMAGE
    ReceivingType.AUDIO
    ReceivingType.VIDEO
    ReceivingType.FILE
    ReceivingType.LOCATION
    ReceivingType.STICKER
    ReceivingType.POSTBACK
    ReceivingType.AUTHENTICATION
    ReceivingType.ACCOUNT_LINKING
    ReceivingType.DELIVERED
    ReceivingType.READ
    ReceivingType.ECHO
    # this is not a real type, this is for routing.py to indicate the settings is
    # not for a specific type but for all type
    ReceivingType.DEFAULT
    # the follows are special types to handle thread settings, all of these will
    # be handled by PostbackReceivedChecker
    ReceivingType.PERSISTENT_MENU_ONE
    ReceivingType.PERSISTENT_MENU_TWO
    ReceivingType.PERSISTENT_MENU_THREE
    ReceivingType.PERSISTENT_MENU_FOUR
    ReceivingType.PERSISTENT_MENU_FIVE
    ReceivingType.GET_STARTED_BUTTON

Filters
-------

* LocationFilter: 

    Check if Messaging contains a Location

* StickerFilter: 

    Check if Messaging contains sticker like thumbup

* ThumbUpFilter: 

    Check if Messaging contains thumbup, extends StickerFilter

* PostbackFilter: 

    Check if Messaging contains Postback, which will be sent by Facebook 
    if user clicks on Quick Reply or Button

* SimpleTextRegexFilter: 

    takes a regex and checks whether the text in the Messaging 
    matches the regex

* MultimediaFilter: 

    Check if Messaging contains multimedia, IMAGE, AUDIO, VIDEO and FILE

* EmailFilter: 

    Check if the text in Messaging is an email

* TimeFilter: 

    Check if the Messaging was sent within a predefined time period


Handlers
--------

* UserProfileHandler

    This handler saves user PSID (page-scoped ID, which is required in 
    order to send something back) and/or some user basic info such as
    first name, last name, locale, and etc

* SaveMessagingHandler

    Save the given ``Messaging`` instance into database
    
* ThumbUpHandler

    This handler increment the user's thumbup count in the database

* LocationHandler

    Save the Location for the user into database

* BasePostbackHandler

    Handles postback which will be sent if the user clicks on Quick Reply
    or Button. Dev needs to subclass this to provide custom logic
    
* BaseQuickReplyPayloadHandler

    Handles the quick reply, dev need to subclass this handler to provide
    customized handling logic
    
Repliers
--------

* SimpleMessageReplier

    Sends back a text message

* DefaultMessageReplier (extends SimpleMessageReplier)

    Sends back default message defined in settings
    
* SenderActionReplier

    Sends back a sender action
    
* ImageReplier

    Sends back a IMAGE which needs an URL

* AudioReplier

    Sends back a AUDIO which needs an URL

* VideoReplier

    Sends back a VIDEO which needs an URL

* FileReplier

    Sends back a FILE which needs an URL
    
* BaseQuickReplySender

    Sends back at most 10 quick replies, dev needs to subclass this sender
    to provide custom payload for the quick replies
    
* BaseButtonSender

    Sends back at most 3 buttons, dev needs to subclass this sender to 
    provide custom payload for postback buttons
    
Thread Settings
---------------

Thread settings are defined in settings.py and use management command
to invoke

* Persistent Menu
* Greetings
* Get Started Button

Prerequisites
-------------

1. You must have a Facebook page, this is different from having a personal account, 
   but you can always create a page as you like for free
2. Obtain your page access token
    * Login to `Facebook Developers <https://developers.facebook.com>`_
    * From top right **My Apps**, click on **Add a New App**
    * Enter this new app
    * From left side, **+ Add Product**
    * Click **Get Started** on **Messenger** and **Webhooks**
    * Go to **Messenger**, in **Token Generation**, choose a page and copy the token for later use
    * Click **Webhooks** and leave this page open for later

Minimal BOT Setup
-----------------

https://github.com/ifanchu/djmessenger/wiki/Minimal-BOT-Setup

Detailed customized BOT
-----------------------

https://github.com/ifanchu/djmessenger/wiki/Customized-BOT-Showcase

Example App
-----------

https://github.com/ifanchu/djmessenger/tree/master/testapp
