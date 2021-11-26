import React, { Component } from 'react'
import { SideNav as SideNavCarbon,
         SideNavItems,
         SideNavLink,
       } from 'carbon-components-react/lib/components/UIShell/'
import { inject, observer } from 'mobx-react'

// Icons
import UserAvatar20 from '@carbon/icons-react/es/user--avatar/20';
import Grid20 from '@carbon/icons-react/es/grid/20';
import Power20 from '@carbon/icons-react/es/power/20';

// CSS
import "./SideNav.scss"

class SideNav extends Component {
  constructor(props) {
    super(props)
    this.logout = this.logout.bind(this)
  }

  logout(){
    this.props.AppStore.logout()
  }

  render() {
    return (
      <div>
        <SideNavCarbon className="sidenav" aria-label="Side navigation">
          <SideNavItems>
            <SideNavLink
              isActive={this.props.projects}
              icon={<Grid20 style={{}}/>} //Empty style fixes lib bug
            >
              Projetos
            </SideNavLink>
            <SideNavLink
              isActive={this.props.logout}
              onClick={this.logout}
              icon={<Power20 style={{}}/>} //Empty style fixes lib bug
            >
              Sair
            </SideNavLink>
          </SideNavItems>
        </SideNavCarbon>
      </div>
    )
  }
}

SideNav = inject('AppStore')(observer(SideNav))
export default SideNav