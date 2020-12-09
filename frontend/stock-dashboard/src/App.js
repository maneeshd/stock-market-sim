import TradingViewWidget, { Themes } from 'react-tradingview-widget';
import { Container } from 'react-bootstrap';

const App = () => (
    <Container className='py-4'>
      <TradingViewWidget
        symbol="NASDAQ:AAPL"
        theme={Themes.DARK}
        locale="en"
      />
    </Container>
);

export default App;
