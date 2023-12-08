// import React, { useEffect, useState } from "react";
// import { Switch, Route } from "react-router-dom";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "./Footer";

function App() {
  return (
    <div>
      <Navbar />
      <h1>App Header</h1>
      <Outlet />
      <Footer />
    </div>
  );
}

export default App;
