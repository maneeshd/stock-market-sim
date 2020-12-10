import React, {Component} from 'react';
import Layout from './components/Layout/Layout';
import styles from './App.module.css';

class App extends Component {
  render (){
  return (
    <div>
      <div className={styles.Nav}>stock-market-sim Candlestick Chart</div>
      <Layout>
      </Layout>
      <div>&copy; </div>
    </div>
  );
  }
}

export default App;
