import { useLocation } from "react-router-dom";
import { useEffect } from "react";

const NotFound = () => {
  const location = useLocation();

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted">
      <div className="text-center">
        <p className="mb-4 text-xl text-white">Page not found</p>
      </div>
    </div>
  );
};

export default NotFound;
