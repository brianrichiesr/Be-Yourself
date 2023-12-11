import React, { useContext } from "react";
import UserContext from "./User";

function Navbar() {
    const value = useContext(UserContext)
    const func = value[0]
    const obj = {user_name: "Demo"}
    return <>
        <h1 onClick={() => func(obj)}>{value[1]}</h1>
    </>;
}

export default Navbar;