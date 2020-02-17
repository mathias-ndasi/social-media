import React, { Component } from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { loginUser } from "../reducers/user/actions";
import { setLoader, resetLoader } from "../reducers/loading/actions";
import login_logo from "../images/login.png";

import "../styles/login.css";
import Loading from "../components/Loading";

class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLogin: false,
      data: {
        email: "",
        password: ""
      }
    };
  }

  handleInput = e => {
    this.setState({
      ...this.state,
      data: {
        ...this.state.data,
        [e.target.name]: e.target.value
      }
    });
  };

  handleSubmit = e => {
    e.preventDefault();
    this.props.setLoader();
    let data = this.jsonData(this.state.data);

    this.props.loginUser(data, this.props.history);
    this.refs.loginForm.reset();
    this.setState({
      ...this.state,
      data: {
        email: "",
        password: ""
      }
    });
  };

  jsonData = data => {
    return JSON.stringify(data);
  };

  componentDidMount() {
    if (this.props.isLogin) {
      this.props.history.push("/");
    }
    this.props.setLoader();
    setTimeout(() => {
      this.props.resetLoader();
    }, 1000);
  }

  render() {
    let email, password;

    if (this.props.error.email) {
      email = this.props.error.email;
    }
    if (this.props.error.password) {
      password = this.props.error.password;
    }

    // loader controller
    if (this.props.error.email || this.props.error.password) {
      setTimeout(() => {
        this.props.resetLoader();
      }, 1000);
    }

    const { message } = this.props;

    return (
      <div className="login">
        {this.props.loading ? (
          <Loading />
        ) : (
          <div className="login-content">
            {message && (
              <div className="message">
                <p>{message}</p>
              </div>
            )}
            <form action="" onSubmit={this.handleSubmit} ref="loginForm">
              <div className="login-logo">
                <img src={login_logo} alt="login_logo" />
              </div>
              <div className="input">
                <label htmlFor="email">Email</label> <br />
                <input
                  type="email"
                  name="email"
                  value={this.state.data.email}
                  placeholder="Enter email"
                  onChange={this.handleInput}
                  required
                  autoComplete="off"
                  autoFocus="True"
                />
                {email && <p className="error">{email}</p>}
              </div>
              <br />
              <div className="input">
                <label htmlFor="password">Password</label> <br />
                <input
                  type="password"
                  name="password"
                  value={this.state.data.password}
                  placeholder="Enter password"
                  onChange={this.handleInput}
                  required
                  autoComplete="off"
                />
                {password && <p className="error">{password}</p>}
              </div>
              <br />
              <div className="submit">
                <button type="submit" onSubmit={this.handleSubmit}>
                  login
                </button>
              </div>
              <br />
              <p className="below">
                Don't have an account yet? <Link to="/signup">signup</Link>
              </p>
            </form>
          </div>
        )}
      </div>
    );
  }
}

const mapStateToProps = state => {
  return state;
};

const mapDispatchToProps = dispatch => ({
  loginUser: (data, history) => {
    dispatch(loginUser(data, history));
  },
  setLoader: () => {
    dispatch(setLoader());
  },
  resetLoader: () => {
    dispatch(resetLoader());
  }
});

export default connect(mapStateToProps, mapDispatchToProps)(Login);
