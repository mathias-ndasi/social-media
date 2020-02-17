import { SET_ERROR, RESET_ERROR } from "./actions";

const initialState = {};

export default (state = initialState, action) => {
  switch (action.type) {
    case SET_ERROR:
      return action.error;
    case RESET_ERROR:
      return initialState;
    default:
      return state;
  }
};
