import React from 'react';
import BodyLeft from "./BodyLeft"
import BodyRight from "./BodyRight"
import { Container, Row, Col } from 'reactstrap';

export default class MyBody extends React.Component {
  render() {
    return (
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
    );
  }
}