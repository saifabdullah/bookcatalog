# Introduction-
Item Catalog project of Udacity Full Stack Web Developer Nanodegree
-This is an online book catalog where users can add, edit and delete books across categories.
-To sucessfully run this web application, you need to install Python 3.1, flask 1.0 Sqlalchemy 1.2
- Project files includes book_database_setup.py, tonsofbooks.py, application.py and static and templates folder.
- In the templates folder, the templates are catalog.html, layout.html, layout2.html, login.html, newbook.html, deletebook.html, editbook.html etc.


#Installation notes-
-To run the application install latest version of  virtual box and vagrant.
-Run vagrant up using the vagrantfile provided in the requirements.txt.
-Start vagrant up and go to catalog folder.
- Google OAuth2.0 service setup for BookCatalog Application, provided in the Google_Oauth2.0_setupintro.txt file


#Operating Instructions:
-After running vagrant up, type "vagrant ssh" in Git Bash.
-Then in the console type "cd /vagrant/catalog"
- To set up the book catalog database run this command "Python book_database_setup.py" . Run this command only for initial setup.
- After the the database sucessfully created, run this command "python tonsofbooks.py" Run this command only for initial setup.
- After successfully setting up and populating the database
-Run this command "python application.py" 
-After the application started, open any browser and type localhost://5000
-The homepage of the web application will be displayed.
-You can log-in with your google id and start adding, editing and deleting  books in the bookcatalog.













