import { useSelector } from "react-redux";
import './HomePage.css';

function HomePage() {
    const sessionUser = useSelector((state) => state.session.user);

    return (
        <div className="home-page-container">
            <img
                src="https://redeem-innovations.com/wp-content/uploads/2025/08/RedeemBooksHome.png"
                alt="Redeem Books Home"
                className="home-page-image"
            />
            {!sessionUser ? (
                <>
                    <h1>Welcome to Redeem Books Accounting App</h1>
                    <p>Your one-stop solution for managing your book accounting needs.</p>
                    <p>Explore our features and get started today!</p>
                </>
            ) : (
                <>
                    <h1>Welcome back to Redeem Books</h1>
                    <p>Maximize your productivity — track your accounting in one place.</p>
                    <p>Thank you for choosing Redeem Books to power your business success.</p>
                </>
            )}
        </div>
    );
}

export default HomePage;
