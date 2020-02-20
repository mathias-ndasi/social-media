import {
  LOGIN_USER,
  LOGOUT_USER,
  SIGNUP_ACTION,
  ACCOUNT_CONFIRMATION,
  UPDATE_PROFILE,
  UPDATE_PROFILE_BIO
} from "./actions";

const initialState = {};

export default (state = initialState, action) => {
  switch (action.type) {
    case SIGNUP_ACTION:
      return action.message;
    case ACCOUNT_CONFIRMATION:
      return action.message;
    case LOGIN_USER:
      return action.user;
    case LOGOUT_USER:
      return initialState;
    case UPDATE_PROFILE:
      return {
        ...state,
        profile_pic: action.profile_pic
      }
      case UPDATE_PROFILE_BIO:
        return action.user
      default:
        return state;
  }
};