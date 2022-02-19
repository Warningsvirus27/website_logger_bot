# website_logger_bot

The program is written to log you in for multiple websites.
The program uses selenium module to automate the login process and beautifulsoup module to dynamically locate the login fields

The program is fully dynamic and prints out the login at console as successfull or vice versa

The program reads a txt file containing the website url, username and password for the login; seperated by comma
The login continues untill the last url is not visited

For dynamic logging, selenium module
opens up the crome browser, redirect to the specified url
now the beautifulsoup module, helps in web scaraping and located the username login field and password login field, 
thenafter the username and password is filled in the same, and login is made.

