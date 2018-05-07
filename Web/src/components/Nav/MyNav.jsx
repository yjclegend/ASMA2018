import React from 'react';
import { NavItem, NavLink,Nav,Navbar } from 'reactstrap';
import { BrowserRouter as Router,Route, Link } from 'react-router-dom';
import SentimentOne from "../../components/Sentiment/SentimentOne";
import SentimentTwo from "../../components/Sentiment/SentimentTwo"
import MyBody from "../Home/MyBody";
import "./MyNav.css";

const PageOne = () => (
  <div className = "container-fluid" >
    <SentimentOne/>
  </div>
)
const PageTwo = () => (
  <div className = 'container-fluid'>
    <SentimentTwo/>
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
                <NavLink to="/PageTwo"tag={Link} >Analysis Two</NavLink>
              </NavItem>
            </Nav>
          </div>
        </Navbar>
        <div>
          <Route path="/" exact component={Home} />
          <Route path="/PageOne" component={PageOne} />
          <Route path="/PageTwo" component={PageTwo} />
        </div>
      </div>
    );
  }
  
}
export default MyNav