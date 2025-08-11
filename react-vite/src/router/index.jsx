import { createBrowserRouter } from "react-router-dom";
import Layout from "./Layout";
import RequireAuth from "./RequireAuth";

import LoginFormPage from "../components/LoginFormPage";
import SignupFormPage from "../components/SignupFormPage";
import HomePage from "../components/HomePage";
import VendorsPage from "../components/VendorsPage";
import VendorDetailsPage from "../components/VendorDetailsPage";
import CategoriesPage from "../components/CategoriesPage";
import CategoryInvoicesPage from "../components/CategoryInvoicesPage";

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: "/", element: <HomePage /> },
      { path: "login", element: <LoginFormPage /> },
      { path: "signup", element: <SignupFormPage /> },

      { path: "vendors", element: <RequireAuth><VendorsPage /></RequireAuth> },
      { path: "vendors/:vendorId", element: <RequireAuth><VendorDetailsPage /></RequireAuth> },

      { path: "categories", element: <RequireAuth><CategoriesPage /></RequireAuth> },
      { path: "categories/:categoryId/invoices", element: <RequireAuth><CategoryInvoicesPage /></RequireAuth> },
    ],
  },
]);
