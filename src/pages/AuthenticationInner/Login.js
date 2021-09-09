import React, { useEffect, useState } from "react";
import MetaTags from "react-meta-tags";
import axios from "axios";
import {useHistory} from "react-router-dom";
// Redux
import { Link } from "react-router-dom";

import { Card, CardBody, Col, Container, Row } from "reactstrap";

// availity-reactstrap-validation
import { AvField, AvForm } from "availity-reactstrap-validation";


const AuthenticateAPI = axios.create({
  baseURL: "http://213.139.209.59:8250/api/Authenticate"
})

// import images

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const history = useHistory()

  const handlePasswordChange = (e) => setPassword(e.target.value);
  const handleUsernameChange = (e) => setUsername(e.target.value);

  function handleSubmit() {
    const formData = { username, password}

    AuthenticateAPI.post("/login/", formData)
      .then(res => {
        console.log(res.data.auth_token)
        history.push("/")
      })
      .catch(err => console.log(err))
  }

  return (
    <React.Fragment>
      <MetaTags>
        <title>Login</title>
      </MetaTags>
      <div className="home-btn d-none d-sm-block">
        <Link to="/" className="text-dark">
          <i className="bx bx-home h2" />
        </Link>
      </div>
      <div className="account-pages my-5 pt-sm-5">
        <Container>
          <Row className="justify-content-center align-items-middle">
            <Col md={8} lg={6} xl={5}>
              <Card className="overflow-hidden">
                <div className="bg-primary bg-soft">
                  <div className="text-primary p-4">
                    <h5 className="text-primary">Welcome!</h5>
                    <p>Sign in to continue to Sanri.</p>
                  </div>
                </div>
                <CardBody className="pt-15">
                  <div className="p-2">
                    <AvForm className="form-horizontal" onSubmit={handleSubmit}>
                      <div className="mb-3">
                        <AvField
                          name="username"
                          label="Username"
                          value=""
                          className="form-control"
                          placeholder="Enter username"
                          type="text"
                          required
                          onInput={handleUsernameChange}
                        />
                      </div>

                      <div className="mb-3">
                        <AvField
                          name="password"
                          label="Password"
                          value=""
                          type="password"
                          required
                          placeholder="Enter password"
                          onInput={handlePasswordChange}
                        />
                      </div>

                      <div className="form-check">
                        <input
                          type="checkbox"
                          className="form-check-input"
                          id="customControlInline"
                        />
                        <label
                          className="form-check-label"
                          htmlFor="customControlInline"
                        >
                          Remember me
                        </label>
                      </div>

                      <div className="mt-3 d-grid">
                        <button
                          className="btn btn-primary btn-block"
                          type="submit"
                        >
                          Log In
                        </button>
                      </div>

                      <div className="mt-4 text-center">
                        <h5 className="font-size-14 mb-3">Sign in with</h5>

                        <ul className="list-inline">
                          <li className="list-inline-item">
                            <Link
                              to="#"
                              className="social-list-item bg-primary text-white border-primary"
                            >
                              <i className="mdi mdi-facebook" />
                            </Link>
                          </li>
                          {" "}
                          <li className="list-inline-item">
                            <Link
                              to="#"
                              className="social-list-item bg-info text-white border-info"
                            >
                              <i className="mdi mdi-twitter" />
                            </Link>
                          </li>
                          {" "}
                          <li className="list-inline-item">
                            <Link
                              to="#"
                              className="social-list-item bg-danger text-white border-danger"
                            >
                              <i className="mdi mdi-google" />
                            </Link>
                          </li>
                        </ul>
                      </div>

                      <div className="mt-4 text-center">
                        <Link to="/pages-forgot-pwd" className="text-muted">
                          <i className="mdi mdi-lock me-1" /> Forgot your
                          password?
                        </Link>
                      </div>
                    </AvForm>
                  </div>
                </CardBody>
              </Card>
              <div className=" text-center">
                {/*<p>*/}
                {/*  Don&apos;t have an account ?{" "}*/}
                {/*  <Link*/}
                {/*    to="pages-register"*/}
                {/*    className="fw-medium text-primary"*/}
                {/*  >*/}
                {/*    {" "}*/}
                {/*    Signup now{" "}*/}
                {/*  </Link>{" "}*/}
                {/*</p>*/}
                <p>
                  © {new Date().getFullYear()} Sanri
                </p>
              </div>
            </Col>
          </Row>
        </Container>
      </div>
    </React.Fragment>
  );
}

export default Login;
