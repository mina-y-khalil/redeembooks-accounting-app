import { createBrowserRouter } from 'react-router-dom';
import LoginFormPage from '../components/LoginFormPage';
import SignupFormPage from '../components/SignupFormPage';
import Layout from './Layout';
import VendorsPage from "../components/VendorsPage";
import VendorDetailsPage from "../components/VendorDetailsPage";
import HomePage from '../components/HomePage';

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "login",
        element: <LoginFormPage />,
      },
      {
        path: "signup",
        element: <SignupFormPage />,
      },
      {
        path: "vendors",
        element: <VendorsPage />,
      },
      {
        path: "vendors/:vendorId",
        element: <VendorDetailsPage />,
      },
    ],
  },
]);
