import { Navbar, Nav } from 'react-bootstrap';
import {
    BrowserRouter as Router,
    Switch,
    Route, Link
} from "react-router-dom";
import LiveGraph from './components/LiveGraph';
import HistoricalData from './components/HistoricalData';


const App = () => (
    <Router>
        <Navbar bg="dark" variant="dark" expand="lg" className="shadow">
            <Navbar.Brand to="/" id="#live_data" as={Link}>StockStream</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link to="/" as={Link}>Live Data</Nav.Link>
                    <Nav.Link to="/historical_data" as={Link}>Historical Data</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <Switch>
          <Route exact path="/">
            <LiveGraph />
          </Route>
          <Route path="/historical_data">
            <HistoricalData />
          </Route>
        </Switch>
    </Router>
);

export default App;
