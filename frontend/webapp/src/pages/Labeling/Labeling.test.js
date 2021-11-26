import React from 'react';
import ReactDOM from 'react-dom';
import Labeling from './Labeling';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<Labeling />, div);
  ReactDOM.unmountComponentAtNode(div);
});
