import React, { useEffect, useState } from 'react'
import { Container, Row, Col, Dropdown, DropdownButton } from 'react-bootstrap';
import { Line } from 'react-chartjs-2';
import io from 'socket.io-client';


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


const init_live_data = {
    labels: [],
    datasets: [
        {
            label: 'Stock Price in USD',
            data: [],
            fill: false,
            lineTension: 0,
            backgroundColor: 'rgb(255, 0, 0)',
            borderColor: 'rgba(255, 0, 0, 0.25)',
        },
    ],
}


const LiveGraph = (props) => {
    const [curStock, setCurStock] = useState(STOCKS[0]);
    const [liveData, setLiveData] = useState(init_live_data);

    const handleStockSymbolChange = (eventKey) => {
        setCurStock(eventKey);
    };

    // ComponentDidMount
    useEffect(() => {
        const socket = io('http://127.0.0.1:5000/api/socket.io');

        socket.on('connect', () => {
            console.log(`SocketIO: Connected! (${socket.id})`);
            socket.emit('message', 'Connected');
        }).emit(
            'get_live_data', curStock
        ).on('graph_data', (resp) => {
            const newState = {
                ...liveData,
                labels: [...resp.labels],
                datasets: [...liveData.datasets]
            }
            newState.datasets[0].data = [...resp.data];
            setLiveData(newState);
        });

        socket.on('diconnect', () => {
            socket.emit('disconnect');
            console.log('SocketIO: Disconnected!');
        });

        return () => socket.disconnect();
    }, [curStock]);

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

            <Line data={liveData} />
        </Container>
    );
};

export default LiveGraph;
