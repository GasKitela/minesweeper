import React, { Component } from "react";
import BoardHeader from "./components/BoardHeader";
import Board from "./components/Board";
import Gameconf from "./components/Gameconf";
import { Route, BrowserRouter as Router } from 'react-router-dom'
import api from "./utils/client/client.js"

class App extends Component {
    constructor() {
        super();

        this.state = {
            gameStatus: "waiting", // can be running, waiting, or ended //AGREGAR OTRO STATUS, ALGO TIPO TO_START, PARA PANTALLA LOGIN
            time: 0, // in seconds, will format later
            flagCount: 0,
            openSquares: 0,
            mines: 0,
            rows: 0,
            columns: 0,
            field: [],
            shownComponent: 'gameconf'
        };

        this.baseState = this.state;
    }

    createNewGame = (rows, cols, mines) => {
        api.createGame("sarasa", rows, cols, mines).then(({ data }) => this.setStartGameState(data))
    }

    componentDidMount() {
        //this.createNewGame()
    }

    componentToShow = comp => {
        this.setState({
            shownComponent: comp
        })
    }

    componentDidUpdate(nextProps, nextState) {
        if (this.state.gameStatus === "running") {
            api.holaMundo().then( ({ data }) => console.log(data));
            this.checkForWinner();
        }
    }

    setStartGameState = (data) => {
        console.log(data.field)
        this.setState( {
            mines: data.numMines,
            rows: data.numRows,
            columns: data.numCols,
            flagCount: data.numMines,
            field: data.field,
            shownComponent: 'board'
        })
    }

    updateAfterClick = data => {
        this.setState( {
            field: data.field,
        })
    }

    checkForWinner = () => {
        if (this.state.mines + this.state.openSquares >= this.state.rows * this.state.columns) {
            this.setState({
                gameStatus: "ended"
            }, alert("you won!"))
        }
    }

    componentWillMount() {
        this.intervals = [];
    }

    setInterval = (fn, t) => {
        this.intervals.push(setInterval(fn, t));
    };

    reset = () => {
        this.intervals.map(clearInterval);
        this.setState(Object.assign({}, this.baseState), () => {
            debugger;
            this.createNewGame();
            this.intervals = [];
        });
    };

    tick = () => {
        if (this.state.openSquares > 0 && this.state.gameStatus === "running") {
            let time = this.state.time + 1;
            this.setState({ time });
        }
    };

    endGame = () => {
        this.setState({
            gameStatus: "ended"
        }, alert("you lose!"));
    };

    changeFlagAmount = amount => {
        this.setState({ flagCount: this.state.flagCount + amount });
    };

    countOpenSquares = () => {
        let openSquares = 0
        for (let i = 0; i < this.state.rows; i++) {
            for (let j = 0; j < this.state.columns; j++) {
                if (this.state.field[i][j].open)
                    openSquares++
            };
        }
        return openSquares
    }

    handleSquareClick = () => {
        if (this.state.openSquares === 0 && this.state.gameStatus !== "running") {
            this.setState(
                {
                    gameStatus: "running"
                },
                this.setInterval(this.tick, 1000)
            );
        }
        this.setState(prevState => {
            return { openSquares: this.countOpenSquares() };
        });
    };

    render() {
        return (
            <div className="minesweeper">
                {(() => {
                    switch (this.state.shownComponent) {
                        case 'gameconf':
                            return <Gameconf
                                    onClickCreateNewGame={this.createNewGame}
                                />
                        case 'board':
                            return <div>
                                    <h1>Welcome to minesweeper.</h1>
                                    <BoardHeader
                                        time={this.state.time}
                                        flagsUsed={this.state.flagCount}
                                        reset={this.reset}
                                        status={this.state.gameStatus}
                                        show={this.state.shownComponent}
                                    />
                                    <Board
                                        show={this.state.shownComponent}
                                        openSquares={this.state.openSquares}
                                        mines={this.state.mines}
                                        rows={this.state.rows}
                                        columns={this.state.columns}
                                        field={this.state.field}
                                        endGame={this.endGame}
                                        status={this.state.gameStatus}
                                        onSquareClick={this.handleSquareClick}
                                        changeFlagAmount={this.changeFlagAmount}
                                        updateAfterClick={this.updateAfterClick}
                                    />
                            </div>
                    }
                })()}
            </div>
        );
    }
}

export default App;