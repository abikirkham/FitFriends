# FitFriends

## Purpose

A social app used for gym goers who want to find friends to go to the gym with, motivate and find new fitness tips. To build thier own profile with fitness states and what they are about and how they enjoy fitness. To message new firends privately and have a more personalised conversation to share tips and experiences. 

## User stories
- authorisation 
- profiles
- add friends
- post updates
- comment
- like
- private message

## Wireframes

<img width="273" alt="User Profile" src="https://github.com/abikirkham/FitFriends/assets/144112159/98a625b1-164f-4e09-a371-d76cb53cfc29">

<img width="289" alt="Overview homepage" src="https://github.com/abikirkham/FitFriends/assets/144112159/bbfe03ad-bf5d-477d-a70c-1d90fdf13f45">

<img width="273" alt="Login" src="https://github.com/abikirkham/FitFriends/assets/144112159/12944704-38e9-4dd8-a512-3365f15d1a0e">

<img width="272" alt="Direct Messages" src="https://github.com/abikirkham/FitFriends/assets/144112159/47bff5fa-4b0c-4cb7-97fc-99dae41fac1c">


## Flow chart 
Start
|
|__Homepage
|   |
|   |__Signup Option
|   |   |
|   |   |__User provides: Username, Email, Password, Confirm Password
|
|__Login Page
|   |
|   |__Username
|   |
|   |__Password
|   |
|   |__Login Button
|
|__Homepage (Logged in)
|   |
|   |__User Statistics (personal or shared)
|   |   |
|   |   |__Height
|   |   |
|   |   |__Weight
|   |   |
|   |   |__Age
|   |   |
|   |   |__Flexibility Level
|   |   |
|   |   |__Confidence Level
|   |   |
|   |   |__Stress Level
|   |   |
|   |   |__More... ? connect to Apple Watch?
|   |
|   |__Add friends
|   |
|   |__search option
|       |
|       |__view their profile
|           |
|           |__add
|           |
|           |__Message
|
|__Settings Page
|   |
|   |__Change Personal Details
|   |   |
|   |   |__Username
|   |   |
|   |   |__Email
|   |   |
|   |   |__Password
|   |   |
|   |   |__Confirm Password
|   |   |
|   |   |__Save Changes Button
|   |
|   |__Close Account
|       |
|       |__Confirmation Dialog
|       |   |
|       |   |__Yes, Close Account
|       |   |
|       |   |__No, Cancel
|
|
|__Chat Page
    |
    |__Search Users
    |
    |__Conversations
    |
    |__Share Fitness Tips/Progress Tracker



## Technologies used 
- HTML
- CSS
- PYTHON
- JAVASCRIPT
- DJANGO 
- BOOTSTRAP
- BULMA
- HEROKU
- NEON
- WHITENOISE

## Set up
https://docs.djangoproject.com/en/dev/intro/tutorial01/ - understand set up
used codde institute google doc cheatsheets to ensure cloudinary, neon sql and heroku set up.

## Testing

## Issues

- intial issues - when the base was set up - the links would not work to go to the other pages, for example, when click register it would not log them in, when uodate profile, it would go to error page 505. I checked the django documentation which i saw these were in line and written correctly, the urls and views where matched up well and my directory was in the correct order. I asked code institute tutors for assistance. 

## Credits
- [WireFrames](https://cacoo.com/diagrams/QXSJF7qPDCKNuzVk/B4F94?reload_rt=1718100120618_1&)
- [Base project for a social network site](https://realpython.com/django-social-network-1/)
