import { useSelector } from "react-redux";
import { Navigate, useLocation } from "react-router-dom";

export default function RequireAuth({ children }) {
    const user = useSelector((s) => s.session.user);
    const location = useLocation();
    if (!user) return <Navigate to="/login" replace state={{ from: location }} />;
    return children;
}
