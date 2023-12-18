// import React from "react";
// import App from "./components/App";
// import "./index.css";
// import { createRoot } from "react-dom/client";

// const container = document.getElementById("root");
// const root = createRoot(container);
// root.render(<App />);

// import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import { GoogleOAuthProvider } from "@react-oauth/google";

import "./index.css"
import App from "./components/App";
import Error from "./components/Error";
import Landing from "./components/Landing";
import Signup from "./components/Signup";
import Posts from "./components/Posts";
import Submission from "./components/Submission";
import Login from "./components/Login";
import PostDetails from "./components/PostDetails";
import Profile from "./components/Profile";
import Users from "./components/Users";
import UserDetails from "./components/UserDetails";
const clientId = process.env.REACT_APP_GOOGLE_CLIENT_ID
const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

const router = createBrowserRouter([
  {
    element: <App />,
    errorElement: <Error />,
    children: [
      {
        path: "/",
        element: <Landing />
      }, 
      {
        path: "/login",
        element: <Login />
      }, 
      {
        path: "/signup",
        element: <Signup />
      }, 
      {
        path: "/posts",
        element: <Posts />
      }, 
      {
        path: "/posts/:id",
        element: <PostDetails />
      }, 
      {
        path: "/users",
        element: <Users />
      }, 
      {
        path: "/users/:id",
        element: <UserDetails />
      },, 
      {
        path: "/submission",
        element: <Submission />
      }, 
      {
        path: "/profile",
        element: <Profile />
      }
    ]
  }
])

root.render(
    <GoogleOAuthProvider clientId={clientId}>
        <RouterProvider router={router} />
    </GoogleOAuthProvider>
);
