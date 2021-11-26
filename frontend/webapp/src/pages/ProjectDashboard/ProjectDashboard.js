import React, { Component } from 'react'
import SideNav from '../../components/SideNav/SideNav'
import Pagination from '../../components/Pagination/Pagination'
import LabelersTable from '../../components/LabelersTable/LabelersTable'
import Button from '../../components/Button/Button'
import Modal from './Modal/Modal'
import "./ProjectDashboard.scss"

export default class ProjectDashboard extends Component {
  constructor(props) {
    super(props)
    this.requestAddMember = this.requestAddMember.bind(this)
    this.state = {
       openModal:false
    }
  }

  requestAddMember(username, permission) {
    this.props.requestAddMember(username, permission)
    this.setState({
      openModal:false
    })
  }

  render() {
    return (
      <div>
        <div >
          <SideNav projects={true}/>
        </div>
        <div className="title">
          <h1>{this.props.project.name}</h1>
        </div>
        <div className="project_dashboard_content">
          <div className="project_dashboard_data">
            <div className="project_dashboard_accuracy">
              <h3>Acurácia do Classificador:</h3>
              <h1 className="project_dashboard_accuracy_text">{this.props.accuracy}%</h1>
            </div>
            <div className="project_dashboard_accuracy">
              <h3>Dados rotulados:</h3>
              <h1 className="project_dashboard_accuracy_text">{this.props.project.labelled_count}</h1>
            </div>
            <div className="project_dashboard_accuracy">
              <h3>Dados totais:</h3>
              <h1 className="project_dashboard_accuracy_text">{this.props.project.data_count}</h1>
            </div>
          </div>
          <div className="labelers_list">
            <h2>Membros</h2>
            <Pagination totalItems={5}/>
            <LabelersTable
              members={this.props.members}
            />
            <div className="project_dashboard_add_member">
              <Button
                text="Adicionar Membro"
                onClick={() => { this.setState({ openModal: true })} }
              />
            </div>
          </div>
          <div>
           <Modal
            open={this.state.openModal}
            primaryButtonText="Adicionar Membro"
            secondaryButtonText="Voltar"
            onRequestClose={() => { this.setState({ openModal: false })} }
            submit={this.requestAddMember}
           />
          </div>
        </div>
      </div>
    )
  }
}
