import React from 'react';
import { NavItem, NavLink,Nav,Navbar } from 'reactstrap';
import { BrowserRouter as Router,Route, Link } from 'react-router-dom';
import Sentimentone from "../../SentimentOne";
import MyBody from "../Body/MyBody";
import "./MyNav.css";

const PageOne = () => (
  <div className = "container-fluid" >
      <Sentimentone/>
  </div>
)

const Home = () => (
  <div className = "container-fluid">
      <MyBody />
  </div>
)

class MyNav extends React.Component {
  render() {
    return (
      <div>
        <Navbar className="NavBar" expand="md" >
          <div class="container-fluid">
            <Nav class="navbar-nav mr-auto mt-2 mt-lg-0"  >
              <NavItem className='NavItem'>
                <NavLink to = "/" tag={Link} >Home</NavLink>
              </NavItem>
              <NavItem className='NavItem'>
                <NavLink to="/PageOne"tag={Link} >Analysis One</NavLink>
              </NavItem>
              <NavItem className='NavItem'>
                <NavLink  >Analysis Two</NavLink>
              </NavItem>
            </Nav>
          </div>
        </Navbar>
        <div>
          <Route path="/" exact component={Home} />
          <Route path="/PageOne" component={PageOne} />
        </div>
      </div>
    );
  }
  
}
export default MyNav