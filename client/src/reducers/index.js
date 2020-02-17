import {
  combineReducers
} from "redux";
import user from "./user/index";
import isLogin from "./user/isLogin";
import token from "./user/tokenManager";
import error from "./user/error";
import post from "./post/index";
import loading from "./loading";
import message from './message'
import popup from './popup'

const rootReducer = combineReducers({
  user,
  isLogin,
  token,
  posts: post,
  error,
  loading,
  message,
  popup,
});

export default rootReducer;