# FBTetris

At the time of publication, this is my most serious project. Based on a not very complex game (Tetris), I tried to write a whole game, adding a few things that were new to me.
## Things that I have implemented:
* [The game itself](#Game)
* [Window system implemented with OOP](#Windows)
* [Account system with data storage on the server](#Account)
* Also I compiled it first in .exe and then in setup.exe (You can download FBSetup.exe [here](https://drive.google.com/file/d/1W37PBUKz2k8AWsnhq_YuxuHU8iFts4Fc/view?usp=sharing))

---

## <a name="Game"></a> Game (game.py file)

The whole game is collected in a separate file.
You can see 3 classes:
###  Field

Following the field. Stores score, time, field, next figure and current one.
##### Methods:
* `spawn(self)` Spawns a new figure.
* `fig_rotate(self, direction: int)` and `figure_update(self, add: bool)` Used to control the rotation of figures.
* `check(self)` Checks for collision.
* `move(self, direction='d')` Moves the active figure. There are 3 directions: d - down, r - right, l - left.
* `game_end(self)` Checks the field for a losing state.
* `line_search(self)` Searches for complete lines, returns their numbers.
* `line_delete(self, number)` Deletes a line with a specific number.
* `line_check(self)` Is a union of the previous two functions, also calculates points for lines according to their count 1 line - 100, 2 lines - 300, 3 lines - 700, 4 lines - 1500.

###  Figure

Stores information about a figure. The figures are numbered from 1 to 7.
##### Methods:
* `rot(self, direction: int)` rotates the figure, takes the direction of rotation: -1 - clockwise, 1 - counterclockwise.

### Stopwatch

My class - stopwatch. Starts the stopwatch when the object is created.
##### Methods:
* `pause(self)` Pauses the stopwatch.
* `play(self)` Unpauses the stopwatch.
* `time(self)` Returns the time on the stopwatch.

---

## <a name="Windows"></a> Windows (main.py and next_figures.py files)

Working with windows is divided into 2 files. main.py is a file with main classes, next_figured.py is an auxiliary file, let's look at it first.
### _next_figures.py_
Figures are drawn in this file to display the next figure. This takes up quite a lot of lines of code, but it only needs to be done once when starting the application.
### _main.py_
In this file, I describe all the windows, as well as their work. Each window has its own class. __The following is a description of the classes.__
### ControlClass
This class is different from the others. This is the controlling class. It handles all pygame events, dispatches some events to the active window, causes the display to be drawn.
##### Methods:
* `turn_on(self, window)` Turns on the window passed in the argument, turns off the rest.
* `turn_on_if(self, window, if_window)` Turns on window if if_window is on, otherwise turns on if_window.
* `control_events(self)` Iterates over all events, if the event is for an enabled window, then passes the event to the active window object. Working with pygame events is quite confusing, but the main purpose of this function is to switch windows. Look for the description of event handling of any window in the corresponding function from the class of this window.
* `update(self)` assembles and merges the main surface.
### GameWindow
This class works with the game and handles events related to it.
##### Methods:
* `new_game(self)` Returns the object to its factory settings.
* `event_work(self, event)` Works with pygame events. Returns True if a loss has been determined. Otherwise False. Handles 3 important kinds of events: userevent, keydown and keyup.
> `USEREVENT` is used to move the figures down and control game speed.

> `KEYDOWN` is used to detect WASD button pressed.

> `KEYUP` is used to determine the end of holding the ASD buttons.
* `upd_surface(self)` Responds to pressing AD keys, draws the field and bar
### EndWindow
The only class that is used to work with 2 different windows at once: these are the windows for starting the application and losing the game. These windows do not work with events, not taking into account switching windows (ControlClass works with them), so there is no event_work(self, event) function in EndWindow.
##### Methods:
* `upd_surface(self, score, lines, figures, game_time)` Draw windows for starting the application and for playing the game.
### PauseWindow
This is the pause window. It is static, so this class does not have any methods.
### HighscoresWindow
This window is responsible for the leaderboard. It has no event handling similar to EndWindow.
##### Methods:
* `upd_surface(self, hs_dict)` It takes the prepared leaderboard and writes in it the names and data of the top three players.
### LogWindow
This is the login window.
##### Methods:
* `event_work(self, event)` Works with pygame events. This method works with 5 events:
> `MOUSEBUTTONDOWN` monitors mouse clicks on the Log in button and on the places to enter the login and password.

> `KEYDOWN` monitors keystrokes so that you can type your username and password.

> `KEYUP` keeps track of BACKSPACE being held down so that you can erase text by holding down a key.

> `USEREVENT + 1` is only needed to blink the cursor.

> `USEREVENT + 2` is needed to control the erasing speed by holding the BACKSPACE button. Also thanks to this, the cursor does not blink during erasing (Also it does not blink during printing).
* `upd_surface(self)` renders the surface.
### SignWindow
Logging in is very similar to logging into an account, so I inherit this class from LogWindow.
The main difference is the _show password_ button.

---

## <a name="Account"></a> Account work (account.py file)
In this file, I described the class that works with the account and with the server. __The following is a description of the class.__
### User
It is worth explaining how the account system works in my project.

All information is stored in one json file at [JsonBin](https://jsonbin.io)

___Example:___

>{
>
>  "Leaders": [
>>
>>    "qwert",
>>
>>    "forber",
>>
>>    "hgfdhgsdgds"
>>
>>  ],
>  
>  "forber": {
>>  
>>    "pw": "9a900403ac313ba27a1bc81f0932652b8020dac92c234d98fa0b06bf0040ecfd",
>>    
>>    "score": 6500,
>>    
>>    "lines": 24,
>>    
>>    "figures": 82,
>>    
>>    "s_hash": "29b1bb0b63d187d27ff730632887493d9d336141378469a746a7309316821cd2"
>>    
>>  },
>  
>  "qwert": {
>>  
>>    "pw": "9a900403ac313ba27a1bc81f0932652b8020dac92c234d98fa0b06bf0040ecfd",
>>    
>>    "score": 7500,
>>    
>>    "lines": 20,
>>    
>>    "figures": 80,
>>    
>>    "s_hash": "1546dbd5f8c911c403a9add64380f5bd10ba5a966e98038010ff927cc2b7eae6"
>>    
>>  },
>  
>  "hgfdhgsdgds": {
>>  
>>    "pw": "887463f6dfbbd5fd2a8aa3487a72e124e940003c4ece7294f572607f9c8e7c6e",
>>    
>>    "score": 100,
>>    
>>    "lines": 1,
>>    
>>    "figures": 11,
>>    
>>    "s_hash": "5ddbc24c8edb25c27b686bd51c1487c1b1ae41aefe127492b760e3c1d57ea009"
>>    
>>  }
>>  
>}

The root dictionary has a list with the key `"Leaders"`, which obviously stores the names of the 3 leaders and dictionaries for each user, where the key is the username.
There are 5 elements in the user's dictionary: the password hash, the score, the number of figures, the number of lines (the last three display statistics for the user's best attempt), and a special hash under the key `"s_hash"`.

All elements are intuitive, I will explain only `"s_hash"`.

This hash is obtained from the username and his game statistics, it does not repeat for different users, so you won't be able to copy information from another user. When the application starts, a full check of the special hashes takes place. If the saved hash does not match the newly obtained hash from the statistics and name, the program understands that changes have been made to the database and the script will reset the person's game statistics. This system is not ideal and not always fair, and now I see more correct ways of implementation, but at the time of writing the code it was a new idea for me, which I immediately implemented.

Let's go back to `User`.
##### Methods:
* `special_hash(self)` creates a special hash using user data.
* `check_leaders(self)` iterates over the entire database to check the leaders, very rarely used, really only needed if someone changes the leaderboard externally.
* `check_data(self)` checks the database against special hashes.
* `load(self)` loads information from the server and at the same time checks for the presence of the Internet.
* `unload(self)` uploads information to the server.
* `log_in(self, name, password)` checks the password and logs in.
* `sign_up(self, name, password)` checks if the name is taken and registers the user.
* `upd(self, score, lines, figures)` updates the user information in the database. It also monitors entry into the leaderboard.
