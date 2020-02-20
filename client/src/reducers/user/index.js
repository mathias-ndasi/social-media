import {
  LOGIN_USER,
  LOGOUT_USER,
  SIGNUP_ACTION,
  ACCOUNT_CONFIRMATION,
  UPDATE_PROFILE
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
      console.log(state, 'hello...')
      return {
        ...state,
        data: {
          ...state.data,
          profile_pic: action.profile_pic
        }
      }
      default:
        return state;
  }
};