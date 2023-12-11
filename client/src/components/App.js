import React, { useState} from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "./Footer";
import UserContext from "./User";


function App() {
  // const UserContext = createContext(null)
  const demo = {
    user_name: "Dave",
    id: 0
  }
  const [user, setUser] = useState(demo)
  const clickMe = (obj) => {
    // const obj = {obj}
    // obj.user_name = "Nobody"
    setUser(obj)
    // console.log(user)
  }
  console.log("App Demo -", user)
  return (
    <div>
      <UserContext.Provider value={[clickMe, "This is how useContext works!"]}>
        <Navbar />
      <h1>App Header</h1>
      <Outlet />
      <Footer />
      </UserContext.Provider>
    </div>
  );
}

export default App;
