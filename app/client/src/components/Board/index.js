import React, { Component } from "react";
import Row from "../Row";
import api from "../../utils/client/client";

class Board extends Component {
    constructor(props) {
        super(props);

        this.state = {
            rows: this.createBoard(props)
        };
    }

    componentDidUpdate(nextProps) {
        if (
            this.props.openSquares > nextProps.openSquares ||
            this.props.columns !== nextProps.columns
        ) {
            this.setState({
                rows: this.createBoard(nextProps)
            });
        }
    }

    populateSquare = (board, x, y, field) => {
        board[x].push({
            x: x,
            y: y,
            value: field[x][y].value,
            open: field[x][y].open,
            is_mine: field[x][y].value === -1,
            flagged: field[x][y].flagged,
            question: field[x][y].question
        });
    }

    createBoard = props => {
        // create 2d grid for our board based off the number of columns and rows passed in from props
        let board = [];
        for (let i = 0; i < props.rows; i++) {
            board.push([]);
            for (let j = 0; j < props.columns; j++) {
                this.populateSquare(board, i, j, props.field)
            };
        }
        return board;
    };

    updateBoard = data => {
        let board = [];
        for (let i = 0; i < this.props.rows; i++) {
            board.push([]);
            for (let j = 0; j < this.props.columns; j++) {
                this.populateSquare(board, i, j, data.field)
            };
        }
        return board;
    }

    shouldDecrementMineCount = square => {
        if (square.flagged && !square.question) return -1
        else if (!square.flagged && square.question) return 1
        else return 0
    }

    flag = square => {
        if (this.props.status === "ended") {
            return;
        }
        api.clickSquare("sarasa", square.x, square.y, 'FLAG').then(({data}) => {
            this.props.updateAfterClick(data)
            this.setState( { rows: this.updateBoard(data)})

            let updatedSquare = this.state.rows[square.x][square.y];
            this.props.changeFlagAmount(this.shouldDecrementMineCount(updatedSquare))
        })
    }

    open = square => {
        if (this.props.status === "ended") {
            return;
        }
        api.clickSquare("sarasa", square.x, square.y, 'CLICK').then(({data}) => {
            this.props.updateAfterClick(data)
            this.setState( { rows: this.updateBoard(data)})

            if (square.is_mine) {
                this.props.endGame()
            }
            this.props.onSquareClick()
        })
    }

    render() {
        let rows = this.state.rows.map((squares, index) => (
            //console.log(squares),
            <Row
                squares={squares}
                open={this.open}
                flag={this.flag}
                key={index}
            />
        ));


        return <div className="board">{rows}</div>;
    }
}

export default Board;