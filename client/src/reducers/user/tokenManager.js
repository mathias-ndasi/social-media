import {
  REFRESH_TOKEN,
  RESET_TOKEN
} from "./actions";

const initialState = "";

export default (state = initialState, action) => {
  switch (action.type) {
    case REFRESH_TOKEN:
      return action.token;
    case RESET_TOKEN:
      return initialState;
    default:
      return state;
  }
};