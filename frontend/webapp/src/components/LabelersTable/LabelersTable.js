import React, { Component } from 'react'
import { DataTable } from 'carbon-components-react'
const { Table, TableHead, TableHeader, TableContainer, TableRow, TableBody, TableCell } = DataTable;

const ROLES = [
  'Rotulador',
  'Admin',
  'Dono'
]

// We would have a headers array like the following
const headers = [
  {
    key: 'name',
    header: 'Nome',
  },
  {
    key: 'permission',
    header: 'Permissão',
  }
];

export default class LabelersTable extends Component {
  constructor(props) {
    super(props)
    this.getMembers = this.getMembers.bind(this)
  }

  getMembers(){
    return this.props.members.map(member => {
      return {
        id: member.name,
        name: member.name,
        permission: ROLES[member.permission]
      }
    })
  }

  render() {
    return (
      <DataTable
        rows={this.getMembers()}
        headers={headers}
        render={({ rows, headers, getHeaderProps }) => (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  {headers.map(header => (
                    <TableHeader {...getHeaderProps({ header })}>
                      {header.header}
                    </TableHeader>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map(row => (
                  <TableRow key={row.id}>
                    {row.cells.map(cell => (
                      <TableCell key={cell.id}>{cell.value}</TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      />
    )
  }
}
