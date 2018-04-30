import React from 'react';
import { NavItem, NavLink,Nav,Navbar } from 'reactstrap';
import "./MyNav.css";
import { Link } from 'react-router-dom';
import "../../App"
import "../../SentimentOne"
import "../../SentimentTwo"

export default class MyNav extends React.Component {
  render() {
    return (
      <Navbar className="NavBar" expand="md" >
        <div class="container-fluid">
          <Nav class="navbar-nav mr-auto mt-2 mt-lg-0"  >
            <NavItem className='NavItem'>
              <NavLink to="/" tag={Link}>Home</NavLink>
            </NavItem>
            <NavItem className='NavItem'>
              <NavLink to="/SentimentOne"  tag={Link}>Analysis One</NavLink>
            </NavItem>
            <NavItem className='NavItem'>
              <NavLink to= "/SentimentTwo" tag={Link}>Analysis Two</NavLink>
            </NavItem>
          </Nav>
        </div>
    </Navbar>
    );
  }
}