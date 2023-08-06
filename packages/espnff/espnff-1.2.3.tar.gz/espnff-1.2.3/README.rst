ESPN Fantasy Football API
=========================

| Using ESPN�s Fantasy Football private API, this package interfaces
  with
| ESPN Fantasy Football to gather data from any public league. A good
  way to mine data
| without webscraping for data manipulation projects.

Getting Started
---------------

| These instructions will get you a copy of the project up and running
| on your local machine for development and testing purposes.

Installing
~~~~~~~~~~

With pip:

.. code:: python3

    pip3 install espnff

With Git:

.. code:: bash

    git clone https://github.com/rbarton65/espnff

    cd espnff

    python3 setup.py install

Basic Usage
-----------

This gives an overview of all the features of ``espnff``

Downloading a public league
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python3

    >>> from espnff import League
    >>> league_id = 123456
    >>> year = 2016
    >>> league = League(league_id, year)
    >>> league
    League 123456, 2016 Season

Viewing teams in a public league
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python3

    >>> from espnff import League
    >>> league_id = 123456
    >>> year = 2016
    >>> league = League(league_id, year)
    >>> league.teams
    [Team(Team 1), Team(Team 2), Team(Team 3), Team(Team 4),
    Team(Team 5), Team(Team 6), Team(Team 7), Team(Team 8)]
    >>> team1 = league.teams[0]
    >>> team1
    Team 1

Viewing data for specific team
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python3

    >>> league.teams
    [Team(Team 1), Team(Team 2), Team(Team 3), Team(Team 4),
    Team(Team 5), Team(Team 6), Team(Team 7), Team(Team 8)]
    >>> team1 = league.teams[0]
    >>> team1.team_id
    1
    >>> team1.team_name
    Team 1
    >>> team1.team_abbrev
    T1
    >>> team1.owner
    Roger Goodell
    >>> team1.division_id
    0
    >>> team1.division_name
    Division 1
    >>> team1.wins
    5
    >>> team1.losses
    1
    >>> team1.points_for
    734.69
    >>> team1.points_against
    561.15
    >>> team1.schedule
    [Team(Team 2), Team(Team 3), Team(Team 4), Team(Team 5), Team(Team 6), Team(Team 7), Team(Team 8),
    Team(Team 2), Team(Team 3), Team(Team 4), Team(Team 5), Team(Team 6), Team(Team 7), Team(Team 8)
    >>> team1.scores
    [135.5, 126.38, 129.53, 126.65, 114.81, 101.82, 1.15, 0, 0, 0, 0, 0, 0, 0]
    >>> team1.mov
    [32.12, 24.92, 45.97, 34.17, 41.74, -5.39, 1.15, 0, 0, 0, 0, 0, 0, 0]

Viewing power rankings
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python3

    >>> from espnff import League
    >>> league_id = 123456
    >>> year = 2016
    >>> league = League(league_id, year)
    >>> league.power_rankings(week=5)
    [('31.85', Team(Team 1)), ('25.60', Team(Team 3)), ('25.60', Team(Team 6)), ('22.45', Team(Team 2)),
    ('20.70', Team(Team 8)), ('18.20', Team(Team 7)), ('18.20', Team(Team 4)), ('18.10', Team(Team 5))]

Viewing scoreboard
~~~~~~~~~~~~~~~~~~

.. code:: python3

    >>> from espnff import League
    >>> league_id = 123456
    >>> year = 2016
    >>> league = League(league_id, year)
    >>> league.scoreboard() # grab current week
    ["Matchup(Team(Team 2), Team(Team 7))", "Matchup(Team(Team 1), Team(Team 11))",
    "Matchup(Team(Team 6), Team(Team 9))", "Matchup(Team(Team 12), Team(Team 4))",
    "Matchup(Team(Team 10), Team(Team 3))", "Matchup(Team(Team 8), Team(Team 5))"]
    >>> scoreboard = league.scoreboard(week=12) # define week
    >>> scoreboard
    ["Matchup(Team(Team 2), Team(Team 7))", "Matchup(Team(Team 1), Team(Team 11))",
    "Matchup(Team(Team 6), Team(Team 9))", "Matchup(Team(Team 12), Team(Team 4))",
    "Matchup(Team(Team 10), Team(Team 3))", "Matchup(Team(Team 8), Team(Team 5))"]
    >>> matchup = scoreboard[1]
    >>> matchup
    "Matchup(Team(Team 1), Team(Team 11))"
    >>> matchup.home_team
    "Team(Team 1)"
    >>> matchup.home_score
    7.05
    >>> matchup.away_team
    "Team(Team 11)"
    >>> matchup.away_score
    45.85

Running the tests
-----------------

| Automated tests for this package are included in the ``tests``
  directory. After installation,
| you can run these tests by changing the directory to the ``espnff``
  directory and running the following:

.. code:: python3

    python3 setup.py test

Versioning
----------

| This library uses `SemVer`_ for versioning. For available versions,
  see the
| `tags on this repository`_

.. _SemVer: http://semver.org/
.. _tags on this repository: https://github.com/rbarton65/espnff/tags

.. |Build Status| image:: https://travis-ci.org/rbarton65/espnff.svg?branch=master
   :target: https://travis-ci.org/rbarton65/espnff
.. |version| image:: https://img.shields.io/badge/version-1.1.0-blue.svg
   :target: https://github.com/rbarton65/espnff/blob/master/CHANGELOG.md
.. |PyPI version| image:: https://badge.fury.io/py/espnff.svg
   :target: https://badge.fury.io/py/espnff