import { axiosConfig } from "../../config";
import { setMessage, resetMessage } from "../message/actions";
import { setPopup, resetPopup } from "../popup/actions";
import { setLoader, resetLoader } from "../loading/actions";

export const SIGNUP_ACTION = "SIGNUP_ACTION";
export const ACCOUNT_CONFIRMATION = "ACCOUNT_CONFIRMATION";
export const LOGIN_USER = "LOGIN_USER";
export const LOGOUT_USER = "LOGOUT_USER";
export const IS_LOGIN = "IS_LOGIN";
export const IS_LOGOUT = "IS_LOGOUT";
export const REFRESH_TOKEN = "REFRESH_TOKEN";
export const RESET_TOKEN = "RESET_TOKEN";
export const SET_ERROR = "SET_ERROR";
export const RESET_ERROR = "RESET_ERROR";
export const UPDATE_PROFILE = "UPDATE_PROFILE";

export const loginUser = (jsonData, history) => {
  return dispatch => {
    axiosConfig
      .post("/account/login", jsonData)
      .then(res => {
        if (res.data.success) {
          delete res.data.data["password"];
          dispatch(setToken(res.data.data["token"]));
          delete res.data.data["token"];
          dispatch(loginAction(res.data));
          dispatch(isLoginAction(true));

          if (res.data.message) {
            dispatch(setMessage(res.data.message));

            setTimeout(() => {
              dispatch(resetMessage());
            }, 4000);
          }

          history.push("/");
          dispatch(setLoader());

          // setInterval(() => {
          //   dispatch(getToken(res.data.data['username']))
          // }, 2414000000)
        }
      })
      .catch(err => {
        console.log(err.response);
        try {
          if (err.response.data.error) {
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

export const accountConfirm = (jsonData, history) => {
  return dispatch => {
    axiosConfig
      .put("/account/account_confirmation", jsonData)
      .then(res => {
        if (res.data.success) {
          if (res.data.message) {
            dispatch(setMessage(res.data.message));

            setTimeout(() => {
              dispatch(resetMessage());
            }, 4000);
          }

          dispatch(resetPopup());

          history.push("/login");
        }
      })
      .catch(err => {
        console.log(err.response);
        try {
          if (err.response.data.error) {
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

export const setError = error => {
  return {
    type: SET_ERROR,
    error
  };
};

export const resetError = () => {
  return {
    type: RESET_ERROR
  };
};

export const setToken = token => {
  return {
    type: REFRESH_TOKEN,
    token
  };
};

export const resetToken = () => {
  return {
    type: RESET_TOKEN
  };
};

export const getToken = username => {
  return dispatch => {
    axiosConfig
      .get(`/account/${username}/refresh_token`)
      .then(res => {
        dispatch(setToken(res.data.token));
        return res.data.token;
      })
      .catch(err => console.log(err.response));
  };
};

export const loginAction = res => {
  return {
    type: LOGIN_USER,
    data: res
  };
};

export const logoutAction = () => {
  return {
    type: LOGOUT_USER
  };
};

export const isLoginAction = bool => {
  return {
    type: IS_LOGIN,
    isLogin: bool
  };
};

export const logoutUser = history => {
  return dispatch => {
    dispatch(isLoginAction(false));
    dispatch(logoutAction());
    dispatch(resetToken());

    dispatch(setMessage("User logout successfull!!!"));

    setTimeout(() => {
      dispatch(resetMessage());
    }, 4000);

    history.push("/login");
  };
};

export const signupUser = jsonData => {
  return dispatch => {
    axiosConfig
      .post("/account/signup", jsonData)
      .then(res => {
        if (res.data.success) {
          console.log(res.data);
          dispatch(setLoader());

          dispatch(signupAction(res.data.message));

          if (res.data.message) {
            dispatch(setMessage(res.data.message));

            setTimeout(() => {
              dispatch(resetMessage());
            }, 4000);
          }

          setTimeout(() => {
            dispatch(resetLoader());
            dispatch(setPopup());
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

export const signupAction = message => {
  return {
    type: SIGNUP_ACTION,
    message
  };
};

export const updateProfile = (username, file, token) => {
  return dispatch => {
    axiosConfig
      .put(`/account/${username}/profile_pic`, file, {
        headers: { "x-access-token": token }
      })
      .then(res => {
        console.log(res.data);
        return dispatch({
          type: UPDATE_PROFILE,
          profile_pic: res.data.data.profile_pic
        });
      })
      .catch(err => {
        try {
          console.log(err.response.data);
          if (err.response.data.error) {
            // dispatch(setLoader());

            // setTimeout(() => {
            //   dispatch(resetLoader());
            // }, 1000);

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

export const updateProfileBio = (username, jsonData, token) => {
  return dispatch => {
    axiosConfig
      .put(`/account/user/update/${username}/bio`, jsonData, {
        headers: { "x-access-token": token }
      })
      .then(res => {
        console.log(res.data);
      })
      .catch(err => {
        console.log(err.response);
      });
  };
};
