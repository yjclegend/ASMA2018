import React, { Component } from 'react';
import MyNav from "./components/Header/MyNav"
import MyBody from "./components/Body/MyBody"
import './App.css';
import 'bootstrap/dist/css/bootstrap.css'

class App extends Component {
  render() {
    return (
      <div class = "container-fluid">
        <div className='Nav'>
          <MyNav />
        </div>
        <div>
          <MyBody />
        </div>
      </div>
    );
  }
}

export default App;
