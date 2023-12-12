// import React from "react";
// import App from "./components/App";
// import "./index.css";
// import { createRoot } from "react-dom/client";

// const container = document.getElementById("root");
// const root = createRoot(container);
// root.render(<App />);

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom"

import "./index.css"
import App from "./components/App";
import Post from "./components/Post";
import Error from "./components/Error";
import Landing from "./components/Landing";
import Signup from "./components/Signup";
import Posts from "./components/Posts";
import Submission from "./components/Submission";
import Login from "./components/Login";
import PostDetails from "./components/PostDetails";

const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

const router = createBrowserRouter([
  {
    path: "/",
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
        path: "/submission",
        element: <Submission />
      }, 
      {
        path: "/posts",
        element: <Post />
      }, 
      {
        path: "/posts/:id",
        element: <PostDetails />
      }
    ]
  }
])

root.render(
    <StrictMode>
        <RouterProvider router={router} />
    </StrictMode>
);
