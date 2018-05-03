import React from "react";
import { Container, Row, Col } from 'reactstrap';
import Map from "./components/SentimentOne/Map"
import 'bootstrap/dist/css/bootstrap.css'
import './App.css'

class SentimentOne extends React.Component {
    render(){
        return (
                <div>
                    <Container>
                        <Row>
                            <Col> 
                                <Map/>
                            </Col>
                            <Col>
                            put the explaination of the data
                            </Col>
                         </Row>
                    </Container>

                </div>
        )
    }
}
export default SentimentOne;