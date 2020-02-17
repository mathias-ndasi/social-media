import React from "react";
import Home from "./pages/Home";
import Navbar from "./components/Navbar";
import { Switch, Route } from "react-router";
import NotFound from "./pages/NotFound";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

import "./styles/index.css";

const App = () => {
  return (
    <div className="App">
      <Navbar />

      <Switch>
        <Route exact path="/" component={Home} />
        <Route exact path="/login" component={Login} />
        <Route exact path="/signup" component={Signup} />
        <Route component={NotFound} />
      </Switch>
    </div>
  );
};

export default App;
