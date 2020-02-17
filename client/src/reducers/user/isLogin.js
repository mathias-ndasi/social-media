import { IS_LOGIN } from "./actions";

const initialState = false;

export default (state = initialState, action) => {
  switch (action.type) {
    case IS_LOGIN:
      return action.isLogin;
    default:
      return state;
  }
};
