import React, { Component } from "react"
import MetaTags from 'react-meta-tags';
import { Col, Container, Row, Button, Card, CardBody, CardTitle } from "reactstrap"

import ReactDrawer from 'react-drawer';
import 'react-drawer/lib/react-drawer.css';

//Import Breadcrumb
import Breadcrumbs from "../../components/Common/Breadcrumb"

class UiDrawer extends Component {
    constructor(props) {
        super(props)
        this.state = {
            open: false,
            position: 'right',
        };

        this.toggleTopDrawer = this.toggleTopDrawer.bind(this);
        this.toggleBottomDrawer = this.toggleBottomDrawer.bind(this);
        this.toggleLeftDrawer = this.toggleLeftDrawer.bind(this);
        this.toggleRightDrawer = this.toggleRightDrawer.bind(this);
        this.closeDrawer = this.closeDrawer.bind(this);
        this.onDrawerClose = this.onDrawerClose.bind(this);
        this.setPosition = this.setPosition.bind(this);
    }

    setPosition(e) {
        this.setState({ position: e.target.value });
    }

    toggleTopDrawer() {
        this.setState({ position: 'top' });
        this.setState({ open: !this.state.open });
    }
    toggleBottomDrawer() {
        this.setState({ position: 'bottom' });
        this.setState({ open: !this.state.open });
    }
    toggleLeftDrawer() {
        this.setState({ position: 'left' });
        this.setState({ open: !this.state.open });
    }
    toggleRightDrawer() {
        this.setState({ position: 'right' });
        this.setState({ open: !this.state.open });
    }
    closeDrawer() {
        this.setState({ open: false });
    }
    onDrawerClose() {
        this.setState({ open: false });
    }

    render() {
        return (
            <React.Fragment>
                <div className="page-content">
                    <MetaTags>
                        <title>Drawer | Skote - React Admin & Dashboard Template</title>
                    </MetaTags>
                    <Container fluid={true}>
                        <Breadcrumbs title="UI Elements" breadcrumbItem="Drawer" />
                        <Row>
                            <Col>
                                <Card>
                                    <CardBody>
                                        <CardTitle className="h4">Drawer</CardTitle>
                                        <p className="card-title-desc">
                                            Navigation drawers can toggle open or closed. Closed by default,
                                            the drawer opens temporarily above all other content until a section is selected.
                                        </p>
                                        <Button
                                            color="primary"
                                            onClick={this.toggleTopDrawer} disabled={this.state.open}
                                        >
                                            Top
                                        </Button>{" "}
                                        <Button
                                            color="primary"
                                            onClick={this.toggleBottomDrawer} disabled={this.state.open}
                                        >
                                            Bottom
                                        </Button>{" "}
                                        <Button
                                            color="primary"
                                            onClick={this.toggleLeftDrawer} disabled={this.state.open}
                                        >
                                            Left
                                        </Button>{" "}
                                        <Button
                                            color="primary"
                                            onClick={this.toggleRightDrawer} disabled={this.state.open}
                                        >
                                            Right
                                        </Button>{" "}
                                    </CardBody>
                                </Card>
                            </Col>
                        </Row>

                        <ReactDrawer
                            open={this.state.open}
                            className="drawer-open"
                            position={this.state.position}
                            onClose={this.onDrawerClose}>
                            <ul className="drawer-main-menu list-unstyled">
                                <li className="drawer-menu">
                                    <a href="#">
                                        <i className="bx bx-home-circle"></i><span>Dashboards</span>
                                    </a>
                                </li>
                                <li className="drawer-menu"><a href="#">
                                    <i className="bx bx-calendar"></i><span>Calendar</span></a>
                                </li>
                                <li className="drawer-menu"><a href="#">
                                    <i className="bx bx-chat"></i><span>Chat</span></a>
                                </li>
                                <li className="drawer-menu">
                                    <a href="#">
                                        <i className="bx bx-file"></i><span>File Manager</span>
                                    </a>
                                </li>
                                <li className="drawer-menu">
                                    <a href="#">
                                        <i className="bx bx-store"></i><span>Ecommerce</span>
                                    </a>
                                </li>
                            </ul>
                        </ReactDrawer>

                    </Container>
                </div>
            </React.Fragment>
        )
    }
}

export default UiDrawer