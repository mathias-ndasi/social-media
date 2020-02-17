import React from "react";

const PopupModal = props => {
  return (
    <div className="popup-modal-container">
      <div className="popup-modal-content">{props.children}</div>
    </div>
  );
};

export default PopupModal;

// TODO: control popup from various components by managin the state of that component..this
