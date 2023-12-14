import React, { useContext } from "react";
import UserContext from "./User";
import Button from "./Button";

function Navbar() {
    const value = useContext(UserContext)
    const user_name = value && value[2] ? value[2]['user_name'] : ''
    const admin = value && value[2] ? value[2]['admin'] : ''
    return <>
        <h1>Welcome {user_name || ''}!</h1>
        {admin ? <Button target={'Users'} /> : null}
        {user_name ? <Button target={'Posts'} /> : null}
        {user_name ? null : <Button target={'Signup'} />}
        {user_name ? null : <Button target={'Login'} />}
        {user_name ? <Button target={'Submission'} /> : null}
        {user_name ? <Button target={'Profile'} /> : null}
        {user_name ? <Button target={'Logout'} /> : null}
    </>;
}

export default Navbar;