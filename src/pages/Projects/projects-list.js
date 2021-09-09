import React, { Component } from "react"
import PropTypes from "prop-types"
import MetaTags from 'react-meta-tags';
import { connect } from "react-redux"
import { Link, withRouter } from "react-router-dom"
import * as moment from 'moment';

import {
  Badge,
  Col,
  Container,
  DropdownItem,
  DropdownMenu,
  DropdownToggle,
  Row,
  Table,
  UncontrolledDropdown,
  Modal,
  ModalHeader,
  ModalBody
} from "reactstrap"

import { AvForm, AvField } from "availity-reactstrap-validation"

//Import Breadcrumb
import Breadcrumbs from "../../components/Common/Breadcrumb"

import { map } from "lodash"

//Import Image
import images from "assets/images"
import companies from "assets/images/companies"

import {
  getProjects,
  updateProject,
  deleteProject
} from "../../store/projects/actions"

class ProjectsList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      projects: [],
      modal: false,
    }

    this.handleProjectClick = this.handleProjectClick.bind(this)
    this.toggle = this.toggle.bind(this)
    this.handleValidProjectSubmit = this.handleValidProjectSubmit.bind(this)
    this.handleProjectClicks = this.handleProjectClicks.bind(this)

  }

  componentDidMount() {
    const { projects, onGetProjects } = this.props;
    onGetProjects()
    this.setState({ projects })
  }

  handleProjectClicks = arg => {
    this.setState({ selectedProject: arg })
    this.toggle()
  }

  handleDeleteProject = (project) => {
    const { onDeleteProject } = this.props
    onDeleteProject(project)
  }

  handleProjectClick = arg => {
    const project = arg

    this.setState({
      projects: {
        id: project.id,
        img: project.img,
        name: project.name,
        description: project.description,
        status: project.status,
        color: project.color,
        dueDate: project.dueDate,
        team: project.team
      },
      isEdit: true,
    })

    this.toggle()
  }

  toggle() {
    this.setState(prevState => ({
      modal: !prevState.modal,
    }))
  }

  /**
   * Handling submit user on user form
   */
  handleValidProjectSubmit = (e, values) => {

    const { onAddNewProject, onUpdateProject } = this.props
    const { isEdit, projects, selectedProject } = this.state

    if (isEdit) {
      const updateProject = {
        id: projects.id,
        img: values.img,
        name: values.name,
        description: values.description,
        status: values.status,
        color: values.color,
        dueDate: values.dueDate,
        team: values.team
      }

      // update user
      onUpdateProject(updateProject)
    } else {

      const newProject = {
        id: Math.floor(Math.random() * (30 - 20)) + 20,
        name: values["name"],
        description: values["description"],
        status: values["status"],
        color: values["color"],
        dueDate: values["dueDate"],
        team: values["team"]
      }
      // save new user
      onAddNewProject(newProject)
    }
    this.setState({ selectedProject: null })
    this.toggle()
  }

  handleValidDate = (date) => {
    const date1 = moment(new Date(date)).format('DD MMM Y');
    return date1;
  }

  render() {
    const { projects } = this.props
    const { isEdit } = this.state

    return (
      <React.Fragment>
        <div className="page-content">
          <MetaTags>
            <title>Projects List | Skote - React Admin & Dashboard Template</title>
          </MetaTags>
          <Container fluid>
            {/* Render Breadcrumbs */}
            <Breadcrumbs title="Projects" breadcrumbItem="Projects List" />
            <p> DMY Format: {this.state.dateDMY} </p>
            <Row>
              <Col lg="12">
                <div className="">
                  <div className="table-responsive">
                    <Table className="project-list-table table-nowrap align-middle table-borderless">
                      <thead>
                        <tr>
                          <th scope="col" style={{ width: "100px" }}>
                            #
                          </th>
                          <th scope="col">Projects</th>
                          <th scope="col">Due Date</th>
                          <th scope="col">Status</th>
                          <th scope="col">Team</th>
                          <th scope="col">Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {map(projects, (project, index) => (
                          <tr key={index}>
                            <td>
                              <img
                                src={companies[project.img]}
                                alt=""
                                className="avatar-sm"
                              />
                            </td>
                            <td>
                              <h5 className="text-truncate font-size-14">
                                <Link
                                  to={`/projects-overview/${project.id}`}
                                  className="text-dark"
                                >
                                  {project.name}
                                </Link>
                              </h5>
                              <p className="text-muted mb-0">
                                {project.description}
                              </p>
                            </td>

                            <td>
                              {this.handleValidDate(project.dueDate)}
                            </td>
                            <td>
                              <Badge color={project.color} className={"bg-" + project.color}>
                                {project.status}
                              </Badge>
                            </td>
                            <td>
                              <div className="avatar-group">
                                {map(project.team, (member, index) =>
                                  !member.img || member.img !== "Null" ? (
                                    <div className="avatar-group-item" key={index}>
                                      <Link
                                        to="#"
                                        className="d-inline-block"
                                        id={"member" + member.id}
                                      >
                                        <img
                                          src={images[member.img]}
                                          className="rounded-circle avatar-xs"
                                          alt=""
                                        />
                                      </Link>
                                    </div>
                                  ) : (
                                    <Link
                                      to="#"
                                      className="d-inline-block"
                                      id={"member" + member.id}
                                      key={"_team_" + index}
                                    >
                                      <div className="avatar-xs">
                                        <span
                                          className={
                                            "avatar-title rounded-circle bg-" +
                                            member.color +
                                            " text-white font-size-16"
                                          }
                                        >
                                          {member.name}
                                        </span>
                                      </div>
                                    </Link>
                                  )
                                )}
                              </div>
                            </td>
                            <td>
                              <UncontrolledDropdown>
                                <DropdownToggle href="#" className="card-drop" tag="a">
                                  <i className="mdi mdi-dots-horizontal font-size-18" />
                                </DropdownToggle>
                                <DropdownMenu className="dropdown-menu-end">
                                  <DropdownItem href="#" onClick={() => this.handleProjectClick(project)}>
                                    <i className="mdi mdi-pencil font-size-16 text-success me-1" />{" "}
                                    Edit
                                  </DropdownItem>
                                  <DropdownItem href="#" onClick={() => this.handleDeleteProject(project)}>
                                    <i className="mdi mdi-trash-can font-size-16 text-danger me-1" />{" "}
                                    Delete
                                  </DropdownItem>
                                </DropdownMenu>
                              </UncontrolledDropdown>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                    <Modal
                      isOpen={this.state.modal}
                      className={this.props.className}
                    >
                      <ModalHeader toggle={this.toggle} tag="h4">
                        {!!isEdit ? "Edit Project" : "Add Project"}
                      </ModalHeader>
                      <ModalBody>
                        <AvForm
                          onValidSubmit={
                            this.handleValidProjectSubmit
                          }
                        >
                          <Row form>
                            <Col xs={12}>

                              <AvField type="hidden" value={this.state.projects.img || ""} name="img" />

                              <AvField type="hidden" value={this.state.projects.team || ""} name="team" />

                              <div className="mb-3">
                                <AvField
                                  name="name"
                                  label="Name"
                                  type="text"
                                  errorMessage="Invalid name"
                                  validate={{
                                    required: { value: true },
                                  }}
                                  value={this.state.projects.name || ""}
                                />
                              </div>

                              <div className="mb-3">
                                <AvField
                                  name="description"
                                  label="Description"
                                  type="text"
                                  errorMessage="Invalid Description"
                                  validate={{
                                    required: { value: true },
                                  }}
                                  value={this.state.projects.description || ""}
                                />
                              </div>

                              <div className="mb-3">
                                <AvField
                                  name="status"
                                  label="Status"
                                  id="status1"
                                  type="select"
                                  className="form-select"
                                  errorMessage="Invalid Status"
                                  validate={{
                                    required: { value: true },
                                  }}
                                  value={this.state.projects.status || "Pending"}
                                >
                                  <option>Completed</option>
                                  <option>Pending</option>
                                  <option>Delay</option>
                                </AvField>
                              </div>

                              <div className="mb-3">
                                <AvField
                                  name="color"
                                  label="Color"
                                  type="select"
                                  className="form-select"
                                  errorMessage="Invalid Color"
                                  validate={{
                                    required: { value: true },
                                  }}
                                  value={this.state.projects.color || "success"}
                                >
                                  <option>success</option>
                                  <option>warning</option>
                                  <option>danger</option>
                                </AvField>

                              </div>

                              <div className="mb-3">

                                <AvField
                                  name="dueDate"
                                  label="dueDate"
                                  type="date"
                                  errorMessage="Invalid Color"
                                  format='YYYY/MM/DD'
                                  validate={{
                                    required: { value: true },
                                  }}
                                  value={this.state.projects.dueDate || ""}
                                >
                                </AvField>

                              </div>

                            </Col>

                          </Row>
                          <Row>
                            <Col>
                              <div className="text-end">

                                <button
                                  type="submit"
                                  className="btn btn-success save-user"
                                >Save</button>
                              </div>
                            </Col>
                          </Row>
                        </AvForm>
                      </ModalBody>
                    </Modal>
                  </div>
                </div>
              </Col>
            </Row>

            <Row>
              <Col xs="12">
                <div className="text-center my-3">
                  <Link to="#" className="text-success">
                    <i className="bx bx-loader bx-spin font-size-18 align-middle me-2" />
                    Load more
                  </Link>
                </div>
              </Col>
            </Row>
          </Container>
        </div>
      </React.Fragment>
    )
  }
}

ProjectsList.propTypes = {
  projects: PropTypes.array,
  className: PropTypes.any,
  onGetProjects: PropTypes.func,
  onDeleteProject: PropTypes.func,
  onUpdateProject: PropTypes.func,
  onAddNewProject: PropTypes.func
}

const mapStateToProps = ({ projects }) => ({
  projects: projects.projects,
})

const mapDispatchToProps = dispatch => ({
  onGetProjects: () => dispatch(getProjects()),
  onUpdateProject: project => dispatch(updateProject(project)),
  onDeleteProject: project => dispatch(deleteProject(project)),
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withRouter(ProjectsList))