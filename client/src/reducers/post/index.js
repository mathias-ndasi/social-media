import { GET_ALL_POST, SET_POST, LIKE_POST, DELETE_POST } from "./actions";

const initialState = [];

export default (state = initialState, action) => {
  switch (action.type) {
    case GET_ALL_POST:
      return action.posts;
    case SET_POST:
      return [action.post, ...state];
    case LIKE_POST:
      let index = state.findIndex(post => {
        return post.id === action.post.id;
      });
      return state.splice(index + 1, 1, action.post);
    case DELETE_POST:
      return state.filter(post => {
        return post.id !== action.id;
      });
    default:
      return state;
  }
};
