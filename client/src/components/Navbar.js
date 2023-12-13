import React, { useContext } from "react";
import UserContext from "./User";
import Button from "./Button";

function Navbar() {
    const value = useContext(UserContext)
    const user_name = value && value[2] ? value[2]['user_name'] : ''
    // const token = JSON.parse(localStorage.getItem('access_token'))
    return <>
        <h1>Welcome {user_name || ''}!</h1>
        <Button target={user_name ? 'Posts' : 'Login'} />
        <Button target={user_name ? '' : 'Signup'} />
        <Button target={user_name ? 'Submission' : ''} />
        <Button target={user_name ? 'Profile' : ''} />
        <Button target={user_name ? 'Logout' : ''} />
    </>;
}

export default Navbar;