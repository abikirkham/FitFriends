# FitFriends

<img width="1489" alt="Screenshot 2024-06-20 at 16 51 09" src="https://github.com/abikirkham/FitFriends/assets/144112159/d3fdcc55-1988-4ad0-8b66-e484321c2e05">

## Purpose

A social app used for gym goers who want to find friends to go to the gym with, motivate and find new fitness tips. To build thier own profile with fitness states and what they are about and how they enjoy fitness. To message new firends privately and have a more personalised conversation to share tips and experiences. 

## User Stories

1. **Authorization**
   - As a user, I can log in and log out of the site which ensures my account is secure and provides access to personalized features.

2. **Profiles**
   - As a user, I can create and edit my profile which displays and updates my personal information and activities.

3. **Add Friends**
   - As a user, I can add friends who have the same interests which allows me to connect with or remove connections with other users.

4. **Post Updates**
   - As a user, I can post my thoughts and activities with everyone on the site which allows me to find new friends with similar interests.

5. **Comment**
   - As a user, I can comment on others posts which allows me to interact with and manage my contributions to my friends' posts.

6. **Like**
   - As a user, I can like and unlike updates which shows or removes my appreciation for my friends' posts.

7. **Private Message**
   - As a user, I can send and receive private messages which allows me to communicate directly and privately with other users.


## Wireframes

<img width="273" alt="User Profile" src="https://github.com/abikirkham/FitFriends/assets/144112159/98a625b1-164f-4e09-a371-d76cb53cfc29">

<img width="289" alt="Dashboard" src="https://github.com/abikirkham/FitFriends/assets/144112159/bbfe03ad-bf5d-477d-a70c-1d90fdf13f45">

<img width="273" alt="Login" src="https://github.com/abikirkham/FitFriends/assets/144112159/12944704-38e9-4dd8-a512-3365f15d1a0e">

<img width="272" alt="Messages" src="https://github.com/abikirkham/FitFriends/assets/144112159/47bff5fa-4b0c-4cb7-97fc-99dae41fac1c">


## Flow chart 
<img width="850" alt="FlowChart" src="https://github.com/abikirkham/FitFriends/assets/144112159/d94951a3-dfa9-4344-8ff1-9312b267aa30">

Using: [Lucidchart Flowchart](https://lucid.app/lucidspark/9fbfecbb-4dd1-4c0a-8630-f0a85bd5505f/edit?beaconFlowId=644738E63C273F37&invitationId=inv_6a141c5b-80a3-42e5-890c-93dc1ef500d8&page=0_0)



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
- WHITENOISE / Clouidnary initially


## Setup

### DJANGO

1. **Install Django** :
pip install django

2. **Create a Django project** :
django-admin startproject myproject
cd myproject


### NEON

1. **Install Neon**:
pip install neon


2. **Setup Neon**:
- Create a `neon_settings.py` file in your Django project directory.
- Configure your settings in this file using Neon's syntax for environment-based configuration. For example:
  ```python
  from neon import settings

  settings.configure(
      DEBUG=True,
      DATABASES={
          'default': {
              'ENGINE': 'django.db.backends.sqlite3',
              'NAME': 'mydatabase',
          }
      },
      # Add other settings as needed
  )
  ```

3. **Integrate Neon with Django settings**:
Modify your `settings.py` to load settings from `neon_settings.py`:
```python
# settings.py
from neon.contrib.django import get_neon_settings

neon_settings = get_neon_settings()
if neon_settings:
    locals().update(neon_settings)
```

### Whitenoise
1. **Install Whitenoise**:

pip install whitenoise

2. **Configure Whitenoise**:

Add 'whitenoise.middleware.WhiteNoiseMiddleware', to the MIDDLEWARE list in your settings.py:

```python
MIDDLEWARE = [
    # Other middleware classes
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
```
3. **Configure static file handling in settings.py**:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

4. **Final Steps**
Collect static files:

python manage.py collectstatic
Run migrations:

python manage.py migrate
Start the Django development server:

python manage.py runserver




## Features 

- HOME
- USER AUTH / LOGIN / SIGN UP
- DASHBOARD
- PROFILE
- MESSAGES
- ABOUT

## Testing

## Issues

- intial issues with static files - look back on code insitute tutor chat 

## Credits
- [WireFrames](https://cacoo.com/diagrams/QXSJF7qPDCKNuzVk/B4F94?reload_rt=1718100120618_1&)
- [Base project for a social network site](https://realpython.com/django-social-network-1/)
