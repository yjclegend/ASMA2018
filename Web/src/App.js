import React, { Component } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import MyNav from './components/Nav/MyNav';


class App extends Component {
  render() {
    return (
      <Router>
        <div>
          <MyNav />
        </div>
      </Router>  
    
    );
  }
}

export default App;
