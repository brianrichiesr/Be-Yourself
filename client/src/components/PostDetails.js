import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { v4 as uuid } from 'uuid';

function PostDetails() {
// comments: [{…}, {…}, {…}, {…}, {…}]
// description: "Service certainly identify firm product. Friend network bank figure apply stop subject."
// id: 14
// image: "https://dummyimage.com/751x687"
// post_author: {email: 'vbaxter@example.net', id: 8, user_name: 'Jeffrey Guerrero'}
// status: "pending"

    const postObj = {
        comments: [],
        description: "",
        id: 0,
        image: "",
        post_author: {
            email: "",
            id: 0,
            user_name: ""
        },
        status: "pending"
    }

    const [post, setPost] = useState(postObj)
    const { id } = useParams()
    const navigate = useNavigate()
    
    useEffect(() => {
        fetch(`/posts/${id}`)
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                throw (res.statusText)
            }
        })
        .then(setPost)
        .catch(err => {
            alert(err)
            navigate('/main')
        })
    }, [])

    return <div className="post-details">
        <h2>Post # {post.id}</h2>
        <img src={post.image} alt="post image" />
        <h2>{post.description}</h2>
        <h3>Comments:</h3>
        {post.comments.map(item => {
            return (
                <div key={uuid()}>
                    <p>{item.comment}</p>
                    <p>{item.user.user_name}</p>
                    <hr />
                </div>
            )
        })}
    </div>;
}

export default PostDetails;