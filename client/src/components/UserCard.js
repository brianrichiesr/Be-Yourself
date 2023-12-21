import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import UserContext from "./User";
import { v4 as uuid } from 'uuid';

function UserCard({ user }) {
    const navigate = useNavigate();
    const value = useContext(UserContext);
    const admin_user = value[2]
    const displayUser = () => {
        navigate(`/users/${user.id}`)
    }
    /* Do not return the user's own info */
    if (user.id === admin_user.id) return null
    return <div className="user-card" onClick={displayUser}>
        <h2>Id: {user.id}</h2>
        <h3>Name: {user.user_name}</h3>
        <h3>Email: {user.email}</h3>      
        <h3>Admin: {JSON.stringify(user.admin)}</h3>     
    </div>;
}

export default UserCard;