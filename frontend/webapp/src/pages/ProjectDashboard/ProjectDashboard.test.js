import React from 'react';
import ReactDOM from 'react-dom';
import ProjectDashboard from './ProjectDashboard';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<ProjectDashboard />, div);
  ReactDOM.unmountComponentAtNode(div);
});
