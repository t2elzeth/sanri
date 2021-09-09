import React, { Component } from "react"
import PropTypes from 'prop-types';
import MetaTags from 'react-meta-tags'
import { Link } from "react-router-dom"
import { Col, Container, Row, Button, Alert } from "reactstrap"

// availity-reactstrap-validation
import { AvField, AvForm } from "availity-reactstrap-validation"

//import images
import logodark from "../../assets/images/logo-dark.png"
import logolight from "../../assets/images/logo-light.png"
import CarouselPage from "./CarouselPage"

export default class Recoverpw2 extends Component {
  render() {
    return (
      <React.Fragment>
        <div>
          <MetaTags>
            <title>Recover Password 2 | Skote - React Admin & Dashboard Template</title>
          </MetaTags>
          <Container fluid className="p-0">
            <Row className="g-0">
              <CarouselPage />

              <Col xl={3}>
                <div className="auth-full-page-content p-md-5 p-4">
                  <div className="w-100">
                    <div className="d-flex flex-column h-100">
                      <div className="mb-4 mb-md-5">
                        <a href="/" className="d-block auth-logo">
                          <img
                            src={logodark}
                            alt=""
                            height="18"
                            className="auth-logo-dark"
                          />
                          <img
                            src={logolight}
                            alt=""
                            height="18"
                            className="auth-logo-light"
                          />
                        </a>
                      </div>
                      <div className="my-auto">
                        <div>
                          <h5 className="text-primary"> Reset Password</h5>
                          <p className="text-muted">Re-Password with Skote.</p>
                        </div>

                        <div className="mt-4">
                          <div
                            className="alert alert-success text-center mb-4"
                            role="alert"
                          >
                            Enter your Email and instructions will be sent to
                            you!
                          </div>
                          <AvForm className="form-horizontal">
                            {this.props.error && this.props.error ? (
                              <Alert color="danger">{this.props.error}</Alert>
                            ) : null}

                            <div className="mb-3">
                              <AvField name="email"
                                label="Email"
                                value=""
                                className="form-control"
                                placeholder="Enter Email"
                                type="text"
                                required
                              />
                            </div>
                            <div className="text-end">
                              <Button className="btn btn-primary w-md" color="primary" type="submit">
                                Reset
                              </Button>
                            </div>
                          </AvForm>
                          <div className="mt-5 text-center">
                            <p>
                              Remember It ?{" "}
                              <Link
                                to="pages-login-2"
                                className="fw-medium text-primary"
                              >
                                {" "}
                                Sign In here
                              </Link>{" "}
                            </p>
                          </div>
                        </div>
                      </div>

                      <div className="mt-4 mt-md-5 text-center">
                        <p className="mb-0">
                          © {new Date().getFullYear()} Skote. Crafted with{" "}
                          <i className="mdi mdi-heart text-danger"></i> by
                          Themesbrand
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </Col>
            </Row>
          </Container>
        </div>
      </React.Fragment>
    )
  }
}


Recoverpw2.propTypes = {
  error: PropTypes.any,
}

