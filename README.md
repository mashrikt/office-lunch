# Office Lunch API

> Helps Offices Decide Their Lunch Menu!

Office Lunch has two types of users, regular and admin users. Admin users can add restaurants and daily menus. Users 
can then vote for their favorite menu of the day. Admin users can then generate the winning menu. 

## Features
- Each user can vote once per day.
- Once winner is generated, users cannot vote anymore.
- If one restaurant's menu has won on two working days in a row, they will not be chosen as a winner on the third day.

## Prerequisites
- [Docker](https://docs.docker.com/docker-for-mac/install/)

## Local Development
Start the dev server for local development:
```shell script
$ docker-compose up --build
```

Run the tests
```shell script
$ docker-compose exec web bash
# pytest -v -W ignore::DeprecationWarning
```

Create superuser
```shell script
$ docker-compose exec web bash
# python manage.py createsuperuser
```

## API Structure
- `api/auth`: authentication endpoints
- `api/users`: admin only endpoint for creating updating and deleting users
- `api/restauramts`: admin only endpoint for creating updating and deleting restaurants
- `api/menus`:  admins create menus and users can see list of menus
- `api/votes`: endpoint for users to list and create their votes
- `api/winners`: admin only endpoint to generate the winner for the day.
- `docs`: documentation
- `admin`: admin panel

## Improvements
- More test coverage (currently only test cases added for critical behavior)
- Handling timezone
- Pagination for list endpoints
- Logging
- Handling collision (ie. when 2 or more menus have the highest votes)
