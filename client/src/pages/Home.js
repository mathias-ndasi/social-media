import React, { Component } from "react";
import { connect } from "react-redux";
import { getAllPost } from "../reducers/post/actions";
import PostList from "../components/postList";
import { resetPopup, setPopup } from "../reducers/popup/actions";
import { resetLoader, setLoader } from "../reducers/loading/actions";

import { IoMdPin, IoMdCreate, IoIosCalendar, IoMdLink } from "react-icons/io";
import "../styles/Home.css";
import Loading from "../components/Loading";

class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {
      popup: false,
      data: {
        body: null,
        commented_by: null
      }
    };
  }

  componentDidMount() {
    if (!this.props.isLogin) {
      this.props.history.push("/login");
    }

    // get all post
    if (this.props.user) {
      this.props.getAllPost(this.props.token);
      this.props.resetPopup();
    }
  }

  render() {
    const { message, loading, user } = this.props;

    return (
      <div className="home">
        {message && (
          <div className="message">
            <p>{message}</p>
          </div>
        )}

        <br />

        <>
          {loading ? (
            <Loading />
          ) : (
            <div className="container">
              <div className="posts">
                {this.props.posts ? (
                  <PostList />
                ) : (
                  <h1>No post available yet</h1>
                )}
              </div>
              <div className="user">
                <center className="user-data">
                  <div className="profile">
                    <div>
                      <img src={user && user.profile_pic} alt="profile" />
                    </div>
                  </div>

                  <p className="username">@{user && user.username}</p>

                  {user.bio && <p className="bio">{user.bio}</p>}

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
                </center>
              </div>
            </div>
          )}
        </>
      </div>
    );
  }
}

const mapStateToProps = state => {
  return state;
};

const mapDispatchToProps = dispatch => ({
  getAllPost: token => {
    dispatch(getAllPost(token));
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

export default connect(mapStateToProps, mapDispatchToProps)(Home);
