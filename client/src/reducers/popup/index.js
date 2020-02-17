import {
  SET_POPUP,
  RESET_POPUP
} from "./actions";

const initialState = false

export default (state = initialState, action) => {
  switch (action.type) {
    case SET_POPUP:
      return true
    case RESET_POPUP:
      return initialState;
    default:
      return state;
  }
};