import React, { Component } from "react";
import "../styles/post.css";
// import image from "../images/login.png";
import {
  IoIosHeartEmpty,
  IoMdText,
  IoIosHeart,
  IoMdTrash,
  IoIosCloseCircle
} from "react-icons/io";

import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import { connect } from "react-redux";
import { likePost, deletePost } from "../reducers/post/actions";
import PopupModal from "./popup";
import { resetLoader, setLoader } from "../reducers/loading/actions";

// const convertMiliseconds = miliseconds => {
//   var days, hours, minutes, seconds, total_hours, total_minutes, total_seconds;

//   total_seconds = parseInt(Math.floor(miliseconds / 1000));
//   total_minutes = parseInt(Math.floor(total_seconds / 60));
//   total_hours = parseInt(Math.floor(total_minutes / 60));
//   days = parseInt(Math.floor(total_hours / 24));

//   return days;
// };

class PostItem extends Component {
  constructor(props) {
    super(props);

    this.state = {
      delete: false
    };
  }

  like = post_id => {
    let data = { user_id: this.props.user.id };
    this.props.likePost(JSON.stringify(data), post_id, this.props.token);
  };

  deleteRequest = () => {
    this.setState({
      ...this.state,
      delete: true
    });
  };

  confirmPostDelete = post_id => {
    this.props.setLoader();
    this.props.deletePost(post_id, this.props.token);
    this.setState({
      ...this.state,
      delete: false
    });
    setTimeout(() => {
      this.props.resetLoader();
    }, 1000);
  };

  modalClose = e => {
    this.setState({
      ...this.state,
      delete: false
    });
  };

  render() {
    dayjs.extend(relativeTime);
    const { post, user } = this.props;

    // let now_date = new Date();
    // let post_date = new Date(post.posted_date);
    // let millsec = now_date - post_date;
    // let no_days = convertMiliseconds(millsec);

    return (
      <>
        <div className="post-container">
          <div className="user-img">
            <img src={post.created_by.profile_pic} alt="user-image" />
          </div>
          <div className="body">
            <p className="body-username">
              <a href="#">{post.created_by.username}</a>
              {post.created_by.id === user.id ? (
                <a
                  href="#"
                  className="trash icon-anim"
                  onClick={this.deleteRequest}
                >
                  <IoMdTrash />
                </a>
              ) : null}
            </p>
            <p className="days">{dayjs(post.posted_date).fromNow()}</p>

            <p className="post-body">{post.body}</p>
            <div className="likes-comments">
              <div>
                <a
                  href="#"
                  className="post-icon-like"
                  onClick={() => this.like(post.id)}
                >
                  {post.liked_by.includes(user.username) ? (
                    <IoIosHeart />
                  ) : (
                    <IoIosHeartEmpty />
                  )}
                </a>
                <span>
                  {post.no_likes} {post.no_likes > 1 ? "likes" : "like"}
                </span>
              </div>
              <div>
                <a href="#" className="post-icon">
                  <IoMdText />
                </a>
                <span>
                  {post.no_comments}{" "}
                  {post.no_comments > 1 ? "comments" : "comment"}
                </span>
              </div>
            </div>
          </div>
        </div>
        <br />
        {this.state.delete ? (
          <PopupModal>
            <a href="#" className="close" onClick={this.modalClose}>
              <IoIosCloseCircle />
            </a>
            <h1>Confirm Delete</h1>
            <br />

            <center className="post-delete">
              <p>Are you sure you want to delete post?</p> <br />
              <div>
                <button onClick={() => this.confirmPostDelete(post.id)}>
                  Yes
                </button>
                <button onClick={this.modalClose}>No</button>
              </div>
            </center>
          </PopupModal>
        ) : null}
      </>
    );
  }
}

const mapStateToProps = state => {
  return state;
};

const mapDispatchToProps = dispatch => ({
  likePost: (data, post_id, token) => {
    dispatch(likePost(data, post_id, token));
  },
  deletePost: (post_id, token) => {
    dispatch(deletePost(post_id, token));
  },
  setLoader: () => {
    dispatch(setLoader());
  },
  resetLoader: () => {
    dispatch(resetLoader());
  }
});

export default connect(mapStateToProps, mapDispatchToProps)(PostItem);
