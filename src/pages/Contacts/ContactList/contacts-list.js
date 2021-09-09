import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import MetaTags from 'react-meta-tags';
import { withRouter, Link } from "react-router-dom";
import { Card, CardBody, Col, Container, Row, Modal, Button, ModalHeader, ModalBody } from "reactstrap";
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';

import ToolkitProvider, { Search } from "react-bootstrap-table2-toolkit";
import BootstrapTable from "react-bootstrap-table-next";

import images from "assets/images";

import { AvForm, AvField } from "availity-reactstrap-validation";

//Import Breadcrumb
import Breadcrumbs from "components/Common/Breadcrumb";

import {
  getUsers,
  addNewUser,
  updateUser,
  deleteUser
} from "store/contacts/actions";

import { isEmpty, size, map } from "lodash";

class ContactsList extends Component {
  constructor(props) {
    super(props);
    this.node = React.createRef();
    this.state = {
      users: [],
      modal: false,
      contactListColumns: [
        {
          text: "id",
          dataField: "id",
          sort: true,
          hidden: true,
          formatter: (cellContent, user) => (
            <>
              {user.id}
            </>
          ),
        },
        {
          dataField: "img",
          text: "#",
          formatter: (cellContent, user) => (
            <>
              {!user.img ? (
                <div className="avatar-xs">
                  <span className="avatar-title rounded-circle">
                    {user.name.charAt(0)}
                  </span>
                </div>
              ) : (
                <div>
                  <img
                    className="rounded-circle avatar-xs"
                    src={images[user.img]}
                    alt=""
                  />
                </div>
              )}
            </>
          ),
        },
        {
          text: "Name",
          dataField: "name",
          sort: true,
          formatter: (cellContent, user) => (
            <>
              <h5 className="font-size-14 mb-1">
                <Link to="#" className="text-dark">
                  {user.name}
                </Link>
              </h5>
              <p className="text-muted mb-0">{user.designation}</p>
            </>
          ),
        },
        {
          dataField: "email",
          text: "Email",
          sort: true,
        },
        {
          text: "Tags",
          dataField: "tags",
          sort: true,
          formatter: (cellContent, user) => (
            <>
              {map(
                user.tags,
                (tag, index) =>
                  index < 2 && (
                    <Link
                      to="#"
                      className="badge badge-soft-primary font-size-11 m-1"
                      key={"_skill_" + user.id + index}
                    >
                      {tag}
                    </Link>
                  )
              )}
              {size(user.tags) > 2 && (
                <Link
                  to="#"
                  className="badge badge-soft-primary font-size-11 m-1"
                  key={"_skill_" + user.id}
                >
                  {size(user.tags) - 1} + more
                </Link>
              )}
            </>
          ),
        },
        {
          dataField: "projects",
          text: "Projects",
          sort: true,
        },
        {
          dataField: "menu",
          isDummyField: true,
          editable: false,
          text: "Action",
          formatter: (cellContent, user) => (
            <div className="d-flex gap-3">
              <Link className="text-success" to="#"><i className="mdi mdi-pencil font-size-18" id="edittooltip" onClick={() => this.handleUserClick(user)}></i></Link>
              <Link className="text-danger" to="#"><i className="mdi mdi-delete font-size-18" id="deletetooltip" onClick={() => this.handleDeleteUser(user)}></i></Link>
            </div>
          ),
        },
      ]
    };
    this.handleUserClick = this.handleUserClick.bind(this);
    this.toggle = this.toggle.bind(this);
    this.handleValidUserSubmit = this.handleValidUserSubmit.bind(this);
    this.handleUserClicks = this.handleUserClicks.bind(this);
  }

  componentDidMount() {
    const { users, onGetUsers } = this.props;
    if (users && !users.length) {
      onGetUsers();
    }
    this.setState({ users });
  }

  toggle() {
    this.setState(prevState => ({
      modal: !prevState.modal,
    }));
  }

  handleUserClicks = arg => {
    this.setState({ users: '', isEdit: false });
    this.toggle();
  };

  // eslint-disable-next-line no-unused-vars
  componentDidUpdate(prevProps, prevState, snapshot) {
    const { users } = this.props;
    if (!isEmpty(users) && size(prevProps.users) !== size(users)) {
      this.setState({ users: {}, isEdit: false });
    }
  }

  onPaginationPageChange = page => {
    if (
      this.node &&
      this.node.current &&
      this.node.current.props &&
      this.node.current.props.pagination &&
      this.node.current.props.pagination.options
    ) {
      this.node.current.props.pagination.options.onPageChange(page);
    }
  };

  /* Insert,Update Delete data */

  handleDeleteUser = (user) => {
    const { onDeleteUser } = this.props;
    if (user.id !== undefined) {
      onDeleteUser(user);
      this.onPaginationPageChange(1);
    }
  };

  handleUserClick = arg => {
    const user = arg;

    this.setState({
      users: {
        id: user.id,
        name: user.name,
        designation: user.designation,
        email: user.email,
        tags: user.tags,
        projects: user.projects
      },
      isEdit: true,
    });

    this.toggle();
  };

  /**
   * Handling submit user on user form
   */
  handleValidUserSubmit = (e, values) => {
    const { onAddNewUser, onUpdateUser } = this.props;
    const { isEdit, users, selectedUser } = this.state;

    if (isEdit) {
      const updateUser = {
        id: users.id,
        name: values.name,
        designation: values.designation,
        tags: values.tags,
        email: values.email,
        projects: values.projects
      };

      // update user
      onUpdateUser(updateUser);
    } else {

      const newUser = {
        id: Math.floor(Math.random() * (30 - 20)) + 20,
        name: values["name"],
        designation: values["designation"],
        email: values["email"],
        tags: values["tags"],
        projects: values["projects"]
      };
      // save new user
      onAddNewUser(newUser);
    }
    this.setState({ selectedUser: null });
    this.toggle();
  };

  /* Insert,Update Delete data */

  render() {
    // const { users } = this.state
    const { SearchBar } = Search;

    const { users } = this.props;

    const { isEdit } = this.state;

    const pageOptions = {
      sizePerPage: 10,
      totalSize: users.length, // replace later with size(users),
      custom: true,
    };

    const defaultSorted = [{
      dataField: 'id', // if dataField is not match to any column you defined, it will be ignored.
      order: 'desc' // desc or asc
    }];

    const selectRow = {
      mode: 'checkbox'
    };

    return (
      <React.Fragment>
        <div className="page-content">
          <MetaTags>
            <title>Users List | Skote - React Admin & Dashboard Template</title>
          </MetaTags>
          <Container fluid>
            {/* Render Breadcrumbs */}
            <Breadcrumbs title="Contacts" breadcrumbItem="Users List" />
            <Row>
              <Col lg="12">
                <Card>
                  <CardBody>

                    <PaginationProvider
                      pagination={paginationFactory(pageOptions)}
                      keyField='id'
                      columns={this.state.contactListColumns}
                      data={users}
                    >
                      {
                        ({
                          paginationProps,
                          paginationTableProps
                        }) => (
                          <ToolkitProvider
                            keyField='id'
                            columns={this.state.contactListColumns}
                            data={users}
                            search
                          >
                            {
                              toolkitprops => (
                                <React.Fragment>
                                  <Row className="mb-2">
                                    <Col sm="4">
                                      <div className="search-box ms-2 mb-2 d-inline-block">
                                        <div className="position-relative">
                                          <SearchBar {...toolkitprops.searchProps} />
                                          <i className="bx bx-search-alt search-icon" />
                                        </div>
                                      </div>
                                    </Col>
                                    <Col sm="8">
                                      <div className="text-sm-end">
                                        <Button
                                          color="primary"
                                          className="font-16 btn-block btn btn-primary"
                                          onClick={this.handleUserClicks}
                                        >
                                          <i className="mdi mdi-plus-circle-outline me-1" />
                                          Create New User
                                        </Button>
                                      </div>
                                    </Col>
                                  </Row>
                                  <Row>
                                    <Col xl="12">
                                      <div className="table-responsive">
                                        <BootstrapTable
                                          {...toolkitprops.baseProps}
                                          {...paginationTableProps}
                                          selectRow={selectRow}
                                          defaultSorted={defaultSorted}
                                          classes={
                                            "table align-middle table-nowrap table-hover"
                                          }
                                          bordered={false}
                                          striped={false}
                                          responsive
                                          ref={this.node}
                                        />

                                        <Modal
                                          isOpen={this.state.modal}
                                          className={this.props.className}
                                        >
                                          <ModalHeader toggle={this.toggle} tag="h4">
                                            {!!isEdit ? "Edit User" : "Add User"}
                                          </ModalHeader>
                                          <ModalBody>
                                            <AvForm
                                              onValidSubmit={
                                                this.handleValidUserSubmit
                                              }
                                            >
                                              <Row form>
                                                <Col className="col-12">
                                                  <div className="mb-3">

                                                    <AvField
                                                      name="name"
                                                      label="Name"
                                                      type="text"
                                                      errorMessage="Invalid name"
                                                      validate={{
                                                        required: { value: true },
                                                      }}
                                                      value={this.state.users.name || ""}
                                                    />
                                                  </div>
                                                  <div className="mb-3">

                                                    <AvField
                                                      name="designation"
                                                      label="Designation"
                                                      type="text"
                                                      errorMessage="Invalid Designation"
                                                      validate={{
                                                        required: { value: true },
                                                      }}
                                                      value={this.state.users.designation || ""}
                                                    />
                                                  </div>
                                                  <div className="mb-3">
                                                    <AvField
                                                      name="email"
                                                      label="Email"
                                                      type="email"
                                                      errorMessage="Invalid Email"
                                                      validate={{
                                                        required: { value: true },
                                                      }}
                                                      value={this.state.users.email || ""}
                                                    />
                                                  </div>
                                                  <div className="mb-3">
                                                    <AvField type="select" name="tags" className="form-select" label="Option" helpMessage="MULTIPLE!" multiple={true} required
                                                      value={this.state.users.tags || ""}

                                                    >
                                                      <option>Photoshop</option>
                                                      <option>illustrator</option>
                                                      <option>Html</option>
                                                      <option>Php</option>
                                                      <option>Java</option>
                                                      <option>Python</option>
                                                      <option>UI/UX Designer</option>
                                                      <option>Ruby</option>
                                                      <option>Css</option>
                                                    </AvField>
                                                  </div>
                                                  <div className="mb-3">
                                                    <AvField
                                                      name="projects"
                                                      label="Projects"
                                                      type="text"
                                                      errorMessage="Invalid Projects"
                                                      validate={{
                                                        required: { value: true },
                                                      }}
                                                      value={this.state.users.projects || ""}
                                                    />
                                                  </div>
                                                </Col>

                                              </Row>
                                              <Row>
                                                <Col>
                                                  <div className="text-end">

                                                    <button
                                                      type="submit"
                                                      className="btn btn-success save-user"
                                                    >
                                                      Save
                                                    </button>
                                                  </div>
                                                </Col>
                                              </Row>
                                            </AvForm>
                                          </ModalBody>
                                        </Modal>
                                      </div>
                                    </Col>
                                  </Row>
                                  <Row className="align-items-md-center mt-30">
                                    <Col className="pagination pagination-rounded justify-content-end mb-2">
                                      <PaginationListStandalone
                                        {...paginationProps}
                                      />
                                    </Col>
                                  </Row>
                                </React.Fragment>
                              )}
                          </ToolkitProvider>
                        )}
                    </PaginationProvider>
                  </CardBody>
                </Card>
              </Col>
            </Row>
          </Container>
        </div>
      </React.Fragment>
    );
  }
}

ContactsList.propTypes = {
  users: PropTypes.array,
  className: PropTypes.any,
  onGetUsers: PropTypes.func,
  onAddNewUser: PropTypes.func,
  onDeleteUser: PropTypes.func,
  onUpdateUser: PropTypes.func,
};

const mapStateToProps = ({ contacts }) => ({
  users: contacts.users,
});

const mapDispatchToProps = dispatch => ({
  onGetUsers: () => dispatch(getUsers()),
  onAddNewUser: user => dispatch(addNewUser(user)),
  onUpdateUser: user => dispatch(updateUser(user)),
  onDeleteUser: user => dispatch(deleteUser(user)),
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withRouter(ContactsList));