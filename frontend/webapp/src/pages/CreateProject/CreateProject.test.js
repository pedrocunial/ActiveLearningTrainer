import React from 'react';
import ReactDOM from 'react-dom';
import CreateProject from './CreateProject'
import { Provider } from 'mobx-react'

import CreateProjectStore from '../../stores/CreateProjectStore'
import AppStore from '../../stores/AppStore'


it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(
    <Provider 
      CreateProjectStore={CreateProjectStore}
      AppStore={AppStore}>
      <CreateProject />
    </Provider>, 
  div);
  ReactDOM.unmountComponentAtNode(div);
});
