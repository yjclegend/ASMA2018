import React from "react";
import { Container, Row, Col } from 'reactstrap';
import Map from "./Map"
import 'bootstrap/dist/css/bootstrap.css'

class SentimentTwo extends React.Component {
    render(){
        return (
                <div>
                    <Container>
                        <Row>
                            <Col md="8"> 
                                <Map />
                            </Col>
                            <Col>
                                <p>Put the map here</p>
                            </Col>
                         </Row>
                    </Container>

                </div>
        )
    }
}
export default SentimentTwo;