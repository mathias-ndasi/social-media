import { SET_MESSAGE, RESET_MESSAGE } from "./actions";

const initialState = "";

export default (state = initialState, action) => {
  switch (action.type) {
    case SET_MESSAGE:
      return action.message;
    case RESET_MESSAGE:
      return initialState;
    default:
      return state;
  }
};
