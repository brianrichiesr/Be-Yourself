import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import UserContext from "./User";
import Button from "./Button";

function Navbar() {
    const value = useContext(UserContext);
    const navigate = useNavigate();
    const user_name = value && value[2] ? value[2]['user_name'] : '';
    const admin = value && value[2] ? value[2]['admin'] : '';
    const sendUser = () => {
        navigate('/')
    }
    return <>
        {/* <h1>Welcome {user_name || ''}!</h1> */}
        <div id="navBar" className="inverted">
            <div id="logo" onClick={sendUser}>Believe</div>
            <div id="navContainer">
            {admin ? <Button target={'Users'} /> : null}
            {user_name ? <Button target={'Posts'} /> : null}
            {user_name ? null : <Button target={'Signup'} />}
            {user_name ? null : <Button target={'Login'} />}
            {user_name ? <Button target={'Submission'} /> : null}
            {user_name ? <Button target={'Profile'} /> : null}
            {user_name ? <Button target={'Logout'} /> : null}
            </div>
        </div>
    </>;
}

export default Navbar;