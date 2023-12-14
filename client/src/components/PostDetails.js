import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
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
            alert(err)
            navigate('/')
        })
    }

    const checkToken = (acc_token) => fetch("/check_token", {
        headers: {
          "Authorization": `Bearer ${acc_token}`
        }
      })
    
      const postRefreshToken = (ref_token) => {
        return fetch("/refresh", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${ref_token}`
          }
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
                alert("Access Has Expired, Please Login Again")
              }
            })
            .then(data => {
              localStorage.setItem("access_token", JSON.stringify(data["access_token"]))
              get_post()
            })
            .catch(err => alert(err))
          }
        })
        .then(data => {
          if (data) {
            get_post()
          }
        })
        .catch(err => alert(err))
        
        }, [])

    return <div className="post-details">
        <h2>Post Details</h2>
        <img src={post.image} alt="post image" />
        <h2>Honoring: {post.honoree["user_name"]}</h2>
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