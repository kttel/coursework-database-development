const express = require("express");
const cookie = require("cookie");
const fetch = (...args) =>
    import("node-fetch").then(({default: fetch}) => fetch(...args));

const router = express.Router();

router.get("/api/users/logout/", (req, res) => {
    res.setHeader('Set-Cookie', [
        cookie.serialize('access', '', {
            httpOnly: true,
            expires: new Date(0),
            path: '/api/',
            sameSite: 'strict',
            secure: process.env.NODE_ENV === 'production',
        }),
        cookie.serialize('refresh', '', {
            httpOnly: true,
            expires: new Date(0),
            path: '/api/',
            sameSite: 'strict',
            secure: process.env.NODE_ENV === 'production',
        }),
    ])

    return res.status(200).json({ success: "Logged out!" });
});

module.exports = router;