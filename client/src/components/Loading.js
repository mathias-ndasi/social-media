import React from "react";
// import loader from "../images/loading.gif";

const Loading = () => {
  return (
    <div className="loading">
      {/* <img src={loader} alt="loading..." /> */}

      <div>
        <div className="loader">
          <span> </span> <span> </span> <span> </span> <span> </span>
          <span> </span>
        </div>
      </div>
    </div>
  );
};

export default Loading;

// TODO: mockup for loading skeleton
