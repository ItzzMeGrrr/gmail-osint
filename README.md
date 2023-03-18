# Get Google user ID from email address

This is a simple script to get the Google UID from an email address.

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

### Example

```bash
$ python3 getUID.py larry.page@google.com
{"UID":"111627209495762463002","image_url":"https://lh3.googleusercontent.com/a-/ACB-R5TQDeBKd3nXn_1WQlBDQ3hmvueUq1915eySpGb-b3M"}

```

### References

https://medium.com/hacking-info-sec/how-to-gmail-osint-like-a-boss-1ca4f55f55e2
