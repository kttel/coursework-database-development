const express = require("express");
const fetch = (...args) =>
    import("node-fetch").then(({default: fetch}) => fetch(...args));

const router = express.Router();

router.get('/api/products/:id/', async (req, res) => {
    const id = req.params.id;
    try {
        const apiRes = await fetch(`${process.env.API_URL}/api/products/${id}/`, {
            method: 'GET',
            headers: {
                Accept: 'application/json'
            }
        });

        const data = await apiRes.json();

        return res.status(apiRes.status).json(data);
    } catch(err) {
        return res.status(500).json({
            error: "Something wrong with product retrieving"
        });
    }
})

module.exports = router;