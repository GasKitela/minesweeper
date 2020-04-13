import React, { Component } from "react";
import { Button, FormGroup, FormControl } from "react-bootstrap";
import "./gameconf.css";
import api from "../../utils/client/client";

class Gameconf extends Component {
    constructor(props) {
        super(props);

        this.state = {
            showGameconf: true,
            rows: 0,
            cols: 0,
            mines: 0
        };
    }

    validations = () => {
        return (this.state.rows > 0 &&
            this.state.cols > 0 &&
            this.state.mines > 0 &&
            this.state.mines < this.state.rows * this.state.cols)
    }

    handleSubmit(event) {
        event.preventDefault();
    }

    handleRowsChange = value => {
        this.setState({
            rows: value
        })
    }

    handleColsChange = value => {
        this.setState({
            cols: value
        })
    }

    handleMinesChange = value => {
        this.setState({
            mines: value
        })
    }

    handleOnClick = () => {
        if (this.validations)
            this.props.onClickCreateNewGame(this.state.rows, this.state.cols, this.state.mines)
    }

    render() {
        return (
            <div className="Gameconf">
                <form onSubmit={this.handleSubmit}>
                    <label htmlFor="rows">Rows</label><br/>
                    <input type="text" id="rows" name="rows" onChange={(event) => this.handleRowsChange(event.target.value)}/><br/>
                    <label htmlFor="cols">Columns:</label><br/>
                    <input type="text" id="cols" name="cols" onChange={(event) => this.handleColsChange(event.target.value)}/><br/>
                    <label htmlFor="mines">Mines:</label><br/>
                    <input type="text" id="mines" name="mines" onChange={(event) => this.handleMinesChange(event.target.value)}/><br/>
                    <input type="submit" value="Create game" onClick={this.handleOnClick}/>
                </form>
            </div>
        )};
}

export default Gameconf;