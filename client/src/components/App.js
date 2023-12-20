import React, { useState, useEffect } from "react";
import { Outlet } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import { checkToken, postRefreshToken} from "./Authorize";
import Navbar from "./Navbar";
import Footer from "./Footer";
import UserContext from "./User";


function App() {
  /* Create default info for user state */
  const default_user = {
    user_name: "",
    id: 0
  }
  /* Set user state to default */
  const [user, setUser] = useState(default_user);

  
  useEffect(() => {
    /* Grab tokens from localStorage */
    const token = JSON.parse(localStorage.getItem('access_token'));
    const refresh_token = JSON.parse(localStorage.getItem('refresh_token'));
    /* Call 'checkToken' */
    checkToken(token)
    .then(res => {
      /* If res.ok, meaning if access token still valid and not expired, return json */
      if (res.ok) {
        return res.json()
      } else if (res.status === 401) {
        /* Call 'postRefreshToken' to see a new access token can be issued */
        postRefreshToken(refresh_token)
        .then(resp => {
          /* If res.ok, meaning if access token reissued, return json */
          if (resp.ok) {
            return resp.json();
            /* Else refresh has expired and user must login again */
          } else {
            /* Clear localStorage and display message in toast */
            localStorage.clear();
            toast("Access Has Expired, Please Login Again");
          }
        })
        .then(data => {
          /* Assign new access token to localStorage */
          localStorage.setItem("access_token", JSON.stringify(data["access_token"]));
          /* Set user state */
          setUser(data["user"]);
        })
      }
    })
    .then(data => {
      /* If there is data, set user state */
      if (data) {
        setUser(data["user"]);
      }
    })
    /* Any errors that make it this far, display in toast */
    .catch(err => toast(err));
  }, []);
  /* Function available to entire app through useContext that will set user state to 'obj' passed */
  const setUserData = (obj) => {
    setUser(obj);
  }

  return (
    <div id="appDiv">
      <UserContext.Provider value={[setUserData, "This is how useContext works!", user]}>
      <Navbar />
      <Toaster />
      <Outlet />
      </UserContext.Provider>
      <Footer />
    </div>
  );
}

export default App;
