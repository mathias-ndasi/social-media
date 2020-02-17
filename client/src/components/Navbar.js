import React, { Component } from "react";
import { Link } from "react-router-dom";
import logo from "../images/twitter-512.png";
import "../styles/Navbar.css";
import { connect } from "react-redux";

import {
  IoIosAdd,
  IoIosNotifications,
  IoMdMenu,
  IoIosCloseCircle
} from "react-icons/io";
import SideNav from "./SideNav";
import { setPopup, resetPopup } from "../reducers/popup/actions";
import { resetLoader, setLoader } from "../reducers/loading/actions";
import PopupModal from "./popup";
import { createPost } from "../reducers/post/actions";
import Loading from "./Loading";

class Navbar extends Component {
  constructor(props) {
    super(props);

    this.state = {
      data: {
        body: ""
      }
    };
  }

  slider = e => {
    let icon = document.querySelector("#slider");
    let main_nav = document.querySelector(".navbar");
    let side_nav = document.querySelector(".side-nav");

    if (icon.classList.contains("anim")) {
      icon.classList.remove("anim");
    } else {
      icon.classList.add("anim");
    }

    if (main_nav.classList.contains("push")) {
      main_nav.classList.remove("push", "fix");
      side_nav.classList.remove("show");
      icon.querySelector("a").innerHTML = `
      <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 512 512" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M64 384h384v-42.666H64V384zm0-106.666h384v-42.667H64v42.667zM64 128v42.665h384V128H64z"></path></svg>
      `;
    } else {
      icon.querySelector("a").innerHTML = `
      <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 512 512" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M278.6 256l68.2-68.2c6.2-6.2 6.2-16.4 0-22.6-6.2-6.2-16.4-6.2-22.6 0L256 233.4l-68.2-68.2c-6.2-6.2-16.4-6.2-22.6 0-3.1 3.1-4.7 7.2-4.7 11.3 0 4.1 1.6 8.2 4.7 11.3l68.2 68.2-68.2 68.2c-3.1 3.1-4.7 7.2-4.7 11.3 0 4.1 1.6 8.2 4.7 11.3 6.2 6.2 16.4 6.2 22.6 0l68.2-68.2 68.2 68.2c6.2 6.2 16.4 6.2 22.6 0 6.2-6.2 6.2-16.4 0-22.6L278.6 256z"></path></svg>
      `;
      main_nav.classList.add("push", "fix");
      // main_nav.cla
      side_nav.classList.add("show");
    }
  };

  fixNav = e => {
    let main_nav = document.querySelector(".navbar");

    if (main_nav.classList.contains("push")) {
      main_nav.classList.remove("push");
    }
  };

  modalClose = () => {
    this.props.resetPopup();
  };

  newPost = () => {
    this.props.setPopup();
  };

  handleInput = e => {
    this.setState({
      ...this.state,
      data: {
        [e.target.name]: e.target.value
      }
    });
  };

  handleSubmit = e => {
    e.preventDefault();
    this.props.setLoader();

    let data = this.jsonData();

    this.props.createPost(data, this.props.token);
    this.refs.createPostForm.reset();
    this.setState({
      ...this.state,
      data: {
        body: ""
      }
    });
  };

  jsonData = () => {
    let data = this.state.data;
    data["user_id"] = this.props.user.data.id;
    return JSON.stringify(data);
  };

  render() {
    const { isLogin, loading, popup } = this.props;

    let body;

    if (this.props.error.body) {
      body = this.props.error.body;
      setTimeout(() => {
        this.props.resetLoader();
      }, 1000);
    }

    const navLinks = isLogin ? (
      <>
        <li>
          <a href="#" className="icon-anim" onClick={this.newPost}>
            <IoIosAdd />
          </a>
        </li>
        <li>
          <a href="#" className="icon-anim notification">
            <span className="notification-count">6</span>
            <IoIosNotifications />
          </a>
        </li>
        <li id="slider">
          <a href="#" className="icon-anim" onClick={this.slider}>
            <IoMdMenu />
          </a>
        </li>
      </>
    ) : (
      <>
        <li>
          <Link to="/login" className="link">
            login
          </Link>
        </li>
        <li>
          <Link to="/signup" className="link">
            signup
          </Link>
        </li>
      </>
    );

    return (
      <>
        <nav className="navbar">
          <ul>
            <li>
              <div className="logo">
                <Link to="/">
                  <img src={logo} alt="logo" />
                </Link>
              </div>
            </li>
          </ul>
          <ul>{navLinks}</ul>
        </nav>
        {isLogin && <SideNav slider={this.slider} fixNav={this.fixNav} />}

        {popup ? (
          <>
            {loading ? (
              <Loading />
            ) : (
              <PopupModal style={{ border: "red" }}>
                <a href="#" className="close" onClick={this.modalClose}>
                  <IoIosCloseCircle />
                </a>
                <h1>Create New Post</h1>
                <br />

                <form
                  onSubmit={this.handleSubmit}
                  ref="createPostForm"
                  className="new-post"
                >
                  <div className="textarea-input">
                    <label htmlFor="post">New Post</label>
                    <br />
                    <textarea
                      name="body"
                      value={this.state.data.body}
                      placeholder="Create new post"
                      onChange={this.handleInput}
                      // required
                      autoComplete="off"
                    ></textarea>
                    {body && <p className="error">{body}</p>}
                  </div>
                  <br />

                  <div className="submit">
                    <button type="submit" onSubmit={this.handleSubmit}>
                      Create Post
                    </button>
                  </div>
                </form>
              </PopupModal>
            )}
          </>
        ) : null}
      </>
    );
  }
}

const mapStateToProps = state => {
  return state;
};

const mapDispatchToProps = dispatch => ({
  setLoader: () => {
    dispatch(setLoader());
  },
  resetLoader: () => {
    dispatch(resetLoader());
  },
  setPopup: () => {
    dispatch(setPopup());
  },
  resetPopup: () => {
    dispatch(resetPopup());
  },
  createPost: (data, token) => {
    dispatch(createPost(data, token));
  }
});

export default connect(mapStateToProps, mapDispatchToProps)(Navbar);
