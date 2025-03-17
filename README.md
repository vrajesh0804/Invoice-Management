Welcome to the Invoice-Management wiki! 
Install Django using the below command
python -m pip install Django

You need Wamp/Lamp/Xampp to connect with the database.

Then, go to setting.py and change the DB configuration. DATABASES = {
	'default': {
	'ENGINE': 'django.db.backends.mysql',
	'NAME': 'database_name',
	'USER':'database_username',
	'PASSWORD':'database_password',
	'HOST':'localhost',
	'PORT':'3306'
}
}

For Mail configuation change below code as per your requirement 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
EMAIL_HOST='smtp.gmail.com' 
EMAIL_PORT=587 
EMAIL_HOST_USER = 'your email id' 
EMAIL_HOST_PASSWORD = 'password' 
EMAIL_USE_TLS = True

After these extra lines of code have been added to your project, you can send emails now. But if you are using Gmail, then the first time you make these changes in your project and run, you might get an SMTP error.

To correct that- 1-Go to the Google account registered with the sender’s mail address and select Manage your account 2-Go to the security section at the left nav and scroll down. In Less secure app access, turn on the access. By default, it would be turned off. Finally, run the application.
