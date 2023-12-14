import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import PostContext from "./Post";
import { v4 as uuid } from 'uuid';

function PostCard() {
    const navigate = useNavigate();
    const value = useContext(PostContext);
    const description = value.description.length > 100 ? (value.description.slice(0, 97) + "...") : value.description;
    const displayPost = () => {
        navigate(`/posts/${value.id}`)
    }
    return <div className="post-card" onClick={displayPost}>
        <img src={value.image} alt="post image" />
        <h2>Honoring: {value.honoree["user_name"]} / Id: {value.honoree["id"]}</h2>
        <h2>{description}</h2>
        <h3>Comments:</h3>
        {value.comments.map((item, idx) => {
            if (idx < 3) {
                return (
                    <div key={uuid()}>
                        <p>{item.comment}</p>
                        <p>{item.user.user_name}</p>
                        <hr />
                    </div>
                )
            }
            return null
        })}
    </div>;
}

export default PostCard;