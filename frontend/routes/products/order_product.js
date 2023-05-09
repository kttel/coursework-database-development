const express = require("express");
const fetch = (...args) =>
    import("node-fetch").then(({default: fetch}) => fetch(...args));

const router = express.Router();

router.post('/api/products/:id/order/', async (req, res) => {
    const id = req.params.id;
    const { access } = req.cookies;
    const { quantity } = req.body;

    const body = JSON.stringify({
        quantity
    });

    try {
        const apiRes = await fetch(`${process.env.API_URL}/api/products/${id}/order/`, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                Authorization: `Bearer ${access}`
            },
            body,
        });

        const data = await apiRes.json();
        return res.status(apiRes.status).json(data);
    } catch(err) {
        return res.status(500).json({
            error: "Something wrong with ordering this product"
        });
    }
})

module.exports = router;