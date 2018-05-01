import React from 'react';
import { NavItem, NavLink,Nav,Navbar } from 'reactstrap';
import "./MyNav.css";


class MyNav extends React.Component {
  render() {
    return (
      <Navbar className="NavBar" expand="md" >
        <div class="container-fluid">
          <Nav class="navbar-nav mr-auto mt-2 mt-lg-0"  >
            <NavItem className='NavItem'>
              <NavLink  >Home</NavLink>
            </NavItem>
            <NavItem className='NavItem'>
              <NavLink  >Analysis One</NavLink>
            </NavItem>
            <NavItem className='NavItem'>
              <NavLink  >Analysis Two</NavLink>
            </NavItem>
          </Nav>
        </div>
    </Navbar>
    );
  }
}
export default MyNav