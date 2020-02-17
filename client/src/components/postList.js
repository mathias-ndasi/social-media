import React from "react";
import { getAllPost } from "../reducers/post/actions";
import { connect } from "react-redux";
import PostItem from "./postItem";

const postList = props => {
  const { posts } = props;
  const postItems = posts.map(post => {
    return <PostItem post={post} key={post.id} />;
  });

  return <>{postItems}</>;
};

const mapStateToProps = state => {
  return state;
};

const mapDispatchToProps = dispatch => ({
  getAllPost: token => dispatch(getAllPost(token))
});

export default connect(mapStateToProps, mapDispatchToProps)(postList);
