import { SET_LOADER, RESET_LOADER } from "./actions";

const initialState = false;

export default (state = initialState, action) => {
  switch (action.type) {
    case SET_LOADER:
      return true;
    case RESET_LOADER:
      return initialState;
    default:
      return state;
  }
};
