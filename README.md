# Usage

Please Note this application/project uses python 3.9

- to run the application as below and open your browser http://localhost:9001/api/docs
  ```bash
  $ docker-compose up
  ```

- to run test and linting
  ```bash
  $ make install
  $ make lint
  $ make test
  ```

# Challenge

A Company needs internal service for its employees which
helps them to make a decision on lunch place.

Each restaurant will be uploading menus using the system every day over API
Employees will vote for the menu before leaving for lunch on mobile app for whose backend has to be implemented.

There are users which did not update the app to the latest version and backend has to support both versions.

Mobile app always sends build version in the headers.

Needed APIs:

- [x] Authentication
- [x] Create Restaurant
- [x] Uploading menu for restaurant (There should be a menu for each day)
- [x] Creating employee
- [x] Getting current day menu
- [x] Voting for restaurant menu (Old version api accepted one menu, New one accepts top three menus) with respective points (1 to 3)
- [x] Getting results for current day

Requirements:

- [x] Solution should be built using Python and preferably Django Rest Framework, but any other framework works.
- [x] App should be containerized
- [x] Project and API Documentation
- [x] Tests

## Assumptions

- employee can't upload menu
- one 1 vote per employee
- votes are for limited time during lunch-time (12pm to 2pm) to make sure only employee's that tasted the food during lunch can vote
- Results can only finalized after voting period
- restaurant can't vote
- authentication will use JWT
- old build of mobile client will be aware of v1 endpoint and new version would be aware of v2 endpoint 
  thus making new version of mobile to connect to v2
- for old vote endpoint it is assumed that the score is always max since it is single vote

## Stack
- FastAPI - Since the project is purely API, I prefer using FastAPI for its focus on API and not having bloat codes which are not needed
- Postgresql - the most common and preferred database used with python
- traefik - loadbalancer 

## Extra
- Argon2 - to hash the passwords safely argon2 is chosen instead of bcrypt refer to for more details
