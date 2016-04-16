# tournament_database

**Introduction**

Carolyn’s Tournament Database uses a PostgresQL database and
Python to create a set of queries that produce a swiss-style
tournament bracket.

**Features**

* Supports any even-numbered group of players per tournament
* Automatically calculates player rankings based on wins 
and creates pairings for future matches
* Creates match ID numbers to track who has played whom 
in past match-ups

**Libraries & Sub-Modules**

* [PostgresQL](https://wiki.postgresql.org/wiki/Detailed_installation_guides)
* [Python](https://docs.python.org/2/howto/webservers.html)
* tournament.sql
* tournament.py

**License**

* This code is available for redistribution and use without restriction

**Installation**

* After making sure Python and PostgresQL are installed (see links above), upload the following to your web server:
  * tournament.sql
  * tournament.py
* Create a new database entitled 'tournament'
* To instantiate necessary tables and views, run tournament.sql
* To edit or add Python functionality, edit tournament.py

**Authors**

* Udacity team -- [see GitHub page](https://github.com/udacity)
* Additions by [Carolyn Gibney](https://github.com/cemgibney)

**Bugs & Feature Requests**

* Please submit to the Udacity team via their [GitHub page](https://github.com/udacity)
