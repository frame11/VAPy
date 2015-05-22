# VAPy
###The Voat API wrapper for Python3  
---  
#####IN PROGRESS - ALL CLAIMS SUBJECT TO CHANGE
---  

####ABOUT  

VAPy is intended to provide a simple, highly explicit Python interface to the Voat API.  

While Python wrappers for other APIs are typically centered around Submission and Comment classes, VAPy encourages a somewhat more functional approach and consists largely of simple functions and methods designed to make it easier for users to chain those functions together in meaningful ways.

VAPy provides a Profiles class, which can be run as a stand alone application providing a simple user agent and API key management system. Profiles can be used with VAPy applications, providing secure local persistence and renewal for API tokens. Profiles encrypts the voat username, API key, and API token with the Voat password. The Voat password is not stored in the database. Profiles uses [SQLite3](https://www.sqlite.org/) and [simplecrypt](https://github.com/andrewcooke/simple-crypt).

VAPy includes Vapp, a Voat application framework designed to make it even easier to implement simple applications using VAPy. Vapp is more a thought than it is code right now, but it'll have to exist in some form. It may just end up as an additional set of functions in VAPy instead of their own classes.



---
####GETTING STARTED  
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
####VAPy METHODS  

#####Voat Content Dictionaries
Most VAPy functions take a voat content dicitonary as an argument. This is the Python dict corresponding to the json data of the API response to a GET query for a submission or comment.  

**submission_by_id(**submissionID**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a submission dictionary.

**submissions_by_subverse(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a list of submission dictionaries.

**comment_by_id(**commentID**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a submission dictionary.

**comments_by_submission(**submissionID**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns a list comments dictionaries.


#####Dictionary Methods  
Accept Voat submission or comment dictionaries (or both) and return dictionary values. Intended for primary use with list comprehensions.  

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


#####Filter Methods  
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


#####Find Methods

#####Post Methods


#####Subverse Information Methods
Accept a subverse name as a string and return the appropriate subverse information.  

**get_subverse_creation_date(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns string "YYY-MM-DDDOWHH:MM:SS:MSS"  

**get_subverse_subscriber_count(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns int value of number of subverse subscribers

**get_subverse_rated_adult(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns boolean value of adult content (NSFW) flag

**get_subverse_sidebar(**subverse**)**  
&nbsp;&nbsp;&nbsp;&nbsp;Returns raw (html) sidebar text

