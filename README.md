# Car Selector

## Resource

**User**

Users:

* First Name (string)
* Last Name (string)
* Email (string)
* Password (string)

**Car**

Attributes:

* Year (integer)
* Make (string)
* Model (string)
* Type (string)
* Rating (integer)

## Schema

```sql
CREATE TABLE cars (
id INTEGER PRIMARY KEY,
year INTEGER,
make TEXT,
model TEXT,
type TEXT,
rating INTEGER);
```
## Schema

```sql
CREATE TABLE users (
id INTEGER PRIMARY KEY,
fname TEXt,
lname TEXT,
email TEXT,
password TEXT);
```
## REST Endpoints

Name                           | Method | Path
-------------------------------|--------|------------------
Retrieve car collection | GET    | /cars
Retrieve car member     | GET    | /cars/*\<id\>*
Create car member       | POST   | /cars
Update car member       | PUT    | /cars/*\<id\>*
Delete car member       | DELETE | /cars/*\<id\>*
Create user member      | POST   | /users
Login user member       | POST   | /sessions

## Password
Passwords encrypted using bcrypt.
