const express = require("express");
const cookieParser = require("cookie-parser");
const path = require("path");

require('dotenv').config();

const registerRoute = require('./routes/auth/register');
const loginRoute = require('./routes/auth/login');
const logoutRoute = require('./routes/auth/logout');
const verifyRoute = require('./routes/auth/verify');
const meRoute = require('./routes/auth/me');
const productsRoute = require('./routes/products/products');
const orderProductRoute = require('./routes/products/order_product');
const wishProductRoute = require('./routes/products/wish_product');
const productRoute = require('./routes/products/single_product');
const categoriesRoute = require('./routes/products/categories');
const reviewProductRoute = require('./routes/products/review_product');
const getWishlistRoute = require('./routes/customers/get_wishlist');
const getCartRoute = require('./routes/customers/get_cart');
const getOrdersRoute = require('./routes/orders/get_orders');
const getOrderRoute = require('./routes/orders/single_order')
const cancelOrderRoute = require('./routes/orders/cancel_order');
const cancelOrdersRoute = require('./routes/orders/cancel_orders');
const deleteWishRoute = require('./routes/customers/delete_wish');
const deleteCartItemRoute = require('./routes/customers/delete_cartitem');
const orderCartRoute = require('./routes/customers/order_cart');
const deleteReviewRoute = require('./routes/products/delete_review');

const app = express();

app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cookieParser());

app.use(registerRoute);
app.use(loginRoute);
app.use(logoutRoute);
app.use(verifyRoute);
app.use(meRoute);
app.use(productsRoute);
app.use(orderProductRoute);
app.use(wishProductRoute);
app.use(productRoute);
app.use(categoriesRoute);
app.use(reviewProductRoute);
app.use(getWishlistRoute);
app.use(getCartRoute);
app.use(getOrdersRoute);
app.use(getOrderRoute);
app.use(cancelOrderRoute);
app.use(cancelOrdersRoute);
app.use(deleteWishRoute);
app.use(deleteCartItemRoute);
app.use(orderCartRoute);
app.use(deleteReviewRoute);

app.use(express.static("client/build"));
app.get("*", (req, res) => {
    const myPath = path.resolve(__dirname, "client", "build", "index.html");
    return res.sendFile(myPath);
})

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
