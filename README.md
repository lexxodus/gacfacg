Generic Analytics Component for Adapative Computer Games
========================================================

This web application can store and track player progressions and thereby provides means to dynamically adjust game challenges for any kind of computer game.
Additionally it provides a simple graphical representation of these player progressions.

This tool includes an restful api to interact with computer games and its own visualization component.
It is built on python-flask and requires a PostgreSQL database for data storage.
The web interface is built with AngularJS.
A webserver is required to handle http requests and serve the analytics component.

For testing purposes two game dummies (word domination and bottle quiz quest) are included.
Each of them in a version without and with adpatation of game difficulties.

# Installation

Once the repository has been checked out a PostgreSQL database has to created. 
In `config.py` the used database connection is defined, and has to be adobted. 
Once the python dependencies defined in the `requirements.txt` have been installed,
the database is deployed using alembic:

- python manage.py db init
- python manage.py db migrate
- python manage.py db upgrade

Then the webserver has to be set up to serve the wsgi application.
Therefore correct paths have to be configured in `gacfacg.wsgi`.

It is recommended to run the application server in a virtual environment.


# Usage

## Managing Game Attributes

According to a game's specific properties one has to add levels, level types, tasks and events. 
This can be achieved by using the web interface or the restful api.
These attributes are used to distingish between the skill of different players.

### Level(api entity: level)

A game can have multiple levels. 

Attributes:
- Name: A name to identify a level.
- Description: An optional description.
- Level Type: The type of the level.
- Custom Attributes: Self defined attributes that can be accessed by the game.

### Level Type(api entity: level_type)

Similar levels should be tagged by one or more level types.

Attributes:
- Name: A name to identify a level type.
- Description: An optional description.
- Custom Attributes: Self defined attributes that can be accessed by the game.

### Task(api entity: task)

A common task a player has to perform in the game. These tasks should be very general (e.g. in a 3D shooter: "shooting", "surviving")

Attributes:
- Name: A name to identify a task.
- Description: An optional description.
- Custom Attributes: Self defined attributes that can be accessed by the game.

### Event(api entity: event)

A very precise formulation of a task. A player's progression is based on often he triggers certains events that are related to tasks.

Attributes:
- Task: The corresponding task.
- Name: A name to identify an event.
- Description: An optional description.
- Skill/ Score Points: Points awarded to a player when the event occurs. Events that represent a good performance should be awarded with positive skill points and otherwise with skill negative points. These are used to track a player's performance, while Score points are only used to store level high scores and should not be negative.
- Skill/ Score Interval: How often points should be awarded to a player (e.g. 1 = whenever a event occurs, 10 = every tenth time the event occurs).
- Skill/ Score Rule: Allows it to create mathematical terms that will be evaluated in order to award score/ skill points. Variables can be used based on all entities numerical attributes (e.g. event__score_points, level__difficulty).


## Integration into Game

The game interacts with the analytics component via its restful api:

`https://<hostname>/<path>/api/<entity>/<id>`

Thereby any entity can be accessed. In order to provide meaningful data the three entities have to be filled by the game.

### Level Instance(api entity: level_instance)

A concrete instance of a level in which one or more players play.

Required actions:
POST: create level instance(start_time defaults to current server time)
PUT: end level instance (end_time has to be provided) 

Attributes:
- lid: The corresponding level id.
- start_time: The time when the instance was created (ISO 8601 formated string: e.g. "2015-09-23T16:23:15").
- end_time: The time of destruction of the instance (ISO 8601 formated string).
- (custom_attributes): Self defined attributes that can be accessed by the game.

### Participation(api entity: participation)

An instance of a player that joined a level instance.

Required actions:
POST: create participation(start_time defaults to current server time).
PUT: end participation(end_time has to be provided).

Attributes:
- pid: The corresponding player id.
- lid: The corresponding level id.
- start_time: The time when the instance was created (ISO 8601 formated string: e.g. "2015-09-23T16:23:15").
- end_time: The time of destruction of the instance (ISO 8601 formated string).
- (custom_attributes): Self defined attributes that can be accessed by the game.

### Triggered Event(api entity: triggered_event)

A event that was triggered by a player.

Required actions:
POST: create triggered event(timestamp defaults to current server time)

Attributes:
- paid: corresponding participation id.
- eid: corresponding event id.
- timestamp: time when the event was triggered by the player (ISO 8601 formated string: e.g. "2015-09-23T16:23:15").
- given_skill_points (calculated by the application): awared skill points.
- given_score_points (calculated by the application): awared score points.
- (custom_attributes): Self defined attributes that can be accessed by the game (useful for event_rule evaluation).


## Performance calculation and adaptation

Whenever the performance of a player should be calculated a post request has to be sent to the corresponding skill entity.
By providing `interval` or `amount` parameters to get requests only the sum of events of the within a recent time interval.

### Level, Level Type, Task, Event Skill(api entries: level_skill, level_type_skill, task_skill, event_skill)

Required actions:
POST: calculate the corresponing skill.
GET: ?interval - return the skill of values calculated in the last <interval> seconds.
GET: ?amount   - return the skill last <amount> values calculated.

Attributes:
- pid: corresponding player id
- lid/liid/tid/eid: corresponding level/level_instance/task/event id.
- timestamp: time when skill was calculated.
- considered_rows: the amount of rows that were used to calculate the skill (useful to determine how representative the skill value is).
- score points: the high score of a player for a level (only applies for level_skill)
- skill points: the total amount of achieved skill points.
