import React, { Component } from 'react'
import {XYPlot, XAxis, YAxis, HorizontalGridLines, VerticalGridLines, LineMarkSeries} from 'react-vis';
import '../../../node_modules/react-vis/dist/style.css';

export default class LineChart extends Component {
  render() {
    return (
      <XYPlot
      width={400}
      height={300}>
        <VerticalGridLines />
        <HorizontalGridLines />
        <XAxis title="Número de amostras"/>
        <YAxis title="Acurácia (%)"/>
        <LineMarkSeries
          curve={'curveMonotoneX'}
          data={this.props.data}/>
      </XYPlot>
    )
  }
}
