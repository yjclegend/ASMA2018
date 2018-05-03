import React from 'react';
import BodyLeft from "./BodyLeft"
import BodyRight from "./BodyRight"
import { Container, Row, Col } from 'reactstrap';
import "./MyBody.css";

export default class MyBody extends React.Component {
  render() {
    return (
      <div className = "body">  
      <Container>
        <Row>
          <Col> 
            <BodyLeft/>
          </Col>
          <Col>
            <BodyRight/>
          </Col>
        </Row>
      </Container>
      </div>
    );
  }
}