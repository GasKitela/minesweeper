
## What's build

* Design and implement  a documented RESTful API for the game (think of a mobile app for your API)
* When a cell with no adjacent mines is revealed, all adjacent squares will be revealed (and repeat)
* Ability to 'flag' a cell with a question mark or red flag
* Detect when game is over
* Ability to start a new game and preserve/resume the old ones
* Ability to select the game parameters: number of rows, columns, and mines

## What's in progress
* Implement an API client library for the API designed above. Ideally, in a different language, of your preference, to the one used for the API
* Persistence
* Time tracking
* Ability to support multiple users/accounts
 
## API available at:

http://minesweeper-api-gk.herokuapp.com/

## Usage

#### POST /ms/new-game (start new game with random generated game_id)

Request body:

{
    "rows": Int,
    "cols": Int,
    "mines": Int
}

- Mines amount must not exceed rows * cols

Response: 

{
    "id": String,
    "num_rows": Int,
    "num_cols": Int,
    "num_mines": Int,
    "field": Array[Field],
    "is_over": Boolean,
    "time": Int
}

Field:

{
    "row": Int,
    "col": Int,
    "value": Int,
    "flagged": Boolean,
    "question": Boolean,
    "is_mine": Boolean,
    "open": Boolean
}

- Field values go from -1 to 8, with -1 meaning it's a mine

#### GET /ms/<game_id> (retrieve game with game_id)

Response:

{
    "id": String,
    "num_rows": Int,
    "num_cols": Int,
    "num_mines": Int,
    "field": Array[Field],
    "is_over": Boolean,
    "time": Int
}

#### PUT /ms/<game_id>/click (interaction with specific square)

Request body:

{
    "row": Int,
    "col": Int,
    "action": String 
}

- Possible action values are 'CLICK', 'FLAG'. Calling with FLAG twice will mark the square as question. Calling it again turns it back to normal.

Response: 

{
    "id": String,
    "num_rows": Int,
    "num_cols": Int,
    "num_mines": Int,
    "field": Array[Field],
    "is_over": Boolean,
    "time": Int
}
 