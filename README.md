## Simple blog web app using Flask

This blog supports full user authorization. Users can register, update profile and post blogs. Password reset is also supported. If you forget your password you will get an email with jwt encoded link.

Localization is implemented using Babel. It will detect your local machine's language and display the website based on your machine's language settings. Only supports Bulgarian and English for now.

Live translation of the posts different than native language is also possible thanks to MS Translator Api.

You can search for posts easily. It's implemented using Elasticsearch at the moment but can be easily changed to another engine.

At the moment it works with sqllite because it has only 3 table models. Another db can be easily implemented thanks to easily scalable structure of the project.

--------------------

### Here are some demo pictures from the project.

![Demo of software](/project-demo/Login-page.png)

![Demo of software](/project-demo/main-page.png)

![Demo of software](/project-demo/live-translate-demo.png)

![Demo of software](/project-demo/user-page.png)

![Demo of software](/project-demo/email-pass-reset.png)

--------------------

If you would like to run this project on your local machine:

1. Have python installed.
2. Create and activate a new virtual enviroment for the project.
3. Download all the project files.
4. Install all required modules defined in requirements.txt -- run: pip install -r requirements.txt in your shell
5. You need to create .env file and define Mail service provider like Sendgrid.net
6. You also need to provide a ms translator api for the translation to work. That is also defined in .env file
7. type: flask run in your shell to start the project
8. Open http://127.0.0.1:5000/ on your browser.

Have fun! 
If you need any assistance with running the project feel free to contact me and I will do my best to help.

---------------------

### LinkedIn: [Ersin Nurtin](https://www.linkedin.com/in/ersin-nurtin-6ab7528a/)

---------------------

This project is written with the help of [Miguel Grindberg's Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
