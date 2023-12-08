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
import Main from "./components/Main";
import Submission from "./components/Submission";
import Login from "./components/Login";

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
        path: "/main",
        element: <Main />
      }, 
      {
        path: "/submission",
        element: <Submission />
      }, 
      {
        path: "/posts",
        element: <Post />
      }
    ]
  }
])

root.render(
    <StrictMode>
        <RouterProvider router={router} />
    </StrictMode>
);
