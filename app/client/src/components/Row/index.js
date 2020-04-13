import React from "react";
import Square from "../Square";

const Row = props => {
    let squares = props.squares.map((data, index) => (
        <Square data={data} open={props.open} flag={props.flag} key={index} />
    ));
    return <div className="row">{squares}</div>;
};

export default Row;