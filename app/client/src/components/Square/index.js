import React, { Component } from "react";

class Square extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        if (this.props.data.open) {
            if (this.props.data.is_mine) {
                return (
                    <div
                        className="square open"
                        onContextMenu={e => {
                            e.preventDefault() }}
                        onClick={() => this.props.open(this.props.data)}
                    >
                        <span><i className="icon ion-android-radio-button-on"/></span>
                    </div>
                );
            }
            else {
                return (
                    <div
                        className="square open"
                        onContextMenu={e => {
                            e.preventDefault();
                        }}
                        onClick={() => this.props.open(this.props.data)}
                    >
                        {this.props.data.value > 0 ? this.props.data.value : ""}
                    </div>
                );
            }
        }
        else if (this.props.data.flagged) {
            return (
                <div
                    className="square open-flag"
                    onContextMenu={e => {
                        e.preventDefault();
                        this.props.flag(this.props.data);
                    }}
                    onClick={() => this.props.open(this.props.data)}
                >
                    <span><i className="icon ion-flag"/></span>
                </div>
            );
        }
        else if (this.props.data.question) {
            return (
                <div
                    className="square open-flag"
                    onContextMenu={e => {
                        e.preventDefault();
                        this.props.flag(this.props.data);
                    }}
                    onClick={() => this.props.open(this.props.data)}
                >
                    <span><i className="icon ion-help"/></span>
                </div>
            );
        }
        else {
            return (
                <div
                    className="square"
                    onContextMenu={e => {
                        e.preventDefault();
                        this.props.flag(this.props.data);
                    }}
                    onClick={() => {
                        this.props.open(this.props.data)}}
                />
            );
        }
    };

};

export default Square;