# Continuous Integration and Continuous Deployment (CI/CD) for Workplace App
### Link to Project on GitHub
https://github.com/jackcorless91/workplace_app.git
## Project overview
This workplace_app is a RESTful backend built using Flask. It serves as a business management system to look after: employees, departments, client feedback, rosters, performance reviews and projects. The application connects to a PostgreSQL database using SQLAlchemy ORM and containerised using Docker. These updates to the original project introduces automated testing, containerisation, and deployment to Google Cloud Platform (GCP) using GitHub Actions.

## Purpose of CI/CD Implementation
The goal of this ci/cd pipeline is to automate the repetitive mundane process tasks like running tests and deploying updates. Automating these ensured faster release cycles, higher code quality, and reduced cause of human error. It allows developers to focus on building and implementing new features instead of wasting time on setup, configuration and manual deployment.
This setup is well integrated with GitHub and GitHub Actions. It runs a test suite on every push to the main branch and automatically deploys the application to a serverless environment on Google Cloud Run if all tests successfully pass.


## Tools and Technologies Used
### Github Actions
GitHub Actions is both used for integrations and deployment stages. It was chosen for its native support on GitHub, ease of setup and strong ecosystem of reusable actions. Two seperate workflow files are used: ci.yml for testing and deploy.yml for deployment.

### Google Cloud Run (GCR)
GCR was chosen as the hosting platform for its fully managed serverless environment. It simplifies the deployment process and autoscales containerised applications without requiring the managment of virtual machines or kubernetes clusters.

### Google Artifact Registry
Google Artifact Registry stores built docker images that are later deployed to Cloud Run. It provides secure image storage and native integration to GCP.

### Docker
Docker is used to containerise the application. This ensures consistent and reliable environments throughout local testing, development and production. The Dockerfile defines how the application is packaged and exposed on port 8080.

### Pytest
Pytest takes care of all test cases. It's a strong Python testing framework that supports fixtures, assert writing and test discovery.

### PostgreSQL
The database is PostgreSQL. It works hand in hand with Flask and SQLAlchemy and was chosen for its reliability and focus on relational database models.

### dotenv
dotenv is used to manage enviornment variables locally during the development stage. All credentials and configurations are never hardcoded.

## Workflow Explained
1. ci.yml - Continuous Integration
+ Triggered by any push or pull request on main branch.
+ Sets up a Python environment and installs dependencies listed in requirements.txt.
+ Executes all automated tests located in the tests/ directory.
+ If any test fails, the CI job fails and stops the process from moving forward.

2. deploy.yml - Continuous Deployment
+ Triggered when code is pushed to main and tests pass.
+ Authenticates to Google Cloud using a service account stored in GitHub Secrets as a base64-encoded JSON key.
+ Builds a Docker image of the application and pushes it to Artifact Registry.
+ Deploys the image to a pre-defined Cloud Run service.
+ Sets environment variables securely and configures database connectivity.

## Secrets Management and Configuration
All sensitive data included such as API keys and deployment configurations are managed via GitHub Secrets. This ensures credentials aer never exposed in code or logs. The secrets keys utilised were:
+ GCP_PROJECT_ID – The GCP project identifier.
+ GCP_REGION – The target region for deployment.
+ SERVICE – The name of the Cloud Run service.
+ GCP_SA_KEY – A base64-encoded JSON key for the service account with deployment permissions.
+ DATABASE_URI – PostgreSQL connection string used in the deployed environment.
+ SECRET_KEY – Flask’s internal secret key for session management and security.
All secrets are injected during the GitHub Actions workflow and are passed into the Docker container using the environment variables.

## Testing Process
The test suite used includes the use of both GET and Post endpoints to ensure the API's core functionality remained in working order. The test_app.py file uses Flask's test client and Pytest fixtures to simulate and validate HTTP requests without the need to run a live server.
### Examples
+ Verifying that each endpoint returns a 200 OK status and the expected data structure.
+ Testing that new records can be successfully created (e.g., POST /team_members/).
+ Confirming that endpoints like /projects/, /departments/, and /client_feedbacks/ are operational.
Before each and every deployment, the CI ensures all tests pass. This gives developers the confidence their push to main didn't cause a codebase Chernobyl.

## Deployment Process Overview
1. Developer pushes code to the main branch on GitHub.
2. GitHub Actions triggers the ci.yml workflow:
+ Python environment is set up.
+ Dependencies are installed.
+ Tests are executed using Pytest.
3. If tests pass, the deploy.yml workflow begins:
+ Authenticates to Google Cloud using a service account.
+ Docker image is built using the app’s Dockerfile.
+ The image is uploaded to Google Artifact Registry.
+ Cloud Run deploys the container and serves traffic via a public URL.
A successful deployment means the application is now live on the web, with HTTPS and automatic scaling.

### Architecture and Workflow Diagram
 *included as PDF*

## Why These Tools Were Chosen Over Alternatives
Many other tools were considered:
+ AWS EC2 was avoided due to ts higher configuration complexity and managment overhead.
+ Heroku wasn't used due to its limitations on containerisation and scaling for our use case.
+ GitLab CI/CD would require full GitLab migration, while GitHub actions works natively.
+ CircleCI offers a strong CI/CD but GitHub Actions was an easy to use interface that I was already familair with.
Finally Google Cloud Run was chosen for it ease of deployment, scalibility, price and seamless integration with Docker. GitHub Actions was an easy choice for workflow automation due to the project being hosted on GitHub.

## Publicly accessible URI
https://jacks-workplace-db.onrender.com