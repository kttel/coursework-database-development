const express = require("express");
const fetch = (...args) =>
    import("node-fetch").then(({default: fetch}) => fetch(...args));

const router = express.Router();

router.get('/api/users/me/', async (req, res) => {
    const { access } = req.cookies;

    try {
        const meRes = await fetch(`${process.env.API_URL}/api/users/me/`, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                Authorization: `Bearer ${access}`
            }
        });

        const data = await meRes.json();

        return res.status(meRes.status).json(data);
    } catch(err) {
        return res.status(500).json({
            error: "Something wrong with user retrieving"
        });
    }
})

module.exports = router;