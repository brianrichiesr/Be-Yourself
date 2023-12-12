import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import PostContext from "./Post";
import PostCard from "./PostCard";

function Posts() {

  const [posts, setPosts] = useState([])
  const navigate = useNavigate()

  const value = useContext(PostContext)
  const token = JSON.parse(localStorage.getItem('access_token'))
  
  useEffect(() => {
    
      if (token) {
        fetch('/posts', {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          }
        })
        .then(res => {
          if (res.ok) {
            console.log("Res  -", res)
            return res.json()
          } else {
            localStorage.clear()
            const func = value[0]
            func({user_name: "", id: 0})
            navigate('/')
          }
        })
        .then(data => {
          // data = {msg: 'Token has expired}
          debugger
          if (!data.msg) {
            setPosts(data)
          } else {
            console.log("Msg  -")
            localStorage.clear()
            const func = value[0]
            func({user_name: "", id: 0})
            navigate('/')
          }
        })
        .catch(() => {
          console.log("Post Catch -", value)
          localStorage.clear()
          navigate('/')
        })
      } 
    }, [])

  return (
    <>
      <div>Main</div>
        <div>{posts.map((item, idx) => {
          return (
            <PostContext.Provider key={`key-post-${idx}`} value={item}>
            <PostCard />
          </PostContext.Provider>
          )

        })}</div>
    </>
  );
}

export default Posts;