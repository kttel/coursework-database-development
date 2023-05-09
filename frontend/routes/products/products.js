const express = require("express");
const fetch = (...args) =>
    import("node-fetch").then(({default: fetch}) => fetch(...args));

const router = express.Router();

router.get('/api/products/', async (req, res) => {
    const category = req.query.category ? req.query.category : '';
    const page = req.query.page ? req.query.page : 1

    try {
        const apiRes = await fetch(`${process.env.API_URL}/api/products/?category=${category}&page=${page}`, {
            method: 'GET',
            headers: {
                Accept: 'application/json'
            }
        });

        const data = await apiRes.json();
        return res.status(apiRes.status).json(data);
    } catch(err) {
        return res.status(500).json({
            error: "Something wrong with products retrieving"
        });
    }
})

module.exports = router;