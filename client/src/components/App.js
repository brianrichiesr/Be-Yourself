import React, { useState, useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "./Footer";
import UserContext from "./User";


function App() {

  const demo = {
    user_name: "Nobody",
    id: 0
  }
  const [user, setUser] = useState(demo)
  const navigate = useNavigate()
  const token = JSON.parse(localStorage.getItem('access_token'))
  
  useEffect(() => {
    

    if (token) {
      fetch('/check_user', {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        }
      })
      .then(res => {
        if (res.ok) {
          return res.json()
        } else {
          localStorage.clear()
          setUser({user_name: "Unauthorized", id: 0})
          navigate('/')
        }
      })
      .then(data => {
        console.log("App", data)
          if (data.errors) {
              // setSignupError(data.errors);
              localStorage.clear()
              setUser({user_name: "Errors", id: 0})
              // throw (data.errors);
              navigate('/')
          }
          data["access_token"] = token
          setUser(data["user"]);
      })
      .catch(err => {
        localStorage.clear()
        setUser({user_name: "Catch", id: 0})
        navigate('/')
        alert(err)
      })
    }
  }, [])

  const clickMe = (obj) => {
    setUser(obj)
  }

  return (
    <div>
      <UserContext.Provider value={[clickMe, "This is how useContext works!", user]}>
        <Navbar />
      <h1>App Header</h1>
      <Outlet />
      <Footer />
      </UserContext.Provider>
    </div>
  );
}

export default App;
