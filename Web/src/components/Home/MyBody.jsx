import React from 'react';
import { Container, Row, Col } from 'reactstrap';
import earthMap from "../../assets/img/map.png"
import "./MyBody.css";

export default class MyBody extends React.Component {
  render() {
    return (
      <div className = "body">  
      <Container>
        <Row>
          <Col md="8"> 
          <img  src = {earthMap} alt = "map" height = "100%"/>
          </Col>
          <Col>
          <p> This is for COMP90024</p>
          </Col>
        </Row>
      </Container>
      </div>
    );
  }
}