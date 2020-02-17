export const RESET_LOADER = "RESET_LOADER";
export const SET_LOADER = "SET_LOADER";

export const setLoader = () => {
  return {
    type: SET_LOADER
  };
};

export const resetLoader = () => {
  return {
    type: RESET_LOADER
  };
};