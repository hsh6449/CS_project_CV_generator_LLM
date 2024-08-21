# Document for Usage of Our Project

### 1. Make Environment
First, You must pull and make containers (web, llm, db). For db docker, you must pull from the official Docker Hub 
```
docker pull postgres
```
You can find the method for connecting each docker containers in the [issue #11](https://github.com/GIST-AI-Creative-Project-2024Spr/cs-project-2024-team-c/issues/11) 
If you follow all steps correctly, you can access the web homepage with your localhost:8080.

Alternatively, you can also use Docker Compose, if you prefer:
```
docker-compose up --build -d
docker-compose run manage.py runserver
```

### 2. URLs
- localhost:8080 : Main page
- http://localhost:8080/user_form/ : The form to gather user information
- http://localhost:8080/resume_download/ : A page where you can preview the resume, analyze job postings to receive keywords, or edit the resume via chatbot.

### 3. Usage Instructions
1. Fill out your information in detail on the user form and click the submit button.
2. An initial version of your resume will be displayed based on your input.
3. You can edit the resume or ask questions via the chatbot on the right.
4. Click the "Analyze Job Posting" button to open a popup window where you can enter a job posting text. After clicking analyze, four keywords will be displayed.
5. After completing the keyword analysis, you can use these keywords to update your CV. By asking the chatbot to "update the CV based on the keywords," you will see the menu update and the resume will be modified accordingly after a short while.




