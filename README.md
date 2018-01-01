# Satellite Tracking Service

Project of simple satellite tracker. External library PyOrbital provides longitude, latitude and altitude of 
chosen satellites. Program translates geographical positions into pixel coordinates and marks actual position 
on the world map. Past positions are saved in the DB so it is possible to check  satellite position on 
any given time (when the server was running). Positions are updated every minute by means of Kronos. Satellites and past positions are shown with usage of jQuerry and JavaScript. AJAX is used to communicate with REST API server. Best to run on Chrome.

Default localhost sites:

- localhost:8000/satellites  → main project page. Shows satellites that were found by program

- localhost:8000/satellites/{id}  → shows details about satellite with given {id} in DB


- localhost:8000/satellites_list/?sat_name1=sat_name1&sat_name2=sat_name2... (GET) → requests (by GET) present positions of satellites with names in GET parameters, used to draw present satellites positions in the map

- localhost:8000/history/?the_date=isodate&sat_name1=sat_name1&sat_name2=sat_name2... (GET) → requests (by GET) past positions of satellites with names in GET parameters and date (for past positions) in iso date format, used to draw past satellites trajectories in the map


- localhost:8000/map  → if is accessed by GET method for the first time, shows only world map,
                        after filling the form in localhost:8000/satellites, shows present end past positions of choosen satellites in the chosen day

- localhost:8000/space_agencies  → shows list of space agencies in the DB. It is possible to add, 					
                                   remove and modify every agency

- localhost:8000/space_agencies/{id}  → shows details about space agency with given {id} in DB

- localhost:8000/update_spaceagency/{id}  → shows form for space agency (with id = {id} in DB) inforamtion update

- localhost:8000/delete_spaceagency/{id}  → deletes space agency with given {id} in DB


- localhost:8000/personnel  → shows list of personnel in DB. It is possible to add, remove and modify every personnel
                               
- localhost:8000/personnel/{id}  → shows details about personnel with given {id} in DB

- localhost:8000/update_personnel/{id}  → shows form for personnel (with id = {id} in DB) inforamtion update

- localhost:8000/delete_personnel/{id}  → deletes personnel with given {id} in DB

- localhost:8000/add_personnel → shows form for adding new personnel

