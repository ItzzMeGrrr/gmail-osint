# Get Google user ID from email address

This is a simple script to get the Google user ID from an email address.

```
usage: getUID.py [-h] email

Get UID from Gmail

positional arguments:
  email       Email address

options:
  -h, --help  show this help message and exit
```

#### How can I capture the request?

You can use any proxy tool to capture the request and save it to the `request.txt` file. I used [Burp Suite](https://portswigger.net/burp/communitydownload).
#### Which Request should I capture?

Open Gmail, and sign in if not already signed in. Set up the proxy to capture the request. 
1. Now click on compose in Gmail, it will pop up a small window to compose the email. 
1. Now click on the `To` field and start typing any email address. 
    - If you are using burp, you can see the request in the `Proxy` tab.
    - If you are using any other proxy tool, find wherever the requests are displayed.
1. The request will look like this, `https://people-pa.clients6.google.com/$rpc/google.internal.people.v2.minimal.PeopleApiAutocompleteMinimalService/ListAutocompletions`
1. If you are in Burp you can right-click and `copy to file` to save the request. Save it as `request.txt`

That's all now you can run the script and get the UID of any email.


#### Why do I need to capture the request?

The request has cookies and access tokens that are required to make the request.
So, DO NOT share that file with anyone because with the file they can impersonate you.

### Example

```bash
$ python3 getUID.py larry.page@google.com
{"UID":"111627209495762463002","image_url":"https://lh3.googleusercontent.com/a-/ACB-R5TQDeBKd3nXn_1WQlBDQ3hmvueUq1915eySpGb-b3M"}

```

### References

https://medium.com/hacking-info-sec/how-to-gmail-osint-like-a-boss-1ca4f55f55e2
