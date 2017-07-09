# Satellite Tracking Service

Project of simple satellite tracker. External library PyOrbital provides longitude, latitude and altitude of 
chosen satellites. Program translates geographical positions onto pixel coordinates and marks actual position 
on the world map. Past positions are saved in the DB so it is possible to check  satellite position on 
any given time. Positions are updated every minute by means of Kronos. Satellites and past positions are shown 
with usage of jQuerry.


Default localhost sites:

- localhost:8000/satellites  → main project page. Shows satellites that were found by program.

- localhost:8000/satellites/{id}  → shows details about satellite with given {id} in DB.

- localhost:8000/map  → if is accessed by GET method shows only world map,
                        if is accessed by POST method shows satellites (and their positions past
                        positions) that were chosen in checkboxes in localhost:8000/satellites.

- localhost:8000/space_agencies  → shows list of space agencies in the DB. It is possible to add, 					
                                   remove and modify every agency.

- localhost:8000/space_agencies/{id}  → shows details about space agency with given {id} in DB

- localhost:8000/update_spaceagency/{id}  → shows form for space agency (with id = {id} in DB) inforamtion update

- localhost:8000/delete_spaceagency/{id}  → deletes space agency with given {id} in DB


- localhost:8000/astronauts  → shows list of astronauts in DB. It is possible to add, remove and 					   
                               modify every astronaut.
                               
- localhost:8000/astronauts/{id}  →shows details about astronaut with given {id} in DB.

- localhost:8000/update_astronauts/{id}  → shows form for astronaut (with id = {id} in DB) inforamtion update

- localhost:8000/delete_astronauts/{id}  → deletes astronaut with given {id} in DB
