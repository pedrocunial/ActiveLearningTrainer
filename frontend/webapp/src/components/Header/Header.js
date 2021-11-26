import React, { Component } from 'react'
import { Header as HeaderCarbon,
         HeaderName,
       } from 'carbon-components-react/lib/components/UIShell/'
import "./Header.scss"

export default class Header extends Component {
  render() {
    return (
      <div>
        <HeaderCarbon className="header" aria-label="Ferramenta de Rotulagem">
          <HeaderName>
            [Ferramenta de Rotulagem]
          </HeaderName>
        </HeaderCarbon>
      </div>
    )
  }
}
