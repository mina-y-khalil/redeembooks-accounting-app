import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";
import "./CategoryInvoicesPage.css";

export default function CategoryInvoicesPage() {
    const { categoryId } = useParams();
    const category = useSelector((state) =>
        state.categories ? state.categories[categoryId] : null
    );

    return (
        <div className="category-invoices-page">
            <h2>
                {category
                    ? `Invoices linked to [${category.name}]`
                    : "Invoices linked to this category"}
            </h2>
            <div className="coming-soon-container2">
                <h1>Coming Soon ⏳</h1>
                <img
                    src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2V1MGFyZDN2YnJidjh1OXVyMHljeWtkZGtyb293bGViczJqeXNleCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/sQuHLqjWwRXGvrjkg0/giphy.gif"
                    alt="Coming Soon"
                    className="coming-soon-gif"
                />
            </div>
        </div>
    );
}
