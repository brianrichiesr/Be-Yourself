import React, { useContext } from "react";
import { Link } from "react-router-dom";
import UserContext from "./User";

function Button({ target }) {
    /* Grab 'UserContext' */
    const value = useContext(UserContext);
    /* Function that will log user out, reset user state, and clear localStorage */
    const logout = () => {
        if (target === "Logout") {
            const updateUser = value[0]
            updateUser({
                user_name: "",
                id: 0
            });
            localStorage.clear();
        }
    }
    /* Assign prop value to variable in lowercase to be used in 'Link' component */
    const linkTo = `${target.toLowerCase()}`;

    return (
        <Link
        className="navLink"
        onClick={() => logout()}
        to={target === "Logout" ? "/" :(target ? linkTo : "")}
        >
            {target}
        </Link>
    );
}

export default Button;