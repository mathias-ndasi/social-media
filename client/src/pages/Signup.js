import React, { Component } from "react";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import { signupUser, accountConfirm } from "../reducers/user/actions";
import { setLoader, resetLoader } from "../reducers/loading/actions";
import signup_logo from "../images/login.png";

import "../styles/signup.css";
import { IoIosCloseCircle } from "react-icons/io";
import Loading from "../components/Loading";
import PopupModal from "../components/popup";
import { resetPopup } from "../reducers/popup/actions";

class Signup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLogin: false,
      popup: false,
      data: {
        username: "",
        email: "",
        password: ""
      },
      account_confirm: {
        secret_code: ""
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
    this.props.signupUser(data);

    this.refs.signupForm.reset();
    this.setState({
      ...this.state,
      data: {
        username: "",
        email: "",
        password: ""
      }
    });
  };

  handleAccountConfirmInput = e => {
    this.setState({
      ...this.state,
      account_confirm: {
        [e.target.name]: e.target.value
      }
    });
  };

  handleAccountConfirmSubmit = e => {
    e.preventDefault();
    this.props.setLoader();
    let data = JSON.stringify(this.state.account_confirm);
    this.props.accountConfirm(data, this.props.history);

    this.setState({
      ...this.state,
      account_confirm: {
        secret_code: ""
      }
    });
  };

  modalClose = () => {
    this.props.resetPopup();
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
    let username, email, password, secret_code;

    if (this.props.error.username) {
      username = this.props.error.username;
    }
    if (this.props.error.email) {
      email = this.props.error.email;
    }
    if (this.props.error.password) {
      password = this.props.error.password;
    }
    if (this.props.error.secret_code) {
      secret_code = this.props.error.secret_code;
    }

    if (this.props.popup) {
      this.props.resetLoader();
    }

    const { message, popup } = this.props;

    return (
      <div className="signup">
        <div className="signup-content">
          {message && (
            <div className="message">
              <p>{message}</p>
            </div>
          )}
          {this.props.loading ? (
            <Loading />
          ) : (
            <form action="" onSubmit={this.handleSubmit} ref="signupForm">
              <div className="signup-logo">
                <img src={signup_logo} alt="signup_logo" />
              </div>

              <div className="input">
                <label htmlFor="username">Username</label> <br />
                <input
                  type="text"
                  name="username"
                  value={this.state.data.username}
                  placeholder="Enter username"
                  onChange={this.handleInput}
                  required
                  autoComplete="off"
                />
                {username && <p className="error">{username}</p>}
              </div>
              <br />

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
                  signup
                </button>
              </div>
              <br />

              <p className="below">
                already have an account, <Link to="/login">login</Link>
              </p>
            </form>
          )}
        </div>
        {popup ? (
          <PopupModal>
            <a href="#" className="close" onClick={this.modalClose}>
              <IoIosCloseCircle />
            </a>
            <h1>Account Confirmation</h1>
            <br />
            <form onSubmit={this.handleAccountConfirmSubmit}>
              <div className="input">
                <label htmlFor="secret_code">Account Activation Code</label>{" "}
                <br />
                <input
                  type="text"
                  name="secret_code"
                  value={this.state.account_confirm.secret_code}
                  placeholder="Enter Code"
                  onChange={this.handleAccountConfirmInput}
                  required
                  autoComplete="off"
                />
                {secret_code && <p className="error">{secret_code}</p>}
              </div>
              <br />

              <div className="submit">
                <button
                  type="submit"
                  onSubmit={this.handleAccountConfirmSubmit}
                >
                  Activate
                </button>
              </div>
            </form>
          </PopupModal>
        ) : null}
      </div>
    );
  }
}

const mapStateToProps = state => {
  return state;
};

const mapDispatchToProps = dispatch => ({
  signupUser: data => {
    dispatch(signupUser(data));
  },
  accountConfirm: (data, history) => {
    dispatch(accountConfirm(data, history));
  },
  setLoader: () => {
    dispatch(setLoader());
  },
  resetLoader: () => {
    dispatch(resetLoader());
  },
  resetPopup: () => {
    dispatch(resetPopup());
  }
});

export default connect(mapStateToProps, mapDispatchToProps)(Signup);
