import React, { Component } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import {
  logoutUser,
  updateProfile,
  updateProfileBio
} from "../reducers/user/actions";

import {
  IoMdPin,
  IoMdCreate,
  IoIosUndo,
  IoIosCalendar,
  IoMdLink,
  IoIosCloseCircle
} from "react-icons/io";
import PopupModal from "./popup";
import { resetPopup, setPopup } from "../reducers/popup/actions";
import { resetLoader, setLoader } from "../reducers/loading/actions";
import Loading from "./Loading";

class SideNav extends Component {
  constructor(props) {
    super(props);

    this.state = {
      popup: false,
      data: {
        bio: "",
        location: "",
        website: ""
      }
    };
  }

  updateProfileBio = e => {
    this.setState({
      ...this.state,
      popup: true
    });
  };

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
    console.log(this.state.data);

    // this.props.setLoader();
    // let data = this.jsonData(this.state.data);

    // this.props.loginUser(data, this.props.history);
    // this.refs.loginForm.reset();
    // this.setState({
    //   ...this.state,
    //   popup: false,
    //   data: {
    //     bio: "",
    //     location: "",
    //     website: ""
    //   }
    // });
  };

  jsonData = data => {
    return JSON.stringify(data);
  };

  modalClose = e => {
    this.setState({
      ...this.state,
      popup: false
    });
  };

  handleClick = e => {
    e.preventDefault();
    this.props.fixNav();
    this.props.logoutUser(this.props.history);
  };

  updateProfilePic = e => {
    let formData = new FormData();
    formData.append("profile_pic", e.target.files[0], e.target.files[0].name);
    this.props.updateProfile(
      this.props.user.username,
      formData,
      this.props.token
    );
  };

  render() {
    let bio, location, website, profile_pic;

    if (this.props.error.bio) {
      bio = this.props.error.bio;
    }
    if (this.props.error.location) {
      location = this.props.error.location;
    }
    if (this.props.error.website) {
      website = this.props.error.website;
    }

    if (this.props.error.profile_pic) {
      console.log(this.props.error.profile_pic);
      profile_pic = this.props.error.profile_pic;
      // setTimeout(() => {
      //   this.props.resetLoader();
      // }, 1000);
    }

    const { isLogin, loading, user } = this.props;

    const sideContent = user ? (
      <nav className="side-nav">
        <center className="user-data">
          <div className="profile">
            <div>
              <img src={user && user.profile_pic} alt="profile" />
            </div>
            <p>
              <a href="#" className="icon-anim">
                <label htmlFor="pic" className="icon-anim">
                  <IoMdCreate />
                </label>
                <input
                  type="file"
                  name="pic"
                  onChange={this.updateProfilePic}
                  id="pic"
                  style={{ display: "none" }}
                />
              </a>
            </p>
            {profile_pic && <p className="error">{profile_pic}</p>}
          </div>

          <p className="username">@{user && user.username}</p>

          {user.bio && <p>{user.bio}</p>}

          {user.location && (
            <p>
              <a href="#" className="icon-anim">
                <IoMdPin />
              </a>
              <span>{user.location}</span>
            </p>
          )}

          {user.website && (
            <p>
              <a href="#" className="icon-anim">
                <IoMdLink />
              </a>
              <span>{user.website}</span>
            </p>
          )}
          <p>
            <a href="#" className="icon-anim">
              <IoIosCalendar />
            </a>
            <span>{user && user.joined_date}</span>
          </p>
          <div className="navigation">
            <a href="#" className="icon-anim" onClick={this.props.slider}>
              <IoIosUndo />
            </a>
            <a href="#" className="icon-anim" onClick={this.updateProfileBio}>
              <IoMdCreate />
            </a>
          </div>
        </center>
        <ul>
          <li>
            <a href="#" className="link">
              Reset Password
            </a>
          </li>
          <li>
            <a href="#" className="link" onClick={this.handleClick}>
              Logout
            </a>
          </li>
        </ul>
      </nav>
    ) : null;

    return (
      <>
        {isLogin ? (
          <>
            {sideContent}

            {this.state.popup ? (
              <>
                {loading ? (
                  <Loading />
                ) : (
                  <PopupModal>
                    <a href="#" className="close" onClick={this.modalClose}>
                      <IoIosCloseCircle />
                    </a>
                    <h1>Update Profile</h1>
                    <br />

                    <form
                      onSubmit={this.handleSubmit}
                      ref="createPostForm"
                      className="new-post"
                    >
                      <div className="textarea-input">
                        <label htmlFor="bio">Bio</label>
                        <br />
                        <textarea
                          name="bio"
                          value={this.state.data.bio}
                          placeholder="Enter biography"
                          onChange={this.handleInput}
                          autoComplete="off"
                          required
                        ></textarea>
                        {bio && <p className="error">{bio}</p>}
                      </div>
                      <br />
                      <div className="input">
                        <label htmlFor="location">Location</label> <br />
                        <input
                          type="text"
                          name="location"
                          value={this.state.data.location}
                          placeholder="Enter location"
                          onChange={this.handleInput}
                          autoComplete="off"
                          required
                        />
                        {location && <p className="error">{location}</p>}
                      </div>
                      <br />
                      <div className="input">
                        <label htmlFor="website">website</label> <br />
                        <input
                          type="url"
                          name="website"
                          value={this.state.data.website}
                          placeholder="Enter website (optional)"
                          onChange={this.handleInput}
                          autoComplete="off"
                        />
                        {website && <p className="error">{website}</p>}
                      </div>
                      <br />
                      <div className="submit">
                        <button type="submit" onSubmit={this.handleSubmit}>
                          Update Profile
                        </button>
                      </div>
                    </form>
                  </PopupModal>
                )}
              </>
            ) : null}
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
  logoutUser: history => {
    dispatch(logoutUser(history));
  },
  updateProfile: (username, file, token) => {
    dispatch(updateProfile(username, file, token));
  },
  updateProfileBio: (username, data, token) => {
    dispatch(updateProfileBio(username, data, token));
  },
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
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(withRouter(SideNav));
