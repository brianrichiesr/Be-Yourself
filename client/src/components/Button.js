import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import UserContext from "./User";

function Button({ target }) {
    const navigate = useNavigate()
    const labels = {
        "Login": "login",
        "Posts": "posts",
        "Profile": "profile",
        "Signup": "signup",
        "Submission": "submission",
        "Users": "users"
    }
    const value = useContext(UserContext)
    const sendUser = () => {
        if (target === "Logout") {
            const updateUser = value[0]
            updateUser({
                user_name: "",
                id: 0
            })
            localStorage.clear()
        }
    }

    return (
        <Link
        className="navLink"
        onClick={() => sendUser()}
        to={target === "Logout" ? "/" :(target ? labels[target] : "")}
        >
            {target}
        </Link>
    );
}

export default Button;