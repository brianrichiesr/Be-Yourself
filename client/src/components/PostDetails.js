import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import { checkToken, postRefreshToken} from "./Authorize";
import { v4 as uuid } from 'uuid';

function PostDetails() {

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
        honoree: {
            email: "",
            id: 0,
            user_name: ""
        },
        status: "pending"
    }

    const [post, setPost] = useState(postObj)
    const { id } = useParams()
    const navigate = useNavigate()

    const get_post = () => {
        fetch(`/posts/${id}`)
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                throw (res.statusText)
            }
        })
        .then(data => setPost(data))
        .catch(err => {
            toast(err)
            navigate('/')
        })
    }
      
      useEffect(() => {
        const token = JSON.parse(localStorage.getItem('access_token'))
        if (!token) {
            localStorage.clear()
            navigate('/')
            return
          }
        const refresh_token = JSON.parse(localStorage.getItem('refresh_token'))
        checkToken(token)
    
        checkToken(token)
        .then(res => {
          if (res.ok) {
            return res.json()
          } else if (res.status === 401) {
            postRefreshToken(refresh_token)
            .then(resp => {
              if (resp.ok) {
                return resp.json()
              } else {
                localStorage.clear()
                toast("Access Has Expired, Please Login Again")
              }
            })
            .then(data => {
              localStorage.setItem("access_token", JSON.stringify(data["access_token"]))
              get_post()
            })
            .catch(err => toast(err))
          }
        })
        .then(data => {
          if (data) {
            get_post()
          }
        })
        .catch(err => toast(err))
        
        }, [])
    return (
        <div className="post-details">
            <Toaster />
            <h2>Post Details</h2>
            <img src={post.image} alt="post image" />
            <h2>Honoring: {post.honoree["user_name"]} / Id: {post.honoree["id"]}</h2>
            <h2>{post.description}</h2>
            <h3>Author: {post.post_author.user_name} / Id: {post.post_author.id}</h3>
            <h3>Comments:</h3>
            {post.comments.map(item => {
                return (
                    <div key={uuid()}>
                        <p>{item.comment}</p>
                        <p>Author: {item.user.user_name} / Id: {item.user.id}</p>
                        <hr />
                    </div>
                )
            })}
        </div>
    );
}

export default PostDetails;