import React, { Component } from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import MetaTags from 'react-meta-tags';
import { withRouter } from "react-router-dom";
import { isEmpty, size } from "lodash";
import BootstrapTable from "react-bootstrap-table-next";
import
paginationFactory, {
  PaginationProvider,
  PaginationListStandalone,
} from "react-bootstrap-table2-paginator";
import ToolkitProvider, { Search } from "react-bootstrap-table2-toolkit";
import { Link } from "react-router-dom";
import * as moment from 'moment';

import { Button, Card, CardBody, Col, Container, Row, Modal, Badge, ModalHeader, ModalBody } from "reactstrap";

import { AvForm, AvField } from "availity-reactstrap-validation";

//Import Breadcrumb
import Breadcrumbs from "components/Common/Breadcrumb";
import {
  getOrders,
  addNewOrder,
  updateOrder,
  deleteOrder
} from "store/actions";

import EcommerceOrdersModal from "./EcommerceOrdersModal";

class EcommerceOrders extends Component {
  constructor(props) {
    super(props);
    this.node = React.createRef();
    this.state = {
      viewmodal: false,
      modal: false,
      orders: [],
      EcommerceOrderColumns: [
        {
          text: "id",
          dataField: "id",
          sort: true,
          hidden: true,
          formatter: (cellContent, user) => (
            <>
              {order.id}
            </>
          ),
        },
        {
          dataField: "orderId",
          text: "Order ID",
          sort: true,
          formatter: (cellContent, row) => (
            <Link to="#" className="text-body fw-bold">
              {row.orderId}
            </Link>
          ),
        },
        {
          dataField: "billingName",
          text: "Billing Name",
          sort: true,
        },
        {
          dataField: "orderdate",
          text: "Date",
          sort: true,
          formatter: (cellContent, row) => (
            this.handleValidDate(row.orderdate)
          ),
        },
        {
          dataField: "total",
          text: "Total",
          sort: true,
        },
        {
          dataField: "paymentStatus",
          text: "Payment Status",
          sort: true,
          formatter: (cellContent, row) => (
            <Badge
              className={"font-size-12 badge-soft-" + row.badgeclass}
              color={row.badgeclass}
              pill
            >
              {row.paymentStatus}
            </Badge>
          ),
        },
        {
          dataField: "paymentMethod",
          isDummyField: true,
          text: "Payment Method",
          sort: true,
          formatter: (cellContent, row) => (
            <>
              <i className={
                (row.paymentMethod !== 'COD') ?
                  'fab fa-cc-' + this.toLowerCase1(row.paymentMethod) + " me-1"
                  : 'fab fas fa-money-bill-alt me-1'
              } />{" "}
              {row.paymentMethod}
            </>
          ),
        },
        {
          dataField: "view",
          isDummyField: true,
          text: "View Details",
          sort: true,
          formatter: () => (
            <Button
              type="button"
              color="primary"
              className="btn-sm btn-rounded"
              onClick={this.toggleViewModal}
            >
              View Details
            </Button>
          ),
        },
        {
          dataField: "action",
          isDummyField: true,
          text: "Action",
          formatter: (cellContent, order) => (
            <>
              <div className="d-flex gap-3">
                <Link to="#" className="text-success">
                  <i className="mdi mdi-pencil font-size-18" id="edittooltip" onClick={() => this.handleOrderClick(order)} />
                </Link>
                <Link to="#" className="text-danger">
                  <i className="mdi mdi-delete font-size-18" id="deletetooltip" onClick={() => this.handleDeleteOrder(order)} />
                </Link>
              </div>
            </>
          ),
        },
      ]
    };

    this.handleOrderClick = this.handleOrderClick.bind(this);
    this.toggle = this.toggle.bind(this);
    this.handleValidOrderSubmit = this.handleValidOrderSubmit.bind(this);
    this.handleOrderClicks = this.handleOrderClicks.bind(this);
    this.toLowerCase1 = this.toLowerCase1.bind(this);
  }

  toLowerCase1(str) {
    return str.toLowerCase();
  }

  componentDidMount() {
    const { orders, onGetOrders } = this.props;
    if (orders && !orders.length) {
      onGetOrders();
    }
    this.setState({ orders });
  }

  // eslint-disable-next-line no-unused-vars
  componentDidUpdate(prevProps, prevState, snapshot) {
    const { orders } = this.props;
    if (!isEmpty(orders) && size(prevProps.orders) !== size(orders)) {
      this.setState({ orders: {}, isEdit: false });
    }
  }

  toggle() {
    this.setState(prevState => ({
      modal: !prevState.modal,
    }));
  }

  handleOrderClicks = () => {
    this.setState({ orders: '', isEdit: false });
    this.toggle();
  };

  // eslint-disable-next-line no-unused-vars
  handleTableChange = (type, { page, searchText }) => {
    const { orders } = this.props;
    this.setState({
      orders: orders.filter(order =>
        Object.keys(order).some(
          key =>
            typeof order[key] === "string" &&
            order[key].toLowerCase().includes(searchText.toLowerCase())
        )
      ),
    });
  };

  toggleViewModal = () => {
    this.setState(prevState => ({
      viewmodal: !prevState.viewmodal,
    }));
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

  handleDeleteOrder = (order) => {
    const { onDeleteOrder } = this.props;
    if (order.id !== undefined) {
      onDeleteOrder(order);
      this.onPaginationPageChange(1);
    }
  };

  handleOrderClick = arg => {
    const order = arg;

    this.setState({
      orders: {
        id: order.id,
        orderId: order.orderId,
        billingName: order.billingName,
        orderdate: order.orderdate,
        total: order.total,
        paymentStatus: order.paymentStatus,
        paymentMethod: order.paymentMethod,
        badgeclass: order.badgeclass
      },
      isEdit: true,
    });

    this.toggle();
  };

  /**
   * Handling submit Order on Order form
   */
  handleValidOrderSubmit = (e, values) => {
    const { onAddNewOrder, onUpdateOrder } = this.props;
    const { isEdit, orders, selectedOrder } = this.state;

    if (isEdit) {
      const updateOrder = {
        id: orders.id,
        orderId: values.orderId,
        billingName: values.billingName,
        orderdate: values.orderdate,
        total: values.total,
        paymentStatus: values.paymentStatus,
        paymentMethod: values.paymentMethod,
        badgeclass: values.badgeclass
      };

      // update Order
      onUpdateOrder(updateOrder);
    } else {

      const newOrder = {
        id: Math.floor(Math.random() * (30 - 20)) + 20,
        orderId: values["orderId"],
        billingName: values["billingName"],
        orderdate: values["orderdate"],
        total: values["total"],
        paymentStatus: values["paymentStatus"],
        paymentMethod: values["paymentMethod"],
        badgeclass: values['badgeclass']
      };
      // save new Order
      onAddNewOrder(newOrder);
    }
    this.setState({ selectedOrder: null });
    this.toggle();
  };

  handleValidDate = (date) => {
    const date1 = moment(new Date(date)).format('DD MMM Y');
    return date1;
  };

  render() {
    const { orders } = this.props;

    const { SearchBar } = Search;

    const { isEdit } = this.state;

    //pagination customization
    const pageOptions = {
      sizePerPage: 10,
      totalSize: orders.length, // replace later with size(Order),
      custom: true,
    };

    const defaultSorted = [{
      dataField: 'orderId',
      order: 'desc'
    }];

    const selectRow = {
      mode: 'checkbox',
    };

    return (
      <React.Fragment>
        <EcommerceOrdersModal
          isOpen={this.state.viewmodal}
          toggle={this.toggleViewModal}
        />
        <div className="page-content">
          <MetaTags>
            <title>Orders | Skote - React Admin & Dashboard Template</title>
          </MetaTags>
          <Container fluid>
            <Breadcrumbs title="Ecommerce" breadcrumbItem="Orders" />
            <Row>
              <Col xs="12">
                <Card>
                  <CardBody>
                    <PaginationProvider
                      pagination={paginationFactory((pageOptions || []))}
                      keyField='id'
                      columns={(this.state.EcommerceOrderColumns || [])}
                      data={(orders || [])}
                    >
                      {({ paginationProps, paginationTableProps }) => (
                        <ToolkitProvider
                          keyField="id"
                          data={orders}
                          columns={(this.state.EcommerceOrderColumns || [])}
                          bootstrap4
                          search
                        >
                          {toolkitProps => (
                            <React.Fragment>
                              <Row className="mb-2">
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
                                      onClick={this.handleOrderClicks}
                                    >
                                      <i className="mdi mdi-plus me-1" />{" "}
                                      Add New Order
                                    </Button>
                                  </div>
                                </Col>
                              </Row>
                              <div className="table-responsive">
                                <BootstrapTable
                                  {...toolkitProps.baseProps}
                                  {...paginationTableProps}
                                  responsive
                                  defaultSorted={defaultSorted}
                                  bordered={false}
                                  striped={false}
                                  selectRow={selectRow}
                                  classes={
                                    "table align-middle table-nowrap table-check"
                                  }
                                  headerWrapperClasses={"table-light"}
                                  ref={this.node}
                                />
                                <Modal
                                  isOpen={this.state.modal}
                                  className={this.props.className}
                                >
                                  <ModalHeader toggle={this.toggle} tag="h4">
                                    {!!isEdit ? "Edit Order" : "Add Order"}
                                  </ModalHeader>
                                  <ModalBody>
                                    <AvForm
                                      onValidSubmit={
                                        this.handleValidOrderSubmit
                                      }
                                    >
                                      <Row form>
                                        <Col className="col-12">

                                          <div className="mb-3">
                                            <AvField
                                              name="orderId"
                                              label="Order Id"
                                              type="text"
                                              errorMessage="Invalid orderId"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={this.state.orders.orderId || ""
                                              }
                                            />
                                          </div>
                                          <div className="mb-3">
                                            <AvField
                                              name="billingName"
                                              label="Billing Name"
                                              type="text"
                                              errorMessage="Invalid Billing Name"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={this.state.orders.billingName || ""}
                                            />
                                          </div>
                                          <div className="mb-3">
                                            <AvField
                                              name="orderdate"
                                              label="Date"
                                              type="date"
                                              errorMessage="Invalid Date"
                                              validate={{
                                                required: { value: true },
                                              }}

                                              value={this.state.orders.orderdate || ""}
                                            />
                                          </div>
                                          <div className="mb-3">
                                            <AvField
                                              name="total"
                                              label="Total"
                                              type="text"
                                              errorMessage="Invalid Total"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={this.state.orders.total || ""}
                                            />
                                          </div>
                                          <div className="mb-3">
                                            <AvField
                                              name="paymentStatus"
                                              label="Payment Status"
                                              type="select"
                                              id="status1"
                                              className="form-select"
                                              errorMessage="Invalid Payment Status"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={this.state.orders.paymentStatus || "Paid"}
                                            >
                                              <option>Paid</option>
                                              <option>Chargeback</option>
                                              <option>Refund</option>
                                            </AvField>
                                          </div>
                                          <div className="mb-3">
                                            <AvField
                                              name="badgeclass"
                                              label="Badge Class"
                                              type="select"
                                              className="form-select"
                                              errorMessage="Invalid Badge Class"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={this.state.orders.badgeclass || "success"}
                                            >
                                              <option>success</option>
                                              <option>danger</option>
                                              <option>warning</option>
                                            </AvField>
                                          </div>
                                          <div className="mb-3">
                                            <AvField
                                              name="paymentMethod"
                                              label="Payment Method"
                                              type="select"
                                              className="form-select"
                                              errorMessage="Invalid Payment Method"
                                              validate={{
                                                required: { value: true },
                                              }}
                                              value={this.state.orders.paymentMethod || "Mastercard"}
                                            >
                                              <option>Mastercard</option>
                                              <option>Visa</option>
                                              <option>Paypal</option>
                                              <option>COD</option>
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

EcommerceOrders.propTypes = {
  orders: PropTypes.array,
  onGetOrders: PropTypes.func,
  onAddNewOrder: PropTypes.func,
  onDeleteOrder: PropTypes.func,
  onUpdateOrder: PropTypes.func,
  className: PropTypes.any
};

const mapStateToProps = state => ({
  orders: state.ecommerce.orders,
});

const mapDispatchToProps = dispatch => ({
  onGetOrders: () => dispatch(getOrders()),
  onAddNewOrder: order => dispatch(addNewOrder(order)),
  onUpdateOrder: order => dispatch(updateOrder(order)),
  onDeleteOrder: order => dispatch(deleteOrder(order)),
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withRouter(EcommerceOrders));