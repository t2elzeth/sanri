import React, { Component } from "react";
import PropTypes from "prop-types";
import MetaTags from 'react-meta-tags';
import { connect } from "react-redux";
import { isEmpty, size } from "lodash";
import { Button, Card, CardBody, Col, Container, Row, Badge, UncontrolledDropdown, DropdownToggle, DropdownMenu, DropdownItem, Modal, ModalBody, ModalHeader } from "reactstrap";
import ToolkitProvider, { Search } from "react-bootstrap-table2-toolkit";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, {
  PaginationListStandalone,
  PaginationProvider,
} from "react-bootstrap-table2-paginator";
import * as moment from 'moment';

//Import Breadcrumb
import Breadcrumbs from "components/Common/Breadcrumb";
import { AvForm, AvField } from "availity-reactstrap-validation";

import {
  getCustomers,
  addNewCustomer,
  updateCustomer,
  deleteCustomer
} from "store/e-commerce/actions";

class EcommerceCustomers extends Component {
  constructor(props) {
    super(props);
    this.node = React.createRef();
    this.state = {
      customers: [],
      EcommerceCustomerColumns: [
        {
          text: "id",
          dataField: "id",
          sort: true,
          hidden: true,
          formatter: (cellContent, user) => (
            <>
              {row.id}
            </>
          ),
        },
        {
          dataField: "username",
          text: "Username",
          sort: true,
        },
        {
          text: "Phone / Email",
          dataField: "phone",
          sort: true,
          formatter: (cellContent, row) => (
            <>
              <p className="mb-1">{row.phone}</p>
              <p className="mb-0">{row.email}</p>
            </>
          ),
        },
        {
          dataField: "address",
          text: "Address",
          sort: true,
        },
        {
          dataField: "rating",
          text: "Rating",
          sort: true,
          formatter: (cellContent, row) => (
            <Badge color="success" className="bg-success font-size-12">
              <i className="mdi mdi-star me-1" />
              {row.rating}
            </Badge>
          ),
        },
        {
          dataField: "walletBalance",
          text: "Wallet Balance",
          sort: true,
        },
        {
          dataField: "joiningDate",
          text: "Joining Date",
          sort: true,
          formatter: (cellContent, row) => (
            this.handleValidDate(row.joiningDate)
          ),
        },
        {
          dataField: "menu",
          isDummyField: true,
          text: "Action",
          formatter: (cellContent, customer) => (
            <UncontrolledDropdown>
              <DropdownToggle href="#" className="card-drop" tag="a">
                <i className="mdi mdi-dots-horizontal font-size-18" />
              </DropdownToggle>
              <DropdownMenu className="dropdown-menu-end">
                <DropdownItem href="#" onClick={() => this.handleCustomerClick(customer)}>
                  <i className="mdi mdi-pencil font-size-16 text-success me-1" />{" "}
                  Edit
                </DropdownItem>
                <DropdownItem href="#" onClick={() => this.handleDeleteCustomer(customer)}>
                  <i className="mdi mdi-trash-can font-size-16 text-danger me-1" />{" "}
                  Delete
                </DropdownItem>
              </DropdownMenu>
            </UncontrolledDropdown>
          ),
        },
      ]
    };
    this.handleCustomerClick = this.handleCustomerClick.bind(this);
    this.toggle = this.toggle.bind(this);
    this.handleValidCustomerSubmit = this.handleValidCustomerSubmit.bind(this);
    this.handleCustomerClicks = this.handleCustomerClicks.bind(this);
  }

  componentDidMount() {
    const { customers, onGetCustomers } = this.props;
    if (customers && !customers.length) {
      onGetCustomers();
    }
    this.setState({ customers });
  }

  // eslint-disable-next-line no-unused-vars
  componentDidUpdate(prevProps, prevState, snapshot) {
    const { customers } = this.props;
    if (!isEmpty(customers) && size(prevProps.customers) !== size(customers)) {
      this.setState({ customers: {}, isEdit: false });
    }
  }

  toggle() {
    this.setState(prevState => ({
      modal: !prevState.modal,
    }));
  }

  handleCustomerClicks = arg => {
    this.setState({ selectedCustomer: arg });
    this.toggle();
  };

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

  handleDeleteCustomer = (customer) => {
    const { onDeleteCustomer } = this.props;
    if (customer.id !== undefined) {
      onDeleteCustomer(customer);
      this.onPaginationPageChange(1);
    }
  };

  handleCustomerClick = arg => {
    const customer = arg;

    this.setState({
      customers: {
        id: customer.id,
        username: customer.username,
        phone: customer.phone,
        email: customer.email,
        address: customer.address,
        rating: customer.rating,
        walletBalance: customer.walletBalance,
        joiningDate: customer.joiningDate,
      },
      isEdit: true,
    });

    this.toggle();
  };

  /**
   * Handling submit Customer on Customer form
   */
  handleValidCustomerSubmit = (e, values) => {
    const { onAddNewCustomer, onUpdateCustomer } = this.props;
    const { isEdit, customers, selectedCustomer } = this.state;

    if (isEdit) {
      const updateCustomer = {
        id: customers.id,
        username: values.username,
        phone: values.phone,
        email: values.email,
        address: values.address,
        rating: values.rating,
        walletBalance: values.walletBalance,
        joiningDate: values.joiningDate,
      };

      // update Customer
      onUpdateCustomer(updateCustomer);
    } else {

      const newCustomer = {
        id: Math.floor(Math.random() * (30 - 20)) + 20,
        username: values["username"],
        phone: values["phone"],
        email: values["email"],
        address: values["address"],
        rating: values["rating"],
        walletBalance: values["walletBalance"],
        joiningDate: values["joiningDate"],
      };
      // save new Customer
      onAddNewCustomer(newCustomer);
    }
    this.setState({ selectedCustomer: null });
    this.toggle();
  };

  handleValidDate = (date) => {
    const date1 = moment(new Date(date)).format('DD MMM Y');
    return date1;
  };


  /* Insert,Update Delete data */

  render() {

    const { customers } = this.props;

    const { isEdit } = this.state;

    //pagination customization
    const pageOptions = {
      sizePerPage: 10,
      totalSize: customers.length, // replace later with size(customers),
      custom: true,
    };

    const defaultSorted = [{
      dataField: 'id',
      order: 'desc'
    }];

    const { SearchBar } = Search;

    const selectRow = {
      mode: 'checkbox'
    };

    return (
      <React.Fragment>
        <div className="page-content">
          <MetaTags>
            <title>Customers | Skote - React Admin & Dashboard Template</title>
          </MetaTags>
          <Container fluid>
            <Breadcrumbs title="Ecommerce" breadcrumbItem="Customers" />
            <Row>
              <Col xs="12">
                <Card>
                  <CardBody>
                    <PaginationProvider
                      pagination={paginationFactory(pageOptions)}
                      keyField='id'
                      columns={this.state.EcommerceCustomerColumns}
                      data={customers}
                    >
                      {({ paginationProps, paginationTableProps }) => (
                        <ToolkitProvider
                          keyField='id'
                          columns={this.state.EcommerceCustomerColumns}
                          data={customers}
                          search
                        >
                          {toolkitProps => (
                            <React.Fragment>
                              <Row>
                                <Col sm="4">
                                  <div className="search-box me-2 mb-2 d-inline-block">
                                    <div className="position-relative">
                                      <SearchBar
                                        {...toolkitProps.searchProps}
                                      />
                                      <i className="bx bx-search-alt search-icon" />
                                    </div>
                                  </div>
                                </Col>
                                <Col sm="8">
                                  <div className="text-sm-end">
                                    <Button
                                      type="button"
                                      color="success"
                                      className="btn-rounded mb-2 me-2"
                                      onClick={this.handleCustomerClicks}
                                    >
                                      <i className="mdi mdi-plus me-1" />{" "}
                                      New Customers
                                    </Button>
                                  </div>
                                </Col>
                              </Row>

                              <div className="table-responsive">
                                <BootstrapTable
                                  keyField={"id"}
                                  responsive
                                  bordered={false}
                                  striped={false}
                                  defaultSorted={defaultSorted}
                                  selectRow={selectRow}
                                  classes={
                                    "table align-middle table-nowrap"
                                  }
                                  headerWrapperClasses={"thead-light"}
                                  {...toolkitProps.baseProps}
                                  {...paginationTableProps}
                                  ref={this.node}
                                />

                                <Modal
                                  isOpen={this.state.modal}
                                  className={this.props.className}
                                >
                                  <ModalHeader toggle={this.toggle} tag="h4">
                                    {!!isEdit ? "Edit Customer" : "Add Customer"}
                                  </ModalHeader>
                                  <ModalBody>
                                    <AvForm
                                      onValidSubmit={
                                        this.handleValidCustomerSubmit
                                      }
                                    >
                                      <Row form>
                                        <Col className="col-12">

                                          <div className="mb-3">
                                            <AvField
                                              name="username"
                                              label="User Name"
                                              type="text"
                                              errorMessage="Invalid user name"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={
                                                this.state.customers
                                                  ? this.state.customers.username
                                                  : ""
                                              }
                                            />
                                          </div>

                                          <div className="mb-3">
                                            <AvField
                                              name="phone"
                                              label="Phone No"
                                              type="text"
                                              errorMessage="Invalid Phone no"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={
                                                this.state.customers
                                                  ? this.state.customers.phone
                                                  : ""
                                              }
                                            />
                                          </div>

                                          <div className="mb-3">
                                            <AvField
                                              name="email"
                                              label="Email Id"
                                              type="email"
                                              errorMessage="Invalid Email"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={
                                                this.state.customers
                                                  ? this.state.customers.email
                                                  : ""
                                              }
                                            />
                                          </div>

                                          <div className="mb-3">
                                            <AvField
                                              name="address"
                                              label="Address"
                                              type="textarea"
                                              errorMessage="Invalid Address"
                                              rows="3"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={
                                                this.state.customers
                                                  ? this.state.customers.address
                                                  : ""
                                              }
                                            />
                                          </div>

                                          <div className="mb-3">
                                            <AvField
                                              name="rating"
                                              label="Rating"
                                              type="text"
                                              errorMessage="Invalid Rating"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={
                                                this.state.customers
                                                  ? this.state.customers.rating
                                                  : ""
                                              }
                                            />
                                          </div>

                                          <div className="mb-3">
                                            <AvField
                                              name="walletBalance"
                                              label="Wallet Balance"
                                              type="text"
                                              errorMessage="Invalid Wallet Balance"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={
                                                this.state.customers
                                                  ? this.state.customers.walletBalance
                                                  : ""
                                              }
                                            />
                                          </div>

                                          <div className="mb-3">
                                            <AvField
                                              name="joiningDate"
                                              htmlFor="joiningDate"
                                              label="Joining Date"
                                              type="date"
                                              errorMessage="Invalid Joining Date"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={
                                                this.state.customers
                                                  ? this.state.customers.joiningDate
                                                  : ""
                                              }
                                            />
                                          </div>

                                        </Col>
                                      </Row>
                                      <Row>
                                        <Col>
                                          <div className="text-end">

                                            <button
                                              type="submit"
                                              className="btn btn-success save-customer"
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
                              <div className="pagination pagination-rounded justify-content-end mb-2">
                                <PaginationListStandalone
                                  {...paginationProps}
                                />
                              </div>
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

EcommerceCustomers.propTypes = {
  customers: PropTypes.array,
  onGetCustomers: PropTypes.func,
  onAddNewCustomer: PropTypes.func,
  onDeleteCustomer: PropTypes.func,
  onUpdateCustomer: PropTypes.func,
  className: PropTypes.any
};

const mapStateToProps = ({ ecommerce }) => ({
  customers: ecommerce.customers,
});

const mapDispatchToProps = dispatch => ({
  onGetCustomers: () => dispatch(getCustomers()),
  onAddNewCustomer: customer => dispatch(addNewCustomer(customer)),
  onUpdateCustomer: customer => dispatch(updateCustomer(customer)),
  onDeleteCustomer: customer => dispatch(deleteCustomer(customer)),
});

export default connect(mapStateToProps, mapDispatchToProps)(EcommerceCustomers);