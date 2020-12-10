import React, { useEffect, useState } from 'react'
import { Container, Row, Col, Dropdown, DropdownButton } from 'react-bootstrap';
import { Line } from 'react-chartjs-2';

const STOCKS = ["AAPL", "AMZN", "FB", "GOOGL", "INTC", "MSFT", "NFLX", "NVDA", "QCOM", "TSLA"]

const STOCK_DETAILS = {
    "AAPL": "Apple, Inc.",
    "AMZN": "Amazon.com, Inc.",
    "FB": "Facebook, Inc",
    "GOOGL": "Alphabet, Inc.",
    "INTC": "Intel Corporation",
    "MSFT": "Microsoft Corporation",
    "NFLX": "Netflix Inc.",
    "NVDA": "Nvidia Corporation",
    "QCOM": "Qualcomm, Inc.",
    "TSLA": "Tesla Inc"
};


const HistoricalData = (props) => {
    const [curStock, setCurStock] = useState(STOCKS[0]);

    const handleStockSymbolChange = (eventKey) => {
        setCurStock(eventKey);
    };

    return (
        <Container className="p-2">
            <Row className="align-items-end p-2">
                <Col md={9} className="align-self-end">
                    <span className="text-secondary font-weight-bold" style={{
                        fontSize: '24px', fontFamily: 'Monospace', textDecoration: 'underline'
                    }}>
                        {STOCK_DETAILS[curStock]}
                    </span>
                </Col>
                <Col md={3} className="text-right">
                    <DropdownButton id="stock-symbol-select-btn" title={curStock} onSelect={handleStockSymbolChange}>
                        {
                            STOCKS.map((ele, idx) => (
                                <Dropdown.Item key={idx} eventKey={ele} href={`#${ele}`}>
                                    {ele}
                                </Dropdown.Item>
                            ))
                        }
                    </DropdownButton>
                </Col>
            </Row>
        </Container>);
};

export default HistoricalData;
