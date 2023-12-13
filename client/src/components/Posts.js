import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import PostContext from "./Post";
import PostCard from "./PostCard";
import { v4 as uuid } from 'uuid'

function Posts() {

  const [posts, setPosts] = useState([])
  // const navigate = useNavigate()

  // const value = useContext(PostContext)

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

  const get_posts = (post_token) => {
    fetch('/posts', {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${post_token}`
      }
    })
    .then(res => {
      if (res.ok) {
        return res.json()
      }
    })
    .then(data => {
      if (data) {
        setPosts(data)
      }
    })
    .catch(err => alert(err))
  }
  
  useEffect(() => {
    const token = JSON.parse(localStorage.getItem('access_token'))
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
          get_posts(data["access_token"])
        })
        .catch(err => alert(err))
      }
    })
    .then(data => {
      if (data) {
        get_posts(token)
      }
    })
    .catch(err => alert(err))
    
    }, [])

  return (
    <>
      <div>Main</div>
        <div>{posts.map((item, idx) => {
          return (
            <PostContext.Provider key={uuid()} value={item}>
            <PostCard num={idx} />
          </PostContext.Provider>
          )

        })}</div>
    </>
  );
}

export default Posts;