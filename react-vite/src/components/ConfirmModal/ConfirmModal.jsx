import { useRef, useEffect } from "react";
import { useModal } from "../../context/Modal";
import "./ConfirmModal.css";

function ConfirmModal({ message = "Are you sure you want to proceed?", onConfirm }) {
    const { closeModal } = useModal();
    const ref = useRef(null);

    useEffect(() => {
        const onDown = (e) => { if (ref.current && !ref.current.contains(e.target)) closeModal(); };
        document.addEventListener("mousedown", onDown);
        return () => document.removeEventListener("mousedown", onDown);
    }, [closeModal]);

    return (
        <div className="confirm-overlay">
            <div className="confirm-card" ref={ref}>
                <p>{message}</p>
                <div className="confirm-actions">
                    <button className="btn-yes" onClick={() => { onConfirm?.(); closeModal(); }}>Yes</button>
                    <button className="btn-no" onClick={closeModal}>No</button>
                </div>
            </div>
        </div>
    );
}

export default ConfirmModal;
