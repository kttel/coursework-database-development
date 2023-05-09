const express = require("express");
const fetch = (...args) =>
    import("node-fetch").then(({default: fetch}) => fetch(...args));

const router = express.Router();

router.post('/api/orders/:id/cancel_single/', async (req, res) => {
    const id = req.params.id;
    const { access } = req.cookies;

    try {
        const apiRes = await fetch(`${process.env.API_URL}/api/me/orders/${id}/cancel_single/`, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                Authorization: `Bearer ${access}`
            },
        });

        const data = await apiRes.json();
        return res.status(apiRes.status).json(data);
    } catch(err) {
        return res.status(500).json({
            error: "Something wrong with wishing this product"
        });
    }
})

module.exports = router;