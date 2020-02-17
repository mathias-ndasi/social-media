import { axiosConfig } from "../../config";
import { setError, resetError } from "../user/actions";
import { setMessage, resetMessage } from "../message/actions";
import { resetPopup, setPopup } from "../popup/actions";
import { resetLoader, setLoader } from "../loading/actions";

export const GET_ALL_POST = "GET_ALL_POST";
export const SET_POST = "SET_POST";
export const LIKE_POST = "LIKE_POST";
export const DELETE_POST = "DELETE_POST";

export const getAllPost = token => {
  return dispatch => {
    axiosConfig
      .get("/post", { headers: { "x-access-token": token } })
      .then(res => {
        console.log(res.data);
        // dispatch(setLoader());

        dispatch(setAllPost(res.data.data));

        if (res.data.message) {
          dispatch(setMessage(res.data.message));

          setTimeout(() => {
            dispatch(resetMessage());
          }, 4000);
        }

        setTimeout(() => {
          dispatch(resetLoader());
        }, 1000);
      })
      .catch(err => {
        try {
          console.log(err.response.data);

          if (err.response.data.error) {
            dispatch(setLoader());

            setTimeout(() => {
              dispatch(resetLoader());
            }, 1000);

            dispatch(setError(err.response.data.error));

            // clear errors
            setTimeout(() => {
              dispatch(resetError());
            }, 5000);
          }
        } catch {
          console.log("ERROR........");
        }
      });
  };
};

export const setAllPost = posts => {
  return {
    type: GET_ALL_POST,
    posts
  };
};

export const createPost = (JsonData, token) => {
  return dispatch => {
    axiosConfig
      .post("/post/create", JsonData, { headers: { "x-access-token": token } })
      .then(res => {
        console.log(res.data);
        if (res.data.success) {
          dispatch(setLoader());

          dispatch(setPost(res.data.data));

          if (res.data.message) {
            dispatch(setMessage(res.data.message));

            setTimeout(() => {
              dispatch(resetMessage());
            }, 4000);
          }

          setTimeout(() => {
            dispatch(resetLoader());
            dispatch(resetPopup());
            dispatch(getAllPost(token));
          }, 1000);
        }
      })
      .catch(err => {
        try {
          console.log(err.response.data);

          if (err.response.data.error) {
            dispatch(setLoader());

            setTimeout(() => {
              dispatch(resetLoader());
              dispatch(setPopup());
            }, 9000);

            dispatch(setError(err.response.data.error));

            // clear errors
            setTimeout(() => {
              dispatch(resetError());
            }, 5000);
          }
        } catch {
          console.log("ERROR........");
        }
      });
  };
};

export const setPost = post => {
  return {
    type: SET_POST,
    post
  };
};

export const likePost = (JsonData, post_id, token) => {
  return dispatch => {
    axiosConfig
      .put(`/post/like/${post_id}`, JsonData, {
        headers: { "x-access-token": token }
      })
      .then(res => {
        console.log(res.data);
        dispatch({
          type: LIKE_POST,
          post: res.data.data
        });
        dispatch(getAllPost(token));
      })
      .catch(err => {
        console.log(err.response);
      });
  };
};

export const deletePost = (post_id, token) => {
  return dispatch => {
    axiosConfig
      .delete(`/post/${post_id}/delete`, {
        headers: { "x-access-token": token }
      })
      .then(res => {
        console.log(res.data);
        dispatch({
          type: DELETE_POST,
          id: post_id
        });
        dispatch(getAllPost(token));
      })
      .catch(err => {
        console.log(err.response);
      });
  };
};
