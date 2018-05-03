import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import { NavItem, NavLink,Nav,Navbar } from 'reactstrap';
import MyNav1 from "./components/Header/MyNav";
import Sentimentone from "./SentimentOne";
import MyBody from "./components/Body/MyBody";
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import './components/Header/MyNav.css'

const PageOne = () => (
  <div className = "container-fluid">
    <Sentimentone />
  </div>
)

const Home = () => (
  <div className = "container-fluid">
     <MyBody />
  </div>
)

const Index = () => (
  <div className="App">
    <Navbar className = "NavBar" expand="md">
      <div class = "container-fluid">
        <Nav class="navbar-nav mr-auto mt-2 mt-lg-0">
          <NavItem className ='NavItem'>
          <NavLink to="/" tag={Link}>Home</NavLink>
          </NavItem>
          <NavItem className = 'NavItem'>
            <NavLink to="/PageOne" tag={Link}>Analysis One</NavLink>
          </NavItem>
        </Nav>
      </div>
    </Navbar>
    <div>
      <Route path="/" exact component={Home} />
      <Route path="/PageOne" component={PageOne} />
    </div>
  </div>
)

class App extends Component {
  render() {
    return (
    <Router>
      <Index />
    </Router>
    );
  }
}

export default App;
