# C&S Project 2024 - Team C (CV Auto Revising Service)

## Team Member
| **Sanha Hwang** | **Gunwoo Bae** |
| :------: |  :------: |
| [<img src="https://avatars.githubusercontent.com/u/57973170?v=4" height=150 width=150>](https://github.com/hsh6449) | [<img src="https://avatars.githubusercontent.com/u/83867930?v=4" height=150 width=150>](https://github.com/gunwoof) |

## Project Overview
### 이력서를 회사가 원하는 인재상에 맞는 강력한 이력로 다시 만들기!
* ## Project concept
![image](https://github.com/GIST-AI-Creative-Project-2024Spr/cs-project-2024-team-c/assets/83867930/f913690c-3483-4194-881e-93fff4b0f2e7)
![image](https://github.com/GIST-AI-Creative-Project-2024Spr/cs-project-2024-team-c/assets/83867930/a98f9aff-8c44-420b-82ed-481308dea0ee)
* ## Project output
![image](https://github.com/GIST-AI-Creative-Project-2024Spr/cs-project-2024-team-c/assets/83867930/f6d29cd1-f4fe-47ff-8160-bc9504a5f2b1)

## Library
![image](https://github.com/GIST-AI-Creative-Project-2024Spr/cs-project-2024-team-c/assets/83867930/1e346384-df37-4afe-84cb-94c3fbd80eec)

## Environment
![image](https://github.com/GIST-AI-Creative-Project-2024Spr/cs-project-2024-team-c/assets/83867930/7641fa86-88aa-4d55-91cc-8890e4002a7d)
<img width="1142" alt="image" src="https://github.com/GIST-AI-Creative-Project-2024Spr/cs-project-2024-team-c/assets/57973170/fc6793cf-6aff-4324-8851-2b49b3ae03f0">

## Directory Structure

```
/cs-project-2024-team-c
    /docs/
    /Dockerfile  # or, /Containerfile
    /README.md
    /Usage.md
    /project
        │
        ├── model
        │   ├── llm_server.py
        │   ├── Dockerfile # Dockerfile for the llm
        │   └── requirements.txt # Python requirements for the llm
        │   └── start.sh
        │
        ├── backend
        │   ├── myapp
        │   │   ├── templates
        │   │   │   └── custom_tags.py
        │   │   ├── templates
        │   │   │   ├── user_id # user_id에 따라 생성되는 폴더
        │   │   │   ├── home.html
        │   │   │   ├── resume1.html # resume 미리보기 페이지에 사용되는 inner template
        │   │   │   ├── resume_update.html 
        │   │   │   ├── resume_download.html # resume 미리보기 페이지
        │   │   │   ├── resume_content.html  # resume의 메인 내용이 나오는 페이지 
        │   │   │   └── user_form.html
        │   │   ├── static
        │   │   │   ├── css
        │   │   │   │   └── styles.css
        │   │   │   └── js
        │   │   │       ├── resume_download.js
        │   │   │       └── scripts.js
        │   │   ├── views.py
        │   │   ├── urls.py
        │   │   └── ...
        │   ├── myproject
        │   │   ├── settings.py
        │   │   ├── urls.py
        │   │   └── ...
        │   └── manage.py
        │
        ├── .env
        ├── requirements.txt
        ├── credentials.json
        ├── docker-compose.yml
        └── Dockerfile
```

## Guidelines

Team members are responsible for taking on tasks appropriate to their roles and submitting them periodically to the appropriate repositories. At this time, please be aware of the following precautions.

* Prohibition of account sharing: The act of pushing someone else's work to your ID is prohibited. **You can only upload your own results with your GitHub account.**
* Periodic upload recommended: Even if the results such as code are incomplete, **please continue to push the progress so that other team members and evaluators can observe and give feedback.** The act of pushing completed results at once is recognized only as a contribution for that date, and efforts in the process are difficult to be recognized.
* Documentation recommended: Documentation in the `docs` directory provided by default will be credited to the author. In addition, even if presentation materials such as PPT are uploaded in binary format, if the contents are listed in the `docs` directory, contributions can be recognized by quoting them.
* Create a `Dockerfile (Containerfile)`: Project artifacts should be able to be packaged into one (or more) container image with the following command: `docker build --tag cs-project-2024-team-xxx .`
    - Build arguments and environment variable dependencies should not be present.
    - **Execution: Execution and usage for containerized images must be documented in `Usage.md` file.**

## Q&A

Please use the `Issues` function to raise inquiries.
