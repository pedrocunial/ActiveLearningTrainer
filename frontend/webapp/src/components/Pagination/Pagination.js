import React, { Component } from 'react'
import { PaginationV2 } from 'carbon-components-react'

export default class Pagination extends Component {
  render() {
    return (
      <div>
        <PaginationV2
          totalItems={this.props.totalItems}
          onChange={this.props.onChange}
          pageSize={5}
          pageSizes={[
            5
          ]}
        />
      </div>
    )
  }
}
