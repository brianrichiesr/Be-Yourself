import React, { useContext } from "react";
import UserContext from "./User";

function Navbar() {
    const value = useContext(UserContext)
    const user_name = value && value[2] ? value[2]["user_name"] : ""
    const token = JSON.parse(localStorage.getItem('access_token'))
    return <>
        <h1>Welcome {token ? user_name : ""}!</h1>
    </>;
}

export default Navbar;