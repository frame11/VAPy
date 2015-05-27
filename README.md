# VAPy
###The Voat API wrapper for Python3  
---  
#####IN PROGRESS - ALL CLAIMS SUBJECT TO CHANGE
---  

###CONTENTS

1. [About](#about)  
2. [Getting Started](#getting-started)  
2.1. [Initializing VAPy](#initializing-vapy)  
3. [VAPy Methods](#vapy-methods)  
3.1. [Voat Content Dictionaries](#voat-content-dictionaries)  
3.2. [Dictionary Methods](#dictionary-methods)  
3.3. [Filter Methods](#filter-methods)  
3.4. [Post Methods](#post-methods)  
3.5. [Edit Methods](#edit-methods)  
3.6. [Delete Methods](#delete-methods)  
3.7. [Subverse Information Methods](#subverse-information-methods)  
4. [Tests](#tests)  


###ABOUT  

VAPy is intended to provide a simple, highly explicit Python interface to the Voat API.  

While Python wrappers for other APIs are typically centered around Submission and Comment classes, VAPy encourages a somewhat more functional approach and consists largely of simple functions and methods designed to make it easier for users to chain those functions together in meaningful ways.

VAPy provides a Profiles class, which can be run as a standalone application providing a simple user agent and API key management system. Profiles can be used with VAPy applications, providing secure local persistence and renewal for API tokens. This gives users a "setup and ignore" approach to OAuth2 authentication. Profiles encrypts the voat username, API key, and API token with the Voat password. The Voat password is not stored in the database. Profiles uses [SQLite3](https://www.sqlite.org/) and [simplecrypt](https://github.com/andrewcooke/simple-crypt).

VAPy includes [Vapp](#vapp---voat-application-framework), a Voat application framework designed to make it even easier to implement simple applications using VAPy.



---
###GETTING STARTED  
To use VAPy you need a valid Voat.co login and api key.  

It is recommended that you first create a profile by running Profiles as a standalone applicaiton:

`$ python3 Profiles.py`  

Select "add" and provide a profile name, Voat login credentials, and API key when prompted. That's all there is to it.  

After creating a profile, VAPy can handle OAuth2 authentication with the Voat API. Voat usernames and API keys and tokens are encrytped in a locally persistent database. As a Voat password is required for Voat API token generation, that same Voat password is used as the encryption passphrase to eliminate the need for two passwords per profile. Voat passwords are not stored within the local database.  


#####Initializing VAPy

All VAPy methods are available to any instance of VAPy with a properly initialized self.headers attribute. This attribute must contain a current Voat API key and token or communication with the Voat API will not be possible.

`vapy = VAPy.VAPy()`  
`vapy.load_profile(<profile>, <pwd>)`

`load_profile()` will retreive the profile named `<profile>` and create a working headers attribute.

VAPy can be used without the Profiles component by directly calling the `set_headers()` method:  
  
```vapy = Vapy.Vapy()  ```  
```vapy.set_headers(<uname>, <pwd>, <key>, <token>)```
  

After setting the headers attribute, VAPy functions will work regardless of the use of Profiles.  
  
*Where does Profiles store information on my computer?*  

|Operating System|Directory|  
|:-:|:-:|  
| Linux | ~/.vapy/ |
| Windows | ??? |
| OS X | ??? |


---
###VAPy METHODS  

####Voat Content Dictionaries
Most VAPy functions take a voat content dicitonary as an argument. This is the Python dict corresponding to the json data of the API response to a GET query for a submission or comment.  

######Sample submission_dict
```

```  

######Sample comment_dict
```

```  

**get_subverse(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a list of [(submission_dict, [comment_dicts]), ...]

**get_submission_by_id(**subverse, submissionID**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a submission dictionary.

**get_submissions(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a list of submission dictionaries.

**get_content_submissions(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a list of content submission dictionaries.

**get_url_submissions(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a list of url submission dictionaries.

**get_comment_by_id(**commentID**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a submission dictionary.

**get_comments_by_submission(**submission, subverse=None**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a list comments dictionaries. Accepts a submission dict, or submission id and subverse.
  

####Dictionary Methods  
Returns values from (or calculated from) Voat content dictionaries.  

&nbsp;&nbsp;&nbsp;&nbsp;`user_names = [vapy.get_author(d) for d in some_itr_of_voat_content_dicts]`  

Some keys are shared between submission and comment dicts while others are unique to only one. As a result, some VAPy dictionary methods will only return data when passed a specific content dictionary type. For example, **get_submission_type()** will never return a result when passed a comment dictionary just as **get_parent_id()** will never return a result when passed a submission dictionary.

**get_content(**voat_dict, ignore_links=False**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns content of submission or comment. If ignore_links == True and voat_dict is a link submission, returns **None**.  

**get_subverse(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns name of subverse submission or comment is posted to.

**get_author(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns author or submission or comment.  

**get_score(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns integer value of current score for submission or comment.

**get_scores(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns (int, int) tuple of upvotes/downvotes for submission or comment.

**get_date(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns date and time submission or comment was posted.

**get_id(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns integer value of submission or comment ID.

**get_permalink(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns Voat.co url for submission or comment.

**get_submission_type(**submission_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns submission type: "url" or "content".

**get_submission_title(**submission_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns title of submission.

**get_submission_rank(**submission_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns current rank of submission.

**get_submission_comment_count(**submission_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns integer value of total number of comments under a submission.

**get_comment_submission(**comment_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns the ID of the submission a comment is under.

**get_comment_parent(**comment_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns the ID of the a comment's parent comment. Returns **None** if comment is for a top-level comment.


####Filter Methods  
Intended to be used primarily with filter(), VAPy filter methods accept voat content dictionaries and return a boolean value.  
  
&nbsp;&nbsp;&nbsp;&nbsp;`main_comments = filter(vapy.is_top_level_comment, itr_of_dicts`  
  
&nbsp;&nbsp;&nbsp;&nbsp;`links = [vapy.get_links(d) for d in filter(is_url_submission, itr_of_dicts)]`

**contains_regex(**voat_dict, ignore_links=False**)**  
&nbsp;&nbsp;&nbsp;&nbsp; **True** if regex in title or content or link of submission or content of comment, **False** if not. If ignore_links == True, link submissions always return **False**.

**is_submission(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp; **True** if submission, **False** if comment.

**is_comment(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp; **True** if comment, **False** if submission.

**is_top_level_comment(**voat_dict**)**  
&nbsp;&nbsp;&nbsp;&nbsp; **True** if comment is directly under submission, **False** is comment is under another comment.


####Post Methods
**post_text_submission(**subverse, title, text**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Submit a new text submission.

**post_link_submission(**subverse, title, url**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Submit a new link submission.

**post_reply_to_submission(**submission_id, comment**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Submit a new top-level comment to a submission.

**post_reply_to_comment(**comment_id, comment**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Submit a new comment in response to another comment.

**post_reply_to_pm(**pm_id, comment**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Submit reply to a personal message.  

####Edit Methods

**edit_submission(**submission_id, title, content**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Replaces submissions title and content.  

**edit_comment(**comment_id, comment**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Replaces submissions title and content.  

####Delete Methods

**delete_submission(**submission_id**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Replaces submissions title and content.  

**delete_comment(**comment_id**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Replaces submissions title and content.  

####Subverse Information Methods
Accept a subverse name as a string and return the appropriate subverse information.  

**get_subverse_creation_date(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns string "YYY-MM-DDDOWHH:MM:SS:MSS"  

**get_subverse_subscriber_count(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns int value of number of subverse subscribers

**get_subverse_rated_adult(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns boolean value of adult content (NSFW) flag

**get_subverse_sidebar(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns raw (html) sidebar text
  
###Tests
VAPy methods are covered by tests.py, which uses Profiles for OAuth2 management. To run tests.py it is necessary to create a valid profile with the profile name "test". Alternatively, the user can alter the load_profile() call of VAPyTests.setUp() to load any profile desired.

Tests run rather slow because of the overhead on decrypting OAuth2 credentials for each VAPy instance. The values could get loaded into a holder in the setUpClass() call, and then passed to the VAPy isntance with setHeader() rather than using load_profile(). This should greatly reduce testing time.


##Vapp - Voat Application Framework  

The Vapp framework attempt to make it easy for people to make simple Voat applications.


####Vapp()  
Base superclass of the Vapp framework. Initializes VAPy and loads Profile. Initializes the Records class which provides local data persistence for the applicaiton.  

user defined config.json attributes:  
- *app_name* is the name of the applicaiton
- *subverses*  is a list of one or more subverses (strings) that the application will read and write content to and from.  

  
predefined config.json attributes:  
- *nsfw* is a boolean value, default False. If False, the application ignores all NSFW flagged content.  
- *adult_app* is a boolean value, default False. If True, all posts by application are flagged NSFW.   
