import React, { useState, useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "./Footer";
import UserContext from "./User";


function App() {

  const default_user = {
    user_name: "",
    id: 0
  }
  const [user, setUser] = useState(default_user)
  const navigate = useNavigate()
  

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
    const refresh_token = JSON.parse(localStorage.getItem('refresh_token'))
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
          setUser(data["user"])
        })
      }
    })
    .then(data => {
      if (data) {
        setUser(data["user"])
      }
    })
  }, [])

  const clickMe = (obj) => {
    setUser(obj)
  }

  return (
    <div>
      <UserContext.Provider value={[clickMe, "This is how useContext works!", user]}>
        <Navbar />
      <h1>{user.admin ? "Admin Header" : "App Header"}</h1>
      <Outlet />
      <Footer />
      </UserContext.Provider>
    </div>
  );
}

export default App;
